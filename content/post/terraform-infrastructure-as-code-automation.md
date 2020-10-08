---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Terraform Infrastructure as Code: CI/CD automation"
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

- 心得
  - CI/CD 全自動化
  - State backend 選擇
  - 最佳實踐 https://www.terraform.io/docs/cloud/guides/recommended-practices/index.html
- 工具
  - Terraform Atlantis
  - Terragrunt

# CI/CD 全自動化

當公司成功導入 terraform ，並且整合 Git-flow 的工作流程後，應該可以很明顯的感受到，整體的 infrastructure 產出穩定度有大幅提升，畢竟軟體工程中 code review 是穩定度的核心關鍵之一，而導入 terraform 與 infrastructure as code 讓 infrastructure 也能在合理的工作流程中被層層 review。

stable master -> feature/add-new-infra -> PR feature/add-new-infra -> master

feature branch merge 進去 master 之後，就確定是 review 過而且穩定的程式碼，再由工程師 pull 最新的 master ，然後在本地執行 terraform apply，把 infrastructure 生出來。

這樣做本質不會有什麼大問題，畢竟 code 已經是穩定。然而，實務上卻還是會出現偶發的問題。例如：使用錯誤的 credentail 或 context，導致 dev 或 staging 的 infrastructure apply 到 prod 上，直接 p0 issue 大爆發，SRE 都跪著上班。又例如：使用錯誤的 master 版本 apply，結果也是服務掉線，整個 team 跪著上班。

關鍵：團隊整體的安全性，是由程度最菜的同事決定。

對我就是在說你XD。然而人都會菜，而人事成本也是公司經營的關鍵考量，相信所有同事都大神是不切實際的，不如改進工作流程，近一步降低人為操作失誤的可能。人的問題，根本之道還是教育，然而我們可以試著用技術與工具降低風險。

以下的做法，可能會協助避免這個問題。我們要做的就是 CI/CD 的全自動化。

# 需求

- 避免 apply 失誤
  - 避免愚蠢的錯誤
    - 環境切換錯誤
    - apply 錯版本
    - (愚蠢的錯誤比你想的要多，出現後會讓你三觀大開)
- 加速工作流程
  - PR 結束後，在合適的時間自動 apply
  - 自動回報結果
  - 出錯自動 rollback 上個穩定版本
- 最小權限原則 (least privilege access)
  - 原本工程師為了 apply ，會有 admin 權限的 credential
  - 移轉到安全的 CI/CD server 上，在 server 上執行
  - 工程師不再握有這些超級管理員權限，避免工作機被駭的安全隱憂
    - NOTE: 工程師被釣魚 (phishing) 或是社交工程攻擊 (social engineering attacks) 才是導致公司服務被害的主因，不可不防

# 解決方案

- 選擇安全的 CI/CD server，例如在內網的 self-hosted Jenkins server
- 將 terraform 的執行點，從工程師本機移轉到 CI/CD 服務器上
- 更改 CI/CD ，執行以下步驟
  - Terraform validate
  - Terraform plan 的結果輸出到 Github / Slack
  - plan 結束後停住 CI/CD，發送一個 apply request 到 Github comment，不再繼續執行 apply
  - SRE 主管只要透過 Github comment 或是 Slack bot 就可以選擇合適的時間，approve apply
- 最後移除大多數工程師的 terraform 權限

# 範例

事實上，不同家的 CI/CD server，工作流程都是類似

- checkout
- initialize tools / SDK (ex. az/aws/gcloud client)
- inject public cloud credential (ex. Azure/AWS/GCP key)
- terraform validete
- terraform plan
- terraform apply
  - (option) require manual approve

如果是 Jenkins 的使用者，可以參考 [Azure 提供的範例](https://github.com/Azure/terraform-with-jenkins-samples/blob/master/jenkins-pipelines/create-vmss-from-image/provision/Jenkinsfile)

# 環境管理

在人工 apply 的工作流程中，工程師需要自行切換環境，例如 git repo 工作目錄如下

```
tree

project
 ├── dev
 ├── staging
 └── prod

cd project/dev; terraform plan  # plan staging
cd project/prod; terraform plan # plan prod
```

這是相對比較安全的做法，在對的資料夾目錄下，就會 apply 到正確的環境，程式碼與環境有緊密的對映。除了以下幾種情形

- 想要部署 dev，結果沒注意到自己在 staging 或是 prod
- 有一部分的 input variable 會影響結果，然後又輸入錯誤的 input 到錯誤的環境上

對很愚蠢，但我都見過（氣血攻心）。

既然導入了自動化，環境的切換可以自動切換，例如

- 所有 feature branch 執行 CI/CD server 上的本地測試
  - lint
  - init
  - validate
- 所有 PR 都會觸發新的 dev 環境部署
  - plan
  - apply
  - 測試腳本
- 所有 master merge / push 都會觸發 staginge 部署
  - QA 測試
  - 壓力測試
- (optional) 所有 release candidate tag 會部署到 release candinate
  - release management
- 所有發布版本的 tag (ex. 1.1.0 / 1.2.0-release) 會部署 prod
  - 當然要事先通知相關人士 stack holders

資深工程師只要控制 branch / tag 就可以控制發布。

你說這樣，萬一天兵去自己打 tag 打錯 commit，或是推錯 branch 推到 master或是 release candidate，還不是依樣爆掉。那你可以把 master 與 release branch 鎖起來 (protected branch) ，然後把 tag push 權限鎖住。

你說還是錯
那我...
...們看下一段 orz

# 安全性

雖然說是自動化改善工作流程，然而收回存取權限，對於服務的整體安全性大幅提升，畢竟是可以更改 infrastructure 的管理員帳戶。Terraform 既然能夠新增修改雲端的 infrastructure，這個帳號的權限是相當大的，萬一金鑰(GCP/AWS/Azure credentail) 流出或遭駭，後果都是毀滅性的，例如可以直接刪除服務的 infrastructure，或是修改防火牆的規則，偷埋其他金耀，...等於是整座公有雲送給駭客。所以我們使用 Terraform 應該要慎重考慮存取權限的安全性。

本來是每個 SRE 的本機電腦上，可能都會有這把帳戶權限。

如果是 self-hosted Jenkins server，或是 Github enterprise server，把服務權限移轉到這些服務器，便可以確保金鑰永遠都在公司的防火牆內部網路，更加大幅度的提升整體的安全性。

# 其他

可以進一步做金鑰權限分割，將底下四個權限透過公有雲的 IAM role 去切割。要是萬一金鑰還是外洩了，可以降低損失。

- 讀取
- 新增
- 修改
- 刪除

你說這個不用自動化就可以做，我說如果分割金鑰然後人工自己切換操作，反而會增加操作的複雜度，增加錯誤的機會。然後工程師的痛苦程度，與手上的金鑰數量成正比。

或是利用環境存取金耀分割，把金耀進一步切割成不同的權限，萬一掉了，損害也控制在一個環境之內。例如：

- dev
- staging
- prod

不同環境的 infrastructure ，在創建初期就是透過不同的帳號產生的，彼此不會有不乾淨殘留的帳號權限。

# 小結

這邊就講兩件事

- 自動化可以防呆
- 自動化可以增加安全

# 參考文件

[Terraform Official doc: Running Terraform in Automation
](https://learn.hashicorp.com/tutorials/terraform/automate-terraform?in=terraform/automation&utm_source=WEBSITE&utm_medium=WEB_IO&utm_offer=ARTICLE_PAGE&utm_content=DOCS)
