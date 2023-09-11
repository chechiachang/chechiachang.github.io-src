---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Borg Omega and Kubernetes TLDR 摘要翻譯"
subtitle: ""
summary: ""
authors: []
tags: ["kubernetes", "google", "borg"]
category: ["kubernetes"]
date: 2020-08-26T13:50:52+08:00
lastmod: 2020-08-26T13:50:52+08:00
featured: false
draft: false

---

這是原文翻譯的太長不讀 (TL;DR) 版本。完整翻譯請見[Borg Omega and Kubernetes 前世今生浩文完整翻譯]({{< ref "/post/2020-09-12-borg-omega-and-kubernetes" >}})

原文：https://storage.googleapis.com/pub-tools-public-publication-data/pdf/44843.pdf

# 前言

- Borg 以前就有應用管理系統，那時還沒有 Linux control group
- Borg 
  - 是第一套統一的 container-management system
  - Borg 仍被大規模的使用，有許多功能而且非常堅固
- Omega
  - 繼承 Borg 上成功的設計，並希望改進 Borg 的生態系
- Kubernetes
  - 開源
  - 透過 REST API 溝通 client
  - 應用開發導向，著重於開發者的需求，希望能簡單的部署複雜的系統

# Container

- Google 使用 Container 來提昇 utilization
  - 把 batch jobs 跟預留資源的服務 (user-facing app) 放在一起，使用閒置時的資源跑 batch job
- 現代 container 的定義是 runtime-isolation 與 image

# Application-oriented infrastructure

- container 使用久了，不只滿足 utilization 的需求
  - 資料中心從機器導向變成應用導向
- Container 封裝環境，把機器與 OS 的依賴抽象化
  - 應用不依賴
    - 部署流程
    - runtime infrastrcture 
- Container scope 在應用上，專注在應用管理而不是機器管理

# Application environment

- cgroup, chroot, namespace 原本的目的是為了保護應用，不被其他應用影響
  - 混合使用可以在應用與 OS 間產生抽象層，解耦 app 與 OS
    - 提供完全相同的部署環境，避免切換環境(ex. dev, prod)時造成環境差異
  - 進一步把 app 的依賴程式也打包 image
    - container 對 OS 唯一的依賴只剩 Linux kernel system-call interface
      - 大幅增加 app 調度的彈性
  - 然而有些 interface 仍附著 OS 上，ex socket, /prod, ioctl calls
    - 希望透過 Open Container Initiative，清楚定義 interface 與抽象
- 直接的好處，少數幾種 OS 與 OS Version 就可以跑所有應用，新版本也不影響

# Container as the unit of management

- 資料中心的重心，從管理機器變成管理應用
  - 提供彈性給 infrastructure team
    - 提供統一的架構
    - 收集統一的 metrics
- Container 統一的介面，讓 management system (ex. k8s) 可以提供 generic APIs
  - REST API, HTTP, /healthz, exec...
  - 統一的 health check 介面，更方便的終止與重啟
  - 一致性
    - 容器提供統一的資訊，ex. status, text message, ...
    - 管理平台提供統一設定 (ex. resource limits) ，並進行 logging 與 monitoring
      - 提供更精細的功能 ex. graceful-termination
- cgroups 提供 app 的資源使用資訊，而不需要知道 app spec，因為 contaier 本身即是 app
  - 提供更簡單，卻更精細且堅固的 logging 與 monitoring
- 應用導向的 monitoring ，而不是機器導向的 monitoring
  - 可以收集跨 OS 的 app 狀態，進行整合分析，而不會有 OS 不同造成的雜訊
  - 更容易對應用除錯
- nested contaiers
  - resource allocation (aka. alloc in Borg, Pod in Kubernetes)

# Orchestration is the beginning, not the end

- 原本 Borg 只是要把 workload 分配到共用的機器上，來改善 utilization
  - 結果發現可以做更多事情，來幫助開發與部署
    - Naming, service discovery
    - Application-aware load balancing
    - Rollout tool
    - Workflow tool
    - Monitoring tool
  - 成功的工具被留下
    - 然而工具都需要各自的 API，副作用是增加部署的複雜度到 Borg 的生態系
