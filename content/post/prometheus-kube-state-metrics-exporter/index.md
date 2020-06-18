+++
title = "Prometheus & Kubernetes State Metrics Exporter"
subtitle = ""

# Add a summary to display on homepage (optional).
summary = ""

date = 2019-10-07T8:12:10+08:00
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
  - GKE 上自架 Grafana 與設定
  - 使用 exporter 監測 GKE 上的各項服務
  - 輸出 redis-ha 的監測數據
  - Node Exporter 與 kube metrics exporter
  - 輸出 kafka 的監測數據
  - 自幹 exporter

由於我比較熟悉 GCP / GKE 的服務，這篇的操作過程都會以 GCP 平台作為範例，不過操作過程大體上是跨平台通用的。

寫文章真的是體力活，覺得我的文章還有參考價值，請左邊幫我點讚按個喜歡，右上角幫我按個追縱，底下歡迎留言討論。給我一點繼續走下去的動力。

對我的文章有興趣，歡迎到我的網站上 [https://chechia.net](https://chechia.net) 閱讀其他技術文章，有任何謬誤也請各方大德直接聯繫我，感激不盡。

![Exausted Cat Face](https://d32l83enj9u8rg.cloudfront.net/wp-content/uploads/iStock-966846550-cat-overheating-simonkr-1-940x470.jpg)

---

如果要透過 prometheus 來監控集群的運行狀況，有兩個 exporter 是必裝的，一個是把 node 狀態 export 出來的 node exporter，一個是把 kubernetes 集群狀態 export 出來的 kube state metrics exporter。

* Node Exporter 簡介
* kube metrics exporter 安裝與設定

# Node Exporter

[Node Exporter](https://github.com/prometheus/node_exporter) 是 prometheus 官方維護的一個子項目，主要在把類 unix 硬體 kernel 的 metrics 送出來。官方也支援 windows node 與 nvidia gpu metrics，可以說是功能強大。

為了能夠監測 kubernetes node 的基礎設施狀態，通常都會使用 node exporter。

node exporter 安裝，我們在安裝 prometheus helm chart 時就一並安裝了。這邊看一下設定與運行。

# Collectors

Node exporter 把不同位置收集到的不同類型的 metrics ，做成各自獨立的 colletor，使用者可以根據求需求來啟用或是不啟用 collector，[完整的 collector 目錄](https://github.com/prometheus/node_exporter#enabled-by-default) 在這邊。

如果有看我們第一部份的 ELK part，應該會覺得這裡的設定，跟 metricbeat 非常像，基本上這兩者做的事情是大同小異的，收集 metrics 來源都是同樣的類 unix 系統，只是往後送的目標不一樣 (雖然現在兩者都可以兼容混搭了)。如果有接觸過其他平台的 metrics collector，也會發現其實大家做的都差不多。

# Textfile Collector

Prometheus 除了有 scrape 機制，讓 prometheus 去 exporter 撈資料外，還有另外一個機制，叫做 [Pushgateway](https://github.com/prometheus/pushgateway)，這個我們在部屬 prometheus 時也部屬了一個。這邊簡單說明一下。

經常性執行的服務(redis, kafka,...)會一直運行，prometheus 透過這些服務的 metrics 取得 runtime metrics，作為監控資料。可是有一些 job 是暫時性的任務，例如果一個 batch job，這些服務不會有一直運行的 runtime metrics，也不會有 exporter。但這時又希望監控這些 job 的狀態，就可以使用 Pushgateway。

Pushgateway 的作用機制，就是指定收集的目標資料夾，需要監測的 batch job，只要把希望監測的資料，寫到該資料夾。Pushgateway 會依據寫入的資料，轉成 time series metrics，並且 export 出來。

這種去 tail 指定目錄檔案，然後把 metrics 後送的機制，是否跟 filebeat 有一點類似? 只是 filebeat 一般取得資料後，會主動推送到 ELK 上，prometheus pushgateway 會暴露出 metrics 後，讓 prometheus server 來 scrape。

Pushgateway 也會在收集資料時打上需要的 label，方面後段處理資料。

# Kubernetes State Metrics (Exporter)

Node Exporter 將 kubernetes 集群底下的 Node 的硬體狀態，例如 cpu, memory, storage,... expose 出來，然而我們在維運 kubernetes 還需要從 api server 獲得集群內部的資料，例如說 pod state, container state, endpoints, service, ...等，這邊可以使用 kube-state-metrics 來處理。

[kube-state-metrics](https://github.com/kubernetes/kube-state-metrics) 是 kubernetes 官方維護的專案，做的事情就是向 api server 詢問 kubernetes 的 state，例如 pod state, deployment state，然後跟 prometheus exporter 一，開放一個 http endpoint，讓需要的服務來 scrape metrics。

工作雲裡也很單純，kubernetes api server 可以查詢 pod 當下的狀態，kube-state-metrics 則會把當下的狀態依照時間序，做成 time series 的 metrics，例如這個 pod 什麼時候是活著，什麼時候因為故障而 error。

kube-state-metrics 預設的輸出格式是 plaintext，直接符合 Prometheus client endpoint 的格式

# Deployment

如果依照第一篇安裝 prometheus helm 的步驟，現在應該已經安裝完 kube-state-metrics 了。如果沒有安裝，也可以依照官方說明的基本範例安裝。

```
git clone git@github.com:kubernetes/kube-state-metrics.git

cd kube-state-metrics

kubectl apply -f examples/standard/*.yaml
```

安裝完可以看到

```
$ kubectl get pods --selector 'app=prometheus,component=kube-state-metrics'

NAME                                             READY   STATUS    RESTARTS   AGE
prometheus-kube-state-metrics-85f6d75f8b-7vlkp   1/1     Running   0          201d

$ kubectl get svc --selector 'app=prometheus,component=kube-state-metrics'

NAME                            TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
prometheus-kube-state-metrics   ClusterIP   None         <none>        80/TCP    201d
```

我們可以透過 service 打到 pod 的 /metrics 來取得 metrics。

```
kubectl exec -it busybox sh

curl prometheus-kube-state-metrics:8080
<html>
    <head><title>Kube Metrics Server</title></head>
    <body>
    <h1>Kube Metrics</h1>
    <ul>
    	<li><a href='/metrics'>metrics</a></li>
    	<li><a href='/healthz'>healthz</a></li>
    </ul>
    </body>
</html>

curl prometheus-kube-state-metrics:8081

<html>
    <head><title>Kube-State-Metrics Metrics Server</title></head>
    <body>
    <h1>Kube-State-Metrics Metrics</h1>
    <ul>
    	<li>
			<a href='/metrics'>metrics</a>
		</li>
    </ul>
    </body>
</html>
```

這邊有兩套 metrics，一個是 kube-state-metrics 自己自我監測的 metrics，在 8081，另外一個才是 kube metrics，在 8080，兩個都要收，記得不要收錯了。

```
$ curl prometheus-kube-state-metrics:8080/metrics

打下去就可以看到超多 metrics 。
```

[Metrics 的清單與說明文件](https://github.com/kubernetes/kube-state-metrics/tree/master/docs)，有用到的 metrics 使用前都可以來查一下定義解釋。

理論上不用每個 metrics 都 expose 出來，有需要可以把不會用到的 metrics 關一關，可以節省 kube-state-metrics 的 cpu 消耗。

# Resource Recommendation

kube-state-metrics 很貼心的還附上[建議的資源分配](https://github.com/kubernetes/kube-state-metrics#scaling-kube-state-metrics)

```
As a general rule, you should allocate

200MiB memory
0.1 cores
For clusters of more than 100 nodes, allocate at least

2MiB memory per node
0.001 cores per node
```

# Scaling

kube-state-metrics 還有提供 horizontal scaling 的解決方案，如果你的集群很大，node 數量已經讓 kube-state-metrics 無法負荷，也可以使用 sharding 的機制，把 metrics 的工作散布到多個 kube-state-metrics，再讓 prometheus 去收集統整。這部分我覺得很有趣，但還沒實作過，我把[文件](https://github.com/kubernetes/kube-state-metrics#horizontal-scaling-sharding) 放在這邊，有緣大德有時做過請來討論分享。

# Dashboard

metrics 抓出來，當然要開一下 dashboard，這邊使用的是這個[kubernetes cluster](https://grafana.com/grafana/dashboards/7249)，支援

* node exporter
* kube state metrics
* nginx ingress controller

三個願望一次滿足~

# 小結

* 跑 kubernetes 務必使用這兩個 exporter
* kube-state-metrics 整理得很舒服，有時間可以多看看這個專案
