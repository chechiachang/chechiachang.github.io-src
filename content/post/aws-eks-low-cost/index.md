---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Let's Play AWS EKS with Low Cost"
subtitle: ""
summary: ""
authors: []
tags: []
categories: ["kubernetes", "aws", "pricing"]
date: 2020-08-13T16:55:17+08:00
lastmod: 2020-08-13T16:55:17+08:00
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

# Object

- Learn EKS
- Limited credits: $25 USD
  - `FLD_CHI_FY2020_Q1_TW_Kaohsiung_AWSome_Day`
- Use as much time as possible.

# Secondary Object

- 食米毋知米價
- It's profit/cost when comes to business

# Low Cost Policy

- Cluster
  - Delete after playground -> quick-up-quick-down with terraform
- EC2
  - Spot Instance
    - Type: minimal t3.small,t3a.small
  - EBS
- VPC

# EKS pricing planning (per hr)

[EKS pricing](https://aws.amazon.com/tw/eks/pricing/)

alexandra-trusova
- 0.1 USD / hr * 1 cluster
- EC2 * 3
  - t3(2vcpu 2G)  Spot    On-demand (floating)
    - Mumbai      $0.0037 $0.0123 (t3a.small)
    - Seoul       $0.007  $0.0234 .
    - Sydney      $0.0071 $0.0238 .
    - Singapore   $0.0071 $0.0236 .
    - Tokyo       $0.0082 $0.0245 .
    - Hongkong    $0.0088 $0.0292 (t3.small)
  - Set maximum price   $0.01
- EBS
  - minimal 30GB / node (free tier 30 GB / month)

Expected Subtotal:  / hr

# AWS help me!

徵求乾爹，讓我可以繼續用 AWS 寫教學文章
