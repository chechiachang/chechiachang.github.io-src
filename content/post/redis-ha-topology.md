---
title: "Redis Ha Topology"
subtitle: ""

# Add a summary to display on homepage (optional).
summary: ""

date: 2019-08-23T16:12:10+08:00
draft: false

# Authors. Comma separated list, e.g. `["Bob Smith", "David Jones"]`.
authors: []

# Is this a featured post? (true/false)
featured: false

# Tags and categories
# For example, use `tags: []` for no tags, or the form `tags: ["A Tag", "Another Tag"]` for one or more tags.
tags: ["kubernetes", "redis", "ci", "cd"]
categories: []

menu:
  main:
    parent: "Ithelp 鐵人賽"
    weight: 1
---

[2020 It邦幫忙鐵人賽](https://ithelp.ithome.com.tw/2020ironman) 系列文章

- 在 GKE 上部署 Redis HA
  - [使用 helm 部署 redis-ha]({{< ref "/post/redis-ha-deployment" >}})
  - Redis HA with sentinel
  - Redis sentinel topology
  - Redis HA with HAproxy
  - 集群內部的 HA 設定，網路設定
  - 應用端的基本範例，效能調校
  - 在 GKE 上維運 redis

由於我比較熟悉 GCP / GKE 的服務，這篇的操作過程都會以 GCP 平台作為範例，不過操作過程大體上是跨平台通用的。

寫文章真的是體力活，覺得我的文章還有參考價值，請左邊幫我點讚按個喜歡，右上角幫我按個追縱，底下歡迎留言討論。給我一點繼續走下去的動力。

對我的文章有興趣，歡迎到我的網站上 [https://chechia.net](https://chechia.net) 閱讀其他技術文章，有任何謬誤也請各方大德直接聯繫我，感激不盡。

![Exausted Cat Face](https://d32l83enj9u8rg.cloudfront.net/wp-content/uploads/iStock-966846550-cat-overheating-simonkr-1-940x470.jpg)

---

# 摘要

* Redis Sentinel Topology

# Topology

* Masters: M1, M2, M3, ..., Mn.
* Slaves: R1, R2, R3, ..., Rn (R stands for replica).
* Sentinels: S1, S2, S3, ..., Sn.
* Clients: C1, C2, C3, ..., Cn.
* 每個方格代表一台機器或是 VM

### 2 Sentinels

DON'T DO THIS

```
+----+         +----+
| M1 |---------| R1 |
| S1 |         | S2 |
+----+         +----+

Configuration: quorum = 1
```

這個設定下，如果 M1 掛了需要 failover，很有可能 S1 跟著機器一起掛了，S2 會沒有辦法取得多數來執行 failover，整個系統掛掉

### 3 VM

```
       +----+
       | M1 |
       | S1 |
       +----+
          |
+----+    |    +----+
| R2 |----+----| R3 |
| S2 |         | S3 |
+----+         +----+

Configuration: quorum = 2
```

這是最基本的蛋又兼顧安全設定的設置

如果 M1 死了 S1 跟著機器故障，S2 與 S3 還可以取得多數，順利 failover 到 R2 或是 R3。

### 寫入資料遺失

```
         +----+
         | M1 |
         | S1 | <- C1 (writes will be lost)
         +----+
            |
            /
            /
+------+    |    +----+
| [M2] |----+----| R3 |
| S2   |         | S3 |
+------+         +----+
```

* failover 之前，M1 是 master，Client 的寫入往 M1 寫
* M1 網路故障，M2 failover 後成為新的 master，可是 Client 往 M1 寫入的資料並無法 sync 回 M2
* 等網路修復後，M1 回覆後會變成 R1 變成 slave，由 M2 去 sync R1，變成 R1 在 master 時收到的寫入資料遺失

為了避免這種情形，做額外的設定

* min-slaves-to-write 1
* min-slaves-max-lag 10

當 master 發現自己再也無法 sync 到足夠的 slave，表示 master 可能被孤立，這時主動拒絕客戶端的寫入請求。客戶端被拒絕後，會再向 sentinel 取得有效的 master，重新執行寫入請求，確保資料寫到有效的 master 上。

### Sentinel 放在 Client 端

```
            +----+         +----+
            | M1 |----+----| R1 |
            |    |    |    |    |
            +----+    |    +----+
                      |
         +------------+------------+
         |            |            |
         |            |            |
      +----+        +----+      +----+
      | C1 |        | C2 |      | C3 |
      | S1 |        | S2 |      | S3 |
      +----+        +----+      +----+
```

有些情形，redis 這端只有兩台可用機器，這種情形可以考慮把 sentinel 放在客戶端的機器上

* 仍然維持了獨立的 3 sentinels 的穩定
* sentinel 與 client 所觀察到的 redis 狀態是相同的
* 如果 M1 死了，要 failover ，客戶端的 3 sentinel 可以正確地執行 failover，不受故障影響

### 客戶端又不足 3 個

```
            +----+         +----+
            | M1 |----+----| R1 |
            | S1 |    |    | S2 |
            +----+    |    +----+
                      |
               +------+-----+
               |            |  
               |            |
            +----+        +----+
            | C1 |        | C2 |
            | S3 |        | S4 |
            +----+        +----+

      Configuration: quorum = 3

            +----+         +----+
            | M1 |----+----| R1 |
            | S1 |    |    | S2 |
            +----+    |    +----+
                      |
                      |        
                      |        
                   +----+      
                   | C1 |      
                   | S3 |      
                   +----+      

      Configuration: quorum = 2
```

* 跟上個例子類似，但又額外確保 3 sentinels
* 如果 M1 死了，剩下的 sentinel 可以正確 failover
