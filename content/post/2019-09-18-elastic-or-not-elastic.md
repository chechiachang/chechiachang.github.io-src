---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "ELK or Not ELK"
subtitle: ""
summary: ""
authors: []
tags: ["elasticsearch", "devops"]
categories: ["kubernetes", "elasticsearch"]
date: 2019-09-18T18:51:40+08:00
lastmod: 2019-09-18T18:51:40+08:00
featured: false
draft: false

menu:
  main:
    parent: "Ithelp 鐵人賽"
    weight: 1
---

[2020 It邦幫忙鐵人賽](https://ithelp.ithome.com.tw/2020ironman) 系列文章

- [Self-host ELK stack on GCP]({{< ref "/post/2019-09-15-self-host-elk-stack-on-gcp" >}})
- [Secure ELK Stask]({{< ref "/post/2019-09-15-secure-elk-stack" >}})
- [監測 Google Compute Engine 上服務的各項數據]({{< ref "/post/2019-09-18-monitoring-gce-with-elk" >}})
- [監測 Google Kubernetes Engine 的各項數據]({{<ref "/post/2019-09-19-monitoring-gke-with-elk" >}})
- [是否選擇 ELK 作為解決方案]({{< ref "/post/2019-09-18-elastic-or-not-elastic" >}})
- [使用 logstash pipeline 做數據前處理]({{< ref "/post/2019-09-21-logstash-on-gke" >}})
- Elasticsearch 日常維護：數據清理，效能調校，永久儲存
- Debug ELK stack on GCP

對我的文章有興趣，歡迎到我的網站上 [https://chechia.net](https://chechia.net) 閱讀其他技術文章，有任何謬誤也請各方大德直接聯繫我，感激不盡。

---

有板友問到，要如何選擇要不要用 ELK，其實也這是整篇 ELK 的初衷。這邊分享一下 ELK 與其他選擇，以及選擇解決方案應該考慮的事情。

# 其他常用的服務

[Prometheus](https://prometheus.io/): 開源的 time series metrics 收集系統

[Stackdriver](https://cloud.google.com/stackdriver/?hl=zh-tw): GCP 的 log 與 metrics 平台

[Elastic Cloud](https://www.elastic.co/cloud/): ELK 的 Sass

[Self-hosted ELK](https://chechia.net/post/self-host-elk-stack-on-gcp/)

或是依照需求混搭，各個服務使用的各層套件是可以相容，例如

* 在 GKE 上不用 beat 可以用 fluentd
* Prometheus -> Stackdriver
* ELK -> Stackdriver
* Fluentd -> Prometheus
...

* Sass vs cloud self-hosted vs on-premised
* Metrics: ELK vs Prometheus vs Stackdriver
* Logging: ELK vs Stackdriver

# 取捨原則

各個方法都各有利弊，完全取決於需求

1. 已知條件限制，例如安全性考量就是要放在私有網路防火牆內，或是預算
2. 資料讀取方式，有沒有要交叉比對收集的資料，還是單純依照時間序查詢
3. 或是資料量非常大，應用數量非常多
4. 維護的團隊，有沒有想，或有沒有能力自己養 self-host 服務

# Sass vs Self-hosted vs On-premised

Sass: 指的是直接用 Elasitc Cloud，或是直接使用公有雲的服務(ex. 在 GCP 上使用 stackdriver)

Cloud Self-hosted: 在公有雲上使用 ELK

On-Premised: 自己在機房搭設

### 安全性

看公司的安全政策，允許將日誌及監控數據，送到私有網路以外的地方嗎？如果在防火牆內，搞不好 port 根本就不開給你，根本不用考慮使用外部服務。

要知道服務的 log 其實可以看出很多東西．如果有特別做資料分析，敏感的資料，金流相關數據，通常不會想要倒到第三方服務平台。

可能有做金流的，光是安全性這點，就必須選擇自架。

### 成本

金錢成本 + 維護成本

金錢成本就看各個服務的計費方式

* [Elastic Cloud Pricing](https://www.elastic.co/products/elasticsearch/service/pricing)
* Self-hosted ELK & Prometheus：機器成本
* 公有雲服務(ex. [GCP Stackdriver](https://cloud.google.com/stackdriver/pricing?hl=zh-tw)): 用量計費 

維護成本: 工程師的月薪 * 每個月要花在維護服務的工時比例

一般 Sass 代管的服務，會降低維護成本，基本上就是做到網頁點一點就可以用。

如果公司有完整的維護團隊，有機房，服務的使用量也很大，當然 self-hosted 是比較省。
中小型企業以及新創，服務在公有雲上的，直接使用Sass 服務往往比較節省成本，服務直接由 Sass 維護，節省很多機器上管理跟日常維護。

避免迷思，買外部服務的帳單是顯性的，報帳時看得到，而工程師維護的時間成本是隱性的。self-host 可能省下 Sass 費用，但工程因為分了時間去維護，而影響進度。這部分就看團隊如何取捨。

### 易用性

如果應用都跑在公有雲上，可以考慮使用雲平台提供的監測服務，使用便利，而且整合度高。ex  GCP 上，要啟用 Stackdriver 是非常輕鬆的事情，只是改一兩個選項，就可以開啟 / 關閉 logging 與 metrics

如果是 On-premised 自家機房，也許 self-hosted 會更為適合。

### 客製化程度

在大多數時候，沒有需要更改到服務的核心設定，都可以不可律客製化程度，直接使用 Sass 的設定，就能滿足大部分需求。可以等有有明確需求後再考慮這一點。短期內沒有特殊需求就可以從簡使用。

使用GKE 到 Stackdriver 的話，對主機本身的機器是沒有控制權的，執行的 pipeline 也不太能更改
Elastic Cloud 有提供上傳 elasticsearch config 檔案的介面，也就是可以更改 server 運行的參數設定
Self-Hosted 除了上述的設定，還可以依照需求更改 ELK / prometheus 服務，在實體機器上的 topology，cpu 記憶體的資源配置，儲存空間配置等，可以最大化機器的效能。

### Scalability

資料流量大，儲存空間消耗多，服務負擔大，可能就會需要擴展。

一個是資料量的擴展。一個是為了應付服務的負擔，對 ELK 服務元件做水平擴展。

除了 elasticsearch 以爲的元件，例如 kibana，apm-server, beats 都可以透過 kubernetes 輕易的擴展，唯有 elasticsearch ，由於又牽扯上述資料量的擴展，以及分佈，還有副本管理，index 本身的 lifecycle 管理。Elasticsearch 的 scaling 設定上是蠻複雜的，也有很多工要做。index 的 shards / replicas 設定都要注意到。否則一路 scale 上去，集群大的時候彼此 sharding sync 的效能消耗是否會太重。

Stackdriver 從使用者的角度，是不存在服務節點的擴展問題，節點的維護全都給 Sass 管理。資料量的擴展問題也不大，只要整理資料 pipeline，讓最後儲存的資料容易被查找。

# Timeseries vs non-timeseriese

Prometheus [是自帶 time series database](https://prometheus.io/docs/prometheus/latest/storage/)，stackdriver 也是 time series 的儲存。ELK 的 elasticsearch 是全文搜索引擎，用了 timestamp 做分析所以可以做到 time series 的資料紀錄與分析。這點在本質上是完全不同的。

* 光只處理 time series data，Prometheus 的 query 效能是比 elasticsearch 好很多
* Elasticsearch 有大量的 index 維護，需要較多系統資源處理，在沒有 query 壓力的情形下會有系統自動維護的效能消耗
* ELK 的資料不需要預先建模，就可以做到非常彈性的搜尋查找。Stackdriver 的話，無法用未建模的資料欄位交叉查找。
  * Log 收集方面
    * Elasticsearch 中的資料欄位透過 tempalte 匯入後，都是有做 index ，所以交叉查找，例如可以從 log text 中包含特定字串的紀錄，在做 aggregate 算出其他欄位的資料分佈。會比較慢，但是是做得到的全文搜索
    * Stackdriver 可以做基本的 filter ，例如 filter 某個欄位，但不能做太複雜的交叉比對，也不能針對 text 內容作交互查找，需要換出來另外處理。
  * Metrics 收集方面
    * (同上) Elasticsearch 可以用全文搜索，做到很複雜的交叉比對，例如：從 metrics 數值，計算在時間範圍的分佈情形(cpu 超過 50% 落在一天 24 小時，各個小時的次數)
    * Stackdriver 只能做基本的 time series 查找，然後透過預先定義好的 field filter 資料，再各自圖像化。
    * Prometheus 也是必須依照 time series 查找，語法上彈性比 stackdriver 多很多，但依樣不能搜尋沒有 index 的欄位
    * 這邊要替別提，雖然 Elasticsearch 能用全文搜索輕易地做到複雜的查詢語法，但以 metrics 來說，其實沒有太多跳脫 time series 查找的需求。能做到，但有沒有必要這樣做，可以打個問號。

個人心得，如果驗證全新的 business model，或是還不確定的需求，可以使用 ELK 做各種複雜的查詢

如果需求明確，收進來的 log 處理流程都很明確，也許不用使用 ELK。

* 論系統資源 CP 值以及效能，time series 的 db 都會比 Elasticsearch 好上不少。
* Elasticsearch 中也不太適合一直存放大量的資料在 hot 可寫可讀狀態，繪希好很多系統資源。

# 其他服務

Elastic 有出許多不同的增值服務

* Application Performance Monitoring(APM)
* Realtime User Monitoring(RUM)
* Machine Learning(ELK ML)

而 ELK 以外也都有不同的解決方案，例如 

* GCP 也出了自己的 APM Sass
* Google Analytics(GA) 不僅能做多樣的前端使用者行為分析，還能整合 Google 收集到的使用者行為，做更多維度的分析

相較之下 ELK 在這塊其實沒有特別優勢。

# Elastic Cloud

我這邊要特別說 Elastic Cloud vs ELK

Elatic Cloud 的運行方式，是代為向公與恩平台(aaws, gcp,...)，帶客戶向平台租用機器，然後把 ELK 服務部署到租用的機器上。用戶這邊無法直接存取機器，只能透過 ELK 介面或是 Kibana , API 進入 ELK。Elastic Cloud 會監控無誤節點的狀況，並做到一定程度的代管。

這邊指的一定程度的代管，是 Elastic Cloud 只是代為部署服務，監控。有故障時並不負責排除，如果 ELK 故障，簡單的問題（ex. 記憶體資源不足）會代為重開機器，但如果是複雜的問題，還是要用戶自己處理．但是用戶又沒有主機節點的直接存取權限，所以可能會造成服務卡住無法啟動，只能透過 Elastic Cloud 的管理介面嘗試修復。

使用服務除了把服務都架設完以外，還是需要定期要花時間處理 performance tuning，設定定期清理跟維護。包括 kafka, redis, mongoDB, cassandra, SQLs...都是一樣，架構越複雜，效能要求越高，這部分的工都會更多。如果公司有 DBA，或是專職維護工程師，那恭喜就不用煩惱。

Elasticsearch server 目前用起來，算是是數服務中，維護上會花比較多時間的服務。

* 因為引擎本身設計的架構，並不是很多人都熟悉。在使用ELK同時，對ELK底層引擎的運作流程有多熟悉，會直接影響穩定性跟跑出來的效能。
* 需要好好處理設計資料的儲存，如果使用上沒處理好，會直接讓整個ELK 掛掉。
* 然後產品本身的維護介面，目前只是在堪用，許多重要的功能也還在開發中。

如果公司有人會管 ELK，個人建議是可以 self-host

# 小結

* 弄清楚需求，如果沒有特殊需求可以走 general solution
* Sass vs Self-hosted vs On-premised
* Time series vs non time series
