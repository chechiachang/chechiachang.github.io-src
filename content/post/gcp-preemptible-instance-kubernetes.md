---
title: "Gcp Preemptible Instance Kubernetes"
subtitle: ""
summary: ""
authors: []
tags: ["kubernetes", "gcp", "preemptible", "spot-instance"]
category: ["kubernetes"]
date: 2020-09-22T17:24:20+08:00
featured: true
draft: true
---

### 先占虛擬機與 Kubernetes

在 GCP 使用先占虛擬機，會需要面對先占虛擬機的額外限制

- 資料中心會 (可預期或不可預期地) 終止先占虛擬機
- 先占虛擬機不能自動重啟，而是會被資料中心終止後回收
- GCP 不保證有足夠的先占虛擬機

節點的終止會造成額外的維運成本，例如

- 管理多個節點，容忍先占虛擬機的移除，自動補充新的先占虛擬機
- 管理多個應用複本，節點終止時，維護整體應用的可用性
- 將移除節點上的應用，重新排程到其他可用節點
- 動態維護應用複本的服務發現 (Service Discovery) 與服務端點 (Endpoints)
  - 意思是應用關閉重啟後，換了一個新 IP，還要能持續存取應用。舊的 IP 要主動失效
  - 配合應用的健康檢查 (Health Check) 與可用檢查 (Readiness Check)，再分配網路流量

這些需求，必須要有自動化的管理工具，是不可能人工管理的，想像你手上使用 100 個先占節點，平均每天會有 10% - 15% 的先占節點被資料中心回收，維運需要

- 補足被移除的 15 個節點
- 計算被移除的應用，補足移除的應用數量
- 移除失效的應用端點，補上新的應用端點
- 持續監控應用狀態
- ...

沒有自動化管理工具，看了心已累 (貓爪掩面)

我們使用 Kubernetes 協助維運自動化，在 GCP 上我們使用 GKE，除了上述提到的容器應用管理自動化外，GKE 還額外整合先占虛擬機的使用

- 啟用先占虛擬機的節點池 (node-pool)，設定節點池的自動拓展，自動補足先占節點的數量
- GKE 自動維護先占虛擬機的 labels

關於 GKE 的先占虛擬機的完整細節，請見[GCP 官方文件](https://cloud.google.com/kubernetes-engine/docs/how-to/preemptible-vms)。這份文件底下也提供了 GCP 官方建議的先占虛擬機最佳實踐

- 架構設計需要假設，部分或是全部的先占虛擬機都不可用的情形
- Pod 不一定有時間能優雅終止 (graceful shutdown)
- 同時使用隨選虛擬機與先占虛擬機，以維持先占虛擬機不可用時，服務依然可用
- 注意節點替換時的 IP 變更
- 避免使用有狀態的 Pod 在先占虛擬機上 (這點稍後的文章，我們會試圖超越)
- 使用 node taint 來協助排程到先占虛擬機，與非先占虛擬機

總之，由於有容器自動化管理，我們才能輕易的使用先占虛擬機。

### GKE

然而，決定使用 GKE 後，就有許多關於成本的事情需要討論

先看 [GKE 的計費方式 pricing](https://cloud.google.com/kubernetes-engine/pricing)

- 每個 GKE 集群管理費用 $0.1/hr = $72/hr

這個費用是固定收費，只要開一個集群，不論集群的節點數量。所以在節點多、算力大的集群裡，這個費用會被稀釋，但在節點少的集群裡比例會被放大。

然後 GKE 還是會有一些自己的毛，俗話說有一好沒兩好，我們使用它的好處同時，也要注意許多眉眉角角。再來爬[文件](https://cloud.google.com/kubernetes-engine/docs/concepts/cluster-architecture)。如同最前面宣導，用產品就要乖乖把文件看完，不過這裡先針對與先占虛擬機相關的議題

- [Allocatable Resource](https://cloud.google.com/kubernetes-engine/docs/concepts/cluster-architecture#memory_cpu)
- [Regional Cluster](https://cloud.google.com/kubernetes-engine/docs/concepts/regional-clusters)
- [Cluster autoscaler](https://cloud.google.com/kubernetes-engine/docs/concepts/cluster-autoscaler)

### Allocatable Resource

在網路上看到這篇好文 [GKE 上的可使用的資源 Allocatable Resource](https://learnk8s.io/allocatable-resources)。啥意思呢？難道還有不能使用的資源嗎？

沒錯，GKE 會保留一定的機器資源 (e.g. cpu, memory, disk)，來維持節點的管理元件，例如 container runtime (e.g. Docker)、kubelet、cAdvisor。

也就是說，就算我們跟 GCP 購買了算力，有一個比例的資源我們是使用不到的。細節請見 [理解 GKE 集群架構](https://cloud.google.com/kubernetes-engine/docs/concepts/cluster-architecture#memory_cpu)。這會影響我們單一節點的規格，我們也需要一並計算，能實際使用的資源 (allocatable resource)。

Allocatable = Capacity - Reserved - Eviction Threshold

- Capacity，是機器上實際裝載的資源，例如 n1-standard-4 提供 4 cpu 15 Gb memory
- Reserved，公有雲代管集群，預保留的資源
- [Eviction Threshold](https://kubernetes.io/docs/tasks/administer-cluster/out-of-resource/#eviction-thresholds)：Kubernetes 設定的 kubelet 驅逐門檻

### 驅逐門檻 (Eviction threshold)

Kubelet 會主動監測節點上的資源使用狀況，當節點發生資源不足的狀況時，kubelet 會主動終止某些 Pod 的運行，並回收節點的資源，來避免整個節點資源不足導致的系統不穩定。被終止的 Pod 可以再次排程到其他資源足夠的節點上。細節請見 [官方文件 Scheduling and Eviction](https://kubernetes.io/docs/concepts/scheduling-eviction/eviction-policy/)

在 Kubernetes 上，我們可以進一步設定驅逐門檻，當節點的可用資源低於驅逐的門檻，kubelet 會觸發 Pod 驅逐機制

GKE 上每個節點會額外保留 100 MiB 的記憶體，作為驅逐門檻，意思是當節點耗盡資源，導致剩餘記憶體低於 100 MiB 的時候，會直接觸發 GKE 的 Pod Eviction，終止並回收部分的 Pod。換句話說，這 100 MiB 是不能被使用的資源。細節請見[官方文件](https://cloud.google.com/kubernetes-engine/docs/concepts/cluster-architecture#eviction_threshold)

### 集群保留資源精算

資源的定義，使用雲平台的一般費用大多來自此

- cpu
- memory
- storage

然後是這個表，注意保留的資源是累進級距

255 MiB of memory for machines with less than 1 GB of memory
25% of the first 4GB of memory
20% of the next 4GB of memory (up to 8GB)
10% of the next 8GB of memory (up to 16GB)
6% of the next 112GB of memory (up to 128GB)
2% of any memory above 128GB

值計上能夠用到的資源，底下 GCP 也整理好了，例如 n1-standard-4 實際使用的是 memory 12.3/15，cpu 3.92/4。

在維持合理的使用率下，開啟大的機器，可以降低被保留的資源比例，依照筆者公司過去經驗，GKE 起跳就是 n1-standard-4 或是以上規格，如果低於這個規格，可調度的資源比例真的太低，應該重新考慮一下這個解決方案是否合乎成本。

但究竟什麼規格的機器適合我們的需求，說實在完全要看執行的應用而定。
