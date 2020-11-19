---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Terraform Infrastructure as Code: Backends"
subtitle: ""
summary: ""
authors: []
tags: ["kubernetes", "terraform"]
categories: ["kubernetes", "terraform"]
date: 2020-10-04T11:15:48+08:00
lastmod: 2020-10-04T11:15:48+08:00
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

