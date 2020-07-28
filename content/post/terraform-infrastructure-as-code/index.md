---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "從零開始的 Infrastructure as Code: Terraform - 01"
subtitle: "Infrastucture as Code: introduce Terraform from scratch"
summary: ""
authors: []
tags: ["terraform", "kubernetes", "devops"]
categories: []
date: 2020-06-14T16:46:09+08:00
lastmod: 2020-06-14T16:46:09+08:00
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

menu:
  main:
    parent: "Kubernetes"
    weight: 1
---

This article is part of [從零開始的 Infrastructu as Code: Terraform]({{< ref "/post/terraform-infrastructure-as-code" >}})
- [01 - Introduction to Infrastructure as Code]({{< ref "/post/terraform-infrastructure-as-code" >}})
- [02 - Terraform 簡介與基本操作]
- [03 - 為公司導入 Terraform]
- [Get-started examples / SOP on Github](https://github.com/chechiachang/terraform-playground)
- [Introducation to Terraform Iac: Speaker transcript]({{< ref "/post/terraform-infrastructure-as-code" >}})

Check my website [chechia.net](https://chechia.net) for other blog. [Follow my page to get notification](https://www.facebook.com/engineer.from.scratch). Like my page if you really like it :)

---

# 引言 Infrastructure as Code

從字面上解釋，IaC 就是用程式碼描述 infrastructure。那為何會出現這個概念？

如果不 IaC 是什麼狀況？我們還是可以透過 GUI 或是 API 操作。隨叫隨用

雲端運算風行，工程師可以很在 GUI 介面上，很輕易的部署資料中心的架構。輸入基本資訊，滑鼠點個一兩下，就可以在遠端啟用運算機器，啟用資料庫，設置虛擬網路與路由，幾分鐘就可以完成架設服務的基礎建設(infrastructure)，開始運行服務。

然而隨著
- 雲平台提供更多新的（複雜的）服務
  - 服務彼此可能是有相依性（dependency），服務需要仰賴其他服務
  - 或是動態耦合，更改服務會連動其他服務，一髮動全身
- 需要縝密的存取控管（access control）
  - 防火牆，路由規則
  - 雲平台上，團隊成員的存取權限
- 專案的規模與複雜度增加
  - 多環境的部署
  - 多個備援副本設定
  - 大量機器形成的集群

# IaC 的實際需求

以下這些對話是不是很耳熟？

# IaC 的實際需求

沒有需求，就不需要找尋新的解決方案。

有看上面目錄的朋友，應該知道這系列文章的後面，我會實際分享於公司內部導入 Terraform 與 IaC 方法的過程。

各位讀者會找到這篇文，大概都是因為實際搜尋了 Terraform 或是 IaC 的關鍵字才找到這篇。

如果沒有需求，自己因為覺得有趣而拉下來研究，

如果沒有明確需求，就貿然導入
無謂增加亂度

# IaC 的實現工具

# 為何選擇 Terraform 

