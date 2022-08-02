---
title: "2022 05 21 COSCUP Operating Time Series Database in K8s" # Title of the blog post.
date: 2022-05-21T01:04:12+08:00 # Date of post creation.
#description: "Article description." # Description used for search engine.
featured: true # Sets if post is a featured post, making appear on the home page side bar.
draft: true
toc: false # Controls if a table of contents should be generated for first-level links automatically.
# menu: main
#featureImage: "/images/path/file.jpg" # Sets featured image on blog post.
#thumbnail: "/images/path/thumbnail.png" # Sets thumbnail image appearing inside card on homepage.
#shareImage: "/images/path/share.png" # Designate a separate image for social media sharing.
#codeMaxLines: 10 # Override global value for how many lines within a code block before auto-collapsing.
#codeLineNumbers: false # Override global value for showing of line numbers within code block.
#figurePositionShow: true # Override global value for showing the figure label.
categories:
  - Technology
tags:
  - kubernetes
  - devops
  - terraform
---

### Titleq

在 k8s 上跑 time series database 甘苦談 - Operating Time Series Database in K8s

Slides: https://docs.google.com/presentation/d/1PZryGImYRALMJfbEMuf_jPd2P-qzIwDmVd5DgXSuqq0/edit#slide=id.p
Youtube live record: https://youtu.be/YexUnVOZC8M?t=9421

### Description

Influxdb 為市占最高的 time series DBMS 之一，使用上與 RDBMS 有不同優劣勢。

在維運方面，database 有許多相似需求：穩定性、高可用性、備份、還原、資源管理、調度、災難復原...等。社群常聽到有人問：可不可以在 K8s 上跑 database。

本演講會分享在 k8s 中維運，實務上所遇到的問題，提供一些思考方向。

本次演講的 influxdb 版本為 Influxdb OSS / enterprise 1.9+

InfluxDB is one the the most popular time series database management system (DBMS) and is a powerful platform when dealing with time series data.

DBMSs, including RDBMS, have many similar requirements on aspect of infrastructure operation. They all require stability, high availability, backup and restore utilities, cpu / memory resource management, disaster recovery...etc. People often ask about that whether is it ok to run DBMS in kubernetes cluster or not. This lecture try to provide some points from our experiences dealing with real-world issues.

The version of InfluxDB discussed in the lecture is InfluxDB OSS / Enterprise 1.9+


### Content

在 k8s 上跑 time series database 甘苦談

- 簡介 Influxdb，time series 與 RDBMS 的差異
- 使用 time series 的幾個情境: 
- 在 k8s 上跑 DB
  - 穩定性 Availability、HA (enterprise)、faillure recovery
  - 資源管理 OOMKilled、cpu throttling、OutOfDisk
  - DB management: data migration、backup & restore、data retention
- 小結: 你該不該用 cloud service / VM / 在 K8s 上跑 database

Operating Time Series Database in K8s

- A brief introduction about InfluxDB and the differences with RDBMS
- Some scenario to use a time series database (other than RDBMS)
- Operate InfluxDB in K8s
  - Stability, availability, disaster recovery
  - Resource management, OOMKilled, cpu throttling, out of disk
  - DB management: data migration, retention, rotation, backup & restore
- summary: whether or not to run a database in k8s

### About me

Che-Chia Chang，專長的領域是後端開發，開發維運，容器化應用，以及Kubernetes開發管理。
Microsoft 最有價值從業人員 MVP。

目前為 Golang Taiwan Meetup Organizer，常出現於 CNTUG，DevOps Taipei，GDG Taipei， Golang Taipei Meetup。

Che-Chia Chang, an SRE specialize in container and Kubernetes operation. An active member of CNTUG, DevOps Taipei, GDS Taipei, Golang Taiwan Meetup.
Microsoft Most Valuable Professional since 2020.

https://chechia.net

2018 Ithome Cloud Summit
2018 Ithome Kubernetes Summit
2019 Ithome Cloud Summit
2020 Ithome Cloud Summit
2020/12/18	Cloud Native Taiwan 年末聚會
2020/8/17	DevOps Taiwan Meetup #26 - 從零開始導入 Terraform
2021 Ithome Cloud Summit

### Suggested Audience

- 推薦有 k8s 使用經驗的從業人員，對 k8s 有上手經驗
- 問可不可以在 k8s 上面跑 database 的人
