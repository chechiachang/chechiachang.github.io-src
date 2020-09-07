---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Kafka HA Topology"
subtitle: ""
summary: ""
authors: []
tags: ["kafka", "kubernetes"]
categories: ["kubernetes", "kafka"]
date: 2019-09-25T22:50:32+08:00
lastmod: 2019-09-25T22:50:32+08:00
featured: false
draft: false

menu:
  main:
    parent: "Ithelp 鐵人賽"
    weight: 1
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

* Zookeeper Multi-server setup
* Kafka Multi-broker setup

# Zookeeper Multi-Server

為了維持 zookeeper 有效運作，cluster 必須維持 majority (多數)，也就是至少一半的機器在線。如果總共 3 台，便可以忍受 1 台故障仍保有 majority。如果是 5 台就可以容忍 2 台故障。一般來說都建議使用基數數量。[Zookeeper Multi Server Setup](https://zookeeper.apache.org/doc/r3.4.12/zookeeperAdmin.html#sc_zkMulitServerSetup)

普遍情況，3 台 zookeeper 已經是 production ready 的狀態，但如果為了更高的可用性，以方便進行單節點停機維護，可以增加節點數量。

### Topology

需要將 zookeeper 放在不同的機器上，不同的網路環境，甚至是不同的雲平台區域上，以承受不同程度的故障。例如單台機器故障，或是區域性的網路故障。

我們這邊會使用 Kubernetes PodAntiAffinity，要求 scheduler 在部屬時，必須將 zookeeper 分散到不同的機器上。設定如下：

```
vim values-staging.yaml

zookeeper:
  enabled: true

  resources: ~

  env:
    ZK_HEAP_SIZE: "1G"

  persistence:
    enabled: false

  image:
    PullPolicy: "IfNotPresent"

  url: ""
  port: 2181

  ## Pod scheduling preferences (by default keep pods within a release on separate nodes).
  ## ref: https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#affinity-and-anti-affinity
  ## By default we don't set affinity:
  affinity: # Criteria by which pod label-values influence scheduling for zookeeper pods.
   podAntiAffinity:
     requiredDuringSchedulingIgnoredDuringExecution:
       - topologyKey: "kubernetes.io/hostname"
         labelSelector:
           matchLabels:
             release: zookeeper
```

使用 podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution，如果 topologyKey 已經有指定 label 的 pod 存在，則無法部署，需要數到其他台機器。

```
kubectl get pods --output wide | grep zookeeper

NAME                  READY   STATUS      RESTARTS   AGE     IP              NODE                                    
kafka-0-zookeeper-0   1/1     Running     0          42d     10.8.12.4       gke-chechiachang-pool-1-e06e6d00-pc98   
kafka-0-zookeeper-1   1/1     Running     0          42d     10.8.4.4        gke-chechiachang-pool-1-e06e6d00-c29q   
kafka-0-zookeeper-2   1/1     Running     0          42d     10.8.3.6        gke-chechiachang-pool-1-e06e6d00-krwc   
```

效果是 zookeeper 都分配到不同的機器上。

### Guarantees

Zookeeper 對於資料一致性，有這些保障 [Consistency Guarantees](https://zookeeper.apache.org/doc/r3.5.5/zookeeperProgrammers.html#ch_zkGuarantees)

* 順序一致性：資料更新的順序，與發送的順序一致
* 原子性：資料更新只有成功或失敗，沒有部份效果
* 系統一致性：可戶端連到 server 看到的東西都是一樣，無關連入哪個 server
* 可靠性：
  * 客戶端的更新請求，一但收到 server 回覆更新成功，便會持續保存狀態。某些錯誤會造成客戶端收不到回覆， 可能是網路問題，或是 server 內部問題，這邊就無法確定 server 上的狀態，是否被更新了，或是請求已經遺失了。
  * 從客戶讀取到的資料都是以確認的資料，不會因為 server 故障回滾(Roll back)而回到舊的狀態

# Kafka 的設定

```
## The StatefulSet installs 3 pods by default
replicas: 3

resources:
   limits:
     cpu: 200m
     memory: 4096Mi
   requests:
     cpu: 100m
     memory: 1024Mi
kafkaHeapOptions: "-Xmx4G -Xms1G"
```
設定 broker 的數量，以及 Pod 提供的 resource，並且透過 heapOption 把記憶體設定塞進 JVM

```
affinity:
 affinity:
   podAntiAffinity:
     requiredDuringSchedulingIgnoredDuringExecution:
     - labelSelector:
         matchExpressions:
         - key: app
           operator: In
           values:
           - kafka
       topologyKey: "kubernetes.io/hostname"
   podAffinity:
     preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 50
        podAffinityTerm:
          labelSelector:
            matchExpressions:
            - key: app
              operator: In
              values:
                - zookeeper
```
這邊下了兩個 affinity

* podAntiAffinity 盡量讓 kafka-broker 分散到不同機器上
* podAffinity 讓 broker prefer 跟 zookeeper 放在一起

分散的理由同上，不希望一台機器死了，就讓多個 broker 跟著死

要和 zookeeper 放在一起，就要看需求與實際環境調整

```
configurationOverrides:
  "default.replication.factor": 3
  "offsets.topic.replication.factor": 2 # Increased from 1 to 2 for higher output
  "offsets.topic.num.partitions": 3
  "confluent.support.metrics.enable": false  # Disables confluent metric submission
  "auto.leader.rebalance.enable": true
  "auto.create.topics.enable": true
  "message.max.bytes": "16000000" # Extend global topic max message bytes to 16 Mb
```

這邊再把 broker 運行的設定參數塞進去，參數的用途大多與複本與高可用機制有關下面都會提到。

# Kafka 的複本機制

[kafka 的副本機制](https://kafka.apache.org/documentation/#replication) 預設將各個 topic partition 的 log 分散到 server 上，如果其中一台 server 故障，資料仍然可用。

兩個重要的設定

* num.partitions=N
* default.replication.factor=M

kafka 預設使用複本，所有機制與設計都圍繞著複本。如果（因為某些原因）不希望使用複本，可將 replication factor 設為 1。

replication 的單位是 topic partition，正常狀況下

* 一個 partition 會有一個 leader，以及零個或以上個 follower
* leader + follower 總數是 replication factor
* 所有讀寫都是對 leader 讀寫
* leader 的 log 會同步到 follower 上，leader 與 follower 狀態是一樣的

### Election & Load balance

通常一個 topic 會有多個 partition，也就是說，每個 topic 會有多個 partition leader，分散負載

通常 topic partition 的總數會比 broker 的數量多

* 以上一篇範例，我們有三個 kafka-0-broker 各自是一個 Pod
* 有 topic: ticker 跟預設的 `__consumer_offset__`，乘上 partition number 的設定值(N)，會有 2N 個 partitions
* partitiion 會有各自的複本，kafka 會盡量將相同 topic 的複本分散到不同 broker 上
* kafka 也會盡量維持 partition 的 leader 分散在不同的 broker 上，這個部分 kafka 會透過算法做 leader election，也可手動使用腳本做 [Balancing leadership](https://kafka.apache.org/documentation/#basic_ops_leader_balancing)

總之，topic 的 partition 與 leader 會分散到 broker 上，維持 partition 的可用性。

### sync

* node 要能夠維持 zookeeper 的 session (zookeeper 有 heartbeat 機制)
* follower 不能落後 leader 太多

kafka 能保障資料不會遺失，只要至少一個 node 是在 sync 的狀態。例如本來有三個 partition，其中兩個 partition 不同步，只要其中一個 partition 是同步，便能作為 leader 持續提供正確的 message。

# Replicated Logs

kafka 透過 [replicated log](https://kafka.apache.org/documentation/#design_replicatedlog) 維持分散式的 partition

複本間要維持共識(consensus)的最簡單機制，就是單一 leader 決定，其他 follower 跟隨。然而萬一 leader 死了，選出的新 leader 卻還沒跟上原先 leader 的資料。這時便使用 replicated log，來確保新的 leader 就算原先沒跟上，也能透過 replicated log 隨後跟上且不遺失資料。維持 log 一直都同步的前提，就是 leader 要一直確認 followers 的 log 都有跟上，這個其實就是變相的多 leader，效能消耗較大。

另一個維持 log 機制，如果希望 follower 彼此的 log 應該先進行比對，讓資料交接過程有 overlap，這個過程稱為 Quorum。一個常用的方式是多數決(majority)

* 如果總共有 2n+1 的 node，leader 要向 n+1 個 follower 取得共識，才確定這個 log 已經 commit 了
* leader 總是維持 n+1 follower 的 log 有跟上，因此可以容忍最多 n 個 node 死了，集群整體能有 n+1 的 node 維持著正確的 commited log
* 不用向所有 node 確認才 commit ，節省了一半的 ack
* majarity 的另一個好處是，n+1 共識的速度是由前 1/2 快的 node 決定的。由於只要先取得 n+1 就可以 commit，速度快的 node 會先回應，讓整體速度提升。
