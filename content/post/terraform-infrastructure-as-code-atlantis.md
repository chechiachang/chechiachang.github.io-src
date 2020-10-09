---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Terraform Infrastructure as Code: Atlantis"
subtitle: ""
summary: ""
authors: []
tags: ["kubernetes", "terraform"]
categories: ["kubernetes", "terraform"]
date: 2020-10-04T11:15:48+08:00
lastmod: 2020-10-04T11:15:48+08:00
featured: false
draft: true

menu:
  main:
    parent: "Kubernetes"
    weight: 1
---

This article is part of [Infrastructure as Code: introduce Terraform from stratch]({{< ref "/post/terraform-infrastructure-as-code" >}})
- [Get-started examples / SOP on Github](https://github.com/chechiachang/terraform-playground)
- [Introducation to Terraform Iac: Speaker transcript]({{< ref "/post/terraform-infrastructure-as-code" >}})
- [Presentation](https://slides.com/chechiachang/terraform-introduction/edit)

Check my website [chechia.net](https://chechia.net) for other blog. [Follow my page to get notification](https://www.facebook.com/engineer.from.scratch). Like my page if you really like it :)

---

# 需求與問題

- Git-flow
  - PR
  - review
- 有時會忘記 merge
- 有時會忘記 apply

Atlantis 解決方案是與版本控制整合，PR + Review
遠端執行，自動 plan apply 與自動 merge

https://www.runatlantis.io/

- Git-flow
- 自動化 plan
- Webhook 回傳 plan 結果
- 透過 bot 控制 apply
- 自動 merge

# 安裝與設定

https://www.runatlantis.io/docs/installation-guide.html

# 優點

- 可以 self-hosted，credential 不外洩，確保最高的安全性
- 已經整合 Kubernetes, helm chart
- webhook 整合許多版本控制庫，例如 github, gitlab,...
- 實現安全的遠端執行
  - 本地執行還是會有諸多問題
  - terraform cloud 提供的遠端執行
