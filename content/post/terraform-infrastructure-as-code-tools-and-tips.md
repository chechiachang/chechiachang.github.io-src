---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Terraform Infrastructure as Code: Useful tools and tips"
subtitle: ""
summary: ""
authors: []
tags: ["kubernetes", "terraform"]
categories: ["kubernetes", "terraform"]
date: 2020-10-02T11:15:48+08:00
lastmod: 2020-10-02T11:15:48+08:00
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

上面講解 Terraform 的基本操作流程，提供範本原始碼，以及一步一步導入的詳細步驟。各位應該都可以依照上面幾篇的說明，開始快樂的使用 Terraform 了。

而當使用 Terraform 的規模越來越大，管理的資料越來越多時，開始會出現一些問題，例如重複的 terraform code 越來越多，協同工作 review 不太容易，state 的內容管理與鎖管理，等等。這些問題可以透過一些工作流程的改進，或是導入新的小工具，來改善工作效率。

接下來筆者推薦幾個心得與工具，希望能提升使用 Terraform 的效率與產值

以下幾篇文章，適合已經使用過 terraform 一點時間，有經驗的團隊，並打算更大規模導入 terraform，正在尋求改善的方向。

心得
- CI/CD 全自動化
- 最佳實踐

工具
- Terraform Atlantis
- Terragrunt

# CI/CD 全自動化
