---
title: "2022 06 09 IThome 2022 DevOpsDay Introducing policy as code for terraform" # Title of the blog post.
date: 2022-06-09T01:04:12+08:00 # Date of post creation.
#description: "Article description." # Description used for search engine.
featured: true # Sets if post is a featured post, making appear on the home page side bar.
draft: false
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
  - pac
  - devops
  - terraform
---

### Titleq

從零導入 Policy as Code 到 terraform 甘苦談 - Introducing policy as code for terraform

### Presentation

[Google Slides](https://docs.google.com/presentation/d/1yawazO1B_sP5Yiav-XLGJXW3ZS2JTV0wGuJwhrUKQ3A/edit?usp=sharing)

### Description

Terraform 是一個很棒的 Infrastructure as Code 的工具，能夠以現代的軟體工程流程來穩定的建構 infrastructure，並隨著需求變更自動化迭代，將新的 feature 安全地更新到既有的 infrastructure 上。只要是 Infrastructure 有關的問題，我一律推薦 Terraform。

這也意味 Terraform 的品質就等於 infrastructure 的品質，好的 terraform 帶你上天堂，不好的 terraform 全 team 火葬場。
- Infrastructure 有太多資安的考量，新的風險不斷被檢查出來，連帶要不斷的 patch terraform code 來避免潛在的資安風險
- Infrastructure 會不斷地更新，例如公有雲的 api 不斷更新，去年的 code 已經跟不上今年的最佳實踐了
- 好的工程師寫出的 terraform code 屌打菜鳥工程師，要如何讓團隊依循更好的實踐，避免寫出爛 code
維護 code 有 clean code / best practice，Terraform 也有 clean code 與 best practice，工程師要如何工具來輔助，是 Policy as Code 的一大課題。

本演講聚焦於實際經驗，從一大堆 terraform modules 開始，沒有 Policy as Code，到一步步評估、導入、實作、改進與迭代，逐漸的提升團隊 Terraform code 品質，提升 infrastructure 交付品質，並避免到未來潛在的風險。

本次演講的 Terraform 版本為從 0.12, 0.13, 一路推進 1.0+。

### Content

從零導入 Policy as Code 到 terraform 甘苦談

- 簡介 Terraform 與 Policy as Code
- 當你手上有數不完的 terraform modules，管理 terraform 品質是個大問題
- 如何管理 Terraform
  - 自動化: 改變從 Jenkins pipeline 開始，gitflow 改進，pre-commit hook
  - Policy as Code 校驗
  - 使用工具量化 terraform code 品質
  - 完整導入 Policy as Code
- 小結: 玩 infra 必用 terraform，玩 terraform 必做 policy as code

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
2022 Ithome Cloud Summit
2022 COSCUP

### Suggested Audience

- 推薦有 Terraform 使用經驗，特別是公有雲經驗，對 Policy as Code 有興趣的人
- 想要寫出 Terraform clean code 的人
