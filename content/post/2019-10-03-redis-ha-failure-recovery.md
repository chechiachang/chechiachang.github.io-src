---
title: "Redis Ha Failure Recovery"
subtitle: ""

# Add a summary to display on homepage (optional).
summary: ""

date: 2019-10-03T16:12:10+08:00
draft: false

# Authors. Comma separated list, e.g. `["Bob Smith", "David Jones"]`.
authors: []

# Is this a featured post? (true/false)
featured: false

# Tags and categories
# For example, use `tags: []` for no tags, or the form `tags: ["A Tag", "Another Tag"]` for one or more tags.
tags: ["kubernetes", "redis", "ithome"]
categories: ["kubernetes", "redis"]

menu:
  main:
    parent: "Ithelp 鐵人賽"
    weight: 1
---

[2020 It邦幫忙鐵人賽](https://ithelp.ithome.com.tw/2020ironman) 系列文章

- 在 GKE 上部署 Redis HA (5)
  - [使用 helm 部署 redis-ha]({{< ref "/post/2019-09-28-redis-ha-deployment" >}})
  - [Redis HA with sentinel]({{< ref "/post/2019-09-29-redis-ha-sentinel" >}})
  - [Redis sentinel topology]({{< ref "/post/2019-09-30-redis-ha-topology" >}})
  - [Redis HA with HAproxy]({{< ref "/post/2019-10-02-redis-ha-on-haproxy" >}})
  - [Redis HA Failure Recovery]({{< ref "/post/2019-10-03-redis-ha-failure-recovery" >}})
  - Prometheus Metrics Exporter

由於我比較熟悉 GCP / GKE 的服務，這篇的操作過程都會以 GCP 平台作為範例，不過操作過程大體上是跨平台通用的。

寫文章真的是體力活，覺得我的文章還有參考價值，請左邊幫我點讚按個喜歡，右上角幫我按個追縱，底下歡迎留言討論。給我一點繼續走下去的動力。

對我的文章有興趣，歡迎到我的網站上 [https://chechia.net](https://chechia.net) 閱讀其他技術文章，有任何謬誤也請各方大德直接聯繫我，感激不盡。

![Exausted Cat Face](https://d32l83enj9u8rg.cloudfront.net/wp-content/uploads/iStock-966846550-cat-overheating-simonkr-1-940x470.jpg)

---

# 摘要

* Failure Case
* Recovery

# Topology

上篇的例子完成應該是這樣

```

   +-------+   +--------+    +------------+    +---------+
   |Clients|---|HAProxys|----|redis master|----|sentinels|
   +-------+   +--------+    +------------+    +---------+

```

* HAproxy 作為後端 redis 的 gateway
* Client 透過 HAproxy 連入 redis master
* sentinel 負責監測 redis 狀態與 failover，只是 client 不再透過 sentinel 去取得 master，而是透過 HAProxy。

那現在就來聊聊這些服務可能怎麼死的，回復的機制又是如何

# Failure Recovery

### Redis master 故障

這個是目前我們這個 Redis HAProxy 配置主要想解決的問題，故障與回覆的流程大概是這樣

0. Redis Master failing
1. Sentinels detect master failure
  * sentinel 等待 down-after-milliseconds，超過才判定 master failure
  * sentinel 彼此取得 quorum，授權其中一台 sentinel 執行 failover
  * sentinel 指派新的 master
2. master 故障同時，HAProxy 也偵測 master failure
  * HAProxy 發現沒有可用的 master
  * tcp checklist 再次執行時，由於新的 master 尚未選出來，仍會顯示三台 server 都離線
  * 直到 master 選出，role:master 的 tcp check 有回應後，才會將後端接到新的 master
3. Client 由於 HAProxy 沒有可用的 master，所以連線斷掉
  * 持續中斷到 HAProxy 回復

這邊的幾個重要的參數

* sentinel
  * down-after-milliseconds: 斷線多久才會覺得 master 死了需要 failover，可以盡量縮短，加速 failure 發生 failover 的時間

* haproxy.cfg
  * server check inter 1s: 多久跑一次 tcp-check
    * 越短，便能越早接受到 redis instance failure 的發生

從這個例子來看，這個配置的 HA 其實還是有離線時間

* down-after-milliseconds 設定為 2s ，那從 failure 發生，到 sentinel 開始 failover 的時間就會超過 2s，這兩秒客戶端無法寫入。
* 事實上，這也是 redis master-slave 的模式的問題，並無法確保 zero downtime
* 能做到的是秒級的 auto-recovery

### Sentinel Failure

這個是很好解決的錯誤，如同我們在 topology 這篇提到的，原則上只要能維持 quorum 以上的 sentinel 正常運作，就可以容忍多個 sentinel 的錯誤

* 例如 5 sentinel，quorum 3，就可以允許兩個 sentinel 錯誤
  * 服務都正常 zero downtime
  * 等待錯誤的 sentinels 復原
* 錯誤不一定是兩個 sentinel 死了，可能是網路斷開，把 3 sentinels 與 2 sentinels 隔開，無法溝通。
  * 這時也不用會有複數 failover 產生，因為 quorum 只有 3 sentinels 的這端可以取得授權，正常執行 failover
  * 2 sentinels 的這邊只會靜待網路回復。

### HAProxy Failure

這個在 kubernetes 上也是很好解決

* HAProxy 不用知道彼此，只要能夠監測後端服務，並且 proxy request 即可
* 我們啟動 HAProxy 時會一次啟動多個 HAProxy
    * HAProxy 是無狀態的服務，可以直接水平擴展 (Horizontal Scale)
    * 算是成本的地方，就是 HAProxy instance 會各自對後端 redis 做 tcp-check，頻繁的 check，還是會有成本，但相較於 client request 應該是比較輕
    * HAProxy 是高效能，而且只做 proxy，一奔來說只要維持有多餘的副本備用即可，不用開太多
* Kubernetes 會自動透過 stats port，對 HAPRoxy 做 liveness check，check 失敗就不會把流量導近來
* HAproxy 前端的 kubernetes service 會自動 load balance client 到正常運作的 HAProxy 上

* 例如起了 3 HAProxy
* 3 HAProxy 都各自向 redis instance 做 tcp-check，每秒 3 * 3 組 check
* 客戶端連入任一 HAProxy，都可以連入正確的 master
* HAProxy 只要至少有一個活著就可以，也就是可以死 2 個
* Kubernetes service 會自動導向活著的 HAProxy
* 2 HAPRoxy 回復的時候，就是 HAProxy 重啟後重新開始服務

# 拆分 read write client

由於效能瓶頸還是在 redis master，為了能支撐夠多 client，最好把 client 需要讀寫的拆分開來

HAProxy 的設定，就會需要

* 把 frontend redis_gate 拆成
  * redis_slaves_gate: 接收讀取的 client
  * redis_master_gate: 接收寫入的 client
* 把 redis_servers 拆成
  * redis_slaves: 更改 tcp-check 去找 role:slave 的 redis，應該有兩台
  * redis_master: 維持找尋 role:master 的 redis

這樣可以輕易地透過 scale slave 來擴大讀取的流量帶寬

# Redis Cluster

Intro 的時候有提到，redis cluster 是另一個面向的 redis solution。

使用 [redis cluster](https://redis.io/topics/cluster-tutorial) 將資料做 sharding，分散到不同群組內，partitions 由複數的 master 來存取

這部份我們下回待續
