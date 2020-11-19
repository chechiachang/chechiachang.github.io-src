---
title: "2019 IT邦幫忙鐵人賽"
subtitle: ""

# Add a summary to display on homepage (optional).
summary: "2019 IT邦幫忙鐵人賽"

date: 2019-09-09T16:56:03+08:00
draft: false

# Authors. Comma separated list, e.g. `["Bob Smith", "David Jones"]`.
authors: []

# Is this a featured post? (true/false)
featured: true

# Tags and categories
# For example, use `tags = []` for no tags, or the form `tags = ["A Tag", "Another Tag"]` for one or more tags.
tags: ["ithome", "kubernetes", "elk", "kafka", "redis", "nginx", "cert-manager", "crd"]
categories: ["kubernetes"]
---

各位好，我是Che-Chia Chang，社群上常用的名子是 David Chang。是個軟體工程師，專長的領域是後端開發，開發維運，容器化應用，以及Kubernetes開發管理。目前為 [Golang Taiwan Meetup](https://www.meetup.com/golang-taipei-meetup/) 的 organizer。

受到[友人們](https://ithelp.ithome.com.tw/2020ironman/signup/team/63)邀請（推坑）參加了[2020 It邦幫忙鐵人賽](https://ithelp.ithome.com.tw/2020ironman)，挑戰在30天內，每天發一篇技術分享文章。一方面將工作上遇到的問題與解法分享給社群，另一方面也是給自己一點成長的壓力，把這段時間的心得沈澱下來，因此也了這系列文章。

本系列文章重點有三：

1. 提供的解決方案，附上一步步的操作步驟。希望讓讀者可以重現完整操作步驟，直接使用，或是加以修改

2. 著重 Google Cloud Platform，特別是Google Compute Engine (GCE) 與Google Kubernetes Engine (GKE) 兩大服務。這也是我最熟悉的平台，順便推廣，並分享一些雷點。

3. 從維運的角度除錯，分析問題，提升穩定性。

預定的主題如下（可能會依照實際撰寫狀況微調）

- ELK Stask on GCP (8)
  - [Self-host ELK stack on GCP]({{< ref "/post/2019-09-15-self-host-elk-stack-on-gcp" >}})
  - [Secure ELK Stask]({{< ref "/post/2019-09-15-secure-elk-stack" >}})
  - [監測 Google Compute Engine 上服務的各項數據]({{< ref "/post/2019-09-18-monitoring-gce-with-elk" >}})
  - [監測 Google Kubernetes Engine 的各項數據]({{<ref "/post/2019-09-19-monitoring-gke-with-elk" >}})
  - [是否選擇 ELK 作為解決方案]({{< ref "/post/2019-09-18-elastic-or-not-elastic" >}})
  - [使用 logstash pipeline 做數據前處理]({{< ref "/post/2019-09-21-logstash-on-gke" >}})
  - Elasticsearch 日常維護：數據清理，效能調校，永久儲存
  - Debug ELK stack on GCP
- Kafka HA on Kubernetes(6)
  - [Deploy kafka-ha]({{< ref "/post/2019-09-22-kafka-deployment-on-kubernetes" >}})
  - [Kafka Introduction]({{< ref "/post/2019-09-23-kafka-introduction" >}})
  - [kafka 基本使用]({{< ref "/post/2019-09-24-kafka-basic-usage" >}}) 
  - [kafka operation scripts]({{< ref "/post/2019-09-25-kafka-operation-scripts" >}})
  - [集群內部的 HA topology]({{< ref "/post/2019-09-25-kafka-ha-topology" >}})
  - [集群內部的 HA 細節]({{< ref "/post/2019-09-26-kafka-ha-continued" >}})
  - Prometheus Metrics Exporter 很重要
  - 效能調校
- 在 GKE 上部署 Redis HA (5)
  - [使用 helm 部署 redis-ha]({{< ref "/post/2019-09-28-redis-ha-deployment" >}})
  - [Redis HA with sentinel]({{< ref "/post/2019-09-29-redis-ha-sentinel" >}})
  - [Redis sentinel topology]({{< ref "/post/2019-09-30-redis-ha-topology" >}})
  - [Redis HA with HAproxy]({{< ref "/post/2019-10-02-redis-ha-on-haproxy" >}})
  - [Redis HA Failure Recovery]({{< ref "/post/2019-10-03-redis-ha-failure-recovery" >}})
  - Prometheus Metrics Exporter
- Prometheus / Grafana (5)
  - [GKE 上自架 Prometheus]({{< ref "/post/2019-10-04-prometheus-deployment-on-kubernetes" >}})
  - [GKE 上自架 Grafana]({{< ref "/post/2019-10-04-prometheus-deploy-grafana" >}})
  - [scrape config & exporter]({{< ref "/post/2019-10-04-prometheus-scrape">}})
  - [Dive into Redis Exporter]({{< ref "/post/2019-10-06-prometheus-exporter-library-redis-exporter" >}})
  - [輸出 kube-state 的監測數據]({{< ref "/post/2019-10-07-prometheus-kube-state-metrics-exporter" >}})
- Nginx Ingress (3)
  - [Deploy Nginx Ingress Controller]({{< ref "/post/2019-10-08-kubernetes-nginx-ingress-controller" >}})
  - [Configure Nginx Ingress]({{< ref "/post/2019-10-08-kubernetes-nginx-ingress-config" >}})
- Cert-manager (3)
  - [Deploy cert-manager]({{< ref "/post/2019-10-10-cert-manager-deployment" >}})
  - [How cert-manager work]({{< ref "/post/2019-10-11-cert-manager-how-it-work" >}})
  - [Cert-manager complete workflow]({{< ref "/post/2019-10-12-cert-manager-complete-workflow" >}})
- Kubernetes CRD & Operator-sdk (3)
  - [Introduction about custom resource]({{< ref "/post/2019-10-13-kubernetes-custom-resources-basic">}})
  - [Deployment & Usage]({{< ref "/post/2019-10-13-kubernetes-custom-resources-basic">}})
  - [Deployment & Usage]({{< ref "/post/2019-10-15-kubernetes-custom-resource-with-operator-sdk">}})

文章發表於[鐵人挑戰頁面](https://ithelp.ithome.com.tw/users/20120327/ironman/2444)，同時發布與本站備份。有任何謬誤，還煩請各方大德<3透過底下的聯絡方式聯絡我，感激不盡。

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
