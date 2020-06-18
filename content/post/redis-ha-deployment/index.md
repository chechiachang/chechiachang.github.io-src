---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Redis Ha Deployment"
subtitle: ""
summary: ""
authors: []
tags: []
categories: []
date: 2019-09-28T15:14:23+08:00
lastmod: 2019-09-28T15:14:23+08:00
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: false

# Projects (optional).
#   Associate this post with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects = ["internal-project"]` references `content/project/deep-learning/index.md`.
#   Otherwise, set `projects = []`.
projects: []
---

[2020 It邦幫忙鐵人賽](https://ithelp.ithome.com.tw/2020ironman) 系列文章

- 在 GKE 上部署 Redis HA
  - [使用 helm 部署 redis-ha]({{< ref "/post/redis-ha-deployment" >}})
  - Redis HA with sentinel
  - Redis HA with HAproxy
  - 集群內部的 HA 設定，網路設定
  - 應用端的基本範例，效能調校
  - 在 GKE 上維運 redis

由於我比較熟悉 GCP / GKE 的服務，這篇的操作過程都會以 GCP 平台作為範例，不過操作過程大體上是跨平台通用的。

寫文章真的是體力活，覺得我的文章還有參考價值，請左邊幫我點讚按個喜歡，右上角幫我按個追縱，底下歡迎留言討論。給我一點繼續走下去的動力。

對我的文章有興趣，歡迎到我的網站上 [https://chechia.net](https://chechia.net) 閱讀其他技術文章，有任何謬誤也請各方大德直接聯繫我，感激不盡。

今天的文會比較短，因為我早上在綠島已經水肺潛水潛了三趟，有點累哈哈

![Exausted Cat Face](https://d32l83enj9u8rg.cloudfront.net/wp-content/uploads/iStock-966846550-cat-overheating-simonkr-1-940x470.jpg)

---

# Redis introduction

[Redis](https://redis.io/) 是常用的 in-memory 的資料儲存庫，可作為資料庫，快取，message broker 使用，都非常好用。Redis 官方支援 high availability，使用的是 [redis-sentinel](https://redis.io/topics/sentinel)
，今天我們就來部署一個有完整 sentinel 的 redis-ha。

Redis 另外提供了一個 solution [Redis cluster (multiple writer solution)](https://redis.io/topics/cluster-tutorial)，作為增加資料輸出帶寬，與增加資料耐用度的分散式解決方案，與 redis sentinel  所處理的 ha 問題是不相同的。有機會我們也來談。

# Deploy

我把我的寶藏都在這了[https://github.com/chechiachang/go-redis-ha](https://github.com/chechiachang/go-redis-ha)

下載下來的 .sh ，跑之前養成習慣貓一下
```
cat install.sh

#!/bin/bash
HELM_NAME=redis-1

# Stable: chart version: redis-ha-3.6.1	app version: 5.0.5
helm upgrade --install ${HELM_NAME} stable/redis-ha --version 3.6.1 -f values-staging.yaml
```

### Helm

我們這邊用 helm 部屬，之所以用 helm ，因為這是我想到最簡單的方法，能讓輕鬆擁有一套功能完整的 kafka。所以我們先用。

沒用過 helm 的大德可以參考 [Helm Quickstart](https://helm.sh/docs/using_helm/#quickstart)，先把 helm cli 與 kubernetes 上的 helm tiller 都設定好

### Redis-ha

[helm chart github](https://github.com/helm/charts/tree/master/stable/redis-ha)

# Install

這邊是用 upgrade --install，已安裝就 upgrade，沒安裝就 install，之後可以用這個指令升版

```
helm upgrade --install ${HELM_NAME} incubator/kafka --version 0.16.2 -f values-staging.yaml
```

### values-staging

完整的 values.yaml 在 [helm chart github](https://github.com/helm/charts/blob/master/stable/redis-ha/values.yaml)

```
image:
  repository: redis
  tag: 5.0.5-alpine
  pullPolicy: IfNotPresent

## replicas number for each component
replicas: 3

servers:
  serviceType: ClusterIP  # [ClusterIP|LoadBalancer]
  annotations: {}

auth: true

## Redis password
## Defaults to a random 10-character alphanumeric string if not set and auth is true
## ref: https://github.com/kubernetes/charts/blob/master/stable/redis-ha/templates/redis-auth-secret.yaml
##
#redisPassword:

## Use existing secret containing key `authKey` (ignores redisPassword)
existingSecret: redis-credentials

## Defines the key holding the redis password in existing secret.
authKey: auth
```

這邊有準備 secret/redis-credentials 裡面的 key[auth] 存放 redis 密碼，要連入的 pod 需要掛載 secret 並把 auth 匯入。

### Version

這邊使用的版本：

* chart version:    redis-ha-3.6.1
* app version:      5.0.5
* Redis Image:      redis:5.0.5-alpine
* Redis exporter:   oliver006/redis_exporter:v0.31.0

安裝完變這樣
```
$ kubectl get po | grep redis

NAME                                                     READY   STATUS      RESTARTS   AGE
redis-1-redis-ha-server-0                                3/3     Running     0          3d4h
redis-1-redis-ha-server-1                                3/3     Running     0          3d5h
redis-1-redis-ha-server-2                                3/3     Running     0          3d4h
```

describe pod 可以看到裡面有三個 container

* redis: 主要的 redis
* sentinel: 維護 redis 可用性的服務，會監測 redis 狀態，並把連線指派到新的 master
* redis-exporter: 把 redis 的運行資料(metrics) 送出到 promethues

# Networking

Service
```
NAME                        TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)                       AGE    SELECTOR
redis-redis-ha              ClusterIP   None           <none>        6379/TCP,26379/TCP,9121/TCP   46m    app=redis-ha,release=redis
redis-redis-ha-announce-0   ClusterIP   10.3.243.81    <none>        6379/TCP,26379/TCP            46m    app=redis-ha,release=redis,statefulset.kubernetes.io/pod-name=redis-redis-ha-server-0
redis-redis-ha-announce-1   ClusterIP   10.3.250.151   <none>        6379/TCP,26379/TCP            46m    app=redis-ha,release=redis,statefulset.kubernetes.io/pod-name=redis-redis-ha-server-1
redis-redis-ha-announce-2   ClusterIP   10.3.242.59    <none>        6379/TCP,26379/TCP            46m    app=redis-ha,release=redis,statefulset.kubernetes.io/pod-name=redis-redis-ha-server-2
```

```
nslookup redis-redis-ha

Name:      redis-redis-ha
Address 1: 10.0.0.42 redis-redis-ha-server-1.redis-redis-ha.default.svc.cluster.local
Address 2: 10.0.1.13 redis-redis-ha-server-2.redis-redis-ha.default.svc.cluster.local
Address 3: 10.0.2.8 redis-redis-ha-server-0.redis-redis-ha.default.svc.cluster.local

Name:      redis-redis-ha-server-1.redis-redis-ha.default.svc.cluster.local
Address 1: 10.0.0.43 redis-redis-ha-server-1.redis-redis-ha.default.svc.cluster.local
```

# 連線

所有連線透過 redis-redis-ha service 連入
```
redis-cli -h redis-redis-ha -p 6479 -a <password>
```

或是直接指定 redis instance 連入。
```
redis-cli -h redis-redis-ha-announce-0 -p 6479 -a <password>
redis-cli -h redis-redis-ha-announce-1 -p 6479 -a <password>
redis-cli -h redis-redis-ha-announce-2 -p 6479 -a <password>
```

但上面兩者會有問題，redis 只有 master 是 writable，連入 slave 會變成 readonly，如果沒有任何 probe 機智，那就是每次連線時有 2/3 機率會連到 readonly 的 redis slave 。所以連線前要先找到正確的 master

# Sentinel

Sentinel 是 redis 官方提供的 HA solution，主要負責監控 redis 的狀態，並控制 redis master 的 failover 機制，一但超過 threshold，sentinel 就會把 master failover 到其他 slave 上。並把 master 連線指向新 master。

redis sentinel 與 redis 使用相容的 api，直接使用 redis-cli 透過 26479 port 連入，可以連到 sentinel，透過 sentinel 可以取得 redis master 的狀態與連線設定。
```
redis-cli -h redis-redis-ha -p 26479
```

# App 端支援 sentinel

需要有支援 sentinel 的 redis client library，例如: python redis-py 有支援 sentinel 的設定。

這邊就會比較麻煩，因為不是所有的語言對 redis-sentinel 的支援性都夠好，或是沒辦法設定到妮旺使用的情境上。

如果你找得到支援性良好的套件，恭喜你。不然就像我們公司，與我們的需求有衝突，只好自己 fork library。

所以說直接使用有支援 redis-sentinel 可能會遇到一些問題。那也沒有更好的解決方法？我們下次說明使用 HAproxy 的高可用方案。

# Benchmark

部署完後，可以跑一下 benchmark，看看在 kubernetes 上運行的效能有沒有符合需求。

Run a redis pod with sleep command
NOTE: CPU usage (rapidly) increasing during benchmark
DON'T DO THIS on PRODUCTION
```
kubectl run test-redis --image redis:5.0.5-alpine --command sleep 36000
kubectl exec -it test-redis-xxxxxxxxx-xxxxx sh
```

Benchmark
```
redis-benchmark --help
redis-benchmark \
  -h haproxy-service.local \
  -p 6379 \
  -c 100 \
  -d 30 \
  -n 1000000

====== MSET (10 keys) ======
100000 requests completed in 2.32 seconds
50 parallel clients
3 bytes payload
keep alive: 1

85.37% <= 1 milliseconds
98.06% <= 2 milliseconds
99.18% <= 3 milliseconds
99.62% <= 4 milliseconds
99.93% <= 5 milliseconds
100.00% <= 5 milliseconds
43066.32 requests per second
```
