---
title: "Gcp Preemptible Instance Speficication"
subtitle: ""
summary: ""
authors: []
tags: ["kubernetes", "gcp", "preemptible", "spot-instance"]
category: ["kubernetes"]
date: 2020-09-23T16:23:14+08:00
draft: true
---

# 終止流程 (Preemption process)

子曰：未知生焉知死。但做工程師要反過來，考量最差情形，也就是要知道應用可能噂麽死。不知道應用可能怎麼死，別說你知道應用活得好好的。

如同前幾篇所說的，先占虛擬機會被公有雲收回，但收回的時候不會突然機器就 ben 不見，會有一個固定的流程。

如果你的應用很強壯，能夠承受機器突然變不見，服務還好好的，仍然要花時間理解這邊的流程，藉此精算每天虛擬機的終止與替換，應用會有什麼反應，會產生多少衝擊，這邊可以量化服務的影響。例如

 - 應用初始化時 cpu memory 突然拉高
 - 承受節點錯誤後的復原流程，需要消耗額外算力。例如需要從上個 checkpoint 接續做，需要去讀取資料造成 IO，或是資料需要做 rebalance ...等等

如果你的應用需要有 graceful shutdown 的機制，那你務必要細心理解這邊的步驟。並仔細安排安全下樁的步驟。又或是無法保證在先占虛擬機回收的作業時限內，完成優雅終止，要考慮其他可能的實作解法。

這邊有幾個面向要注意

1. GCP 如何終止先占節點
2. GCP 移除節點對 GKE 、以及執行中應用的影響
3. GKE 集群如何應對的節點失效
4. GCP 自動調度補足新的先占節點
5. GKE 集群如何應對節點補足

三個重點

- 先占虛擬機終止對集群的影響
- Pod 隨之終止對應用的影響，是否能夠優雅終止
- 有沒有方法可以避免上面兩者的影響

劇透一下：有的，有一些招式可以處理。讓我們繼續看下去。

### GCP 如何終止先占節點