- Kubernetese 試圖降低複雜度
  - 提供一致的 API
    - ex. ObjectMetadata, Specification, Status
    - Object metadata 是全域共通的
    - Spec 與 Status 根據 Object 有所不同，但是概念是一致的
      - Spec 描述 desired state of object
      - Status 提供 read-only 的 current state of object
- Uniform API 有許多好處
  - 降低學習成本
  - 可以使用 generic 的工具讓所有 workflow 使用
  - 統一使用者的開發流程與開發經驗
  - Kubernetes 本身模組化，可以使用延伸模組
    - ex. pod API 讓使用者使用，kubernetes 內部使用，外部自動化工具也使用
    - 使用者可以自己增加 customized API
- 如何達到 Uniform API
  - decoupling API
    - 切分 API 關注的面向，變成不同 components API. ex.
      - replication controller 確保 desired 數量的 Pod 存在
      - autoscaler 關注在需求與使用的預測，然後控制 replication controller API
    - higher-level 服務都共用相同的 basic API
    - 切分 API 而外的好處
      - 有關聯但是用途不同的 API 的內容與使用方式十分相似. ex.
        - ReplicationController: 控制長時間運行的 containers 與其複本
        - DeamonSet: 每個機器上都跑一個 container
        - Job: 一次性執行完畢的 container
  - Common design patterns
    - ex. reconciliation controller loop 在 Borg, Omega, Kubernetes 中大量使用
      - 需求(desired state)
      - 觀察現況(current state)
      - 執行動作，收斂需求與現況(reconcile)
      - loop
    - 由於狀態是基於實際觀測產生，reconciliation loop 非常堅固，可以承受相當的 failure
- Kubernetes 設計為一連串的為服務系統，以及許多小型的 control loop
  - 對比大型的 centralized orchestration system

# Things to avoid

Google 開發過程中，也發現許多不該做的事情

- 不要使用 conainer system 來管理 port numbers
  - Borg 會指定 unique port number 給每個 container
    - 必須用其他方法取代 DNS
    - port 也不易嵌入 URL 中，要另外處理轉址
    - 需要而外的系統處理 ip:port
  - Kubernetes 選擇指派 IP 給 Pod
    - 可以直接使用常用 port (ex. 80,443)
    - 可以使用內部 DNS，使用一般常用的工具
    - 大部分公有雲都提供 networking underlays，達成 Ip-per-pod
    - 可以使用 DNS overlay 或是 L3 routing，來控制一台機器上的多個 IPs
- 不要幫 container 編號，使用 label 來管理大量的 container
  - Borg 會幫 job 從 0 開始編號
    - 很直覺很直接，但稍後就後悔了
      - 如果 job 死了，重啟新的 job 在機器上後，還需要去找上個死掉的 job
      - task 中間會有很多洞 (死掉的 job)
      - 更新版本，要更新 jobs 時會依序重啟 jobs
      - 資料如果也是根據 index 做 sharding，重啟時要復原 index，不然會有資料遺失
  - Kubernetes 使用 label
    - 可以透過 label 管理一組 container
    - 一個 container 可使用多個 labels，更方便的調度
    - 需要的資訊打在 label 上 (ex. role assignments, work-partitioning, sharding...)，更容易管理
- 注意所有權
  - Borg 上，tasks 都綁定在 job 上，產生 job 也產生 tasks
    - 很直覺方便
    - 只剩下一種 group 控制機制
  - Kubernetes 的 pod-lifecycle management (ex. replication controller) 使用 label selector 來控制 pod
    - 可以彈性控制大量 pod
    - 可能有多個上層 controller 控制同一個 pod，要盡量避免這種情況
    - 好處是保留彈性的同時，可以很清楚界定管理的 pod，不會有 orphan / adapt pod
    - 透過 label 進行 service load balance
      - 如果 pod 有問題，可以變更 label，讓流量不要進來，但又保留 Pod debug
- 不要暴露 raw state
  - Borgmaster 是 monolithic，可見所有的 API Operation
  - Omega 不是 centralized，只保留被動的資訊，使用 optimistic concurrent control
    - state 存到 client store，並基於 state 進行 operation
    - 所有 client 需要使用一樣的 client store library
  - Kubernetes 走中間
    - 所有 state 存取需要透過 centralized API server
    - client components 可以獨立運作

# Some open, hard problems

- configuration
- dependency management
