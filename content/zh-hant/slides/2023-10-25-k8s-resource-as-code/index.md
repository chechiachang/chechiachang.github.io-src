---
title: "Kubernetes Summit: Resource as Code for Kubernetes: Stop kubectl apply"
summary: 將 k8s resource 以 code 管理，推上 vcs，並使用 argoCD, secret operator 等工具進行管理，來讓避免低級的人工操作錯誤，降低團隊整體失誤率，並降低 k8s admin 管理的成本，提高管理效率
authors: []
tags: ["kafka", "kubernetes"]
categories: ["kubernetes"]
date: '2023-10-25T00:00:00Z'
slides:
  # Choose a theme from https://github.com/hakimel/reveal.js#theming
  #theme: black
  theme: white
  # Choose a code highlighting style (if highlighting enabled in `params.toml`)
  #   Light style: github. Dark style: dracula (default).
  highlight_style: dracula
---

# Info

Title: Resource as Code for Kubernetes: stop kubectl apply

https://k8s.ithome.com.tw/CFP

Infrastrure as Code (IaC) 與 PaC，在萬物都該 as Code 得時代，你還在不斷的 kubectl apply 嗎？

手動 apply 的痛點：
- 人就是會忘：是誰 apply 這個在 k8s 上的？是誰上次漏 apply 所以壞了？
- 人就是會寫錯：能否 apply 
- 管理大量的 label, taint, annotation
- 安全：apply 變更內容是否有經過資訊安全的 review

當服務的 app code base 都已經用 chart 打包，使用 vcs 管理後，為何依賴的 k8s resource (namespace, secret, label, crd, ...) 不需要推上 vcs 管理的？

本次演講集合幾個管理 k8s 的範例，將 k8s resource 以 code 管理，推上 vcs，並使用 argoCD, secret operator, ... 等工具進行管理，來讓避免低級的人工操作錯誤，降低團隊整體失誤率，並降低 k8s admin 管理的成本，提高管理效率

# target group

Kubernetes User who want to increase performance in k8s management

# Scenario

Reduce incident / maintenance effor caused by human error(i.e. 忘記 or 沒注意)
- Yes, you will always forget what have been done (and what have not been done).
- orphan resource without maintainer

Standarize common component in multiple k8s clusters
 - for multiple env
 - for multiple region-zone
 - for multiple microservice

Ship your changes in reviewed

# 10 tips for manage

IaC is a must: provision infra w/ IaC

ex. provision aws lb controller
- 

Leverage Resource label
- 

Secret management
- vault
  - pod 
- cloud provider (aws secret manager)

argocd
- namespace
- crd
- applicationsets for common component
- configmap
  - configmap reloader
- service account (with app)
- role
  - terraform
    - aws-iam
    - service account
