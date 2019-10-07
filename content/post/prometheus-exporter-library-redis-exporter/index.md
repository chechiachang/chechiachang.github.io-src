+++
title = "Prometheus Exporter Library & Redis Exporter"
subtitle = ""

# Add a summary to display on homepage (optional).
summary = ""

date = 2019-10-06T8:12:10+08:00
draft = true

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
  - [GKE 上自架 Prometheus / Grafana]({{< ref "/posts/prometheus-deployment-on-kubernetes" >}})
  - GKE 上自架 Grafana 與設定
  - 使用 exporter 監測 GKE 上的各項服務
  - 輸出 redis-ha 的監測數據
  - 自幹 exporter
  - 輸出 kafka 的監測數據
  - 輸出 kubernetes 的監測數據

由於我比較熟悉 GCP / GKE 的服務，這篇的操作過程都會以 GCP 平台作為範例，不過操作過程大體上是跨平台通用的。

寫文章真的是體力活，覺得我的文章還有參考價值，請左邊幫我點讚按個喜歡，右上角幫我按個追縱，底下歡迎留言討論。給我一點繼續走下去的動力。

對我的文章有興趣，歡迎到我的網站上 [https://chechiachang.github.io](https://chechiachang.github.io) 閱讀其他技術文章，有任何謬誤也請各方大德直接聯繫我，感激不盡。

![Exausted Cat Face](https://d32l83enj9u8rg.cloudfront.net/wp-content/uploads/iStock-966846550-cat-overheating-simonkr-1-940x470.jpg)

---

# 摘要

* Exporter 工作原理簡介
* Prometheus exporter library

# Exporter workflow

上次講到 exporter 可以從服務端把運行資料抽出來，並開成 http endpoint，讓 prometheus 來 scrape metrics。那 exporter 本身是如何取得服務內部的 metrics 呢? 我們今天就稍微看一下。

# Redis Exporter

我們今天以 [Redis Exporter](https://github.com/oliver006/redis_exporter) 為例，研究一下外部的 exporter 是如何取得 redis 內部的 metrcs。

Redis exporter 是用 golang 寫的一個小程式，總共算算才 1000 行，而且很多都是對 redis 內部 metrics 的清單，以及轉化成 prometheus metrics 的 tool functions，主要的邏輯非常簡單。我們簡單看一下源碼。


[Collect](https://github.com/oliver006/redis_exporter/blob/master/exporter.go#L386) 是主要的收集邏輯，就是執行 scrapeRedisHost(ch) ，然後把收集到的資訊，使用 [Prometheus Go Client Library](https://github.com/prometheus/client_golang) 的工具將資料註冊成 prometheus metrics

```
func (e *Exporter) Collect(ch chan<- prometheus.Metric) {
	e.Lock()
	defer e.Unlock()
	e.totalScrapes.Inc()

	if e.redisAddr != "" {
		start := time.Now().UnixNano()
		var up float64 = 1

    // 從 host scrape 資料，然後塞進 channel streaming 出來。
		if err := e.scrapeRedisHost(ch); err != nil {
			up = 0
			e.registerConstMetricGauge(ch, "exporter_last_scrape_error", 1.0, fmt.Sprintf("%s", err))
		} else {
			e.registerConstMetricGauge(ch, "exporter_last_scrape_error", 0, "")
		}

		e.registerConstMetricGauge(ch, "up", up)
		e.registerConstMetricGauge(ch, "exporter_last_scrape_duration_seconds", float64(time.Now().UnixNano()-start)/1000000000)
	}

	ch <- e.totalScrapes
	ch <- e.scrapeDuration
	ch <- e.targetScrapeRequestErrors
}
```

scrapeRedisHost 內部的主要邏輯，又集中在[執行 Info](https://github.com/oliver006/redis_exporter/blob/master/exporter.go#L1144)

```
  // 執行 info 
	infoAll, err := redis.String(doRedisCmd(c, "INFO", "ALL"))
	if err != nil {
		infoAll, err = redis.String(doRedisCmd(c, "INFO"))
		if err != nil {
			log.Errorf("Redis INFO err: %s", err)
			return err
		}
	}
```

也就是說當我們在 redis-cli 連入 redis 時，可以執行 Info command，取得 redis 內部的資訊，包含節點設店與狀態，集群設定，資料的統計數據等等。然後 exporter 這邊維護持續去向 redis 更新 info ，並且把 info data 轉化成 time series 的 metrcs，再透過 [Prometheus Client promhttp](https://github.com/prometheus/client_golang/tree/master/prometheus/promhttp) 提供的 http endpoint library，變成 http endpoint。

首先看一下 [redis info command 的文件](https://redis.io/commands/info)，這邊有說明 info 的 option ，以及 option 各自提供的資料，包括 server 狀態，賀戶端連線狀況，系統資源，複本狀態等等。我們也可以自己透過 info 取得資料。

```
$ kubectl get po | grep redis

redis-2-redis-ha-server-0                                3/3     Running     0          11d
redis-2-redis-ha-server-1                                3/3     Running     0          11d
redis-2-redis-ha-server-2                                3/3     Running     0          11d

$ kubectl exec -it redis-2-redis-ha-server-0  sh
$ redis-cli -h haproxy-service  -a REDIS_PASSWORD
$ haproxy-service:6379>

$ haproxy-service:6379> info server
# Server
redis_version:5.0.5
redis_git_sha1:00000000
redis_git_dirty:0
redis_build_id:4d072dc1c62d5672
redis_mode:standalone
os:Linux 4.14.127+ x86_64
arch_bits:64
multiplexing_api:epoll
atomicvar_api:atomic-builtin
gcc_version:8.3.0
process_id:1
run_id:63a97460b7c3745577931dad406df9609c4e2464
tcp_port:6379
uptime_in_seconds:976082
uptime_in_days:11
...

$ haproxy-service:6379> info clients
# Clients
connected_clients:100
client_recent_max_input_buffer:2
client_recent_max_output_buffer:0
blocked_clients:1
```

Redis exporter 收集這些數據，透過 prometheus client library 把資料轉成 time series prometheus metrics。然後透過 library 放在 http enpoint 上。

配合上次說過的 redis overview dashboard，可以直接在 Grafana 上使用

![Redis Overvies library](https://cloud.githubusercontent.com/assets/1222339/19412031/897549c6-92da-11e6-84a0-b091f9deb81d.png)

這邊 dashboard 顯示幾個重要的 metrics

* Uptime
* Memory Usage，要設定用量太高自動報警
* Command 的執行狀況，回應時間
* 訊息的流量，以及超出 time-to-live 的資料清除。

都是需要好好加上 alert 的核心 metrics

# 貢獻 exporter

其他服務的 exporter 工作原理也相似，如果服務本身有內部的 metrics，可以透過 client command 或是 API 取得，exporter 的工作就只是轉成 time series data。

如果有比較特殊的 metrics 沒有匯出，例如說自家的 metrics ，但又希望能放到 prometheus 上監測，例如每秒收到多少 request count，回應速度，錯誤訊息的統計......等，這點也可以使用 client library 自幹 exporter 然後 expose http endpoint，這樣在 prometheus 上也可以看到自家產品的 metrics，非常好用。有機會我們來聊自幹 exporter。