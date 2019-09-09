+++
title = "2020 Ithome Ironman Challenge"
subtitle = ""

# Add a summary to display on homepage (optional).
summary = ""

date = 2019-09-09T16:56:03+08:00
draft = false

# Authors. Comma separated list, e.g. `["Bob Smith", "David Jones"]`.
authors = []

# Is this a featured post? (true/false)
featured = true

# Tags and categories
# For example, use `tags = []` for no tags, or the form `tags = ["A Tag", "Another Tag"]` for one or more tags.
tags = []
categories = []

# Projects (optional).
#   Associate this post with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects = ["deep-learning"]` references 
#   `content/project/deep-learning/index.md`.
#   Otherwise, set `projects = []`.
# projects = ["internal-project"]

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder. 
[image]
  # Caption (optional)
  caption = ""

  # Focal point (optional)
  # Options: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight
  focal_point = ""
+++

受有[友人](https://ithelp.ithome.com.tw/2020ironman/signup/team/63)邀請（推坑）參加了[2020 It邦幫忙鐵人賽](https://ithelp.ithome.com.tw/2020ironman)，挑戰在30天內，每天發一篇技術分享文章。一方面將工作上遇到的問題與解法分享給社群，另一方面也是給自己一點成長的壓力，把這段時間的心得沈澱下來，因此也了這系列文章。

本系列文章重點有三：
1. 提供的解決方案，附上一步步的操作步驟
2. 著重 Google Cloud Platform，特別是Google Compute Engine (GCE) 與Google Kubernetes Engine (GKE) 兩大服務
3. 從維運的角度除錯，分析問題，提升穩定性

預定的主題如下（可能會依照實際撰寫狀況微調）

- ELK Stask on GCP (8)
  - GCE 上自架 ELK Stask
  - ELK Stask 的安全性連線(TLS/HTTP2) 設定
  - 監測 Google Compute Engine 上服務的各項數據
  - 監測 Google Kubernetes Engine 的各項數據
  - 使用 logstash pipeline 做數據前處理
  - Elasticsearch 日常維護：數據清理，效能調校，永久儲存
  - 於 GKE 上為 ELK stack 除錯
  - 我們為何不使用 Elastic Cloud Sass 方案
- GKE 維運心得 (5)
  - 我的 Kubernetes 除錯流程
  - Kubectl cheat sheet
  - 使用 cert-manager 維護 TLS/HTTPS
  - 使用 redhat operator-sdk 初探 CRD 與 operator
    - 我的 operator 範例分享
- 在 GKE 上部署 Kafka HA (4)
  - 使用 helm 部署 kafka-ha
  - 集群內部的 HA 設定，網路設定
  - 應用端的基本範例，效能調校
  - 在 GKE 上維運 kafka
- 在 GKE 上部署 Redis HA (4)
  - 使用 helm 部署 redis-ha
  - 集群內部的 HA 設定，網路設定
  - 應用端的基本範例，效能調校
  - 在 GKE 上維運 redis
- Prometheus / Grafana (5)
  - GKE 上自架 Prometheus / Grafana
  - 使用 exporter 監測 GKE 上的各項服務
  - 輸出 kubernetes 的監測數據
  - 輸出 redis-ha 的監測數據
  - 輸出 kafka 的監測數據
- GCP 網路設定 (3)
  - 防火牆的私有網路基本設定
  - 配合 GKE 實現負載均衡
  - DNS 基本觀念，從 kube-dns 到 GCP DNS service
- GCP 日誌管理 (2)
  - 基本 GCP 日誌管理與錯誤回報
  - Stackdriver 服務的日誌管理，監測數據，告警

文章發表於

---

Features
- step-by-step guide for deployment: guarentee a running deployment on GCP
- basic configuration, usage, monitoring, networking on GKE
- debugging, stability analysis in an aspect of devop

Topics
- ELK stack(8)
  - Deploy self-hosted ELK stack on GCE instance
  - Secure ELK stack with SSL and role-based authentication
  - Monitoring services on Kubernetes with ELK beats
  - Monitoring services on GCE instances
  - Logstash pipelines and debugging walk through
  - Elasticsearch operations: house-cleaning, tuning, pernament storage
  - Elasticsearch maitainence, trouble shooting
  - Get-Started with Elastic Cloud SASS
- General operations on Kubernetes(4)
  - Kubernetes Debug SOP
  - Kubectl cheat sheet
  - Secure services with SSL by cert-manager
  - Speed up container updating with operator
    - My operator example
- Deploy Kafka HA on Kubernetes(4)
  - deploy kafka-ha on Kubernertes with helm
  - in-cluster networking configuration for high availability
  - basic app-side usage, performance tuning
  - Operate Kafka: update config, upgrade version, migrate data
- Promethus / grafana(5)
  - Deploy Prometheus / Grafana stack on GCE instance
  - Monitoring services on Kubernetes with exporters
  - Export Kubernetes metrics to Prometheus
  - Export Redis-ha metrics to Prometheus
  - Export Kafka metrics to Prometheus
- GCP networking(4)
  - Firewall basic concept for private network with GCE instances & Kubernetes
  - Load balancer for Kubernetes service & ingress
  - DNS on GCP from Kube-dns to GCP DNS service
- GCP log management(3)
  - Basic usage about GCP logging & GCP Error Report
  - Stackdriver, metrics, alerts
  - [x] Logging on GKE from gcp-fluentd to stackdriver
