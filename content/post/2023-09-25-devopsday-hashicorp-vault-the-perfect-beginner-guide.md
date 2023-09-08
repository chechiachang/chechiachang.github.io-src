---
title: "2023 09 25 DevopsDay 2023 Hashicorp Vault perfect start for beginner" # Title of the blog post.
date: 2023-09-25T12:19:02+08:00 # Date of post creation.
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
categories:
  - Technology
tags:
  - Tag_name1
  - Tag_name2
---

# Info

Title: Hashicorp Vault in K8s：自建金鑰管理最佳入坑姿勢

https://devopsdays.tw/CFP

# target group

# 10 tips for using vault

IaC is a must
- provision infra w/ IaC
- config vault w/ IaC

choose your auth method
- public cloud iam auth
- k8s auth
- auth method 以外就無法 auth

Use HA vault
- 

Vault K8s Secret Operator

given k8s auth is by service account
- define service accounts for each deployment / release

separated envs:
- put vault in separted k8s in separated subnet, vpc
- use lb and firewall rules to control visibility access

- deploy 1 k8s deployment with 100 pods

path naming: use google naming convention
- path should be define by [role] / [deployment unit]
- /k8s/ns/deploy/key
- /account/dev/project/deploy
- /account/dev/ec2-group/service

define [role]
- a sa in a ns of a k8s
- a iam role
- 讓 iam-role 接近 sa
  - ns/role1
  - role:account::dev-k8s-ns-sa1

Simple policy rule: rule should be as simple as possible
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

irsa

use auth log
- log rotate auth log to avoid out of disk
- 
