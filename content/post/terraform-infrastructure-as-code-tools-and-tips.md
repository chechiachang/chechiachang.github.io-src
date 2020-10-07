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

---

# Terraform Backend

剛開始使用 terraform 的時候，大家的第一個範例應該都是 local backend 吧，就是直接在本地 terraform apply，在目前的工作目錄下產生 state 檔案。這個 state 檔案直接 cat 打開來看後，可以發現裡面一切都是明碼的。初學時筆者感覺所謂的 Terraform backend 只是一個存放中繼的 state 資料的 workspace，後來發現完全不是這麼回事，便立刻棄用了 local backend。

之後依照官方推薦就使用了 [Terraform Cloud](https://app.terraform.io/app)，後來便出現許多問題，等等會分析。

最後團隊選用了自家公有雲的 backend，例如
  - AWS S3 作為 state storage，DynamoDB 作為中心化的 workflow lock
  - GCP 

[完整 terraform backend 支援清單可以見官方網站](https://www.terraform.io/docs/backends/index.html)。

這篇文章要來仔細探討所謂的 terraform backend，backend 的重要性，與如選擇適合自己團隊的 backend。

# 問題

如果使用 tf random 產生亂數密碼，直接去 cat state 檔案就可以看到明碼的 random 數值。

多人協作 lock

另外一個解法是，根本不使用 backend，terraform 也支援這樣的做法。雖然[官方也明講 backend are completely optional](https://www.terraform.io/docs/backends/index.html)，但依照筆者的經驗，強烈建議多人團隊務必去啟用，並找尋適合自己的 Backend。


# 需求

- 資訊安全，希望 terraform 使用是安全的，不會暴露敏感資訊
- 多人協作，希望可以同時工作，但又不會互相衝突
- 遠端操作，避免本地操作

# State 存放與鎖

預設的 backend 是 loal backend，也就是執行 terraform apply 後，本地會出現一個 JSON 格式的 state 檔案。然而 local state 會立刻遇到的問題，就是
- 第一個是協作困難，apply 的結果別人看不到，不能接續著做
- 每個人都可以 apply
- 但不同人的 apply 沒有相依性
  - 可是遠端的 infrastructure 有，A B 不同人一起 apply 到 infrastructure 上，可寧就會衝突，或是產生不可預期的錯誤

所以筆者強烈推薦使用外部的 backend 來取代 local backend。多半 backend 會多做許多事，透過控制 state 來確保 infrastrure 的完整性，例如對 state 存取有以下的限制:

- Ａ透過鎖來控制，禁止多人同時存取，例如同時有兩個人 apply 相同或不同檔案，先取得 backend lock 的人執行，後來的人會被 terraform 阻擋
  - 避免多頭馬車的問題
- 確保 state 的唯一性，使用另外一個 repo 的 state 檔案，遠端的 state 會拒絕存取
- 確保 state 的順序，每次 apply 的 state 都是依序產生
  - 如果 state 是舊的，可能就會被遠端的 backend 拒絕，避免使用舊的 apply 覆蓋新的 infrastructure

這些限制，如果使用 local backend 才會容易遇到，使用外部的 backend 其實不容易會發生。Terraform 基於 Infrastructure as Code 實現，可以將整個 terraform repo 視為 code 一部分，這樣就可以想像為何這些 state 限制是重要的。

- state 跟隨 tf 檔案，隨著 tf 檔案的 commit 推進，state 也跟著推進
- commit 1 的 tf 檔案，apply 後產生 state 1
- 如果今天有團隊 force push 了一個 conflict 的 tf 檔案，硬要 apply 的結果也可能造成 infrastructure conflicts
- 如果今天團隊有多個 branch 同時開發，branch A apply 的 state 會與 branch B apply 的 state 也可能造成衝突

# State 手動更改

在很特殊的狀況下，你也可以手動更改 state file，然後 push 上傳，但這點非常不建議，terraform 會自動維護 state 的完整性，手動更改可能會直接破壞正常的 state。什麼情形會用到？就是你的 state 因為某個原因被玩壞，大部分是人為弄壞的。這時候才被迫要手動更改 state。手動更改 state ，講白了不做死就不會死。

```
vault state pull

vim your-local-state-file
# Increment Serial if needed

vault state push
# vault state push -force
```

# Hosted: Terraform Cloud

[Terraform Cloud](https://app.terraform.io/)，是官方提供的解決方案，有提供較多功能，例如在 terraform cloud 的網站上遠端 plan。有提供免費版，提供最多 5 人團隊使用。也有提供進階的方案 $20/user 或是 $70/user，以及 enterprise 版本，可以本地安裝。

使用很簡單，[我在前幾篇提供的範例 repository](https://github.com/chechiachang/terraform-playground)全部都是使用 terraform cloud 作為 Backend。提供
- 遠端的 state 儲存庫
  - 所有團隊成員使用各自帳號登入
  - plan 之前會 sync terraform cloud 上面的 state
- 遠端的 state lock
  - 如果 lock 被人佔據，表示有其他人正在使用，會取消新的操作，避免衝突
- 也提供線上檢視 state ，或是線上修改 state 的功能
  - 貼心小功能，但多半用不到

託管的 Terraform Cloud 作為 backend 他有幾個問題
- 如果要啟用遠端 plan，需要綁定版本控制服務器，例如綁定 Github 或 Gitlab
  - 基於安全性考量，這點很多公司就直接打槍了
    - 暴露原始碼給第三方公司，可能會讓公司的安全性檢驗不過
    - 加上 terraform 的 Git Code，基本上就是所有 infrastructure 的資訊
    - 加上如果有使用 terraform 編輯 IAM 或是 provision vault，等於許多敏感資料都會出現在 terraform repository 中

如果是重視安全性的團隊，則至少要使用可以 self-hosted 的 Terraform Enterprise，而不要使用公有的 Terraform Cloud。然而 Enterprise 我是沒用過，請不要問我價錢。

# Consul

Consul 嚴格來說不是單純的儲存庫，他是 Service Networking 設定與服務發現的解決方案，只是本身帶有 key value 的儲存功能，就被自家整合。換句話說，他不是專門拿來做 terraform backend 的，比較像是如果團隊本來就有使用 consul，可以考慮公用儲存庫，作為 terraform backend。

這是相同公司 Hashicorp 提供的自家的 backend，整合的很完整。但就只是單純的儲存庫，沒有 terraform cloud 的遠端執行啊，或是線上檢視 state 檔案的功能。

可以在公司內部自行架設一組 cluster，然後就可以作為 backend。

問題是
- Consul 這麼大一包，結果只使用了裡面的 kv store
- Consul 是分散式的 Key-value store，不熟悉的話不太好養
  - 換句話說，如果死了救得起來嗎

# Etcd

Etcd 跟 consul 類似，雖然是專業的儲存庫，但是使用這麼複雜的分散式儲存庫，只作為 terraform 的 backend，顯然很不經濟。

可以在公司內部自行架設一組 cluster，然後就可以作為 backend。

一樣只建議已經有在使用 etcd ，且熟悉維運 etcd 的團隊，才考慮使用 etcd 兼作為 terraform backend。

這些分散式的儲存庫，不太容易死，然而萬一死了可能不太好救。

# Public Cloud

[AWS S3 + DynamoDB](https://www.terraform.io/docs/backends/types/s3.html)
[GCP gcs + pg](https://www.terraform.io/docs/backends/types/azurerm.html)
[Azurerm + pg](https://www.terraform.io/docs/backends/types/gcs.html)

只有單純的 state storage 與 lock 的功能，沒有什麼花俏的線上執行或是快速 review。

好處是
- 使用非常單純
- 也是處在安全的內網環境中
- 有於是公有雲提供的服務，基本的 IAM 與權限控管可以直接應用

# Postgresql

[Postgrel 也是一個不錯的選擇](https://www.terraform.io/docs/backends/types/pg.html)

Terraform 並不會帶來大量的資料庫負擔，所以可能會把 terraform 與附載較低的應用，共用資料庫。

使用上作為 state storage 與 lock 很單純沒什麼問題

# 其他

[官方還有提供所有支援的 backend](https://www.terraform.io/docs/backends/types/index.html)

如果 Kubernetes 還有做其他事情的話，請不要用 Kubernetes secret 作為 terraform 的 backend