一樣先看[先占虛擬機的說明文件：終止流程](https://cloud.google.com/compute/docs/instances/preemptible?hl=zh-tw#preemption-process)

- 資料中心開始回收先占虛擬機，選中我們專案其中的一台先占虛擬機
- Compute Engine 傳送 ACPI G2 Soft Off，這裡觸發 [shutdown script](https://cloud.google.com/compute/docs/instances/create-start-preemptible-instance?hl=zh-tw#handle_preemption)，可以做簡短的優雅終止
- 30秒後，ACPI G3 Mechanical off，OS Kill

但 30 秒能做什麼？只能快速的交代當前進度。如果應用需要花時間收尾，保存工作進度，可能會導致大量應用一起進入優雅終止，先占虛擬機最後耗盡資源，來不及做完。如果可能會超時，或是沒完成會有資料遺失風險，就不能在這個階段處理。我們之後要想辦法處理這個不保證做完的優雅終止。

如果應用本身有容錯的框架，或是有容錯機制，我們這邊要額外做的工作就會少很多。例如在外部保存 checkpoint，worker 只負責運算，終止信號一進來，也不用保存，直接拋棄未完成的工作進度，留待繼起的 worker 從 checkpoint 接手。

# Preemption selection

GCP 不會把所你手上的 preemptible 機器都收走，而是依照比例選擇要被撤換的機器。

### GKE 如何處理移除節點

https://kubernetes.io/zh/docs/concepts/workloads/pods/disruptions/

https://dev.to/duske/how-kubernetes-handles-offline-nodes-53b5

### 對應用的影響

https://cloud.google.com/solutions/scope-and-size-kubernetes-engine-clusters

GCP 觸發的 Preemptible process

- 應用收到 kill (SIGTERM) 信號，作最後處理
- 最後處理不能花太多時間
  - Kubernetes 提供的 Graceful-shutdown 可能會跑不完
  - 需要花時間善後的應用可能不適合 (e.g. 花時間保留當前工作狀態)，如果完成前就被機器終止，會出錯

聽起來很難搞，豈不是跟本不給時間作 Graceful-shutdown？再加上 GCP 並不保證收回機器的時間，萬一回收的機器太多，應用還是一樣爆炸。

有個解法：我們在 24 hr 前到之前，先自盡 XD

這個自盡，由於是我們自行驅動的，可以依照我們自行設計的步驟，完整且安全的終止。

再說一次
- GCP 觸發 Preemptible process
  - 可以視作 involuntary disruptions，GCP 突然要把機器關掉，基本上跟機器突然斷線差不多
  - GCP 並不能明確保證收回機器的時間
  - GCP 並不保證收回的機器的數量，同時回收的機器量大，還是會衝擊到服務
- 我們自行了斷 XD，提早關掉跑了比較久的機器
  - 可以按照我們的排程，在固定的時間、汰換固定數量的機器
  - 手動汰換的機器，會刷新先占虛擬機的壽命 (e.g. 活得比較短的機器，不會被收回去)
  - 視為 Voluntary disruptions，可以提供足夠的時間執行，設定 Graceful-shutdown、Pod disruption budgets

所以我們要作以下幾件事
- 為應用設計可容錯分散式架構，例如應用可以同時執行一樣的 API server 3 個 replica
- 分散 Pod 到合適的機器上，例如設置 PodAntiAffinity
- 使用這個有趣的工具 [estafette-gke-preemptible-killer](https://github.com/estafette/estafette-gke-preemptible-killer)，自動汰換先占虛擬機
- 規劃應用的 Graceful-shutdown 流程，從 SIGTERM 開始、到應用收到信號、graceful-shutdown、Pod Terminatation、一路到新的 Pod 產生在新的節點上

estafette-gke-preemptible-killer 非常好玩，使用上簡單，大家自己看著辦 XD。如果大家有興趣，留言的人多的話，我再另外開一篇細講。

---

Day 1 - 需不需要 Kubernetes，這是個好問題XD，從需求量化分析，根據數據做科學決策

Day 2 - Borg Omega and Kubernete，Kubernetes 的前日今生，與 Google 十餘年的容器化技術
Day 3 - Borg Omega and Kubernete， Google 十餘年的容器化技術，應用導向的架構 (Application-oriented infrastructure)
Day 4 - Borg Omega and Kubernete， 容器作為管理單位 (Container as the unit of management)
Day 5 - Borg Omega and Kubernete，協調管理只是開始，而不是終點 (Orchestration is the beginning, not the end)
Day 6 - Borg Omega and Kubernete，前車之鑑 (Things to avoid)
Day 7 - Borg Omega and Kubernete，其他困難的開放問題

Day 8 - 公有雲省錢大作戰 - 我這邊有一批便宜的好 VM 打三折賣你，先占節點實戰分享
Day 9 - 先占節點實戰分享，技術規格簡介，是能有有多便宜
Day 10 - 先占節點實戰分享，需求分析上篇
Day 11 - 先占節點實戰分享，需求分析下篇，在 kubernetes 上跑資料庫，或是分散式資料庫
Day 12 - 先占節點實戰分享，配合 Kubernetes 自動化調度，使用先占虛擬機上篇
Day 13 - 先占節點實戰分享，配合 Kubernetes 自動化調度，使用先占虛擬機下篇
Day 14 - 先占節點實戰分享，所以我機器要開多大台，需求費用試算

Day 15 - 先占節點實戰分享，先占虛擬機如何殺死你的 Pod
Day 16 - 先占節點實戰分享，基於成本的重新設計，先占虛擬機的特化架構
Day 17 - 先占節點實戰分享，實戰

  - 先占節點，可以省多少
  - 先占節點，適用案例實戰分析
  - 先占節點，使用範例
  - 先占節點，經驗分享，雷點
  - [Configure Out of Resource](https://kubernetes.io/docs/tasks/administer-cluster/out-of-resource/#evictio)

  - 怪招分享，不想付 0.1 GKE 費用的自動化先占虛擬機，一天收你 3 元台幣
- 大家都來用 Terraform，Infrastructure as Code 演講全文分享
  - iThome Cloud Summit 講到時間超過，一對東西沒講，所以來這邊發文
  - 真的好用，實戰經驗分享
  - 解答粉專私訊問題與觀眾發問
- elasticsearch HA
  - cluster
    - role
  - cross-cluster replication
  - shard rebalancing
- 應該跑 DB 在 k8s 上嗎？
  https://cloud.google.com/blog/products/databases/to-run-or-not-to-run-a-database-on-kubernetes-what-to-consider
- 分散式工具實驗室 - Scalable Database on Kubernetes
  - Cassandra - 支撐百萬級寫入的分散式資料庫
    - Cassandra 簡介
    - Cassandra 細部原理，分散式的資料庫設計超好玩
    - Cassandra 細部原理，Consistency Hashing
    - Cassandra 細部原理，Data modeling
    - Netflix case study - 偷學 Netflix 能學到幾成功力呢
  - Thanos - Scalable HA Prometheus
    - 簡介
    - 需求分析，Unlimited Retention 鐵一般的需求
    - 一步步帶你架
  - Scalable DB 實驗- Cockroach DB - 耐用打不死又高效能的小強資料庫
    - 前言，分散式系統下的困境，資料庫瓶頸
    - Cockroach DB 基本原理簡介
    - Cockroach DB Free Trial 玩起來
- 社群分享
- 總結

---

導入與否的考量

---

應用範例

https://storage.googleapis.com/gweb-cloudblog-publish/images/5.max-2000x2000.png

---

# Stateful workload

### Use external storage

- State、message
- Mounted volume for log or temp file

# 實務上的一些毛點

- GCP 有根據移除的機器作統計，實際被移除的機器

---

---

單節點 container management 便宜用

這個範例其實不太實用，又要長時間執行，又允許離線(有營業時間的客服嗎)

但作為一個範例，希望能讓大家看到先占虛擬機的可用性

---

使用案例

- 批次工作
- 使用外部的 task queue
- 幾乎現代程式語言都已經有

使用案例 - 可容錯的服務 - 無狀態

面對用戶的 API server

要注意應用是不是真的無狀態
- 用戶的 session 如何處理
- 有長連線 (ex. websocket)
- 用戶不會發現的話

使用案例 - 分散式的資料庫

---

elasticsearch

es 設計本身就能分散是容錯，只要滿足以下幾個條件，服務都可以無損切換先占虛擬機

https://www.elastic.co/guide/en/elasticsearch/reference/current/high-availability.html

https://www.elastic.co/guide/en/elasticsearch/reference/current/high-availability-cluster-design.html

elasticsearch
kafka
cassandra

能承受錯誤
跟每天必然出現錯誤

應用可以容錯，但是錯誤發生後應用的行為是什麼？會不會觸發 rebalance 機制，消耗太多 CPU
那我再補一倍算力給你 rebalance XD

SLA 畫出來，統計受影響的服務
如果
畢竟三折的機器還是非常誘人

# 精算成本與服務水準目標 SLO (Service Level Object)

牛頓說：給我一台夠大的機器，我就能撐起全世界 (?

但實務中我們沒有足夠大的機器，所以工程師針對某些特定的需求，想了不同的解決方案。例如分散式架構。整體架構會變得複雜，但是能夠讓服務可以水平擴展、更能承受錯誤等。

例如：目前的服務品質是 99% 的 latency 在 50ms 內完成，希望降低整體 latency，成為 99.9% 落在 50ms

1. 升級成為更大的機器
1. 改架構變成分散式系統

---

cassandra

https://cassandra.apache.org/
