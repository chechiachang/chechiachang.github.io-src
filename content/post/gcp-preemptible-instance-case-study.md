---
title: "Gcp Preemptible Instance Case Study"
subtitle: ""
summary: ""
authors: []
tags: ["kubernetes", "gcp", "preemptible", "spot-instance"]
category: ["kubernetes"]
date: 2020-09-24T15:03:19+08:00
draft: true
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
Day 15 - 先占節點實戰分享，先占虛擬機如何殺死你的 Pod，如何處置上篇
Day 16 - 先占節點實戰分享，先占虛擬機如何殺死你的 Pod，如何處置下篇

Day 17 - 先占節點實戰分享，Case Study

- [Case study Planet Labs, Inc.](https://cloud.google.com/customers/planet)
- [Google Blog Post: Preemptible VMs improved Musiio’s efficiency by 7000%](https://cloud.google.com/blog/products/containers-kubernetes/microservices-on-gke-preemptible-vms-improved-musiios-efficiency-by-7000)
- [Clemson’s 2.1 million VCPU experiment](https://cloud.google.com/blog/topics/hpc/clemson-experiment-uses-2-1-million-vcpus-on-google-cloud)
- [5 best practices for Compute Engine cost optimization](https://cloud.google.com/blog/products/compute/5-best-practices-compute-engine-cost-optimization)
- [Bayer Crop Science seeds the future with 15000-node GKE clusters](https://cloud.google.com/blog/products/containers-kubernetes/google-kubernetes-engine-clusters-can-have-up-to-15000-nodes)

Day 17 - 先占節點實戰分享，基於成本的重新設計，先占虛擬機的特化架構，各種怪招
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
