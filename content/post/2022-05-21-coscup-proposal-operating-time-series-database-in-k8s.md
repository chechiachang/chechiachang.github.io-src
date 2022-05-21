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

### Description

Influxdb 為市占最高的 time series DBMS 之一，使用上與 RDBMS 有不同優勢。本次演講的 influxdb 版本為 Influxdb OSS / enterprise 1.9+

社群常聽到有人問：可不可以在 K8s 上跑 database，所以來分享一下到底可不可以

### Content

在 k8s 上跑 time series database 甘苦談 - Operating Time Series Database in K8s

- 簡介 Influxdb，time series 與 RDBMS 的差異
- 使用 time series 的幾個情境: 
- 在 k8s 上跑 DB 穩嗎: Availability、faillure recovery、
- 在 k8s 上跑 DB 資源管理: OOMKilled、cpu throttling、OutOfDisk
- 在 k8s 上跑 DB 方便嗎: data migration、backup & restore、data retention
- 小結: 你該不該用 cloud service、放在 VM、在 K8s 上跑 database

### About me

Che-Chia Chang，專長的領域是後端開發，開發維運，容器化應用，以及Kubernetes開發管理。
Microsoft 最有價值從業人員 MVP。

目前為 Golang Taiwan Meetup Organizer，常出現於 CNTUG，DevOps Taipei，GDG Taipei， Golang Taipei Meetup。

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

https://k8s.af/
