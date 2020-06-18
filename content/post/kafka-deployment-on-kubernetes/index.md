---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Kafka Deployment on Kubernetes"
subtitle: ""
summary: ""
authors: []
tags: []
categories: []
date: 2019-09-22T09:58:41+08:00
lastmod: 2019-09-22T09:58:41+08:00
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

- ELK Stack
  - [Self-host ELK stack on GCP]({{< ref "/post/self-host-elk-stack-on-gcp" >}})
  - [Secure ELK Stask]({{< ref "/post/secure-elk-stack" >}})
  - [監測 Google Compute Engine 上服務的各項數據]({{< ref "/post/monitoring-gce-with-elk" >}})
  - [監測 Google Kubernetes Engine 的各項數據]({{<ref "/post/monitoring-gke-with-elk" >}})
  - [是否選擇 ELK 作為解決方案]({{< ref "/post/elastic-or-not-elastic" >}})
  - [使用 logstash pipeline 做數據前處理]({{< ref "/post/logstash-on-gke" >}})
  - Elasticsearch 日常維護：數據清理，效能調校，永久儲存
  - Debug ELK stack on GCP
- Kafka HA on Kubernetes
  - [Deploy kafka-ha]({{ ref "/post/kafka-deployment-on-kubernetes" }})
  - [Kafka Introduction]({{ ref "/post/kafka-introduction" }})
  - [kafka 基本使用]({{ ref "/post/kafka-basic-usage" }}) 
  - [kafka operation scripts]({{ ref "/post/kafka-operation-script"}})
  - [集群內部的 HA topology]({{ ref "/post/kafka-ha-topology" }})
  - [集群內部的 HA 細節]({{ ref "/post/kafka-ha-continuerd" }})
  - Prometheus Metrics Exporter 很重要
  - 效能調校
  
由於我比較熟悉 GCP / GKE 的服務，這篇的操作過程都會以 GCP 平台作為範例，不過操作過程大體上是跨平台通用的。

---

# 碎念

30 天每天一文真的蠻逼人的，每一篇都是新寫，還要盡可能顧及文章品質，下班趕文章，各位大德寫看看就知道

* 這邊調整了當初想寫的文章，內容應該都會帶到
  * elk
  * kafka-ha
  * reids-ha
  * prometheus
  * kubernetes on gcp
* 但不會再一篇 10000 字了，逼死我吧...
* 寫不完的部份 30 天候會在IT邦幫忙，或是[我的 Github Page https://chechia.net/](https:/chechia.net)補完

寫文章真的是體力活，覺得我的文章還有參考價值，請左邊幫我點讚按個喜歡，右上角幫我按個追縱，底下歡迎留言討論。給我一點繼續走下去的動力。

![Exausted Cat Face](https://d32l83enj9u8rg.cloudfront.net/wp-content/uploads/iStock-966846550-cat-overheating-simonkr-1-940x470.jpg)

---

# 摘要

* 簡介 kafka
* 部屬 kafka 到 kubernetes 上

# 簡介 kafka

Kafka 是分散式的 streaming platform，可以 subscribe & publish 訊息，可以當作是一個功能強大的 message queue 系統，由於分散式的架構，讓 kafka 有很大程度的 fault tolerance。

我們今天就來部屬一個 kafka。

# Deploy

我把我的寶藏都在這了[https://github.com/chechiachang/kafka-on-kubernetes](https://github.com/chechiachang/kafka-on-kubernetes)

下載下來的 .sh ，跑之前養成習慣貓一下
```
cat install.sh


#!/bin/bash
#
# https://github.com/helm/charts/tree/master/incubator/kafka

#HELM_NAME=kafka
HELM_NAME=kafka-1

helm repo add incubator http://storage.googleapis.com/kubernetes-charts-incubator

# Stable: chart version: kafka-0.16.2	app version: 5.0.1
helm upgrade --install ${HELM_NAME} incubator/kafka --version 0.16.2 -f values-staging.yaml
```

### Helm

我們這邊用 helm 部屬，之所以用 helm ，因為這是我想到最簡單的方法，能讓輕鬆擁有一套功能完整的 kafka。所以我們先用。

沒用過 helm 的大德可以參考 [Helm Quickstart](https://helm.sh/docs/using_helm/#quickstart)，先把 helm cli 與 kubernetes 上的 helm tiller 都設定好

```
helm init
```

### Helm Chart

一個 helm chart 可以當成一個獨立的專案，不同的 chart 可以在 kubernetes 上協助部屬不同的項目。

這邊使用了還在 incubator 的chart，雖然是 prod ready，不過使用上還是要注意。

使用前先把 incubator 的 helm repo 加進來

```
helm repo add incubator http://storage.googleapis.com/kubernetes-charts-incubator
```

### Install

這邊是用 upgrade --install，已安裝就 upgrade，沒安裝就 install，之後可以用這個指令升版

```
helm upgrade --install ${HELM_NAME} incubator/kafka --version 0.16.2 -f values-staging.yaml
```

### Version

這邊使用的版本：

* chart version:    kafka-0.16.2
* app version:      5.0.1
* kafka Image:      confluentinc/cp-kafka:5.0.1
* zookeeper Image:  gcr.io/google_samples/k8szk:v3
* kafka exporter:   danielqsj/kafka-exporter:v1.2.0

### values-staging

透過 helm chart，把啟動參數帶進去，這邊我們看幾個比較重要的，細節之後的文章在一起討論。

https://github.com/chechiachang/kafka-on-kubernetes/blob/master/values-staging.yaml

```
replicas: 3
```

安裝三個 kafka，topology 的東西也是敬待下篇XD

```
## The kafka image repository
image: "confluentinc/cp-kafka"

## The kafka image tag

底層執行的 kafka 是 conluent kafka

```
## Configure resource requests and limits
## ref: http://kubernetes.io/docs/user-guide/compute-resources/
resources: {}
  # limits:
  #   cpu: 200m
  #   memory: 4096Mi
  # requests:
  #   cpu: 100m
  #   memory: 1024Mi
kafkaHeapOptions: "-Xmx4G -Xms1G"
```

這邊可以調整在 kubernetes 上面的 limit 跟 request

* Deploy 會先去跟 node 問夠不夠，夠的話要求 node 保留這些資源給 Pod
* Runtime 超過 limit，Pod 會被 kubernetes 幹掉，不過我們是 JVM，外部 resource 爆掉前，應該會先因 heap 滿而死。一個施主自盡的感覺。
* CPU 蠻省的，吃比較多是 memory。但也要看你的使用情境

```
prometheus
```

對我們有上 promethues，基本上就是 kafka-exporter 把 kafka metrics 倒出去 prometheus，這個也是詳見下回分解。

# 跑起來了

```
$ kubectl get po | grep kafka

NAME                                                     READY   STATUS      RESTARTS   AGE
kafka-1-0                                                1/1     Running     0          224d
kafka-1-1                                                1/1     Running     0          224d
kafka-1-2                                                1/1     Running     0          224d
kafka-1-exporter-88786d84b-z954z                         1/1     Running     0          224d
kafka-1-zookeeper-0                                      1/1     Running     0          224d
kafka-1-zookeeper-1                                      1/1     Running     0          224d
kafka-1-zookeeper-2                                      1/1     Running     0          224d
```
