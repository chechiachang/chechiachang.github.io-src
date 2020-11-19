---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Terraform Infrastructure as Code: Recommended Practices"
subtitle: ""
summary: ""
authors: []
tags: ["kubernetes", "terraform"]
categories: ["kubernetes", "terraform"]
date: 2020-10-05T11:15:48+08:00
lastmod: 2020-10-05T11:15:48+08:00
featured: false
draft: false

menu:
  main:
    parent: "Kubernetes"
    weight: 1
---

This article is part of [從零開始的 Infrastructu as Code: Terraform]({{< ref "/post/2020-06-14-terraform-infrastructure-as-code" >}})
- [Get-started examples / SOP on Github](https://github.com/chechiachang/terraform-playground)
- [Introducation to Terraform Iac: Speaker transcript]({{< ref "/post/2020-06-15-terraform-infrastructure-as-code-transcript" >}})
- [Presentation](https://slides.com/chechiachang/terraform-introduction/edit)

Check my website [chechia.net](https://chechia.net) for other blog. [Follow my page to get notification](https://www.facebook.com/engineer.from.scratch). Like my page if you really like it :)

---

上面講解 Terraform 的基本操作流程，提供範本原始碼，以及一步一步導入的詳細步驟。各位應該都可以依照上面幾篇的說明，開始快樂的使用 Terraform 了。

以下幾篇文章，適合已經使用過 terraform 一點時間，有經驗的團隊，並打算更大規模導入 terraform，正在尋求改善的方向。

- 心得
  - CI/CD 全自動化
  - State backend 選擇
  - 最佳實踐
- 工具
  - Terraform Atlantis
  - Terragrunt

# 工具與文化

新工具提供解決方案，然而單純導入工具後不是就一勞永逸，許多實務上的問題，還是要依賴改善工作流程，並且避免整體運作的錯誤。

其次，不同團隊已有既有的團隊文化，整合新的工具後還是需要磨合，不一定要照單全收。換句話說，工作流程的不斷改進也是解決方案的一環。

# 建議實踐 Recommended Practices

[Terraform 官網有許多建議的實作與導入流程](https://www.terraform.io/docs/cloud/guides/recommended-practices/index.html)，其中大部分的建議我們都已經在前面的幾篇文章中提到，這邊要來說明一下，並補充其他官方推薦的實踐。

- 技術複雜度: 隨著架構的複雜增加，維護整體架構的困難逐漸增加
- 組織複雜度: 隨著團隊規模增長，分工與權責越顯複雜，團隊的協作困難逐漸增加

Terraform 的目的，在於減少上面兩者的複雜度。

# 工作目錄結構

工作目錄 (workspace) 是 terraform 運作的基準點，容納 tf 檔案，通常會使用版本控制工具管理。

# 一個環境一個工作目錄

這個我們在前面的範例已經實踐，基本上目錄為

```
project (git repository)
├── api-server/
│   ├── dev
│   │   └── terraform.tf
│   ├── stage
│   │   └── terraform.tf
│   └── prod
│       └── terraform.tf
├── grpc-server/
│
```
將產品或專案切割成各自獨立的環境，以某專案的某環境作為管理單位

- project-api-server-dev
- project-api-server-stage
- project-api-server-prod
- project-grpc-server-dev
- ...

這麼做有幾個好處：

- 確保產品與環境的獨立
  - 彼此不互相影響
  - 但又可確保彼此的關連性，例如架構相同
- 以環境的為管理單位，換句話說，一組完整的環境 直接對應到 一組完整的工作目錄
  - 管理上非常直觀明確
- 使用工作目錄分配權限與權責
  - 直接為不同團隊分配不同工作目錄的存取權限
  - 權責與工作目錄的明確對應

# 持續評估與改進

自動化程度也是工作流程進步的指標：

- 手動控制
- 半自動化
- 全自動化

導入 terraform 後的我們已經描述過了，內容詳情請見上上篇文章。下面描述官方推薦的從最開始，完全沒有 terraform 經驗開始導入流程，以筆者個人於公司從零開始導入的經驗，非常直得參考。

1. 如何從完全手動操作，變成半自動操作
1. 如何從半自動，變成 IaC (infrastructure as code)
1. 如何從 IaC，變成 IaC 多人協作
1. 進階改進 IaC 多人協作

# 如何從完全手動操作，變成半自動操作

如果團隊應該是還在完全手動控制 infrastructure
- 查驗 (audit) 困難
- 無法複現 (reproduce)
- 拓展 (scale) 困難
- 很難分享 infrastructure 的知識

第一步要執行的是：選擇少部分，可以控制的 infrastructure 開始導入 terraform。所以要做的就是
- 開始使用 terraform
- 如果需要可以參考一些範例專案
  - [Terraform: Get Started collection](https://learn.hashicorp.com/collections/terraform/aws-get-started?utm_source=WEBSITE&utm_medium=WEB_IO&utm_offer=ARTICLE_PAGE&utm_content=DOCS)

開始進入半自動階段後，團隊中的少部分人員開始使用 terraform，手上也有了可運作的少部分 infrastructure as code，可以作為 demo ，或是其他團隊成員的教育訓練，這個可以幫助下一階段的演進。

# 如何從半自動，變成 IaC (infrastructure as code)

目前半自動的工作專案內容應該是：
- Terraform code
- 手動操作的流程
- 一些輔助腳本

下個階段希望繼續推展 terraform 的使用，降低手動步驟與腳本執行。這個階段可以做的事情
- 使用版本控制管理 tf code
  - 這邊假設團隊本來就有使用版本控制，開始將 tf code 導入版本控制的工作流程
  - 開始將先產生的 tf code 移入版本控制
  - 所有團隊都能共享新 tf code 的知識
- 開始使用第一個 terraform module
  - 一個簡單的方式是將重複使用的 infrastructure 抽出，減少重複的 tf code
  - 這邊需要提醒，盡量以完整個 infrastructure 作為單位抽離 tf code 作為 module
    - 完整的 infrastructure 也是在 provider 中間轉成的單位
- 持續推廣團隊內 terraform 的使用
- 開始設定工作準則 (Guidelines) 來描述並規範工作流程
  - 在團隊上不完全熟悉 terraform 前，可以提升工作效率，推廣最佳實踐，並且降低錯誤風險
  - 團隊的架構師可以依據團隊文化形塑工作流程，更符合團隊需求
- 開始導入 configuration management
  - 例如 Chef cookbook
- 私鑰與隱秘資訊管理
  - 導入 vault 來管理
  - terraform 整合 vault，可以使用 terraform 管理 vault 的結構，使用 vault 來管理 terraform 所需的 credentials

# 如何從 IaC，變成 IaC 多人協作

導入版本控制可以降低堆人協作的複雜度，下個階段需要

- 統一跨團隊的工作流程
- 使用 terraform 管理團隊的 IAM 權限

可以執行的改進如下：

- 官方推薦使用 Terraform Cloud 來做後台，我們稍候推薦的幾個免費工具也有相似功能，團隊可以參考使用。這邊專注在需求與方法。
- 開始設計整個組織間的工作目錄結構
  - 工作目錄要反映
    - 獨立的環境與獨立的專案
    - 負責管理的團隊組織，已分配存取權限
  - 這部分的實作後面的文章也會提到
  - 官方推薦的 Terraform Cloud 可見[官方文件](https://www.terraform.io/docs/cloud/guides/recommended-practices/part3.3.html)

# 進階改進 IaC 多人協作

如今團隊已經有多人協作的介面，也有完整的工作流程，我們可以藉由以下改進，達成更堅固的框架

- 官方建議大量導入 Terraform Cloud，但這會超出免費額度
- 我們之後的文章會提供開源版本的解法
  - 簡化工作目錄的管理
  - 明確的 review 與 audit 工作流程
  - 增加 infrastructure 的監測與效能監控，這些都可以使用 terraform 設置

具體實作，請見下篇文章
