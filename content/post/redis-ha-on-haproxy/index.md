+++
title = "Redis Ha HAProxy"
subtitle = ""

# Add a summary to display on homepage (optional).
summary = ""

date = 2019-10-02T16:12:10+08:00
draft = true

# Authors. Comma separated list, e.g. `["Bob Smith", "David Jones"]`.
authors = []

# Is this a featured post? (true/false)
featured = false

# Tags and categories
# For example, use `tags = []` for no tags, or the form `tags = ["A Tag", "Another Tag"]` for one or more tags.
tags = ["kubernetes", "redis", "ci", "cd"]
categories = []

# Projects (optional).
#   Associate this post with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects = ["deep-learning"]` references 
#   `content/project/deep-learning/index.md`.
#   Otherwise, set `projects = []`.
# projects = ["internal-project"]

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder. 
[image]
  # Caption (optional)
  caption = ""

  # Focal point (optional)
  # Options: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight
  focal_point = ""
+++

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

* HAProxy Introduction
* Redis Sentinel with HAProxy

# HAProxy Intro

[HAproxy](http://www.haproxy.org/#docs) 全名是 High Availability Proxy，是一款開源 TCP/HTTP load balancer，他可以

* 聽 tcp socket，連 server，然後把 socket 接在一起讓雙向流通
* 可做 Http reverse-proxy (Http gateway)，自己作為代理 server，把接受到的 connection 傳到後端的 server。
* SSL 終端，可支援 client-side 與 server-side 的 ssl/tls
* 當 tcp/http normalizer
* 更改 http 的 request 與 response
* 當 switch，決定 request 後送的目標
* 做 load balancer，為後端 server 做負載均衡
* 調節流量，設定 rate limit，或是根據內容調整流量

HAProxy 還有其他非常多的功能，想了解細節可以來看[原理解說文件](http://cbonte.github.io/haproxy-dconv/1.9/intro.html#3)

# Topology

我們今天的範例是在後端的 redis 與 clients 中間多放一層 HAProxys

```

   +-------+   +--------+    +------------+    +---------+
   |Clients|---|HAProxys|----|redis master|----|sentinels|
   +-------+   +--------+    +------------+    +---------+

```

可能有人會問說，那前兩天講的 redis sentinel，跑去哪裡了。

sentinel 還在正常運作，負責監測 redis 狀態與 failover，只是 client 不再透過 sentinel 去取得 master，而是透過 HAProxy。

# Deploy HAProxy

我把我的寶藏都在這了[https://github.com/chechiachang/haproxy-kubernetes](https://github.com/chechiachang/haproxy-kubernetes)

下載下來的 .sh ，跑之前養成習慣貓一下
```
cat install.sh

#!/bin/bash

# redis-db-credentials should already exists
#kubectl create secret generic redis-db-credentials \
   --from-literal=REDIS_PASSWORD=123456

# Update haproxy.cfg as configmap
kubectl create configmap haproxy-config \
   --from-file=haproxy.cfg \
   --output yaml \
   --dry-run | kubectl apply -f -

kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

這邊做的事情有幾件

* 取得 redis 的 auth REDIS_PASSWORD 放在 secret 中，如果前面是照我們的範例，那都已經設定了
* 把 haproxy.cfg 的設定檔，使用 configmap 的方式放到 kubernetes 上
* 部屬 HAProxy deployment
* 部屬 HAProxy service

簡單看一下 deployment

```
apiVersion: apps/v1beta1
kind: Deployment
metadata:
  name: haproxy
spec:
  replicas: 3
  template:
    metadata:
      labels:
        app: haproxy
        app.kubernetes.io/name: haproxy
        component: haproxy
    spec:
      volumes:
      - name: haproxy-config
        configMap:
          name: haproxy-config
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: "app"
                  operator: "In"
                  values:
                  - "haproxy"
              topologyKey: kubernetes.io/hostname
      containers:
      - name: haproxy
        image: haproxy:2.0.3-alpine
        command: ["haproxy", "-f", "/usr/local/etc/haproxy/config/haproxy.cfg"]
        readinessProbe:
          initialDelaySeconds: 15
          periodSeconds: 5
          timeoutSeconds: 1
          successThreshold: 2
          failureThreshold: 2
          tcpSocket:
            port: 26999
            port: 6379
        volumeMounts:
        - name: haproxy-config
          mountPath: /usr/local/etc/haproxy/config
        resources:
          requests:
            cpu: 10m
            memory: 30Mi
        env:
        - name: REDIS_PASSWORD
          valueFrom:
            secretKeyRef:
              name: redis-db-credentials
              key: REDIS_PASSWORD
        ports:
        - containerPort: 8000
          name: http
        - containerPort: 9000
          name: https
        - containerPort: 26999
          name: stats
        - containerPort: 6379
          name: redis
```

* Replicas: 3 ，開起來是三個 HAProxy
* podAntiAffinity，三個分布到不同 node 上，盡量維持 HA
* readinessProbe，等 tcpSocket 26999 (HAProxy Stats) 與 6370 (Redis Proxy) 通了才 READY
* 把 redis password 掛進去
* 把 haproxy.cfg 掛進去
* 開幾個 port

看一下 service

```
kind: Service
apiVersion: v1
metadata:
  name: haproxy-service
spec:
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800 # 3 hr
  selector:
    app: haproxy
  ports:
    - name: http
      protocol: TCP
      port: 8000
    - name: https
      protocol: TCP
      port: 9000
    - name: stats
      protocol: TCP
      port: 26999
    - name: redis
      protocol: TCP
      port: 6379
    - name: redis-exporter
      protocol: TCP
      port: 8404
```

* 很單純，就是把幾個 port 接出來
* 把 sessionAffinity 開起來
   * 這邊希望來自相同 clientIP (kubernetes 內部 app clients) 的 session 能持續走同一個 server
   * 可以降低進到 service 往後送到一直重連浪費資源
   * 但一直連著也不好，可能會 connection not closed 一直佔著
   * HAProxy1 HAProxy2 HAProxy3，上次 Client1 連 HAProxy1，service 也盡量讓你下個 request 也走 HAPRoxy1

```
kubectl get po | grep haproxy

haproxy-56d94f857f-gmd4s                                 1/1     Running     0          47d
haproxy-56d94f857f-p2vj6                                 1/1     Running     0          47d
haproxy-56d94f857f-vhz8b                                 1/1     Running     0          47d
```

# HAProxy Config

看一下 haproxy.cfg

```
# https://cbonte.github.io/haproxy-dconv/2.0/configuration.html

# https://github.com/prometheus/haproxy_exporter
# https://www.haproxy.com/blog/haproxy-exposes-a-prometheus-metrics-endpoint/
# curl http://localhost:8404/metrics
# curl http://localhost:8404/stats
frontend stats
 mode http
 timeout client 30s
 bind *:8404
 option http-use-htx
 http-request use-service prometheus-exporter if { path /metrics }
 stats enable
 stats uri /stats
 stats refresh 10s

# Redis
frontend redis_gate
 mode tcp
 timeout client 7d
 bind 0.0.0.0:6379 name redis
 default_backend redis_servers

backend redis_servers
 mode tcp
 timeout connect 3s
 timeout server 7d
 option tcp-check
 tcp-check connect
 tcp-check send AUTH\ "${REDIS_PASSWORD}"\r\n
 tcp-check send PING\r\n
 tcp-check expect string PONG
 tcp-check send info\ replication\r\n
 tcp-check expect string role:master
 tcp-check send QUIT\r\n
 tcp-check expect string +OK
 server R1 redis-2-redis-ha-announce-0:6379 check inter 1s
 server R2 redis-2-redis-ha-announce-1:6379 check inter 1s
 server R3 redis-2-redis-ha-announce-2:6379 check inter 1s
```

* 兩個 frontend，吃前端 (client) 來的 request
   * frontend stats 是 HAProxy 本身服務的 stats
      * 把 prometheus-exporter 開起來，讓 prometheus 進來 scrape metrics
   * frontend redis_gate 是用來服務 redis client
      * 邏輯很簡單，進來的 request 往有效的 backend redis_server 送，這邊的有效指的是 redis master
      * timeout 7d，因為我們的服務有長時間不間斷的 pubsub，可以視需求調整
* 一個 backend，HAProxy 會維護並監測狀態，然後把 frontend proxy 過去
   * mode tcp，使用 tcp 去 probe
   * option tcp-check，下面是一串 tcp checklist，配合 redis 的 tcp auth protocol 去取得
      * tcp connect 連上
      * send AUTH 密碼 到 redis
      * send ping，redis 要回 pong
      * send info replication 直接打 redis tcp info API
      * 預期 string 內有 role:master 意思是這台 redis 是 master
      * 退出，redis 要回 ok
   * server 有三台，透過 redis 各自的 ha-announce service 去打

HAProxy 會維護 backend 的 proxy stats，找到三台 redis 中，是 master 的這台

Running Log

```
kubectl logs -f haproxy-123-123456789

[WARNING] 273/153936 (1) : Server redis_servers/R2 is DOWN, reason: Layer7 timeout, info: " at step 6 of tcp-check (expect string 'role:master')", check duration: 1000ms. 2 active and 0 backup servers left. 0 sessions active, 0 requeued, 0 remaining in queue.
[WARNING] 273/153937 (1) : Server redis_servers/R3 is DOWN, reason: Layer7 timeout, info: " at step 6 of tcp-check (expect string 'role:master')", check duration: 1001ms. 1 active and 0 backup servers left. 0 sessions active, 0 requeued, 0 remaining in queue.
```

HAProxy 去 redis 問，你是 master 嗎，兩個人回不是，只有一個回 role:master，所以把 client 導過去

# HAProxy vs Sentinel

* Client 不用知道中間的 proxy，只要知道透過 HAproxy service 就會被 proxy 到 master
* HAproxy 是 stateless，非常好 scale
* Client 不用支援 sentinel，只要一般的 redis-cli 就可以連入
