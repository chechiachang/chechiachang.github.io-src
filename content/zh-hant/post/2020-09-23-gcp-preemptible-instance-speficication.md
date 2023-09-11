---
title: "Gcp Preemptible Instance Speficication"
subtitle: ""
summary: ""
authors: []
tags: ["kubernetes", "gcp", "preemptible", "spot-instance", "鐵人賽2020"]
category: ["gcp", "kubernetes"]
date: 2020-09-23T16:23:14+08:00
draft: false
---

# 先占虛擬機終止流程 (Preemption process)

子曰：未知生焉知死。但做工程師要反過來，考量最差情形，也就是要知道應用可能如何死去。不知道應用可能怎麼死，別說你知道應用活得好好的，大概想表達這麼意思。

這對先占虛擬機來說特別重要，一般應用面對的機器故障或是機器終止，在使用先占西你幾的狀況下，變成每日的必然，因此，需要對應用的終止情境，與終止流程有更精細的掌控。如同前幾篇所說的，先占虛擬機會被公有雲收回，但收回的時候不會突然機器就 ben 不見，會有一個固定的流程。

如果你的應用已經帶有可容錯的機制，能夠承受機器突然變不見，服務還好好的，仍然要花時間理解這邊的流程，藉此精算每天虛擬機的終止與替換：應用會有什麼反應，會產生多少衝擊，稍後可以量化服務的影響。例如

 - 應用重啟初始化時 cpu memory 突然拉高
 - 承受節點錯誤後的復原流程，需要消耗額外算力。例如需要從上個 checkpoint 接續做，需要去讀取資料造成 IO，或是資料需要做 rebalance ...等等

如果你的應用需要有 graceful shutdown 的機制，那你務必要細心理解這邊的步驟。並仔細安排安全下樁的步驟。又或是無法保證在先占虛擬機回收的作業時限內，完成優雅終止，需要考慮其他可能的實作解法。

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


### GCP 如何終止虛擬機

