---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Monitoring GCE With ELK"
subtitle: ""
summary: ""
authors: []
tags: []
categories: []
date: 2019-09-18T19:10:50+08:00
lastmod: 2019-09-18T19:10:50+08:00
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

- [Self-host ELK stack on GCP]({{< ref "/post/self-host-elk-stack-on-gcp" >}})
- [Secure ELK Stask]({{< ref "/post/secure-elk-stack" >}})
- [監測 Google Compute Engine 上服務的各項數據]({{< ref "/post/monitoring-gce-with-elk" >}})
- [監測 Google Kubernetes Engine 的各項數據]({{<ref "/post/monitoring-gke-with-elk" >}})
- 使用 logstash pipeline 做數據前處理
- Elasticsearch 日常維護：數據清理，效能調校，永久儲存
- Debug ELK stack on GCP

作為範例的 ELK 的版本是當前的 stable release 7.3.1。

由於我比較熟悉 GCP / GKE 的服務，這篇的操作過程都會以 GCP 平台作為範例，不過操作過程大體上是跨平台通用的。

---

ELK 的 beats 是輕量級的系統監測收集器，beats 收集到的 data 經過 mapping 可以送到 Elasticsearch 後，進行彈性的搜尋比對。

beat 有許多種類，依據收集的 data 區別：

* Auditbeat: Audit data
* Filebeat: Log files
* Functionbeat: Cloud data
* Heartbeat: Availability
* Journalbeat: Systemd journals
* Metricbeat: Metrics
* Packetbeat: Network traffic
* Winlogbeat: Windows event logs

這邊先以 filebeat 為例，在 GCE 上收集圓端服務節點上的服務日誌與系統日誌，並在 ELK 中呈現。

# Installation

安裝及 filebeat 安全性設定的步驟，在這篇[Secure ELK Stack]() 中已經說明。這邊指附上連結，以及[官方文件](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-getting-started.html) 提供參考。

# Configuration

這邊談幾個使用方面的設定。


首先，apt 安裝的 filebeat 預設的 /etc/filebeat/filebeat.yml 不夠完整，我們先到 github 把對應版本的完整載下來。
```
wget https://raw.githubusercontent.com/elastic/beats/master/filebeat/filebeat.reference.yml
sudo mv filebeat.reference.yml /etc/filebeat/filebeat.yml
```

# Beats central management

beats 透過手動更改 config 都可以直接設定，但這邊不推薦在此設定，理由是

* 系統中通常會有大量的 filebeat，每個都要設定，數量多時根本不可能
* 更改設定時，如果不一起更改，會造成資料格式不統一，之後清理也很麻煩

