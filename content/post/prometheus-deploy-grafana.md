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

* Grafana Introduction
* Deploy Grafana

# Grafana Introduction

上偏我們簡單介紹了 Prometheus，prometheus 的 Web Portol 已經附上簡單的 Query 與 Graph 工具，但一般我們在使用時，還是會搭配 Grafana 來使用。

[Grafana 在官網上提到](https://grafana.com/grafana/) 是一個 Analytics system，可以協助了解運行資料，建立完整的 dashboard。

* 支援許多圖表，直線圖，長條圖，區域分析，基本上需要的都有
* 在圖表上定義 alter，並且主動告警，整合其他通訊軟體
* 對後端 data source 的整合，可以同時使用 ELK, prometheus, influxdb 等 30 多種的資料來源
* 有許多公開的 plugin 與 dashboard 可以匯入使用

總之功能強大，至於用起來的感覺，個人是非常推薦。如果有大得想要試玩看看，可以直接到 [Grafana Live Demo](https://play.grafana.org/d/000000029/prometheus-demo-dashboard?orgId=1&refresh=5m) 上面試玩

* 一般使用都會圍繞 dashboard 為核心，透過單一畫面，一覽目前使用者需要讀取的資料
* 左上角的下拉選單，可以選擇不同的 dashboards

# 與 Kibana 做比較

雖然大部分使用上，我們都會使用 ELK 一套，而 Prometheus + Grafana 另一套。但其實兩邊的 data source 都可以互接。例如 grafana 可以吃 elasticsearch 的 data source，而 kibana 有 prometheus module。

我們這邊基於兩款前端分析工具，稍微做個比較，底層的 data source 差異這邊先不提。

* 都是開源: 兩者的開源社群都非常強大
* 兩者內建的 dashboard 都非常完整，而且不斷推出新功能
* Log vs Metrics:
  * Kibana 的 metrics 也是像 log 一樣的 key value pairs，能夠 explore 未定義的 log
  * Grafana 的 UI 專注於呈現 time series 的 metrics，並沒有提供 data 的欄位搜尋，而是使用語法 Query 來取得數據
* Data source:
  * Grafana 可以收集各種不同的後端資料來源
  * ELK 主要核心還是 ELK stack，用其他 Module 輔助其他資料源

# Deploy Grafana

我把我的寶藏都放在這了[https://github.com/chechiachang/prometheus-kubernetes](https://github.com/chechiachang/prometheus-kubernetes)

下載下來的 .sh ，跑之前養成習慣貓一下
```
cd grafana

cat install.sh

#!/bin/bash
HELM_NAME=grafana-1

helm upgrade --install grafana stable/grafana \
  --namespace default \
  --values values-staging.yaml
```

### Helm

我們這邊用 helm 部屬，[Grafana Stable Chart](https://github.com/helm/charts/tree/master/stable/grafana)

### Configuration

簡單看一下設定檔

```
vim values-staging.yaml

replicas: 1

deploymentStrategy: RollingUpdate
```

Grafana 是支援 [Grafana HA](https://grafana.com/docs/tutorials/ha_setup/) ，其實也非常簡單，就是把 grafana 本身的 dashboard database 從每個 grafana 一台 SQLite，變成外部統一的 MySQL，統一讀取後端資料，前端就可水平擴展。

```
readinessProbe:
  httpGet:
    path: /api/health
    port: 3000

livenessProbe:
  httpGet:
    path: /api/health
    port: 3000
  initialDelaySeconds: 60
  timeoutSeconds: 30
  failureThreshold: 10

image:
  repository: grafana/grafana
  tag: 6.0.0
  pullPolicy: IfNotPresent

  ## Optionally specify an array of imagePullSecrets.
  ## Secrets must be manually created in the namespace.
  ## ref: https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/
  ##
  # pullSecrets:
  #   - myRegistrKeySecretName
```

一些 Pod 的基本配置， health check 使用內建的 api，有需要也可以直接打 api

```
securityContext:
  runAsUser: 472
  fsGroup: 472


extraConfigmapMounts: []
  # - name: certs-configmap
  #   mountPath: /etc/grafana/ssl/
  #   configMap: certs-configmap
  #   readOnly: true
```

有要開外部 ingress，需要 ssl 的話可以從這邊掛進去

```
## Expose the grafana service to be accessed from outside the cluster (LoadBalancer service).
## or access it from within the cluster (ClusterIP service). Set the service type and the port to serve it.
## ref: http://kubernetes.io/docs/user-guide/services/
##
service:
  type: LoadBalancer
  port: 80
  targetPort: 3000
    # targetPort: 4181 To be used with a proxy extraContainer
  annotations: {}
  labels: {}

ingress:
  enabled: false
  annotations: {}
    # kubernetes.io/ingress.class: nginx
    # kubernetes.io/tls-acme: "true"
  labels: {}
  path: /
  hosts:
    - chart-example.local
  tls: []
  #  - secretName: chart-example-tls
  #    hosts:
  #      - chart-example.local
```

這邊可以開 service load balancer, 以及 ingress，看實際使用的需求

```
persistence:
  enabled: true
  initChownData: true
  # storageClassName: default
  accessModes:
    - ReadWriteOnce
  size: 10Gi
  # annotations: {}
  # subPath: ""
  # existingClaim:
```

Persistent Volume 作為本地儲存建議都開起來，

```
# Administrator credentials when not using an existing secret (see below)
adminUser: admin
# adminPassword: strongpassword

# Use an existing secret for the admin user.
admin:
  existingSecret: ""
  userKey: admin-user
  passwordKey: admin-password
```

帳號密碼建議使用 secret 掛進去

```
datasources: {}
#  datasources.yaml:
#    apiVersion: 1
#    datasources:
#    - name: Prometheus
#      type: prometheus
#      url: http://prometheus-prometheus-server
#      access: proxy
#      isDefault: true

## Configure grafana dashboard providers
## ref: http://docs.grafana.org/administration/provisioning/#dashboards
##
## `path` must be /var/lib/grafana/dashboards/<provider_name>
##
dashboardProviders: {}
#  dashboardproviders.yaml:
#    apiVersion: 1
#    providers:
#    - name: 'default'
#      orgId: 1
#      folder: ''
#      type: file
#      disableDeletion: false
#      editable: true
#      options:
#        path: /var/lib/grafana/dashboards/default

## Configure grafana dashboard to import
## NOTE: To use dashboards you must also enable/configure dashboardProviders
## ref: https://grafana.com/dashboards
##
## dashboards per provider, use provider name as key.
##
dashboards: {}
  # default:
  #   some-dashboard:
  #     json: |
  #       $RAW_JSON
  #   custom-dashboard:
  #     file: dashboards/custom-dashboard.json
  #   prometheus-stats:
  #     gnetId: 2
  #     revision: 2
  #     datasource: Prometheus
  #   local-dashboard:
  #     url: https://example.com/repository/test.json
  #   local-dashboard-base64:
  #     url: https://example.com/repository/test-b64.json
  #     b64content: true
```

Data source, Dashboard 想要直接載入，可以在這邊設定，或是 grafana 起來後，透過 Web UI 進去新增也可以

```
## Grafana's primary configuration
## NOTE: values in map will be converted to ini format
## ref: http://docs.grafana.org/installation/configuration/
##
grafana.ini:
  paths:
    data: /var/lib/grafana/data
    logs: /var/log/grafana
    plugins: /var/lib/grafana/plugins
    provisioning: /etc/grafana/provisioning
  analytics:
    check_for_updates: true
  log:
    mode: console
  grafana_net:
    url: https://grafana.net
```

然後是 grafana.ini 核心 runtime 設定，更多設定可以參考[官方文件](http://docs.grafana.org/installation/configuration/)


# Deployment

部屬完看一下

```
kubectl get po --selector='app=grafana'


```

# Access

如果沒有透過 service load balancer 打出來，一樣可以使用 kubectl 做 port forwarding，權限就是 context 的權限，沒有 cluster context 的使用者就會進步來

```
GRAFANA_POD_NAME=$(kc get po -n default --selector='app=grafana' -o=jsonpath='{.items[0].metadata.name}')
kubectl --namespace default port-forward ${GRAFANA_POD_NAME} 3000

http://localhost:3000
```

由於我們透過 service load balancer，gcp 會在外部幫忙架一個 load balancer，
可以直接透過 load balancer ip 存取，如果想設定 dns，指向這個 ip 後記得去調整 grafana 的 server hostname。

使用 secret 的密碼登入，username: grafana，這個是系統管理員
```
kubectl get secret --namespace default grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```

# Configuration

近來畫面後先到左邊的[Configuration](https://play.grafana.org/plugins) 調整

* 產生新的 user org 與 user，把 admin 權限控制在需要的人手上
* 把 prometheus data source 加進來，就可以直接看到 prometheus 裡面的資料。
* 切換到非管理員的 user 繼續操作

### Import Dashboard

Grafana 網站上已經有[超多設置好的 Dashboard](https://grafana.com/grafana/dashboards) 可以直接 import，大部分的服務都已經有別人幫我們把視覺畫圖表拉好，使用社群主流的 exporter 的話，參數直接接好。我們匯入後再進行簡單的客製化調整即可。

我們鐵人賽有用到的服務，都已經有 dashboard

* kubernetes Cluster: 6417 
  * https://grafana.com/dashboards/6417
* Kafka Exporter Overview: 7589 
  * https://grafana.com/dashboards/7589
* Prometheus Redis: 763
  * https://grafana.com/dashboards/763
* Kubernetes Deployment Statefulset Daemonset metrics: 8588
  * https://grafana.com/dashboards/8588
* Haproxy Metrics Servers: 367
  * https://grafana.com/dashboards/367
* Go to grafana lab to find more dashboards

### Export Dashboard

dashboard 會依照登入使用者的需求做調整，每個腳色需要看到的圖表都不同，基本上讓各個腳色都能一眼看到所需的表格即可

自己的調整過的 dashboard 也可以匯出分享

# 小結

到這邊就可以正常使用 grafana了，資料來源的 exporter 我們會搭配前幾周分享過的服務，一起來講
