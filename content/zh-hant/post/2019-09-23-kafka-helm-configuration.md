---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Kafka Helm Configuration"
subtitle: ""
summary: ""
authors: []
tags: ["鐵人賽2019", "kafka", "kubernetes", "ithome"]
categories: ["kubernetes", "kafka"]
date: 2019-09-23T21:55:29+08:00
lastmod: 2019-09-23T21:55:29+08:00
featured: false
draft: false
---

[2020 It邦幫忙鐵人賽](https://ithelp.ithome.com.tw/2020ironman) 系列文章

- ELK Stack
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
  
由於我比較熟悉 GCP / GKE 的服務，這篇的操作過程都會以 GCP 平台作為範例，不過操作過程大體上是跨平台通用的。