推薦的方式是透過 Kibana 對所有 filebeat 做集中式的的管理配置，只要初始設定連上 kibana，剩下的都透過 kibana 設定。[文件在此](https://www.elastic.co/guide/en/beats/filebeat/current/configuration-central-management.html)，我們有空有可以分篇談這個主題。

不過這邊還是待大家過一下幾個重要的設定。畢竟要在 kibana 上配置，filebeat 的設定概念還是要有。

### modules

filebeat 有許多[模組](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-modules.html)，裡面已經包含許多預設的 template ，可以直接使用 default 的設定去系統預設的路徑抓取檔案，並且先進一步處理，減少我們輸出到 logstash 還要再做 pipeline 預處理，非常方便。

例如這個 system module 會處理系統預設的 log 路徑，只要開啟 module ，就會自動處理對應的 input。
```
- module: system
  syslog:
    enabled: true
```

剩下的就是照需求啟用 module ，並且給予對應的 input。

ELK 為自己的服務設定了不少 module ，直接啟用就可以獲取這協服務元件運行的 log 與監測數值。這也是 self-monitoring 監測數據的主要來源。
```
- module: kibana
- module: elasticsearch
- module: logstash
...
```

### input

filebeat 支援複數 inputs，每個 input 會啟動一個收集器，而 filebeat 收集目標是 log 檔案。基本上可以簡單理解為 filebeat 去讀取這些 log 檔案，並且在系統上紀錄讀取的進度，偵測到 log 有增加，變繼續讀取新的 log。

filebeat 具體的工作機制，可以看這篇[How Filebeat works?](https://www.elastic.co/guide/en/beats/filebeat/current/how-filebeat-works.html)

這篇文件也提到 filebeat 是確保至少一次(at-least-once delivery)的數據讀取，使用時要特別注意重複獲取的可能。

首先把 input 加上 ubuntu 預設的 log 路徑

```
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /var/log/*.log
```

這邊注意 input 支援多種 type，參照完整設定檔案的說明配合自己的需求使用。

### Processor

在 filebeat 端先進行資料的第一層處理，可以大幅講少不必要的資料，降低檔案傳輸，以及對 elasticsearch server 的負擔。

### output 

output 也是 filebeat 十分重要的一環，好的 filebeat output 設定，可以大幅降低整體 ELK stack 的負擔。壞的設定也會直接塞爆 ELK stask。

output.elasticsearch: 直接向後送進 elasticsearch
output.logstash: 先向後送到 logstash

這邊非常推薦大家，所有的 beat 往後送進 elasticsearch 之前都先過一層 logstash，就算你的 logstash 內部完全不更改 data，沒有 pipeline mutation，還是不要省這一層。

* beat 的數量會隨應用愈來越多而線性增加，elasticsearch 很難線性 scale，或是 scale 成本很大
* filebeat 沒有好好調校的話，對於輸出端的網路負擔很大，不僅佔用大量連線，傳輸檔案的大小也很大。
* logstash 的 queue 與後送的 batch 機制比 filebeat 好使用
* filebeat 是收 log 的，通常 log 爆炸的時候，是應用出問題的時候，這時候需要 log 交叉比對，發現 elasticsearch 流量也爆衝，反應很應用
* logstash 透過一些方法，可以很輕易的 scale，由於 pipeline 本身可以分散是平行處理，scale logstash 並不會影響資料最終狀態。


### load balance

有網友留言詢問 logstash 前面的 load balance 如何處理比較好，我這邊也順便附上。不只是 logstash ，所有自身無狀態(stateless) 的服務都可以照這樣去 scale。

在 kubernetes 上很好處理，使用 k8s 預設的 service 就輕易作到簡易的 load balance
* 設置複數 logstash instances
* 使用 kubernetes 內部網路 service 實現 load balancing。

在 GCE 上實現的話，我說實話沒實作過，所以以下是鍵盤實現XD。

[官方文件](https://www.elastic.co/guide/en/beats/filebeat/7.3/load-balancing.html) 建議使用 beats 端設定多個 logstash url 來做 load balancing。

但我不是很喜歡 beat 去配置多個 logstash url 的作法：beat 要感知 logstash 數量跟 url ，增加減少 logstash instance 還要更改 beats 配置，產生配置的依賴跟耦合。

最好是在 logstash 前過一層 HAproxy 或是雲端服務的 Load balancer（ex. GCP https/tcp load balancer），beat 直接送進 load balance 的端點。

# autodiscover

如果有使用 container ，例如 docker 或 kubernetes，由於 container 內的 log 在主機上的位置是動態路徑，這邊可以使用 autodiscover 去尋找。

在 kubernetes 上面的設定，之後會另開一天討論。

# dashboard

kibana 預設是空的，沒有預先載入 dashboard，但我們會希望資料送進去，就有設定好的 dashboard ，圖像化把資料呈現出來。這部份需要從 beat 這邊向 kibana 寫入。

在上面的部份設定好 kibana 的連線資料，沒有設定的話 beat 啟動會警告。

```
setup.dashboards.enabled: true
```

一起中就會檢查 kibana 是否有匯入 dashboard，沒有的話就匯入。

也會一併匯入 modules 的 dashboard，例如如果有啟用 nginx module 處理 nginx 的 access log，nginx module 會處理 request source ip ，並透過 geoip database, 將 ip 轉會成經緯度座標。這時如果在 kibana 上有匯入 nginx dashboard，就可以看到圖像化的全球 request 分佈圖。

# 小結

* 取得完整 filebeat 設定檔案並設定 filebeat
* 盡量透過 beat central management 來管理 beat 的設定檔
* 啟用對應 module 來更優雅的處理 log
* 後送到 elasticsearch 前的資料都必須經過精細的處理，送進去後就不好刪改了
