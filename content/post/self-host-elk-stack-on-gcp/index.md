---
title: "Self-host ELK stack - Installation"
subtitle: "Self-host ELK stack - Installation"

# Add a summary to display on homepage (optional).
summary: "Self-host ELK stack on GCP - Installation"

date: 2019-09-15T11:43:03+08:00
draft: false

# Authors. Comma separated list, e.g. `["Bob Smith", "David Jones"]`.
authors: []

# Is this a featured post? (true/false)
featured: true

# Tags and categories
# For example, use `tags = []` for no tags, or the form `tags = ["A Tag", "Another Tag"]` for one or more tags.
tags: ["gcp", "elk", "kubernetes", "elasticsearch"]
categories: []

# Projects (optional).
#   Associate this post with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects = ["deep-learning"]` references 
#   `content/project/deep-learning/index.md`.
#   Otherwise, set `projects = []`.
# projects = ["internal-project"]

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder. 
image:
  # Caption (optional)
  caption: ""

  # Focal point (optional)
  # Options: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight
  focal_point: ""
---

[2020 It邦幫忙鐵人賽](https://ithelp.ithome.com.tw/2020ironman) 系列文章

- [Self-host ELK stack on GCP]({{< ref "/post/self-host-elk-stack-on-gcp" >}})
- [Secure ELK Stask]({{< ref "/post/secure-elk-stack" >}})
- [監測 Google Compute Engine 上服務的各項數據]({{< ref "/post/monitoring-gce-with-elk" >}})
- [監測 Google Kubernetes Engine 的各項數據]({{<ref "/post/monitoring-gke-with-elk" >}})
- 使用 logstash pipeline 做數據前處理
- Elasticsearch 日常維護：數據清理，效能調校，永久儲存
- Debug ELK stack on GCP

作為範例的 ELK 的版本是當前的 stable release 7.3.1。

由於我比較熟悉 GCP / GKE 的服務，這篇的操作過程都會以 GCP 平台作為範例，不過操作過程大體上是跨平台通用的。

對我的文章有興趣，歡迎到我的網站上 [https://chechiachang.github.io](https://chechiachang.github.io) 閱讀其他技術文章，有任何謬誤也請各方大德直接聯繫我，感激不盡。

--

# 簡介 ELK stack

[官方說明文件](https://www.elastic.co/guide/index.html)

### ELK 的元件

- Elasticsearch: 基於 Lucene 的分散式全文搜索引擎
- Logstash: 數據處理 pipeline
- Kibana: ELK stack 的管理後台與數據視覺化工具
- Beats: 輕量級的應用端數據收集器，會從被監控端收集 log 與監控數據(metrics)

### ELK 的工作流程

beats -> (logstash) -> elasticsearch -> kibana

1. 將 beats 放在應用端的主機上，或是在容器化環境種作為 sidecar，跟應用放在一起
2. 設定 beats 從指定的路徑收集 log 與 metrics
3. 設定 beats 向後輸出的遠端目標
4. (Optional) beats 輸出到 logstash ，先進行數據的變更、格式整理，在後送到 elasticsearch
5. beats 向後輸出到 elasticsearch，儲存數據文件(document)，並依照樣式(template)與索引(index)儲存，便可在 elasticsearch 上全文搜索數據
7. 透過 Kibana，將 elasticsearch 上的 log 顯示


# 官方不是有出文件嗎

Elastic 官方準備了大量的文件，理論上要跟著文件一步一步架設這整套工具應該是十分容易。然而實際照著做卻遇上很多困難。由於缺乏 get-started 的範例文件，不熟悉 ELK 設定的使用者，常常需要停下來除錯，甚至因為漏掉某個步驟，而需要回頭重做一遍。

說穿了本篇的技術含量不高，就只是一個踩雷過程。

Lets get our hands dirty.

# WARNING

這篇安裝過程沒有做安全性設定，由於 ELK stack 的安全性功能模組，在[v6.3.0 以前的版本是不包含安全性模組的](https://www.elastic.co/what-is/open-x-pack)，官方的安裝說明文件將安全性設定另成一篇。我第一次安裝，全部安裝完後，才發現裏頭沒有任何安全性設定，包含帳號密碼登入、api secret token、https/tls 通通沒有，整組 elk 裸奔。

我這邊分開的目的，不是讓大家都跟我一樣被雷(XD)，而是因為
- 另起一篇對安全性設定多加說明
- 在安全的內網中，沒有安全性設定，可以大幅加速開發與除錯

雖然沒有安全性設定，但仍然有完整的功能，如果只是在測試環境，或是想要評估試用 self-hosted ELK，這篇的說明已足夠。但千萬不要用這篇上 public network 或是用在 production 環境喔。

如果希望第一次安裝就有完整的 security 設定，請等待下篇 [Secure ELK Stask](#secure-elk-stack)

# 討論需求與規格

這邊只是帶大家過一下基礎安裝流程，我們在私有網路中搭建一台 standalone 的 ELK stack，通通放在一台節點(node)上。

```
elk-node-standalone 10.140.0.10
app-node-1          10.140.0.11
...                 ...
```

本機的 ELK stack 元件，彼此透過 localhost 連線

- Elasticsearch:  localhost:9200
- Kibana:         localhost:5601
- Apm-server:     localhost:8200
- Self Monitoring Services

私有網路中的外部服務透過 10.140.0.10

- beats 從其他 node 輸出到 Elasticsearch: 10.140.0.10:9200
- beats 從其他 node 輸出到 Apm-server:    10.140.0.10:8200
- 在內部網路中 透過 browser 存取 Kibana:  10.140.0.10:5601

standalone 的好處:

- 方便 (再次強調這篇只是示範，實務上不要貪一時方便，維運崩潰)
- 最簡化設定，ELK 有非常大量的設定可以調整，這篇簡化了大部分

Standalone可能造成的問題:

- No High Availablity: 沒有任何容錯備援可以 failover，這台掛就全掛
- 外部服務多的話，很容易就超過 node 上對於網路存取的限制，造成 tcp drop 或 delay。需要調整 ulimit 來增加網路，當然這在雲端上會給維運帶來更多麻煩，不是一個好解法。

如果要有 production ready 的 ELK

- HA 開起來
- 把服務分散到不同 node 上, 方便之後 scale out 多開幾台
  - elasticsearch-1, elasticsearch-2, elasticsearch-3...
  - kibana-1
  - apm-server-1, apm-server-2, ...
- 如果應用在已經容器化, 這些服務元件也可以上 Kubernetes 做容器自動化，這個部份蠻好玩，如果有時間我們來聊這篇

# 主機設定

Elasticsearch 儲存數據會佔用不少硬碟空間，我個人的習慣是只要有額外占用儲存空間，都要另外掛載硬碟，不要占用 root，所以這邊會需要另外掛載硬碟。

GCP 上使用 Google Compote Engine 的朋友，可以照 [Google 官方操作步驟操作](https://cloud.google.com/compute/docs/disks/add-persistent-disk?hl=zh-tw)

完成後接近這樣
```
$ df -h
$ df --human-readable

Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       9.6G  8.9G  682M  93% /
/dev/sdb        492G   63G  429G  13% /mnt/disks/elk

$ ls /mnt/disks/elk

/mnt/disks/elk/elasticsearch
/mnt/disks/elk/apm-server
/mnt/disks/elk/kibana
```

至於需要多少容量，取決收集數據的數量，落差非常大，可以先上個 100Gb ，試跑一段時間，再視情況 scale storage disk。


# 開防火牆

需要開放 10.140.0.10 這台機器的幾個 port

- elasticsearch           :9200   來源只開放私有網路其他 ip 10.140.0.0/9
- apm-server              :8200   (同上)
- kibana                  :5601   (同上)，如果想從外部透過 browser開，需要 whitelist ip

GCP 上有 default 的防火牆允許規則，私有網路可以彼此連線
- default-allow-internal: :all    :10.140.0.0/9   tcp:0-65535

# Install Elasticsearch

[Install Elasticsearch 官方文件 7.3](https://www.elastic.co/guide/en/elasticsearch/reference/7.3/install-elasticsearch.html)

我們這邊直接在 ubuntu 18.04 上使用 apt 作為安裝

```
sudo apt-get install apt-transport-https
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
add-apt-repository "deb https://artifacts.elastic.co/packages/7.x/apt stable main"
sudo apt-get update
sudo apt-get install elasticsearch
```

安裝完後路徑長這樣

```
/etc/elasticsearch
/etc/elasticsearch/elasticsearch.yml
/etc/elasticsearch/jvm.options

# Utility
/usr/share/elasticsearch/bin/

# Log
/var/log/elasticsearch/elasticsearch.log
```

有需要也可以複寫設定檔，把 log 也移到 /mnt/disks/elk/elasticsearch/logs

### 服務控制

透過 systemd 管理，我們可以用 systemctl 控制，
用戶 elasticsearch:elasticsearch，操作時會需要 sudo 權限。

但在啟動前要先調整數據儲存路徑，並把權限移轉給使用者。
```
mkdir -p /mnt/disks/elk/elasticsearch
chown elasticsearch:elasticsearch /mnt/disks/elk/elasticsearch
```

### 設定檔案

ELK 提供了許多可設定調整的設定,但龐大的設定檔案也十分難上手。我們這邊先簡單更改以下設定檔案
```
sudo vim /etc/elasticsearch/elasticsearch.yml

# Change Network
network.host: 0.0.0.0
# Change data path
path.data: /mnt/disks/elk/elasticsearch

vim /etc/elasticsearch/jvm-options
# Adjust heap to 4G
-Xms4g
-Xmx4g

# Enable xpack.security
discovery.seed_hosts: ["10.140.0.10"]
discovery.type: "single-node"
xpack.security.enabled: true
xpack.security.transport.ssl.enabled: true
xpack.license.self_generated.type: basic
```

6.3.0 後的版本已經附上安全性模組 xpack，這邊順便開起來。關於 xpack 的安全性設定，這邊先略過不提。

有啟用 xpack ，可以讓我們透過 elasticsearch 附帶的工具，產生使用者與帳號密碼。
```
/usr/share/elasticsearch/bin/elasticsearch-setup-passwords auto

# Keep your passwords safe
```

然後把啟動 Elasticsearch
```
sudo systemctl enable elasticsearch.service
sudo systemctl start elasticsearch.service
sudo systemctl status elasticsearch.service
```

看一下 log，確定服務有在正常工作
```
tail -f /var/log/elasticsearch/elasticsearch.log
```

在 node 上試打 Elasticsearch API
```
$ curl localhost:9200

{
  "name" : "elk",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "uiMZe7VETo-H6JLFLF4SZg",
  "version" : {
    "number" : "7.3.1",
    "build_flavor" : "default",
    "build_type" : "deb",
    "build_hash" : "4749ba6",
    "build_date" : "2019-08-19T20:19:25.651794Z",
    "build_snapshot" : false,
    "lucene_version" : "8.1.0",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}
```

# Kibana

有了正常工作的 Elasticsearch，接下來要安裝 kibana，由於 apt repository 已經匯入，這邊直接

```
sudo apt-get update
sudo apt-get install kibana
```

一樣快速設定一下
```
$ vim /etc/kibana/kinana.yml

# change server.host from localhost to 0.0.0.0 to allow outside requests
server.host: "0.0.0.0"

# Add elasticsearch password
elasticsearch.username: "kibana"
elasticsearch.password:

sudo systemctl enable kibana.service
sudo systemctl start kibana.service
sudo systemctl status kibana.service
```

檢查 log 並試打一下
```
sudo systemctl status kibana

$ curl localhost:5601
```

透過內網 ip 也可以用 browser 存取
使用 elastic 這組帳號密碼登入，可以有管理員權限
可以檢視一下 kibana 的頁面，看一下是否系統功能都上常上線
http://10.140.0.10/app/monitoring#

# Filebeat

以上是 ELK 最基本架構: elasticsearch 引擎與前端視覺化管理工具 Kibana。當然現在進去 kibana 是沒有數據的，所以我們現在來安裝第一個 beat，收集第一筆數據。

你可能會覺得奇怪: 我現在沒有任何需要監控的應用，去哪收集數據?

ELK 提供的自我監測 (self-monitoring) 的功能，也就是在 node 上部屬 filebeat 並啟用 modules，便可以把這台 node 上的 elasticsearch 運行的狀況，包含cpu 狀況、記憶體用量、儲存空間用量、安全性告警、...都做為數據，傳到 elasticsearch 中，並在 Kibana monitoring 頁面製圖顯示。

這邊也剛好做為我們 ELK stack 的第一筆數據收集。

WARNING: 這邊一樣要提醒， production 環境多半會使用另外一組的 elasticsearch 來監控主要的這組 elastic stack，以維持 elk stack 的穩定性，才不會自己 monitoring 自己，結果 elastic 掛了，metrics 跟錯誤訊息都看不到。

[官方安裝文件](https://www.elastic.co/guide/en/beats/filebeat/7.3/filebeat-installation.html)
  

```
sudo apt-get update
sudo apt-get install filebeat
```

預設的 filebeat.yml 設定檔案不是完整的，請到官網下載完整版，但官網沒給檔案連結(慘)，只有網頁版 https://www.elastic.co/guide/en/beats/filebeat/7.3/filebeat-reference-yml.html

我們上 github 把她載下來
```
$ wget https://raw.githubusercontent.com/elastic/beats/v7.3.1/filebeat/filebeat.reference.yml
$ sudo mv filebeat-reference-y
$ sudo vim /etc/filebeat/filebeat.yml

# Enable elasticsearch module and kibana module to process metrics of localhost elasticsearch & kibana
filebeat.modules:
- module: elasticsearch
  # Server log
  server:
    enabled: true

- module: kibana
  # All logs
  log:
    enabled: true

# The name will be added to metadata
name: filebeat-elk
fields:
  env: elk

# Add additional cloud_metadata since we're on GCP
processors:
- add_cloud_metadata: ~

# Output to elasticsearch
output.elasticsearch:
  enabled: true
  hosts: ["localhost:9200"]
  protocol: "http"
  username: "elastic"
  password: 

# Configure kibana with filebeat: add template, dashboards, etc...
setup.kibana:
  host: "localhost:5601"
  protocol: "http"
  username: "elastic"
  password: 
```

啟動 filebeat
```
sudo systemctl start filebeat
```

看一下 log，filebeat 會開始收集 elasticsearch 的 log 與 metrics，可以在 log 上看到收集的狀況。
```
$ sudo journalctl -fu filebeat

Sep 15 06:28:50 elk filebeat[9143]: 2019-09-15T06:28:50.176Z        INFO        [monitoring]        log/log.go:145        Non-zero metrics in the last 30s        {"monitoring": {"metrics": {"beat":{"cpu":{"system":{"ticks":1670860,"time":{"ms":66}},"total":{"ticks":6964660,"time":{"ms":336},"value":6964660},"user":{"ticks":5293800,"time":{"ms":270}}},"handles":{"limit":{"hard":4096,"soft":1024},"open":11},"info":{"ephemeral_id":"62fd4bfa-1949-4356-9615-338ca6a95075","uptime":{"ms":786150373}},"memstats":{"gc_next":7681520,"memory_alloc":4672576,"memory_total":457564560376,"rss":-32768},"runtime":{"goroutines":98}},"filebeat":{"events":{"active":-29,"added":1026,"done":1055},"harvester":{"open_files":4,"running":4}},"libbeat":{"config":{"module":{"running":0}},"output":{"events":{"acked":1055,"active":-50,"batches":34,"total":1005},"read":{"bytes":248606},"write":{"bytes":945393}},"pipeline":{"clients":9,"events":{"active":32,"published":1026,"total":1026},"queue":{"acked":1055}}},"registrar":{"states":{"current":34,"update":1055},"writes":{"success":35,"total":35}},"system":{"load":{"1":1.49,"15":0.94,"5":1.15,"norm":{"1":0.745,"15":0.47,"5":0.575}}}}}}
```

如果數據都有送出，就可以回到 kibana 的頁面，看一下目前這個 elasticsearch 集群，有開啟 monitoring 功能的元件們，是否都有正常工作。

http://10.140.0.10/app/monitoring#

頁面長得像這樣

{{< figure library="1" src="elk/kibana-monitoring.png" title="" width="100%" height="100%">}}

Standalone cluster 中的 filebeat，是還未跟 elasticsearch 配對完成的數據，會顯示在另外一個集群中，配對完後會歸到 elk cluster 中，就是我們的主要 cluster。

點進去可以看各個元件的服務情形。


# 小結

- 簡單思考 self-host ELK stack 搭建的架構
- 在單一 node 上安裝最簡易的 elastic stack
- 設定元件的 output 位置
- 設定 self-monitoring

恭喜各位獲得一個裸奔但是功能完整的 ELK, 我們下篇再向安全性邁進。
