---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Redis Ha Sentinel"
subtitle: ""
summary: ""
authors: []
tags: ["鐵人賽2019", "kubernetes", "redis", "ithome", "haproxy"]
categories: ["kubernetes", "redis"]
date: 2019-09-29T17:14:38+08:00
lastmod: 2019-09-29T17:14:38+08:00
featured: false
draft: false
---

[2020 It邦幫忙鐵人賽](https://ithelp.ithome.com.tw/2020ironman) 系列文章

- 在 GKE 上部署 Redis HA (5)
  - [使用 helm 部署 redis-ha]({{< ref "/posts/2019-09-28-redis-ha-deployment" >}})
  - [Redis HA with sentinel]({{< ref "/posts/2019-09-29-redis-ha-sentinel" >}})
  - [Redis sentinel topology]({{< ref "/posts/2019-09-30-redis-ha-topology" >}})
  - [Redis HA with HAproxy]({{< ref "/posts/2019-10-02-redis-ha-on-haproxy" >}})
  - [Redis HA Failure Recovery]({{< ref "/posts/2019-10-03-redis-ha-failure-recovery" >}})
  - Prometheus Metrics Exporter

由於我比較熟悉 GCP / GKE 的服務，這篇的操作過程都會以 GCP 平台作為範例，不過操作過程大體上是跨平台通用的。

寫文章真的是體力活，覺得我的文章還有參考價值，請左邊幫我點讚按個喜歡，右上角幫我按個追縱，底下歡迎留言討論。給我一點繼續走下去的動力。

對我的文章有興趣，歡迎到我的網站上 [https://chechia.net](https://chechia.net) 閱讀其他技術文章，有任何謬誤也請各方大德直接聯繫我，感激不盡。

![Exausted Cat Face](https://d32l83enj9u8rg.cloudfront.net/wp-content/uploads/iStock-966846550-cat-overheating-simonkr-1-940x470.jpg)

---

# 摘要

* redis-sentinel

redis sentinel 與 redis 使用相容的 api，直接使用 redis-cli 透過 26479 port 連入，可以連到 sentinel，透過 sentinel 可以取得 redis master 的狀態與連線設定。
```
redis-cli -h redis-redis-ha -p 26479
```

上篇我們的 redis-ha 安裝完變這樣
```
$ kubectl get po | grep redis

NAME                                                     READY   STATUS      RESTARTS   AGE
redis-1-redis-ha-server-0                                3/3     Running     0          3d4h
redis-1-redis-ha-server-1                                3/3     Running     0          3d5h
redis-1-redis-ha-server-2                                3/3     Running     0          3d4h
```

有三個 Pod，裡面都是一個 redis, sentinel, 跟 exporter，這篇文章會專注講 sentinel 的功能與機制

# Redis Sentinel

[redis-sentinel](https://redis.io/topics/sentinel) 為 Redis 提供高可用服務，實務上可以透過 sentinel 在錯誤發生時，自動進行 failover。除此之外 sentinel 也提供監測，通知，與 redis 的設定。

* Monitoring: 持續檢測 master 與 slave instances 的狀態
* Notification: 有事件發生可以發出通知
* Automatic failover: 如果 master 失效自動啟動 failover 程序，將一個 slave 指排為 master，並設定其他 slave 使用新的 master
* Configuration provider: 為客戶端提供 service discovery，客戶可以通過 sentinel 取得 master 的連線資料。

# Distributed

Sentinel 本身是一個分散式系統，如我們的範例所示，三個 Pod 立面個含有一個 sentinel，組成 3 個 instace 的 sentinel cluster。

* 錯誤檢測是由多個 sentinel 判定，要有多個 sentinel 都接收 master 已失效的訊息，才會判定成失效。這樣可以降低 false positive 的機率。
* 分散讓 sentinel 本身也具備高可用性，可以承受一定程度的錯誤。用來 fail over 的系統，不能因為自身的單點錯誤(single point failure) 而倒是整個 redis 失效。

# Fundamental

* 一個耐用的 sentinel 需要至少三個 instance
* 最好把 instance 分散在多個獨立的隔離區域，意思是說，三個不會放在同一台機器上，或是放在同一個區域內，因為一個區域網路故障就全死。
* app 使用 sentinel 的話，客戶端要支援
* 有時常測試的 HA 環境，才是有效的 HA

# Configuration

## Sentinel specific configuration options

在上篇我們跳過 sentinel 的設定，這邊說明一下
```
sentinel:
  port: 26379
  quorum: 2
  config:
    ## Additional sentinel conf options can be added below. Only options that
    ## are expressed in the format simialar to 'sentinel xxx mymaster xxx' will
    ## be properly templated.
    ## For available options see http://download.redis.io/redis-stable/sentinel.conf
    down-after-milliseconds: 10000
    ## Failover timeout value in milliseconds
    failover-timeout: 180000
    parallel-syncs: 5

  ## Custom sentinel.conf files used to override default settings. If this file is
  ## specified then the sentinel.config above will be ignored.
  # customConfig: |-
      # Define configuration here

  resources: {}
  #  requests:
  #    memory: 200Mi
  #    cpu: 100m
  #  limits:
  #    memory: 200Mi
```

### Quorum

* quorum 是每次確定 master 失效時，需要達成共識的 sentinel 數量。
* Quorum 使用在錯誤檢測，確定錯誤真的發生後，sentinel 會以多數決(majority) 的方式選出 sentinel leader，讓 leader 處理 failover。

以我們的例子為例，總共三個，確認 master 死掉只要兩個 sentinel 達成共識即可啟動 failover 程序。可以直接測試一下。

```
kubectl logs -f redis-1-redis-ha-server-0

kubectl delete po redis-1-redis-ha-server-1
```
log 一個 Pod ，然後直接把另一個 Pod 幹掉 這樣會有 1/3 的機率砍到 master，砍中的話可以看到 redis failover ，選出新的 master 的過程。

這邊要注意，由於我們的 sentinel 與 redis 是放在同樣一個 Pod，幹掉的同時也殺了一個 sentinel，只剩 2 個，剛好達成共識。如果 quorum 是三，就要等第三個 sentinel 回來才能取得 quorum。

sentinel 與 redis 的配置位置，之後的 topology 會討論。

### Configurations

* down-after-milliseconds: 超過多少時間沒回應 ping 或正確回應，才覺得 master 壞了
* parallel-syncs: failover 時，要重新與新 master sync 的 slave 數量。數量越多 sync 時間就越久，數量少就有較多 slave 沒 sync 資料，可能會讓 client read 到舊的資料
  * 雖然 sync 是 non-blocking ，但在 sync 大筆資料時，slave 可能會沒有回應。設定為 1 的話，最多只會有一個 slave 下線 sync。

這些參數也可以透過 redis-cli 直接連入更改，但我們是在 kubernetes 上跑，臨時的更改不易保存，所以盡可能把這些configurations 放在 configmap 裡面。

# Sentinel command

6379 port 連入 redis，26379 連入 redis sentinel。都是使用 redis-cli，兩者兼容的 protocol。
```
# 使用 kubectl 連入，多個 container 要明確指出連入的 container
kubectl exec -it redis-1-redis-ha-server-0 --container redis sh

redis-cli -h redis-redis-ha -p 26479

# 近來先 ping 一下
$ ping
PONG

# 列出所有 master 的資訊，以及設定資訊
sentinel master
redis-2-redis-ha:26379> sentinel masters
1)  1) "name"
    2) "mymaster"
    3) "ip"
    4) "10.15.242.245"
    5) "port"
    6) "6379"
    7) "runid"
    8) "63a97460b7c3745577931dad406df9609c4e2464"
    9) "flags"
   10) "master"
   11) "link-pending-commands"
   12) "0"
   13) "link-refcount"
   14) "1"
   15) "last-ping-sent"
   16) "0"
   17) "last-ok-ping-reply"
   18) "479"
   19) "last-ping-reply"
   20) "479"
   21) "down-after-milliseconds"
   22) "5000"
   23) "info-refresh"
   24) "5756"
   25) "role-reported"
   26) "master"
   27) "role-reported-time"
   28) "348144787"
   29) "config-epoch"
   30) "13"
   31) "num-slaves"
   32) "2"
   33) "num-other-sentinels"
   34) "2"
   35) "quorum"
   36) "2"
   37) "failover-timeout"
   38) "180000"
   39) "parallel-syncs"
   40) "5"

# 取得集群中的 master 訊息，目前有一個 master
$ sentinel master mymaster

# 取得集群中的 slaves 訊息，目前有兩個 slave
$ sentinel slaves mymaster

# 取得集群中的 master 訊息
$ sentinel sentinels mymaster

# 檢查 sentinel 的 quorum
$ sentinel ckquorum mymaster

OK 3 usable Sentinels. Quorum and failover authorization can be reached

# 強迫觸發一次 failover
sentinel failover mymaster
```

# Sentinel Connection

有支援的客戶端設定，以[Golang FZambia/sentinel](https://github.com/FZambia/sentinel/blob/master/sentinel.go) 為例，透過 sentinel 取得 redis-pool。

```
# 使用獨立的 pod service 連入 sentinel，協助彼此識別
sntnl := &sentinel.Sentinel{
	Addrs:      []string{"redis-2-redis-ha-announce-0:26379", "redis-2-redis-ha-announce-0:26379", "redis-2-redis-ha-announce-0:26379"},
	MasterName: "mymaster",
	Dial: func(addr string) (redis.Conn, error) {
		timeout := 500 * time.Millisecond
		c, err := redis.DialTimeout("tcp", addr, timeout, timeout, timeout)
		if err != nil {
			return nil, err
		}
		return c, nil
	},
}

# 產生 connection pool
return &redis.Pool{
	MaxIdle:     3,
	MaxActive:   64,
	Wait:        true,
	IdleTimeout: 240 * time.Second,
	Dial: func() (redis.Conn, error) {

    # 透過 sentinel 取得 master address，如果 master 死了，再執行可以拿到新的 master
		masterAddr, err := sntnl.MasterAddr()
		if err != nil {
			return nil, err
		}
		c, err := redis.Dial("tcp", masterAddr)
		if err != nil {
			return nil, err
		}
		return c, nil
	},
	TestOnBorrow: func(c redis.Conn, t time.Time) error {
		if !sentinel.TestRole(c, "master") {
			return errors.New("Role check failed")
		} else {
			return nil
		}
	},
}
```

這邊要注意，客戶端 (golang) 處理 connection 的 exception，要記得重新執行 sntnl.MasterAddr() 來取得 failover 後新指派的 master。

# Client 測試

寫一個 golang redis 的 client 跑起來。這個部分我們在 [kafka的章節]({{<ref "/posts/2019-09-24-kafka-basic-usage" >}})做過類似的事情，可以簡單湊一個玩玩。

# 延伸問題

使用上面的 golang 範例，確實是能透過 sentinel 取得 master，再向 master 取得連線。但這邊有兩個問題

* 客戶端需要支援 sentinel
* 客戶端要感知 sentinel 的位址連線，才能知道所有 sentinel 的位置，設定又產生耦合
  * 不能彈性的調度 sentinel，如果需要增加或是減少 sentinel，客戶端需要重新設定
  * 雖然 sentinel 有 HA，可是客戶端對 sentinel 的設定沒有 HA，萬一已知的所有 sentinel 掛了就全掛

有沒有更優雅的方式使用 sentinel，我們下篇會討論使用 HAProxy 來完成
