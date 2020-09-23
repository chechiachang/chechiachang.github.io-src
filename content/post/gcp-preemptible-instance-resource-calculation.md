---
title: "Gcp Preemptible Instance Resource Calculation"
date: 2020-09-23T12:22:02+08:00
draft: true
---

### 資源需求估估看

如果應用開發團隊，有先作應用的 profiling，然後 release candidate 版本有在 staging 上作壓力測試的話，維運團隊這邊應該可以取得幾個數據

- 啟動應用所需的資源
- 沒有大量請求，只維持基本應用運行所施的資源
- 負載壓力灌進來時，應用資源的成長曲線

如果沒有這些數據，其實維運很難事前估計資源，變成要實際推上線後見招拆招，其實很不妥，因此我建議如果開發團隊沒有作 profiling，維運團隊可以在工作流程內簡單加一步 profiling，目前主流語言都有提供相關工具，有做跟沒做差非常多。

至於壓力測試，也是可以使用基本的工具(例如 [Artilery](https://artillery.io/))簡單整到工作流程。特別是面對客戶的應用，務必要進行壓力測試。

有了上述的資源需求數據，才能事先安排機器的規格。例如

- 應用是面對客戶的 API server
- 基本資源是 200m cpu 1Gi memory，這部分直接寫進 Kubernetes resource request，在排程時就先結點上預留。
- 負載拉到 1,000 RPS，latency 95% 20ms  99% 30ms，這時的資源需求的上界大約 2 cpu 4 Gi memory
- 超過 1,000 RPS 就應該要透過水平擴展去增加更多 instamce

如果單跑這個 API server，就可以安排 memory 8，cpu 4 的 GKE node-pool，讓負載落在可用資源的 60%-70%，這樣還有餘裕可以承受大流量，給自動水平擴展做動的時間。

### 資源調整參考

當然這些數據都可以依照時實際需求調整，資源要壓縮得更緊或更鬆都是可行的。

如果應用有整合分析後台，例如 Real-time Uer Monitoring、或是基本的 Google Analytics，都可以觀察這些調整實際對用戶帶來的影響，用戶行為改變對公司營收的影響，全都可以量化。例如

- 機器負載拉到 80%，cpu 的壓力，導致 API latency 增加到 95% 50ms 99% 100ms
- 此時用戶已經很有感了，會導致 0.1% 用戶跳轉離開
- 而這 0.1% 的用戶，以往的平均消費，換算成為公司營收，是 $1,000/month
- 把機器負載壓到 60%，只計算 cpu 的數量的話，需要多開 3 台 n1-standard-4 機器，共計 $337.26/month
- 提供老闆做參考，老闆可能會趨向加開機器

當然上面的例子都非常簡化，變成國中數學問題，這邊只是提供一個估算的例子。現實中的問題都會複雜百倍，例如機器規格拉上去出現新的瓶頸、例如依賴的服務，message queue、database 壓力上升，或是公司內部問題，就拿不到預算(血淚 SRE)。如果要減少機器，也可以參考，一般來說聽到關機器省錢的話，老闆都會接受的 XD。

### 回到先占機器

根據上面的國中數學，把應用一個一個都計算清楚，需求逐漸明確了。假設，架構團隊拿到開機器的工單，掐指一算，決定

- 1 GKE cluster
- 6 n1-standard-4

這些都是隨選虛擬機，價格大約是 $747/month (含集群管理費 $73/month)

今天有人腦動大開，那如果全部換成先占節點呢？變成 $265/month，虛擬機費用 $192 / $674 = 0.28 直接打超過三折。

有人就擔心，這樣真的可以嗎？真的沒問題嗎？會不會影響用戶阿。

答案是會，就是會影響用戶 XD。聽到這邊很多人就怕了。

但是怎麼個影響法呢，還需要看底下幾個段落，如果換成先占虛擬機，用戶會怎麼受到影響。

我們也要試圖量化這個影響，當作要不要導入的判斷依據。

句個反例，「我覺得可以」「你覺得不行」，或是「某某公司的某某團隊可以啊」「我們公司也來做吧」，這些都是很糟糕的理由。除了對內部毫無說服力之外，也沒有辦法作為導入成效的指標，會讓團隊陷入「導入了也不知道有比導入前好？」或是「具體導入後成效量化」，會影響團隊做出真正有效的判斷，應極力避免。

此外，問行不行之前，其實需要知道團隊願意為了三折機器，付出多少成本。如果只是每月省個台幣 15,000，工程師薪水都超過了。但如果手下有三十台或三百台以上，也許就非常值得投資。

成本不是絕對的，很多時候要與其他成本 (e.g. 開發人力時間成本) 一起考量。

以上都是說明導入的動機，以下說明先占虛擬機的各種機制，以及對應用的實際影響。

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

# 終止流程 (Preemption process)

未知生焉知死
做工程師要反過來，考量最差情形，也就是不知道應用可能怎麼死，別說你知道應用活得好好的。

如同上面所說的，先占虛擬機會被公有雲收回，但收回的時候不會突然機器就不見，會有一個固定的流程

如果你的應用很強壯，能夠承受機器突然變不見，服務還好好的，仍然要花時間理解這邊的流程，藉此精算每天虛擬機的終止與替換，應用會有什麼反應，會產生多少衝擊 (e.g. 應用初始化時 cpu memory 突然拉高)，這邊可以量化服務的影響。

如果你的應用需要有 graceful shutdown 的機制，那你務必要細心理解這邊的步驟。並仔細安排安全下庄的步驟。

這邊有幾個面向要注意

1. GCP 如何終止先占節點
2. GCP 移除節點對 GKE 、以及執行中應用的影響
3. GKE 集群如何應對的節點失效
4. GCP 自動調度補足新的先占節點
5. GKE 集群如何應對節點補足

隨手列一列又突然多了好幾篇 orz

### GCP 如何終止先占節點

一樣先看[先占虛擬機的說明文件：終止流程](https://cloud.google.com/compute/docs/instances/preemptible?hl=zh-tw#preemption-process)

# Preemption selection

GCP 不會把所你手上的 preemptible 機器都收走，而是依照比例選擇要被撤換的機器。

### GKE 如何處理移除節點

https://kubernetes.io/zh/docs/concepts/workloads/pods/disruptions/

https://dev.to/duske/how-kubernetes-handles-offline-nodes-53b5

### 對應用的影響

https://cloud.google.com/solutions/scope-and-size-kubernetes-engine-clusters

結論

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
