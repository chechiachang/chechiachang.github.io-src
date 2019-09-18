---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Monitoring Gce With Elk"
subtitle: ""
summary: ""
authors: []
tags: []
categories: []
date: 2019-09-18T19:10:50+08:00
lastmod: 2019-09-18T19:10:50+08:00
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: false

# Projects (optional).
#   Associate this post with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects = ["internal-project"]` references `content/project/deep-learning/index.md`.
#   Otherwise, set `projects = []`.
projects: []
---

Filebeat
===

ELK 的 beats 是輕量級的系統監測收集器，beats 收集到的 data 經過 mapping 可以送到 Elasticsearch 後，進行彈性的搜尋比對。

beat 有許多種類，依據收集的 data 區別：

* Auditbeat: Audit data
* Filebeat: Log files
* Functionbeat: Cloud data
* Heartbeat: Availability
* Journalbeat: Systemd journals
* Metricbeat: Metrics
* Packetbeat: Network traffic
* Winlogbeat: Windows event logs

這邊先以 filebeat 為例，在 GCE 上收集圓端服務節點上的服務日誌與系統日誌，並在 ELK 中呈現。

# Installation

安裝及設定 filebeat 的步驟，在這篇[Secure ELK Stack]() 中已經說明。這邊指附上連結，以及[官方文件]() 提供參考。

# Configuration

```
wget https://raw.githubusercontent.com/elastic/beats/master/filebeat/filebeat.reference.yml
sudo mv filebeat.reference.yml /etc/filebeat/filebeat.yml
```

# input

# output load balance

# modules

# autodiscover
