---
title: "Hashicorp Comminity Presentation Vault Introduction" # Title of the blog post.
date: 2023-05-10T12:19:02+08:00 # Date of post creation.
description: "Article description." # Description used for search engine.
featured: true # Sets if post is a featured post, making appear on the home page side bar.
draft: false # Sets whether to render this page. Draft of true will not be rendered.
toc: false # Controls if a table of contents should be generated for first-level links automatically.
# menu: main
featureImage: "/images/path/file.jpg" # Sets featured image on blog post.
thumbnail: "/images/path/thumbnail.png" # Sets thumbnail image appearing inside card on homepage.
shareImage: "/images/path/share.png" # Designate a separate image for social media sharing.
codeMaxLines: 10 # Override global value for how many lines within a code block before auto-collapsing.
codeLineNumbers: false # Override global value for showing of line numbers within code block.
figurePositionShow: true # Override global value for showing the figure label.

tags: ["vault", "iac", "aws"]
categories: ["vault"]
---

# target group

- 金融客戶
- vault


4/15 上架
- accupass
5/10 (Wed) 11:00-12:00
- webbase link (online)
- 10:30 上線設備測試
- 11:00 Ming 開場
- 11:05 主講
- 12:00 Q&A (留言)

- 當天錄影會上線

# 演講大綱

- 基本介紹 vault 架構
- 企業需求
  - self-host
  - 複雜的 policy
- 用例 demo
  - aws auth
  - k8s auth
  - policy
  - 當天提供 github example
- Q&A (10mins)

# 內容

演講主題：Hashicorp vault 雲端地端通吃的私鑰管理平台

現代網路應用需要處理許多私密金曜的管理，例如：user 的密碼，server 的資料，database 的資料，microservices 彼此 authentication...。加上駭客團體猖獗，許多國內外知名企業紛紛遭駭，導致公司與使用者的損失。
如何系統化且自動化管理大量的私密資料，成為系統整體安全性的關鍵。
Hashicorp Vault 為一款開源的私密資料管理平台，除了保障系統安全性，比起市面上的其他管理工具，有許多特點
- 不依賴外部服務，適合自行架設在內部公有雲/私有雲/傳統server/Kubernetes/VM
- 支援跨環境的應用，可以串連混合雲中的應用，作為私要認證的中心
本次演講簡介 Hashicorp Vault，以 aws cloud 與本地 kubernetes 為例，提供幾個基本的操作範例
適合初次接觸的 Hashicorp Vault，與尋找私要管理平台的團隊

講者簡介

Che-Chia Chang，SRE，喜歡研究公有雲/容器化應用/Kubernetes
Microsoft MVP，Ithome 雲端大會/COSCUP講師，常出現 CNTUG / DevOpsTW / Golang Taipei
技術 blog 收錄過往演講與文章 https://chechia.net

# Presentation

https://docs.google.com/presentation/d/1iex9lm89OCIR8IAoD1RPe4vcW--bcKBmMHoixDybqP8/edit#slide=id.g2403737215e_0_147
