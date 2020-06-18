+++
title = "Prometheus Deployment on Kubernetes"
subtitle = ""

# Add a summary to display on homepage (optional).
summary = ""

date = 2019-10-04T16:12:10+08:00
draft = false

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

- Prometheus / Grafana (5)
  - [GKE 上自架 Prometheus / Grafana]({{< ref "/post/prometheus-deployment-on-kubernetes" >}})
  - [GKE 上自架 Grafana 與設定]({{< ref "/post/prometheus-deploy-grafana" >}})
  - 使用 exporter 監測 GKE 上的各項服務
  - 輸出 kubernetes 的監測數據
  - 輸出 redis-ha 的監測數據
  - 輸出 kafka 的監測數據

由於我比較熟悉 GCP / GKE 的服務，這篇的操作過程都會以 GCP 平台作為範例，不過操作過程大體上是跨平台通用的。

寫文章真的是體力活，覺得我的文章還有參考價值，請左邊幫我點讚按個喜歡，右上角幫我按個追縱，底下歡迎留言討論。給我一點繼續走下去的動力。

對我的文章有興趣，歡迎到我的網站上 [https://chechia.net](https://chechia.net) 閱讀其他技術文章，有任何謬誤也請各方大德直接聯繫我，感激不盡。

![Exausted Cat Face](https://d32l83enj9u8rg.cloudfront.net/wp-content/uploads/iStock-966846550-cat-overheating-simonkr-1-940x470.jpg)

---

# 摘要

* Prometheus Introduction
* Deploy Prometheus

# Prometheus Introduction

生產環境與非生產環境，其中的一指標就是有沒有足夠完整的服務監測系統，這句話可以看出服務監測對於產品化是多麼重要。而監控資料 (metrics) 的收集與可視化工具其實非常多，例如上周介紹的 ELK Stack，這次我們要來介紹另外一個很多人使用的 prometheus。

[Promethues 在官網上提到](https://prometheus.io/) 是一個 Monitoring system and time series database

* 可以收集高維度的資料
* 使用自己的 PromQL 做有效且精簡的資料查詢
* 內建資料瀏覽器，並且與 Grafana 高度整合
* 支援 sharding 與 federation，來達到水平擴展
* 有許多隨插即用的整合 exporter，例如 redis-exporter, kafka-exporter，kubernetes-exporter ，都可以直接取得資料
* 支援 alert，使用 PromQL 以及多功能的告警，可以設定精準的告警條件

# 與 ELK 做比較

基本上 Prometheus 跟 ELK 比，其實是很奇怪的一件事，但這也是最常被問的一個問題。兩者在本質上是完全不同的系統。

* Prometheus 是 based on time series database 的資料收集系統
* ELK 是基於全文搜索引擎的資料查詢系統

是的，他們都能做 metrics 收集，在有限的尺度下，能達到一樣的效果。但這樣說的意思就等於是在說 mesos DC/OS 與 kubenetes 都能跑 container cluster 一樣，底下是完全不一樣的東西。

兩者的差異使用上差非常多

* metrics 結構: ELK 借助全文搜索引擎，基本上送什麼資料近來都可以查找。Prometheus metrics 拉進來是 time series 的 key-value pairs。
* 維護同樣的 metrics，prometheus 的使用的儲存空間遠小於 elasticsearch
* prometheus 針對 time based 的搜尋做了很多優化，效能很高
* Prometheus 對於記憶體與 cpu 的消耗也少很多
* Elasticsearch 資源上很貴，是因為在處理大量 text log 的時候，他能夠用後段的 pipeline 處理內容，再進行交叉比對，可以從 text 裡面提取很多未事先定義的資料
* Elasticsearch 的維護工作也比較複雜困難

如果要收集服務運行資料，可以直接選 prometheus。如果有收集 log 進行交叉比對，可以考慮 elk。

### Helm

我們這邊用 helm 部屬，之所以用 helm ，因為這是我想到最簡單的方法，能讓輕鬆擁有一套功能完整的 prometheus。所以我們先用。

沒用過 helm 的大德可以參考 [Helm Quickstart](https://helm.sh/docs/using_helm/#quickstart)，先把 helm cli 與 kubernetes 上的 helm tiller 都設定好


# Deploy Prometheus

我把我的寶藏都放在這了[https://github.com/chechiachang/prometheus-kubernetes](https://github.com/chechiachang/prometheus-kubernetes)

下載下來的 .sh ，跑之前養成習慣貓一下
```
cat install.sh

#!/bin/bash
HELM_NAME=prometheus-1

helm upgrade --install ${HELM_NAME} stable/prometheus \
  --namespace default \
  --values values-staging.yaml
```

### Configuration

[Prometheus Stable Chart](https://github.com/helm/charts/tree/master/stable/prometheus)

values.yaml 很長，但其實各個元件設定是重複的,設定好各自的 image,
replicas, service, topology 等等
 
```
alertmanager:
  enabled: true

kubeStateMetrics:
  enabled: true

nodeExporter:
  enabled: true

server:
  enabled: true

pushgateway:
  enabled: true
```

底下有更多 runtime 的設定檔

* 定義好 global 的 scrape 間距，越短 metrics 維度就越精準
* PersistenVolume 強謝建議開起來，維持歷史的資料
  * 加上 storage usage 的 self monitoring（之後會講) 才不會滿出來 server 掛掉
* server 的 scrapeConfigs 是 server 去收集的 job 設定。稍後再來細講。

```
server:
  global:
    ## How frequently to scrape targets by default
    ##
    scrape_interval: 10s
    ## How long until a scrape request times out
    ##
    scrape_timeout: 10s
    ## How frequently to evaluate rules
    ##
    evaluation_interval: 10s
  persistentVolume:
    ## If true, Prometheus server will create/use a Persistent Volume Claim
    ## If false, use emptyDir
    ##
    enabled: true

    ## Prometheus server data Persistent Volume access modes
    ## Must match those of existing PV or dynamic provisioner
    ## Ref: http://kubernetes.io/docs/user-guide/persistent-volumes/
    ##
    accessModes:
      - ReadWriteOnce

    ## Prometheus server data Persistent Volume annotations
    ##
    annotations: {}

    ## Prometheus server data Persistent Volume existing claim name
    ## Requires server.persistentVolume.enabled: true
    ## If defined, PVC must be created manually before volume will be bound
    existingClaim: ""

    ## Prometheus server data Persistent Volume mount root path
    ##
    mountPath: /data

    ## Prometheus server data Persistent Volume size
    ##
    size: 80Gi

alertmanagerFiles:

serverFiles:

```

部屬完看一下

```
kubectl get pods --selector='app=prometheus'

NAME                                             READY   STATUS    RESTARTS   AGE
prometheus-alertmanager-694d6694c6-dvkwd         2/2     Running   0          8d
prometheus-kube-state-metrics-85f6d75f8b-7vlkp   1/1     Running   0          8d
prometheus-node-exporter-2mpjc                   1/1     Running   0          8d
prometheus-node-exporter-kg7fj                   1/1     Running   0          51d
prometheus-node-exporter-snnn5                   1/1     Running   0          8d
prometheus-pushgateway-5cdfb4979c-dnmjn          1/1     Running   0          8d
prometheus-server-59b8b8ccb4-bplkx               2/2     Running   0          8d

kubectl get services --selector='app=prometheus'

NAME                            TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
prometheus-alertmanager         ClusterIP   10.15.241.66   <none>        80/TCP     197d
prometheus-kube-state-metrics   ClusterIP   None           <none>        80/TCP     197d
prometheus-node-exporter        ClusterIP   None           <none>        9100/TCP   197d
prometheus-pushgateway          ClusterIP   10.15.254.0    <none>        9091/TCP   197d
prometheus-server               ClusterIP   10.15.245.10   <none>        80/TCP     197d

kubectl get endpoints --selector='app=prometheus'

NAME                            ENDPOINTS                                             AGE
prometheus-alertmanager         10.12.6.220:9093                                      197d
prometheus-kube-state-metrics   10.12.6.222:8080                                      197d
prometheus-node-exporter        10.140.0.30:9100,10.140.0.9:9100,10.140.15.212:9100   197d
prometheus-pushgateway          10.12.6.211:9091                                      197d
prometheus-server               10.12.3.14:9090                                       197d
```

簡單說明一下

* prometheus-server 是主要的 api-server 以及 time series database
* alertmanager 負責告警工作
* pushgateway 提供 client 端主動推送 metrics 給 server 的 endpoint
* kube-state-metrics 是開來收集 cluster wide 的 metrics, 像是 pods running counts, deployment ready count, total pods number 等等 metrics
* node-exporter 是 daemonsets, 把每一個 node 的 metrics, 像是 memory, cpu, disk...等資料,收集出來

主要服務存取就是透過 prometheus-server

# Access Prometheus server

除了直接 exec -it 進去 prometheus-server 以外，由於 prometheus 本身有提供 web portal, 所以我們這邊透過 port forwarding 打到本機上

```
PROMETHEUS_POD_NAME=$(kc get po -n default --selector='app=prometheus,component=server' -o=jsonpath='{.items[0].metadata.name}')

kubectl --namespace default port-forward ${PROMETHEUS_POD_NAME} 9090
```

透過 browser 就可以連入操作

```
http://localhost:9090
```

也可以透過 [HTTP API](https://prometheus.io/docs/prometheus/latest/querying/api/) 用程式接入控制

# Prometheus Web

Prometheus 本慎提供的 UI 其實功能就很強大

* 可以查到 (已經匯入存在) 的 metrics
* 可以在上面執行 PromQL 查詢語法
* 查詢運行的 status
* 查詢目前所有收集的 targets 的狀態,有收集器掛了也可以在這邊看到

# 小結

* 輕鬆自架 prometheus
* Prometheus 頁面有精簡，但是功能完整的 graph 製圖
* 但大家通常會使用 Grafana 搭配使用, 用過都說讚, 我們明天繼續
