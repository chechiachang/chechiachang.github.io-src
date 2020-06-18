---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Kafka Operation Scripts"
subtitle: ""
summary: ""
authors: []
tags: []
categories: []
date: 2019-09-25T22:50:32+08:00
lastmod: 2019-09-25T22:50:32+08:00
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

寫文章真的是體力活，覺得我的文章還有參考價值，請左邊幫我點讚按個喜歡，右上角幫我按個追縱，底下歡迎留言討論。給我一點繼續走下去的動力。

對我的文章有興趣，歡迎到我的網站上 [https://chechia.net](https://chechia.net) 閱讀其他技術文章，有任何謬誤也請各方大德直接聯繫我，感激不盡。

![Exausted Cat Face](https://d32l83enj9u8rg.cloudfront.net/wp-content/uploads/iStock-966846550-cat-overheating-simonkr-1-940x470.jpg)

---

# 摘要

* 從 Zookeeper 獲取資訊
* 取得並處理 topic
* benchmark kafka

# zookeeper

zookeeper 是 kafka 的分散式協調系統，在 kafka 上多個節點間需要協調的內容，例如：彼此節點的ID，位置與當前狀態，或是跨節點 topic 的設定與狀態。取名叫做 zookeeper 就是在協調混亂的分散式系統，,裡面各種不同種類的服務都要協調，象個動物園管理員。[Zookeeper 的官方文件](https://zookeeper.apache.org/doc/r3.3.3/zookeeperAdmin.html) 有更詳細的說明。

Kafka 的節點資訊，與當前狀態，是放在 zookeeper 上，我們可以透過以下指令取得
```
# 首先先取得 zkCli 的 cli，這個只有連進任何一台 zookeeper 內部都有
kubectl exec -it kafka-0-zookeeper-0 --container kafka-broker bash

# 由於是在 Pod 內部，直接 localhost 詢問本地
/usr/bin/zkCli.sh -server localhost:2181

Connecting to localhost:2181
2019-09-25 15:02:36,089 [myid:] - INFO  [main:Environment@100] - Client environment:zookeeper.version=3.4.10-39d3a4f269333c922ed3db283be479f9deacaa0f, built on 03/23/2017 10:13 GMT
2019-09-25 15:02:36,096 [myid:] - INFO  [main:Environment@100] - Client environment:host.name=kafka-0-zookeeper-0.kafka-0-zookeeper-headless.default.svc.cluster.local
2019-09-25 15:02:36,096 [myid:] - INFO  [main:Environment@100] - Client environment:java.version=1.8.0_131
2019-09-25 15:02:36,100 [myid:] - INFO  [main:Environment@100] - Client environment:java.vendor=Oracle Corporation
2019-09-25 15:02:36,100 [myid:] - INFO  [main:Environment@100] - Client environment:java.home=/usr/lib/jvm/java-8-openjdk-amd64/jre
2019-09-25 15:02:36,100 [myid:] - INFO  [main:Environment@100] - Client environment:java.class.path=/usr/bin/../build/classes:/usr/bin/../build/lib/*.jar:/usr/bin/../share/zookeeper/zookeeper-3.4.10.jar:/usr/bin/../share/zookeeper/slf4j-log4j12-1.6.1.jar:/usr/bin/../share/zookeeper/slf4j-api-1.6.1.jar:/usr/bin/../share/zookeeper/netty-3.10.5.Final.jar:/usr/bin/../share/zookeeper/log4j-1.2.16.jar:/usr/bin/../share/zookeeper/jline-0.9.94.jar:/usr/bin/../src/java/lib/*.jar:/usr/bin/../etc/zookeeper:
2019-09-25 15:02:36,100 [myid:] - INFO  [main:Environment@100] - Client environment:java.library.path=/usr/java/packages/lib/amd64:/usr/lib/x86_64-linux-gnu/jni:/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu:/usr/lib/jni:/lib:/usr/lib
2019-09-25 15:02:36,100 [myid:] - INFO  [main:Environment@100] - Client environment:java.io.tmpdir=/tmp
2019-09-25 15:02:36,100 [myid:] - INFO  [main:Environment@100] - Client environment:java.compiler=<NA>
2019-09-25 15:02:36,101 [myid:] - INFO  [main:Environment@100] - Client environment:os.name=Linux
2019-09-25 15:02:36,101 [myid:] - INFO  [main:Environment@100] - Client environment:os.arch=amd64
2019-09-25 15:02:36,101 [myid:] - INFO  [main:Environment@100] - Client environment:os.version=4.14.127+
2019-09-25 15:02:36,101 [myid:] - INFO  [main:Environment@100] - Client environment:user.name=zookeeper
2019-09-25 15:02:36,102 [myid:] - INFO  [main:Environment@100] - Client environment:user.home=/home/zookeeper
2019-09-25 15:02:36,102 [myid:] - INFO  [main:Environment@100] - Client environment:user.dir=/
2019-09-25 15:02:36,105 [myid:] - INFO  [main:ZooKeeper@438] - Initiating client connection, connectString=localhost:2181 sessionTimeout=30000 watcher=org.apache.zookeeper.ZooKeeperMain$MyWatcher@42110406
Welcome to ZooKeeper!
2019-09-25 15:02:36,160 [myid:] - INFO  [main-SendThread(localhost:2181):ClientCnxn$SendThread@1032] - Opening socket connection to server localhost/127.0.0.1:2181. Will not attempt to authenticate using SASL (unknown error)
JLine support is enabled
2019-09-25 15:02:36,374 [myid:] - INFO  [main-SendThread(localhost:2181):ClientCnxn$SendThread@876] - Socket connection established to localhost/127.0.0.1:2181, initiating session
2019-09-25 15:02:36,393 [myid:] - INFO  [main-SendThread(localhost:2181):ClientCnxn$SendThread@1299] - Session establishment complete on server localhost/127.0.0.1:2181, sessionid = 0x16d67baf1310001, negotiated timeout = 30000

WATCHER::

WatchedEvent state:SyncConnected type:None path:null
[zk: localhost:2181(CONNECTED) 0]
```

取得 kafka broker 資料

```
# List root Nodes
$ ls /

[cluster, controller, controller_epoch, brokers, zookeeper, admin, isr_change_notification, consumers, log_dir_event_notification, latest_producer_id_block, config]

# Brokers 的資料節點
$ ls /brokers
[ids, topics, seqid]

# List /brokers/ids 得到三個 kafka broker
$ ls /brokers/ids
[0, 1, 2]

# 列出所有 topic 名稱
ls /brokers/topics
[ticker]
```

ticker 是上篇範利用到的 topic

簡單來說，zookeeper 存放這些狀態與 topic 的 metadata

* 儲存核心的狀態與資料，特別是 broker 萬一掛掉，也還需要維持的資料
* 協調工作，例如協助 broker 處理 quorum，紀錄 partition master 等

```
# 離開 zkCli
quit
```

# Kafka

這邊一樣先連線進去一台 broker，取得 kafka binary

```
kubectl exec -it kafka-0-0 --container kafka-broker bash

 ls /usr/bin/ | grep kafka
kafka-acls
kafka-broker-api-versions
kafka-configs
kafka-console-consumer
kafka-console-producer
kafka-consumer-groups
kafka-consumer-perf-test
kafka-delegation-tokens
kafka-delete-records
kafka-dump-log
kafka-log-dirs
kafka-mirror-maker
kafka-preferred-replica-election
kafka-producer-perf-test
kafka-reassign-partitions
kafka-replica-verification
kafka-run-class
kafka-server-start
kafka-server-stop
kafka-streams-application-reset
kafka-topics
kafka-verifiable-consumer
kafka-verifiable-producer
```

很多工具，我們這邊只會看其中幾個

### topic 資訊

Topic 的資訊，跟 zookeeper 要
```
# List topics
/usr/bin/kafka-topics --list --zookeeper kafka-0-zookeeper

ticker
```

### 操作 message

從 topic 取得 message

```
# This will create a new console-consumer and start consuming message to stdout
/usr/bin/kafka-console-consumer \
--bootstrap-server localhost:9092 \
--topic engine_topic_soundwave_USD \
--timeout 0 \
--from-beginning
```

如果 ticker 那個 example pod 還在執行，這邊就會收到 ticker 的每秒 message

如果沒有，也可以開啟另一個 broker 的連線
```
kubectl exec -it kafka-0-1 --container kafka-broker bash

# 使用 producer 的 console 連入，topic 把 message 塞進去
/usr/bin/kafka-console-producer \
--broker-list localhost:9092\
 --topic ticker

tick [enter]
tick [enter]
```

kafka-console-consumer 那個 terminal 就會收到 message
```
tick
tick
```

當然也可以使用 consumer group

```
# Use consumer to check ticker topics
/usr/bin/kafka-console-consumer \
--bootstrap-server localhost:9092 \
--topic ticker \
--group test
```

有做過上面的操作產生 consumer group，就可以透過 consumer API，取得 consumer group 狀態

```
# Check consumer group
/usr/bin/kafka-consumer-groups \
--bootstrap-server localhost:9092 \
--group ticker \
--describe

Consumer group 'test' has no active members.

TOPIC           PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG             CONSUMER-ID     HOST            CLIENT-ID
ticker          0          23              23              0               -               -               -
```

# Topic 設定操作

[Topic 設定文件](https://kafka.apache.org/documentation/#topicconfigs) 在此

這邊透過 kafka-configs 從 zookeeper 取得 topic 設定，這邊的 max.message.bytes，是這個 topic 每個 message 的最大上限。

```
/usr/bin/kafka-configs --zookeeper kafka-0-zookeeper:2181 --describe max.message.bytes --entity-type topics

Configs for topic '__consumer_offsets' are segment.bytes=104857600,cleanup.policy=compact,compression.type=producer
Configs for topic 'ticker' are
```

`__consumer__offsets` 是系統的 topic ，紀錄目前 consumer 讀取的位置。

ticker 沒有設定，就是 producer 當初產生 topic 時沒有指定，使用 default 值

由於我們公司的使用情境常常會超過，所以可以檢查 producer app 那端送出的 message 大小，在比較這邊的設定。當然現在 ticker 的範例，只有一個 0-60 的數值，並不會超過。這個可以在 helm install 的時候，使用 value.yaml 傳入時更改。

不喜歡這個值，可以更改，這邊增加到 16MB
```
TOPIC=ticker

/usr/bin/kafka-configs \
  --zookeeper kafka-3-zookeeper:2181 \
  --entity-type topics \
  --alter \
  --entity-name ${TOPIC} \
  --add-config max.message.bytes=16000000

```

# Benchmark

使用內建工具跑 benchmark

Producer
```
/usr/bin/kafka-producer-perf-test \
  --num-records 100 \
  --record-size 100 \
  --topic performance-test \
  --throughput 100 \
  --producer-props bootstrap.servers=kafka:9092 max.in.flight.requests.per.connection=5 batch.size=100 compression.type=none

100 records sent, 99.108028 records/sec (0.01 MB/sec), 26.09 ms avg latency, 334.00 ms max latency, 5 ms 50th, 70 ms 95th, 334 ms 99th, 334 ms 99.9th.
```

Consumer
```
/usr/bin/kafka-consumer-perf-test \
  --messages 100 \
  --broker-list=kafka:9092 \
  --topic performance-test \
  --group performance-test \
  --num-fetch-threads 1
```