先占虛擬機的硬體終止步驟與一般隨選虛擬機相同，所以我們要先理解[虛擬機的停止流程](https://cloud.google.com/compute/docs/instances/stop-start-instance)

這裡指的終止 (Stop) 是[虛擬機生命週期](https://cloud.google.com/compute/docs/instances/instance-life-cycle) 的 RUNNING -> instances.stop() -> STOPPING -> TERMINATED 的步驟。

- instances.stop()
- ACPI shutdown
- OS 會進行 shutdown 流程，並嘗試執行各個服務的終止流程，以安全的終止服務。如果虛擬機有設定[Shtudown Script](https://cloud.google.com/compute/docs/shutdownscript) 會在這步驟處理
- [等待至少 90 秒](https://cloud.google.com/compute/docs/instances/deleting-instance)，讓 OS 完成終止的流程
  - 逾時的終止流程，GCP 會直接強制終止，就算 shutdown script 還沒跑完
  - GCP 不保證終止時限的時間，官方建議不要寫重要的依賴腳本在終止時限內
- 虛擬機變成 TERMINATED 狀態

### GCP 如何終止先占虛擬機

與隨選虛擬機不同
- 先占虛擬機的時間 30 秒
- 搭配 GKE 使用 Managed Instance Group，終止的虛擬機會被刪除，Autoscaler 會啟動新的虛擬機 

一樣先看[先占虛擬機的說明文件：終止流程](https://cloud.google.com/compute/docs/instances/preemptible?hl=zh-tw#preemption-process)

- 資料中心開始回收先占虛擬機，選中我們專案其中的一台先占虛擬機
- Compute Engine 傳送 ACPI G2 Soft Off，這裡 OS 會試圖安全關變服務，也會執行 [shutdown script](https://cloud.google.com/compute/docs/instances/create-start-preemptible-instance?hl=zh-tw#handle_preemption)，可以做簡短的優雅終止
- 30秒後，ACPI G3 Mechanical off

但 30 秒能做什麼？只能快速的交代當前進度。如果應用需要花時間收尾，保存工作進度，可能會產生許多問題

- GCP 不保證終止時限的時間，官方建議不要寫重要的依賴腳本在終止時限內
- 在面對大量 IO 的工作，可能會導致者台虛擬機的大量應用一起進入優雅終止，先占虛擬機最後耗盡資源，來不及做完
- 如果可能會超時，或是沒完成會有資料遺失風險，就不能在這個階段處理


依賴 shutdown script 做收尾是危險的，我們之後要想辦法處理這個不保證做完的優雅終止。

如果應用本身有容錯的框架，或是有容錯機制，我們這邊要額外做的工作就會少很多。例如許多程式框架提供自動重啟的功能，在外部保存 checkpoint，worker 只負責運算，終止信號一進來，也不用保存，直接拋棄未完成的工作進度，留待繼起的 worker 從 checkpoint 接手。

### Preemption selection

除了 24 小時的壽命限制會終止虛擬機，資料中心的事件也會觸發主動的虛擬機回收，[由 GCP 主動觸發的回收機制機率很低](https://cloud.google.com/compute/docs/instances/preemptible?hl=zh-tw#limitations)，會根據每日每個區域 (zone) 的狀態而定。這裡描述資料中心啟動的臨時回收。

GCP 不會把所你手上的 preemptible 機器都收走，而是依照[一定的規則](https://cloud.google.com/compute/docs/instances/preemptible?hl=zh-tw#preemption-process)，選擇一個比例撤換的機器。

先看文件敘述

- Compute Engine 會避免從單一客戶移除太多先占虛擬機 
- 優先移除新的虛擬機，偏向保留舊的虛擬機 (但最多仍活不過 24hr)
- 開啟後馬上被移除的先占虛擬機不計費
- 機器尺寸較小的機器，可用性較高。例如：16 cpu 的先占虛擬機，比 128 cpu 的先占虛擬機容易取得

GCP 每天平均會移除一個專案中 5% - 15% 的虛擬機，從用戶的角度我們需要預期至少這個程度的回收。不過這個比例，GCP 也不給予任何保證。以筆者經驗，只能說絕大部分的時候，都不會擔心超過這個比例的回收，但是還是要做好最壞的打算，如果臨時無法取得足夠的先占虛擬機，要有方法暫時補足隨選虛擬機。

### GKE

[使用先占虛擬機會違反 Kubernetes 的設計](https://cloud.google.com/kubernetes-engine/docs/how-to/preemptible-vms#kubernetes_constraint_violations)

- Pod grace period 會被忽略
- [Pod disreuption budget](https://kubernetes.io/zh/docs/concepts/workloads/pods/disruptions/)，不會被遵守 (可能會超過)

### 對應用的影響

GCP 觸發的 Preemptible process，對應用的影響

- involuntary disruptions，GCP 送 ACPI G2 Soft Off 
- OS 終止服務，包含執行 Kubernetes 的 container runtime
- 容器內的應用會收到 SIGTERM，啟動 graceful shutdown
  - Kubernetes 提供的 Graceful-shutdown 可能會跑不完
  - 實務上只是中斷當前工作


https://cloud.google.com/solutions/scope-and-size-kubernetes-engine-clusters

### 大量節點同時回收

由於 GCP 並不保證收回的機器的數量，同時回收的機器量大，還是會衝擊到服務。例如：一次收回 15% 的算力，當然服務還是會受到衝擊。當然這樣事件的機率並不高，但我們仍是需要為此打算。這邊有幾個做法

- 預留更多的算力
- 使用 regional cluster，在多個 zone 上分配先占虛擬機
- 我們自行控制，提前主動回收虛擬機

### 預留更多資源

這點很直觀，由於使用了更加便宜的機器，我們可以用同樣的成本，開更多的機器。

退一步說，使用打三折的先占虛擬機，然後開原本兩倍的機器數量

- 總成本是 0.3 * 2 = 0.6 倍
- 同時間可用資源是 2 倍

由於先占節點回收的單位是一個一個虛擬機

- 安排合適的機器尺寸
- 尺寸較小的先占虛擬機，可用性較高。意思是零碎的先占虛擬機容易取得

但當然也不能都開太小的機器，這會嚴重影響應用的分配。至於具體需要開多大，可以根據預計在機器上運行的應用，做綜合考量，例如有以下影用需要執行：

- app A: 1 cpu 5 replica
- app B: 3 cpu 5 replica
- app C: 5 cpu 5 replica

總共至少 45 cpu ，預期機器負載8 成的話，需要總共 45 / 0.8 = 56 cpu。也許可以考慮

- 8 cpu * 7 先占虛擬機
- 4 cpu * 14

也舉幾個極端不可行的例子

- 56 cpu * 1
  - 這樣的虛擬機回收時的影響範圍 (blast radius) 就是 100% 服務
- 1 cpu * 56
  - 機器太瑣碎，可能超出 Qouta (節點數量，IP 數量...)
  - 應用會更分散，節點間的內部網路流量會增加
  - 前幾篇提到的 reserved resource 比例高，會影響應用的部署

如果希望更保險，可以再補上隨選虛擬機混合搭配，例如

- 8 cpu * 7 
  - 5 先占虛擬機 2 隨選虛擬機
- 4 cpu * 14
  - 10 先占虛擬機 4 隨選虛擬機

### 虛擬機區域

虛擬機的回收觸發，也是會依據服務的區域 (zone) 回收。意思是節點回收不會同時觸發 asia-east1 中所有 zone 的節點回收，一般來說時間是錯開的 (不過GCP 也不保證這點 XD)。為了維持 GKE 的可用性，我們都會開多個 node-pool 在多個區域下。

總之避免把機器都放在同個區域中。

### 自行控制的虛擬機汰換

簡單來說我們在 24 hr 期限之前，先分批自盡 XD，打散個各個虛擬機的 24 小時限制。

使用這個有趣的工具 [estafette-gke-preemptible-killer](https://github.com/estafette/estafette-gke-preemptible-killer)，自動汰換先占虛擬機，讓整個繼起虛擬機都分散在 24 小時間。

estafette-gke-preemptible-killer ，使用上簡單，大家自己看著辦 XD。如果大家有興趣，留言的人多的話，我再另外開一篇細講。

### 小結

為了使用先占虛擬機，我們要多做以下幾件事

- 為應用設計可容錯分散式架構，例如應用可以同時執行一樣的 API server 3 個 replica
- 分散 Pod 到合適的機器上，例如設置 PodAntiAffinity
- 設定合適的虛擬機大小，合適的分散應用
- 使用 [estafette-gke-preemptible-killer](https://github.com/estafette/estafette-gke-preemptible-killer)，自動汰換先占虛擬機
- 不依賴應用的 Graceful-shutdown 流程
