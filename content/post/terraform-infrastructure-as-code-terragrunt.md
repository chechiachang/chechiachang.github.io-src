---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Terraform Infrastructure as Code: Terragrunt"
subtitle: ""
summary: ""
authors: []
tags: ["kubernetes", "terraform"]
categories: ["kubernetes", "terraform"]
date: 2020-10-03T11:15:48+08:00
lastmod: 2020-10-03T11:15:48+08:00
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

- 心得
  - CI/CD 全自動化
  - State backend 選擇
  - 最佳實踐 https://www.terraform.io/docs/cloud/guides/recommended-practices/index.html
- 工具
  - Terraform Atlantis
  - Terragrunt

# 問題與需求

當團隊已經開始大規模使用 terraform，tf 檔案越來越多。我們為了增加程式碼的重複利用性，會使用 terraform module 將常用的 tf 檔案封裝。

- 隨著導入的規模越來越大，這些 module 會越來越多，而且使用這些 module 的 project 也增加
- 隨著管理的 infrastructure 越來越複雜，為了描述這些本來就很複雜的 infrastructure，module 不只越來越多，還會出現 module 引用其他 module，大 module 使用小 module 的 nested module
  - 這點在複雜的 provider 中常出現，例如
    - 使用 terraform 描述網路架構
    - 描述複雜的 IAM & Role
    - terraform vault-provider

使用一段時間 terraform ，很快就會發現的第一個問題是：不論怎麼從 tf 檔案中提取重複部分，做成 module，還是有很多部分的 tf code 是完全重複的，例如：

- 每個 module 會定義的 variable (argument)，使用這個 module 的上層會需要提供傳入 variable
- 每個 module 都會需要提供 provider

Terraform 的語法要求上面這些參數都明確的定義，這讓整個 module 或資料夾的描述非常清楚。但會處就是，這些描述的參數道出都是，而且不斷的重複，每個 module 或資料夾都要提供，不然在 terraform validate 時會因為應提供參數未提供，導致錯誤。雖然立意良好，但卻嚴重違反 DRY (Don't Repeat Yourself) 的原則

- module 多層引用，project 引用大 module，大 module 又引用小 module
- 開始感覺 backend 與 provider 的 code 比其他功能 code 多了

有沒有可能用其他工具，避免這些重複的參數，backend，provider 等等？

# Terragrunt

推薦有大量使用的團隊，直接使用 [Terragrunt](https://terragrunt.gruntwork.io/) 這款工具。

- 他是一層 terraform 的 wrapper
  - i.e. 執行 terraform plan -> terragrunt plan
  - terragrunt 會先解析，產生重複的 code，然後再執行 terraform
  - 編輯時只要寫一次，terragrunt 代為在其他地方產生重複的 code
  - 產生的 code 會被隱藏與 cache

他能夠處理多環境下重複的 tf，例如

# 安裝

# 使用

# 範例

