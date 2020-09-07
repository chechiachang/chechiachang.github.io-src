---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Logstash on GKE"
subtitle: ""
summary: ""
authors: []
tags: ["elasticsearch", "devops", "logstash"]
categories: ["kubernetes", "elasticsearch"]
date: 2019-09-21T15:22:23+08:00
lastmod: 2019-09-21T15:22:23+08:00
featured: false
draft: false

menu:
  main:
    parent: "Ithelp 鐵人賽"
    weight: 1
---

[2020 It邦幫忙鐵人賽](https://ithelp.ithome.com.tw/2020ironman) 系列文章

- [Self-host ELK stack on GCP]({{< ref "/post/self-host-elk-stack-on-gcp" >}})
- [Secure ELK Stask]({{< ref "/post/secure-elk-stack" >}})
- [監測 Google Compute Engine 上服務的各項數據]({{< ref "/post/monitoring-gce-with-elk" >}})
- [監測 Google Kubernetes Engine 的各項數據]({{<ref "/post/monitoring-gke-with-elk" >}})
- [是否選擇 ELK 作為解決方案]({{< ref "/post/elastic-or-not-elastic" >}})
- [使用 logstash pipeline 做數據前處理]({{< ref "/post/logstash-on-gke" >}})
- Elasticsearch 日常維護：數據清理，效能調校，永久儲存
- Debug ELK stack on GCP

作為範例的 ELK 的版本是當前的 stable release 7.3.1。

由於我比較熟悉 GCP / GKE 的服務，這篇的操作過程都會以 GCP 平台作為範例，不過操作過程大體上是跨平台通用的。

---

# 摘要

* 簡介 logstash
* 將 logstash 部屬到 kubernetes 上
* 設定 logstash pipeline 處理 nginx access log

# 介紹 Logstash


Logstash 是開元的資料處理引擎，可以動態的將輸入的資料做大量的處裡。原先的目的是處理 log ，但目前以不限於處理 log ，各種 ELK beat 或是其他來源的不同監測數據，都能處理。

Logastash 內部的功能也大多模組化，因此可以組裝不同的 plugin，來快速處理不同來源資料。

基本上常見的資料來源，logstash 都能夠處理，並且有寫好的 plugin 可以直接使用，細節請見[logstash 官方文件](https://www.elastic.co/guide/en/logstash/current/introduction.html)

![官方架構圖](https://www.elastic.co/guide/en/logstash/current/static/images/logstash.png)

# 後送資料庫與最終儲存庫

在開始架設 logstash 要先考慮 pipeline 處理過後送的資料庫，[可使用的資料庫非常多](https://www.elastic.co/guide/en/logstash/current/introduction.html#_choose_your_stash)，這邊會展示的有：

* ELK Stack 標準配備送到 Elasticsearch
  * 存放會時常查詢的熱資料，只存放一段時間前的資料
  * 太舊的資料自動 Rollout
* 最終 archieving 的資料庫，這邊使用 GCP 的 Big Query
  * 存放查找次數少，但非常大量的歷史紀錄。

Elasticsearch 在前幾篇已經架設好，[GCP Big Query](https://cloud.google.com/bigquery/docs/?hl=zh-tw) 的設定也事先開好。

# 部屬 Logstash

kubernetes resource 的 yaml 請參考 [我的 github elk-kubernetes](https://github.com/chechiachang/elk-kubernetes/tree/master/logstash)

```
kubectl apply -f config-configmap.yaml
kubectl apply -f pipelines-configmap.yam

kubectl apply -f deployment.yaml

kubectl apply -f service.yaml
```

放上去的 resource

* config-configmap:
  * Logstash 服務本身啟動的設定參數
* pipelines-configmap:
  * Logstash 的 pipelines 設定檔案
* Lostagh Deployment
  * Logastash 的服務 instance
  * 可以動態 scaling，也就是會有複數 Logstash instance 做負載均衡
* Logstash service
  * 可透過 kubernetes 內部的 kube-dns 服務
  * 集群內的 filebeat 可以直接透過 logstash.default.svc.chechiachang-cluster.local 的 dns 連線 logstash
  * 集群內的網路，直接使用 http（當然使用 https 也是可以，相關步驟請見前幾篇文章）

簡單講一下 kubernetes service 的負載均衡，關於 [kubernetes service 細節這篇附上文件](https://kubernetes.io/docs/concepts/services-networking/service/)

```
$ kubectl get services

NAME              TYPE           CLUSTER-IP      EXTERNAL-IP     PORT(S)    AGE
logstash          ClusterIP      10.15.254.47    <none>          5044/TCP   182d

$ kubectl get endpoints

NAME              ENDPOINTS                                                          AGE
logstash          10.12.0.132:5044,10.12.10.162:5044,10.12.9.167:5044 + 12 more...   182d
```

* 在 Kubernetes 內部每個 Pod 都能看到 logstash, logstash.default.svc.chechiachang-cluster.local 這兩個 dns
* DNS 直接指向複數的 logstash endpoints， 每一個 ip 都是 kubernetes 內部配置的一個 Pod 的 IP，開啟 5044 的 logstash port
* Service 的 load balance 機制視 service 設定，細節可以看[這邊](https://kubernetes.io/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies)

講到最白，就是 filebeat LOGSTASH URL 設定為 http://logstash 就會打到其中一台 logstash

更改 filebeat configmap

```
$ kubectl edit configmap filebeat-configmap

# Disable output to elasticsearch
output.elasticsearch:
  enabled: false

# Output to logstash
output.logstash:
  hosts: ["logstash:5044"]
  protocol: "http"
  username: "elastic"
  password: 

```

# 設定 logstash

這邊要先說，logstash 也支援 [centralized configuration](https://www.elastic.co/guide/en/logstash/7.3/configuring-centralized-pipelines.html)，如果你的 logstash 不是跑在 Kubernetes 上，沒辦法配置一套 configmap 就應用到全部的 instance，記的一定要使用。

Logastash 的運行設定 logstash.yml，這邊我們沒有做設定，都是預設值，有需求可以自行更改

當然之後要調整 batch size 或是 queue, cache 等等效能調校，也是來這邊改，改完 configmap ，rolling update logstash 就可以。

這邊主要是來講 pipeline 設定。

```
$ kubectl describe configmap pipelines-configmap

apiVersion: v1
kind: ConfigMap
metadata:
  name: logstash-pipelines
  namespace: elk
  labels:
    k8s-app: logstash
data:
  # Nginx Template
  # https://www.elastic.co/guide/en/logstash/7.3/logstash-config-for-filebeat-modules.html#parsing-nginx
  nginx.conf: |
  ...
```

Configmap 裡面只有一個 pipeline，就是 `nginx.conf`，我們這邊就只有一條，這邊一段一段看

### Input

```
input {
  beats {
    # The lisening port of logstash
    port => 5044
    host => "0.0.0.0"
  }
}
```

設定 Input 來源，是 beat 從 5044 進來

### Filter

接下來一大段是 filter，每個 filter 中間的 block 都是一個 plugin，logstash 支援非常多有趣的 plugin ，處理不同來源的工作，[細節請看這篇](https://www.elastic.co/guide/en/logstash/7.3/filter-plugins.html)

``` 
filter {

  # Ignore data from other source in case filebeat input is incorrectly configured.
  if [kubernetes][container][name] == "nginx-ingress-controller" {

    # Parse message with grok
    # Use grok debugger in kibana -> dev_tools -> grok_debugger
    grok {
      match => { "message" => "%{IPORHOST:[nginx][access][remote_ip]} - \[%{IPORHOST:[nginx][access][remote_ip_list]}\] - %{DATA:[nginx][access][user_name]} \[%{HTTPDATE:[nginx][access][time]}\] \"%{WORD:[nginx][access][method]} %{DATA:[nginx][access][request_url]} HTTP/%{NUMBER:[nginx][access][http_version]}\" %{NUMBER:[nginx][access][response_code]} %{NUMBER:[nginx][access][body_sent][bytes]} \"%{DATA:[nginx][access][referrer]}\" \"%{DATA:[nginx][access][agent]}\" %{NUMBER:[nginx][access][request_length]} %{NUMBER:[nginx][access][request_time]} \[%{DATA:[nginx][access][proxy_upstream_name]}\] %{DATA:[nginx][access][upstream_addr]} %{NUMBER:[nginx][access][upstream_response_length]} %{NUMBER:[nginx][access][upstream_response_time]} %{NUMBER:[nginx][access][upstream_status]} %{DATA:[nginx][access][req_id]}" }
    }

    # Match url parameters if has params
    grok {
      match => { "[nginx][access][request_url]" => "%{DATA:[nginx][access][url]}\?%{DATA:[nginx][access][url_params]}" }
    }

    # Remove and add fields
    mutate {
      remove_field => "[nginx][access][request_url]"
      add_field => { "read_timestamp" => "%{@timestamp}" }
      # Add fileset.module:nginx to fit nginx dashboard
      add_field => { "[fileset][module]" => "nginx"}
      add_field => { "[fileset][name]" => "access"}
    }

    # Parse date string into timestamp
    date {
      match => [ "[nginx][access][time]", "dd/MMM/YYYY:H:m:s Z" ]
      remove_field => "[nginx][access][time]"
    }

    # Split url_parameters with &
    # /api?uuid=123&query=456 
    # become 
    # nginx.access.url_params.uuid=123 nginx.access.url_params.query=456
    kv {
      source => "[nginx][access][url_params]"
      field_split => "&"
    }

    # Parse useragent
    useragent {
      source => "[nginx][access][agent]"
      target => "[nginx][access][user_agent]"
      remove_field => "[nginx][access][agent]"
    }

    # Search remote_ip with GeoIP database, output geoip information for map drawing
    geoip {
      source => "[nginx][access][remote_ip]"
      target => "[nginx][access][geoip]"
      #fields => ["country_name","city_name","real_region_name","latitude","longitude","ip","location"]
    }

    # ==============
    # Remove message to reduce data
    # ==============
    if [nginx][access][url] {
      mutate {
        # source:/var/lib/docker/containers/6e608bfc0a437c038a1dbdf2e3d28619648b58a1d1ac58635f8178fc5f871109/6e608bfc0a437c038a1dbdf2e3d28619648b58a1d1ac58635f8178fc5f871109-json.log
        remove_field => "[source]"
        # Origin message
        remove_field => "[message]"
        #add_field => { "[nginx][access][message]" => "[message]"}
        remove_field => "[nginx][access][message]"
        # url_params:client_id=1d5ffd378296c154d3e32e5890d6f4eb&timestamp=1546849955&nonce=9a52e3e6283f2a9263e5301b6724e2c0d723def860c4724c9121470152a42318
        remove_field => "[nginx][access][url_params]"
      }
    }

  } # nginx-ingress-controller

} # filter
```

### Grok

[Grok 本身的文件](https://www.elastic.co/guide/en/logstash/7.3/plugins-filters-grok.html)又是一大段，個人建議各路大德，如果要使用，請直接搜尋人家配置好的設定，不要自己寫

真的要寫的話要善用工具

* Kibana Grok Debugger `YOUR_KIBANA_HOST/app/kibana#/dev_tools/grokdebugger`
* 或是不知名大德貢獻[線上 Debugger](https://grokdebug.herokuapp.com/)

```
grok {
  match => { "message" => "%{IPORHOST:[nginx][access][remote_ip]} - \[%{IPORHOST:[nginx][access][remote_ip_list]}\] - %{DATA:[nginx][access][user_name]} \[%{HTTPDATE:[nginx][access][time]}\] \"%{WORD:[nginx][access][method]} %{DATA:[nginx][access][request_url]} HTTP/%{NUMBER:[nginx][access][http_version]}\" %{NUMBER:[nginx][access][response_code]} %{NUMBER:[nginx][access][body_sent][bytes]} \"%{DATA:[nginx][access][referrer]}\" \"%{DATA:[nginx][access][agent]}\" %{NUMBER:[nginx][access][request_length]} %{NUMBER:[nginx][access][request_time]} \[%{DATA:[nginx][access][proxy_upstream_name]}\] %{DATA:[nginx][access][upstream_addr]} %{NUMBER:[nginx][access][upstream_response_length]} %{NUMBER:[nginx][access][upstream_response_time]} %{NUMBER:[nginx][access][upstream_status]} %{DATA:[nginx][access][req_id]}" }
}
```

其實就是 nginx 的 access log
```
1.2.3.4 - [1.2.3.4] - - [21/Sep/2019:07:21:21 +0000] "GET /v1/core/api/list?type=queued&timestamp=1569050481&nonce=d1e80e00381e0ba6e42d4601912befcf03fbf291748e77b178230c19cd1fdbe2 HTTP/1.1" 200 3 "-" "python-requests/2.18.4" 425 0.031 [default-chechiachang-server-80] 10.12.10.124:8003 3 0.031 200 f43db228afe66da67b2c7417d0ad2c04
```

預設的 log 送件來，格式是 text，經過 pattern matching 後變成 json-like format，也就是可以從資料結構取得 `.nginx.access.remote_ip` 這樣的欄位，讓原本的 access log 從 text 變成可以查找的內容。

原本的 text 送進 elasticsearch 當然也可以查找，但就會在 text 裡面做全文檢索，功能很侷限，效率很差。

### Output

logstash 支援的 output 以及設定[在這邊](https://www.elastic.co/guide/en/logstash/7.3/output-plugins.html)

```
output {
  elasticsearch {
    hosts => ["https://${ELASTICSEARCH_HOST}:${ELASTICSEARCH_PORT}"]
    user => "${ELASTICSEARCH_USERNAME}"
    password => "${ELASTICSEARCH_PASSWORD}"
    index => "%{[@metadata][beat]}-%{[@metadata][version]}-%{+YYYY.MM.dd}"
    manage_template => false
  }
}
```

Elasticsearch 的配置很單純

```
output {
  google_bigquery {
    project_id => ${GCP_PROJECT_ID}
    dataset => ${GCP_BIG_QUERY_DATASET_NAME}
    csv_schema => "path:STRING,status:INTEGER,score:FLOAT"
    json_key_file => ${GCP_JSON_KEY_FILE_PATH}
    error_directory => "/tmp/bigquery-errors"
    date_pattern => "%Y-%m-%dT%H:00"
    flush_interval_secs => 30
  }
}
```

其中的變數，我們全都用環境變數，在 deployment.yaml 配置，啟動 logstash pods 時代入

`GCP_JSON_KEY_FILE_PATH` 這邊要配置一隻 GCP 的服務帳號金鑰，一個有 Big Query 寫入權限的 service account，把 json 使用 kubernetes secret 放到集群上，然後在 pod 上使用 volume from secret 掛載進來。
`csv_schema => "path:STRING,status:INTEGER,score:FLOAT"` 這邊要配置之後會存入 Big Query 的 csv 結構

# 小結

* 部屬 Logstash deployment 到 kubernetes 上
* 設定 pipeline，超多 plugin，族繁不及備載
* Grok 配置
* Big Query output 配置
