---
title: "Hashicorp Comminity Presentation Vault Introduction" # Title of the blog post.
date: 2023-05-10T12:19:02+08:00 # Date of post creation.
description: "Article description." # Description used for search engine.
featured: true # Sets if post is a featured post, making appear on the home page side bar.
draft: true # Sets whether to render this page. Draft of true will not be rendered.
toc: false # Controls if a table of contents should be generated for first-level links automatically.
# menu: main
featureImage: "/images/path/file.jpg" # Sets featured image on blog post.
thumbnail: "/images/path/thumbnail.png" # Sets thumbnail image appearing inside card on homepage.
shareImage: "/images/path/share.png" # Designate a separate image for social media sharing.
codeMaxLines: 10 # Override global value for how many lines within a code block before auto-collapsing.
codeLineNumbers: false # Override global value for showing of line numbers within code block.
figurePositionShow: true # Override global value for showing the figure label.

tags: ["vault", "iac", "aws", "terraform", "kubernetes"]
categories: ["kubernetes", "vault"]
---

Failed to join event

# Info

Hashicorp Vault 自建金鑰管理最佳入坑姿勢

本次演講從導入 Hashicorp Vault 作為起點，直接提供實務上經驗，分享建議的設定與路上可能有的雷。
- Vault 入坑的困難
- Vault + Terraform 一入坑就 IaC
- mount path + role + policy 命名與管理
- 升級與維護
會依據企業需求提供實際用例 demo，當天提供 github code example
不會講太多非常基本介紹 vault 介紹

# target group

聽眾建議要有 secret management 經驗，有使用 Kubernetes，三大公有雲者，Hashicorp Vault 基本使用經驗，希望導入到團隊內部
知道如何安全地且有系統的導入 Hashicorp Vault 自建私鑰管理系統，並避免踩到不必要的雷

# 10 tips for using vault

choose your auth method
- public cloud iam auth
- k8s auth
- auth method 以外就無法 auth

given k8s auth is by service account
- define service accounts for each deployment / release

path should be define by [role] / [deployment unit]

- deploy 1 k8s deployment with 100 pods

- /k8s/ns/deploy/key
- /account/dev/project/deploy
- /account/dev/ec2-group/service

policy should be as simple as possible
- good
  - [role] read /k8s/ns/deploy/key
  - [role] list /k8s/ns/deploy/
- avoid
  - 
  - grant [role] list /k8s/ns/ + deny [role] list /k8s/ns/deploy

- 一眼看下去看不懂的 policy 就很難維護
- 犧牲 DRY 展開，達成簡單肯定句
  - `/k8s/ns/*` 除非這個 role 就是需要 list all
    - /k8s/ns/sa1
    - /k8s/ns/sa2

define [role]
- a sa in a ns of a k8s
- a iam role
- 讓 iam-role 接近 sa
  - ns/role1
  - role:account::dev-k8s-ns-sa1

irsa

use auth log
- log rotate auth log to avoid out of disk
- 
