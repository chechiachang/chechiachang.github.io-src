---
title: "2022 03 11 Ithome Cloud Summit K8s Failure Stories" # Title of the blog post.
date: 2022-03-11T01:04:12+08:00 # Date of post creation.
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

別人的 K8s 死袂了 - Kubernetes Failure Stories

Slides: https://docs.google.com/presentation/d/1jIQBPQ2T4XESTOtaW441KkdatJo6mONZVGf-26CgSdc/edit#slide=id.p

### Description

在一個簡單的系統中，資深工程師可以很清楚地指出，這裡有出過問題、這裡有風險、這裡有雷，做後起團隊的前車之鑑。

Kubernetes 功能強大，底層架構卻十分複雜，且還在持續快速演化。再也沒有工程師可以自稱洞悉 k8s 一切，踩過所有雷，能帶領團隊避開風險。

所以我們需要多聽別人失敗的故事，從中學習別人的經驗。

業界領先企業在災難後會發布 incident report 與 postmortem，本次演講將帶聽眾導讀業界領頭公司的災後報告，並提供改善建議。

### Content

別人的 K8s 死袂了 - Kubernetes Failure Stories

- 領頭企業的故事，別人的 k8s 怎麼死了
- Improvement 1: Prometheus alert 超前部屬
- Improvement 2: 避免工程師犯錯的技術棧與工作流程，Iac 自動化
- Improvement 3: 團隊文化提升，接受犯錯、不貳過

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

- 吸收業界領先企業的經驗
- 知道 k8s 的使用風險，更了解 k8s
- 培養搜尋災難報告的習慣，主動吸收 k8s 經驗

- 推薦有 k8s 使用經驗的從業人員，對 k8s 有上手經驗
- 有玩死 k8s 的經驗更好，知道更多 k8s 的死法
- 有救活死掉 k8s 的經驗更好，知道如何除錯 k8s，並把他救活

https://k8s.af/
