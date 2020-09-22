---
title: "Gcp Preemptible Instance Requirement Distributed"
subtitle: ""
summary: ""
authors: []
tags: ["kubernetes", "gcp", "preemptible", "spot-instance"]
category: ["kubernetes"]
date: 2020-09-22T14:39:00+08:00
featured: true
draft: true
---

我們以下幾個需求：

- 執行短期的 batch job
- 執行長期的 user-facing API server
- 執行長期的 stateful 資料庫、儲存庫

該不該在 Kubernetes 上面跑 database？

TL;DR ，如果你剛開始考慮這件事，通常的答案都是否定的

等等，我們這邊不是討論該不該上 Kuberentes ，而是該不該使用先占虛擬機吧。然而由於先占虛擬機節點的諸多限制，光憑先占虛擬機並不適合跑任何持久性的儲存庫。我們這邊仰賴 Kubernetes 的網路功能 (e.g. 服務發現)，與自動管理 (e.g. health check，HPA，auto-scaler)，基於先占虛擬機，建構高可用性的服務架構，來支撐高可用，且有狀態的的儲存庫。

應用是否適合部署到 Kubernetes 上，可以看這篇 [Google Blog: To run or not to run a database on Kubernetes: What to consider](https://cloud.google.com/blog/products/databases/to-run-or-not-to-run-a-database-on-kubernetes-what-to-consider)，如果大家有興趣，再留言告訴我，我再進行中文翻譯。

文中針對三個可能的方案做分析，以 MySQL 為例：

- Sass，GCP 的 Cloud SQL
  - 最低的管理維運成本
- 自架 MySQL 在 GCP 的 VM 上，自行管理
  - 自負完全的管理責任，包含可用性，備份 (backup)，以及容錯移轉 (failover)
- 自架 MySQL 在 Kubernetes 上
  - 自負完全的管理責任
  - Kubernetes 的複雜抽象層，會加重維運工作的複雜程度

然而 RDBMS 的提供商，自家也提供 Operator

- [Oracle 自家提供的 MySQL Operator](https://github.com/oracle/mysql-operator)
- [CrunchyData 也有提供的 Postgres Operator](https://github.com/CrunchyData/postgres-operator)

你就想，所以這些人是想怎樣，RDBMS 放 Kubernetes 上到底是行不行 XD。Google 的文章說明：如果應用本身並不符合 Kubernetes 的工作流程 (Pod life-cycle)，可以透過上述的 Operator 來自動化許多維運的作業，降低維運的困難。

然而 DB 有千百種，除了 RDBMS 以外，還有另外一批 Database 天生就具有分散式的架構，這些儲存庫部署到 Kubernetes 上，並不會太痛苦 (還是要付出一定的成本XD)，但是卻可以得益於 Kubernetes 的諸多功能。

底下我們先根據分散式的儲存庫做概觀描述，本系列文的最後，會根據時間狀況，做實例分享：Cassandra 或是 CockroachDB。提供各位一點發想，並根據需求去選擇需要的儲存庫

「行不行要問你自己了施主，技術上都可以，維運上要看看你的團隊有沒有那個屁股吃這份藥 XD」

### Distributed Database

底下非常粗淺的簡介分散式儲存庫的概念，提供一個基準點，幫助接下來討論是否可以使用先占虛擬機。這邊要強調，儲存庫的類型千百種，底層的各種實作差異都非常大，底下的模型是基於 cassandra 但不會走太多細節。 cassandra 的規格有機會再細聊。

當後端應用已經順利水平拓展之後，整體服務的效能瓶頸往往都壓在後端 DB 上。這些不同的 DB 面向不同的需求，當需求符合時，可以考慮使用這些解決方法。

這邊要強調，不是放棄現有的 RDBMS ，完全移轉到新的資料庫，這樣的成本太高，也沒有必要性。更好的做法，是搭配既有的關聯性資料庫，將不是核心業務的資料處理抽出，移轉到合適的資料庫上。讓不同需求的資料儲存到更合適的儲存庫，是這段話要強調的重點，關連式資料庫也不是唯一選擇。

分散式的資料庫有以下特徵

- 分散式節點集群 (Cluster)：資料庫是多個節點共存，而非 single master, multiple slaves 的架構
  - 配合共識算法 (consensus algorithm) 溝通節點之間的資訊
- 無單點錯誤 (Single-point failure)：e.g. 不會因為 master 錯誤導致整個服務失效
- 高可用(High Availitility：可以承受集群中一定數量虛擬機故障，服務仍然可用
- 資料 sharding 到不同節點上
- 複本 (replica)
  - 節點複本 (node replicas)：多個節點提供服務，提供流量的帶寬與可用性
  - 資料複本 (data replicas)：在多個節點上儲存資料，提供資料的備份，同時也提供讀取帶寬與可用性

從以上特徵來說，使用此架構的服務可以承受先占虛擬機的不定時終止，或許可以使用。

實務上有非常多需要注意，需要依據各自服務的性質，各自處理。常見的問題舉例如下：

- 應用可以容錯 (fault-tolerent)，然而錯誤發生後，會需要消耗復原成本，例如重啟後需要花時間初始化，或是在多節點上進行 data rebalance。
- 可以承受突然的錯誤，使用先占虛擬機，變成每日固定會承受必然的錯誤。這裡犧牲了部分算力，甚至造成隱性的維護成本，最後是否符合節省成本的需求。

都是需要仔細了解解決方案，並且分析需求，來評估是否有合乎成本。

# GKE

以上分析了三種常見需求例子：從 batch job，user-facing service，與 distributed database。明天會實際搬出 GKE 與 GCP Preemptible Instance 的技術規格，與大家實際討論。
