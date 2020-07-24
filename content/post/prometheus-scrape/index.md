---
title: "Prometheus Deploy Grafana"
subtitle: ""

# Add a summary to display on homepage (optional).
summary: ""

date: 2019-10-04T8:12:10+08:00
draft: false

# Authors. Comma separated list, e.g. `["Bob Smith", "David Jones"]`.
authors: []

# Is this a featured post? (true/false)
featured: false

# Tags and categories
# For example, use `tags: []` for no tags, or the form `tags: ["A Tag", "Another Tag"]` for one or more tags.
tags: ["kubernetes", "redis", "ci", "cd"]
categories: []

# Projects (optional).
#   Associate this post with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects: ["deep-learning"]` references 
#   `content/project/deep-learning/index.md`.
#   Otherwise, set `projects: []`.
# projects: ["internal-project"]

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder. 
image:
  # Caption (optional)
  caption: ""

  # Focal point (optional)
  # Options: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight
  focal_point: ""

menu:
  main:
    parent: "Ithelp 鐵人賽"
    weight: 1
---

[2020 It邦幫忙鐵人賽](https://ithelp.ithome.com.tw/2020ironman) 系列文章

- Prometheus / Grafana (5)
  - [GKE 上自架 Prometheus / Grafana]({{< ref "/post/prometheus-deployment-on-kubernetes" >}})
  - GKE 上自架 Grafana 與設定
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

* Prometheus scrape
* scrape_configs
* Node exporter

# Scrape

Prometheus 收集 metrics 的方式，是從被監測的目標的 http endpoints 收集 (scrape) metrics，目標服務有提供 export metrics 的 endpoint 的話，稱作 exporter。例如 kafka-exporter 就會收集 kafka 運行的 metrics，變成 http endpoint instance，prometheus 從 instance 上面收集資料。

Promethesu 自己也是也提供 metrics endpoint，並且自己透過 scrape 自己的 metrics endpoint 來取得 self-monitoring 的 metrics。把自己當作外部服務監測。下面的設定就是直接透過 http://localhost:9090/metrics 取得。

```
global:
  scrape_interval:     15s # By default, scrape targets every 15 seconds.

  # Attach these labels to any time series or alerts when communicating with
  # external systems (federation, remote storage, Alertmanager).
  external_labels:
    monitor: 'codelab-monitor'

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: 'prometheus'

    # Override the global default and scrape targets from this job every 5 seconds.
    scrape_interval: 5s

    static_configs:
      - targets: ['localhost:9090']
```

透過 Grafana -> explore 就可以看到 Prometheus 的 metrics

![Prometheus Self Metrics](static/img/prometheus-self-metrics.jpg)

而使用 metrics 時最好先查到說明文件，確定 metrics 的定義與計算方法，才可以有效的製圖。關於 [Prometheus Exporter 的 metrics 說明](https://wiki.lnd.bz/display/LFTC/Prometheus) 可以到這裡來找。

# Dashboard

收集到 metrics 之後就可以在 prometheus 中 query，但一般使用不會一直跑進來下 query，而是會直接搭配 dashboard 製圖呈現，讓資料一覽無遺。

例如 prometheus 自身的 metrics 也已經有搭配好的 [Prometheus overview dashboard](https://grafana.com/grafana/dashboards/3662) 可以使用。

使用方法非常簡單，直接透過 Grafana import dashboard，裡面就把重要的 prometheus metrics 都放在 dashboard 上了。不能更方便了。

# Exporters

Prometheus 支援超級多 exporter，包含 prometheus 自身直接維護的 exporter，還有非常多外部服務友也開源的 exporter 可以使用，[清單可以到這裡看](https://prometheus.io/docs/instrumenting/exporters/#exporters-and-integrations)

有希望自己公司的服務，也使用 prometheus

# Node Exporter

[prometheus/node_exporter](https://github.com/prometheus/node_exporter) 是 Prometheus 直接維護的 project，主要用途就是將 node / vm 的運行 metrics export 出來。有點類似 ELK 的 metricbeat。

我們這邊是在 kubernetes 上執行，所以直接做成 daemonsets 在 k8s 上跑，部屬方面在 deploy prometheus-server 的 helm chart 中，就已經附帶整合，部屬到每一台 node 上。

如果是在 kubernetes 外的環境，例如說 on premise server，或是 gcp instance，希望自己部屬 node exporter 的話，可以參考[這篇教學文章](https://prometheus.io/docs/guides/node-exporter/)。

我們這邊可以看一下 config，以及 job 定義。

```
vim values-staging.yaml

  # Enable nodeExporter
  nodeExporter:
    create: true

  prometheus.yml:
    rule_files:
      - /etc/config/rules
      - /etc/config/alerts

    scrape_configs:

    # Add kubernetes node job
    - job_name: 'kubernetes-nodes'

        # Default to scraping over https. If required, just disable this or change to
        # `http`.
        scheme: https

        # This TLS & bearer token file config is used to connect to the actual scrape
        # endpoints for cluster components. This is separate to discovery auth
        # configuration because discovery & scraping are two separate concerns in
        # Prometheus. The discovery auth config is automatic if Prometheus runs inside
        # the cluster. Otherwise, more config options have to be provided within the
        # <kubernetes_sd_config>.
        tls_config:
          ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
          # If your node certificates are self-signed or use a different CA to the
          # master CA, then disable certificate verification below. Note that
          # certificate verification is an integral part of a secure infrastructure
          # so this should only be disabled in a controlled environment. You can
          # disable certificate verification by uncommenting the line below.
          #
          insecure_skip_verify: true
        bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token

        kubernetes_sd_configs:
          - role: node

        relabel_configs:
          - action: labelmap
            regex: __meta_kubernetes_node_label_(.+)
          - target_label: __address__
            replacement: kubernetes.default.svc:443
          - source_labels: [__meta_kubernetes_node_name]
            regex: (.+)
            target_label: __metrics_path__
            replacement: /api/v1/nodes/$1/proxy/metrics
```

kubernetes_sd_config: 可以透過 kubernetes API 來取得 scrape target，以這邊的設定，是使用 node role 去集群取得 node，並且每一台 node 都當成一個 target，這樣就不用把所有 node 都手動加到 job 的 instance list 裡面。

從 node role 取得的 instance 會使用 ip 標註或是 hostname 標註。node role 有提供 node 範圍的 meta labels，例如 __meta_kubernetes_node_name, __meta_kubernetes_node_address_ 等等，方便查找整理資料。

relabel_configs: 針對資料做額外標記，方便之後在 grafana 上面依據需求 query。

