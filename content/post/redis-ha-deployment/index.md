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

對我的文章有興趣，歡迎到我的網站上 [https://chechiachang.github.io](https://chechiachang.github.io) 閱讀其他技術文章，有任何謬誤也請各方大德直接聯繫我，感激不盡。

![Exausted Cat Face](https://d32l83enj9u8rg.cloudfront.net/wp-content/uploads/iStock-966846550-cat-overheating-simonkr-1-940x470.jpg)

---

# Redis introduction

[Redis](https://redis.io/) 是常用的 in-memory 的資料儲存庫，可作為資料庫，快取，message broker 使用，都非常好用。Redis 官方支援 high availability，使用的是 [redis-sentinel](https://redis.io/topics/sentinel)
，今天我們就來部署一個有完整 sentinel 的 redis-ha。

Redis 另外提供了一個 solution [Redis cluster (multiple writer solution)](https://redis.io/topics/cluster-tutorial)，作為增加資料輸出帶寬，與增加資料耐用度的分散式解決方案，與 redis sentinel  所處理的 ha 問題是不相同的。有機會我們也來談。

# Deploy

我把我的寶藏都在這了[https://github.com/chechiachang/kafka-on-kubernetes](https://github.com/chechiachang/kafka-on-kubernetes)

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

# Install

這邊是用 upgrade --install，已安裝就 upgrade，沒安裝就 install，之後可以用這個指令升版

```
helm upgrade --install ${HELM_NAME} incubator/kafka --version 0.16.2 -f values-staging.yaml
```

### Version

這邊使用的版本：

* chart version:    redis-ha-3.6.1
* app version:      5.0.5
* Redis Image:      redis:5.0.5-alpine
* Redis exporter:   oliver006/redis_exporter:v0.31.0

# Architecture

- Pods
  - redis-server-0-master (only read/write instance)
  - redis-server-1-slave (readonly, master elagiable) 
  - redis-server-2-slave (readonly, master elagiable) 
  - ...
  - haproxy server (stateless replica)
  - haproxy server (stateless replica)
  - ...
  - [Client] redis-client app
  - ...
  - [Monitoring] redis-metrics-exporter (sidecar container with redis server)
  - [Monitoring] haproxy-metrics-exporter (native supported by haproxy)

# Redis HA

We use stable/redis-ha with haproxy. Check [this doc] (TODO) to find why we use this.

- Current
  - chart version: 3.6.1 redis version: 5.0.5
  - redis:5.0.5-alpine
  - All pods are master elagible with auto failover

# Networking

Service
```
NAME                        TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)                       AGE    SELECTOR
redis-redis-ha              ClusterIP   None           <none>        6379/TCP,26379/TCP,9121/TCP   46m    app=redis-ha,release=redis
redis-redis-ha-announce-0   ClusterIP   10.3.243.81    <none>        6379/TCP,26379/TCP            46m    app=redis-ha,release=redis,statefulset.kubernetes.io/pod-name=redis-redis-ha-server-0
redis-redis-ha-announce-1   ClusterIP   10.3.250.151   <none>        6379/TCP,26379/TCP            46m    app=redis-ha,release=redis,statefulset.kubernetes.io/pod-name=redis-redis-ha-server-1
redis-redis-ha-announce-2   ClusterIP   10.3.242.59    <none>        6379/TCP,26379/TCP            46m    app=redis-ha,release=redis,statefulset.kubernetes.io/pod-name=redis-redis-ha-server-2
```

### DNS

```
nslookup haproxy-service

Name:      haproxy-service
Address 1: 10.15.252.147 haproxy-service.default.svc.cluster.local
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

# Connect

All standard connection to redis should get connection through haproxy. Haproxy will maintain tcp connection to current redis-master host.
```
redis-cli -h haproxy-service -p 6479 -a <password>
```

Haproxy itself connect to redis using services for each redis instance pods. Check `haproxy.cfg` for configuration.
```
redis-cli -h redis-redis-ha-announce-0 -p 6479 -a <password>
redis-cli -h redis-redis-ha-announce-1 -p 6479 -a <password>
redis-cli -h redis-redis-ha-announce-2 -p 6479 -a <password>
```

Connect through one service to all redis instances with loadbalancing. Since kubernetes servivce does not distinguish writable master from readonly slaves,
there is no garantee to high availability (with only 1/3 change of sucess with 1 master and 2 slaves)
DON'T USE THIS
```
redis-cli -h redis-redis-ha -p 6479 -a <password>
```

# Auto Failover

### Single Slave failure

- [Client] Connection not affected
- [Kubernetes] service liveness check fail
- [Sentinel] notice a slave failure

```
# +sdown slave 10.3.243.81:6379 10.3.243.81 6379 @ mymaster 10.3.250.151 6379
# -sdown sentinel 0c09a3866dba0f3b43ef2e383b5dc05980900fd8 10.3.243.81 26379 @ mymaster 10.3.250.151 6379
# -sdown slave 10.3.243.81:6379 10.3.243.81 6379 @ mymaster 10.3.250.151 6379
```

### Single Master failure

- [Kubernetes] service liveness check fail
  - [Kubernetes] dns endpoints changed
  - [Client] connect to another slave (read-only)
- [Sentinel] liveness check fail
  - [Sentinel] reach quorum and failover old master to new master from 1 of existing slave

```
# oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
# Redis version=5.0.5, bits=64, commit=00000000, modified=0, pid=1, just started
# Configuration loaded
* Running mode=sentinel, port=26379.
# WARNING: The TCP backlog setting of 511 cannot be enforced because /proc/sys/net/core/somaxconn is set to the lower value of 128.
# Sentinel ID is e6be0f70406122877338f7c814b17a7c7b648d82

# +monitor master mymaster 10.3.243.81 6379 quorum 2
* +slave slave 10.3.250.151:6379 10.3.250.151 6379 @ mymaster 10.3.243.81 6379
* +sentinel sentinel 0c09a3866dba0f3b43ef2e383b5dc05980900fd8 10.3.243.81 26379 @ mymaster 10.3.243.81 6379

# +new-epoch 4
# +sdown slave 10.3.250.151:6379 10.3.250.151 6379 @ mymaster 10.3.243.81 6379
# -sdown slave 10.3.250.151:6379 10.3.250.151 6379 @ mymaster 10.3.243.81 6379
* +slave slave 10.3.242.59:6379 10.3.242.59 6379 @ mymaster 10.3.243.81 6379
* +sentinel sentinel 31f8f52b34feaddcabdd6bf1827aeb02be44d2e3 10.3.242.59 26379 @ mymaster 10.3.243.81 6379
# +sdown master mymaster 10.3.243.81 6379
# +sdown sentinel 0c09a3866dba0f3b43ef2e383b5dc05980900fd8 10.3.243.81 26379 @ mymaster 10.3.243.81 6379

# +new-epoch 5
# +vote-for-leader 31f8f52b34feaddcabdd6bf1827aeb02be44d2e3 5
# +odown master mymaster 10.3.243.81 6379 #quorum 2/2
# Next failover delay: I will not start a failover before Tue Jul  9 07:00:01 2019
# +config-update-from sentinel 31f8f52b34feaddcabdd6bf1827aeb02be44d2e3 10.3.242.59 26379 @ mymaster 10.3.243.81 6379
# +switch-master mymaster 10.3.243.81 6379 10.3.242.59 6379
* +slave slave 10.3.250.151:6379 10.3.250.151 6379 @ mymaster 10.3.242.59 6379
* +slave slave 10.3.243.81:6379 10.3.243.81 6379 @ mymaster 10.3.242.59 6379
# +sdown slave 10.3.243.81:6379 10.3.243.81 6379 @ mymaster 10.3.242.59 6379
# Executing user requested FAILOVER of 'mymaster'

# +new-epoch 6
# +try-failover master mymaster 10.3.242.59 6379
# +vote-for-leader e6be0f70406122877338f7c814b17a7c7b648d82 6
# +elected-leader master mymaster 10.3.242.59 6379
# +failover-state-select-slave master mymaster 10.3.242.59 6379
# +selected-slave slave 10.3.250.151:6379 10.3.250.151 6379 @ mymaster 10.3.242.59 6379
* +failover-state-send-slaveof-noone slave 10.3.250.151:6379 10.3.250.151 6379 @ mymaster 10.3.242.59 6379
* +failover-state-wait-promotion slave 10.3.250.151:6379 10.3.250.151 6379 @ mymaster 10.3.242.59 6379
# +promoted-slave slave 10.3.250.151:6379 10.3.250.151 6379 @ mymaster 10.3.242.59 6379
# +failover-state-reconf-slaves master mymaster 10.3.242.59 6379
# +failover-end master mymaster 10.3.242.59 6379
# +switch-master mymaster 10.3.242.59 6379 10.3.250.151 6379
* +slave slave 10.3.243.81:6379 10.3.243.81 6379 @ mymaster 10.3.250.151 6379
* +slave slave 10.3.242.59:6379 10.3.242.59 6379 @ mymaster 10.3.250.151 6379
# +sdown slave 10.3.243.81:6379 10.3.243.81 6379 @ mymaster 10.3.250.151 6379
# -sdown sentinel 0c09a3866dba0f3b43ef2e383b5dc05980900fd8 10.3.243.81 26379 @ mymaster 10.3.250.151 6379
# -sdown slave 10.3.243.81:6379 10.3.243.81 6379 @ mymaster 10.3.250.151 6379
```

### 2/3 Master Failure

- Get error: NOREPLICAS Not enough good replicas to write.
- Whole redis become readonly for a while since there is no healthy mater
- Might fail to auto-recover or loss data if sentinel lose quorum
- Auto-recover
- Become writable after the replica quorum requirements reached

### Single Sentinel Failure


### Haproxy Failure

Since haproxy-server are stateless and working independently, haproxy-service should be fine as long as there is at least 1 healthy haproxy-server.
Kubernetes will restart failed haproxy-server, and server will re-establish liveness checks and connection to redis instances.

# Debug

Run a client pod (ex. golang) with sleep command
```
kubectl run go-test --image golang:1.12.6-alpine3.10 --command sleep 36000
kubectl exec -it go-test-xxxxxxxxx-xxxxx sh
```

Run a client pod (ex. python) with sleep command
```
kubectl run python-test --image python:3.6.5-alpine --command sleep 36000
kubectl exec -it python-test-xxxxxxxxx-xxxxx sh
```
# Benchmark

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
