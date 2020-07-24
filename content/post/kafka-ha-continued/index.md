---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Kafka HA Continued"
subtitle: ""
summary: ""
authors: []
tags: []
categories: []
date: 2019-09-26T22:50:32+08:00
lastmod: 2019-09-26T22:50:32+08:00
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

* Kafka's quorum set

# Kafka 的 quorum set

這篇跟上篇其實再講 quorum，應該連在一起，但礙於篇幅（以及我個人的時間ＱＱ）拆成了兩篇。各位有需要可以回顧一下。

### Replicated log commit decision

上篇提到了兩個維持 replicated log 的 model

* 有更新進來，leader 等待所有 follower 都 ack，才 commit。
* 有更新進來，leader 取得所有 node (2n+1) 中的多數 node 回應(n+1)，就 commit。而 leader election 時，必須比對 node 上的 log，決定誰是 electable leader(有最完整 log 的 follower)，這樣稱為共識(Quorum)

前者的好處是，所有 node 都有完整的 log 後，leader 才會 commit，回覆給客戶 commit  的資訊，所以每個 follower 都是 leader electable 人人都可以當 leader，leader 一故障就選擇新的 leader 即可。壞處就是 leader 在等待所有 follow ack 的時間會非常久，而且時間複雜度可能會隨 cluster size scale，或是變成要等最慢的 node 回應(worst case)。這樣在 node 數量多的時候非常不經濟。 

後者的好處是，n+1 node ack 後就 commit，leader commit 的速度是由前段班的回應速度決定。leader 出現故障，仍能維持多數 node 的資料正確。

### Leader election decision

Leader Election 的問題也是類似，如果選擇 leader 時，所有的 follower 都比對過 log，這樣花的時間會很久。要知道，這是個分散式的架構，沒有中心化的 controller，也就是 follower 彼此需要交互比對。而且時間隨 follower 數量 scale。 造成topic partition 沒有 leader 的時間(downtime)太長。

如果使用 majority，也就是當 leader 死掉，產生新的 leader election 時，只詢問 n+1 個 follower ，然後從選出 log 最完整的人當 leader， 這樣過程中每個 follower 彼此比對，確認，然後才選出 leader，確認 leader 的結果，所花的時間會大幅縮短。

當然，這麼做產生的 tradeoff，就是萬一取得多數決的 n+1 個 follower 裡面，沒有最完整的 log ，那從裡頭選出來的 leader 自然也沒有完整 log，選出來的 leader 就會遺失資料。

### 一個完整的 Quorum 機制

這不是 kafka 的機制，但我們順帶聊聊。

* commit decision 使用多數決(majority)
* leader election 也使用多數決

總共有 2n+1 replicas，leader 取得 n+1 ack 才能 commit message。然後 leader election 時，從至少 n+1 個 follower 中取得多數決才能選出 leader。有過半的完整log，加上取得過半數的人確認，兩者產生 overlap。這樣的共識就確保有完整的 log 的 follower 一定會出現在 leader election 中，確保選出來的 leader 有完整 log。

好處如前面描述，整體效能由前段班的速度決定。

壞處是，很容易就沒有足夠的 electable leader。要容忍 1 個錯誤，需要 3 個完整備份，要容忍 2 個錯誤需要 5 個備份。在實務上，只靠依賴夠多的 redundency 容錯非常的不實際：每一次寫入需要 5 倍寫入跟硬碟空間，但整體效能只有 1/5。資料量大就直接ＧＧ。所以 quorum 才會只存在分散式集群(ex. zookeeper)，而不會直接用在儲存系統。

### Kafka's approach

Kafka 不使用 majority vote，而是去動態維護一套 in-sync replicas(ISR) ，這些 ISR 會跟上 leader 的進度，而只有這些 ISR 才能是 leader eligible。一個 update 只有在所有 ISR 都 ack 後才會 commit。

ISR 的狀態不放在 kafka 而放在 zookeeper 上，也就是目前哪些 node 是 ISR 的記錄存在 zookeeper。這件事對維持 kafka 節點上，leader 能夠分散在各個 kafka node 上(leader rebalance)是很重要的。

kafka's approach 與 majority vote，在等待 message commit ack 上所花的成本是一樣的。 然而在 leader election 上，kafka 的 ISR 確保了更多個 eligiable leader 的數量，持續維持在合理的數量，而不會要維持大量個 redundency。ISR 放在外部，更方便 kafka 做 leader rebalance，增加穩定度。

# Unclean leader election

如果 leaders 都死光了會怎樣？

只要有一個 replica in-sync，Kafka 就保證資料的完整性。然而所有可用的 leaders 都死了，這個就無法保證。

如果這個情形發生了，kafka 會做以下處理

* 等 ISR 中有人完全回復過來，然後選這個 node 作為 leader(有資料遺失的風險)
* 直接選擇第一個回覆的 node (不一定在 ISR 中)，先回覆的就指派為 leader

前者犧牲 availability （回覆前沒有 leader 可作讀寫）來確保資料是來自 ISR，雖然錯誤中無法讀寫(downtime)，但可以確定錯誤前跟錯誤後的資料都來自 ISR

後者犧牲 consistency （來自非 ISR 的 leader 可能導致資料不正確），然而卻能更快的從錯誤中回覆，減少 downtime

0.11.0.0  後的 kafka 預設是選擇前者，也就是 consistency over availability，當然這可以在設定更改。

# Availability and Durability Guarantees

近一步考慮 client 的影響。

Producer 在寫入時可以選擇 message 需要多少 acknowledge，0, 1 or all，ack=all 指的是 message 收到所有 in-sync replicas 的 ack

* 如果 2 replicas 中有 1 個故障，這時寫入只要收到 1 個 ISR 的 ack，就達成 ack=all
* 但如果不幸剩下一個 replicas 也死了 (0/0 ack)，寫入的資料就會遺失

有些使用情境，會希望資料的耐用度(Durability)優先於可用性(Availability)，可以透過以下兩個方式設定

* 禁用 unclean leader election，效果是如果所有的 replicas 都失效，則整個 partition 都失效，直到前一個 leader 回復正常。
* 指定可接受的最少 ISR，如果 partition 中的 ISR 低於這個數量，就停止寫入這個 partition，直到 ISR 的數量回覆。

這樣雖然犧牲了可用性，卻可以最大程度地確保資料的可靠性。

# 複本管理

上面的討論都只是再說一個 topic，實務中 kafka 中會有大量的 topic ，乘上 partition number 與 replication factor，成千上萬的複本分散在集群中，kafka 會試圖分散 replicas 到集群中，並讓 leader 的數量平均在 node 上
