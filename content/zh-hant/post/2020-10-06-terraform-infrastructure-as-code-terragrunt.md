---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Terraform Infrastructure as Code: Terragrunt"
subtitle: ""
summary: ""
authors: []
tags: ["kubernetes", "terraform", "鐵人賽2020", "iac", "aws"]
categories: ["kubernetes", "terraform"]
date: 2020-10-06T11:15:48+08:00
lastmod: 2020-10-06T11:15:48+08:00
featured: false
draft: false
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

# 問題與需求

當團隊已經開始大規模使用 terraform，tf 檔案越來越多。我們為了增加程式碼的重複利用性，會使用 terraform module 將常用的 tf 檔案封裝。

- 隨著導入的規模越來越大，這些 module 會越來越多，而且使用這些 module 的 project 也增加
- 隨著管理的 infrastructure 越來越複雜，為了描述這些本來就很複雜的 infrastructure，module 不只越來越多，還會出現 module 引用其他 module，大 module 使用小 module 的 nested module
  - 這點在複雜的 provider 中常出現，例如
    - 使用 terraform 描述網路架構
    - 描述複雜的 IAM & Role
    - terraform vault-provider
- 管理的環境越來越多，例如 dev, staging, prod,...，每個環境都需要獨立的工作空間，造成大量重複的 tf code

使用一段時間 terraform ，很快就會發現的第一個問題是：不論怎麼從 tf 檔案中提取重複部分，做成 module，還是有很多部分的 tf code 是完全重複的，例如：

- 每個 module 會定義的 variable (argument)，使用這個 module 的上層會需要提供傳入 variable
- 每個 module 都會需要提供 provider

Terraform 的語法要求上面這些參數都明確的定義，這讓整個 module 或資料夾的描述非常清楚。但會處就是，這些描述的參數道出都是，而且不斷的重複，每個 module 或資料夾都要提供，不然在 terraform validate 時會因為應提供參數未提供，導致錯誤。雖然立意良好，但卻嚴重違反 DRY (Don't Repeat Yourself) 的原則

- module 多層引用，project 引用大 module，大 module 又引用小 module
- 開始感覺 backend 與 provider 的 code 比其他功能 code 多了

有沒有可能用其他工具，避免這些重複的參數，backend，provider 等等？

# Terragrunt

推薦有大量使用的團隊，直接使用 [Terragrunt](https://terragrunt.gruntwork.io/) 這款工具。

他是一層 terraform 的 wrapper
- i.e. 執行 terraform plan -> terragrunt plan
- terragrunt 會先解析，產生重複的 code，然後再執行 terraform
- 編輯時只要寫一次，terragrunt 代為在其他地方產生重複的 code
- 產生的 code 會被隱藏與 cache

Terragrunt 有許多功能，例如
- 處理 Backend，provider，與其他不斷重複的 tf code
- 處理多環境下重複的 tf
- ...[完整功能請見官方文件](https://terragrunt.gruntwork.io/docs/)

導入 Terragrunt 可以避免重複代碼，降低維護成本，提升生產效率

# 使用情境

上述說明可能不太清楚，我們實際看範例，以[前幾篇我們使用的範例 repository](https://github.com/chechiachang/terraform-playground) 為例子，把 gcp 的資料夾目錄應該長這樣：

可以很清楚見到底下幾個東西不斷重複
由於 my-new-project, gke-playground, national-team-5g 三個專案是獨立的專案，各自可以獨立運行。但其實同屬於同公司的專案，可能許多內容都是重複的。

```
tree gcp

gcp
├── README.md
├── Makefile
├── my-new-project/
│   ├── terraform.tf
│   ├── terraform.tfvars
│   ├── variable.tf
│   └── provider.tf
├── gke-playground/
│   ├── terraform.tf
│   ├── terraform.tfvars
│   ├── variable.tf
│   └── provider.tf
├── national-team-5g/
│   ├── dev
│   │   ├── terraform.tf
│   │   ├── terraform.tfvars
│   │   ├── variable.tf
│   │   └── provider.tf
│   ├── stag
│   │   ├── terraform.tf
│   │   ├── terraform.tfvars
│   │   ├── variable.tf
│   │   └── provider.tf
│   └── prod
│       ├── terraform.tf
│       ├── terraform.tfvars
│       ├── variable.tf
│       └── provider.tf
├── templates/
└── modules/
```

可以很清楚見到底下幾個東西不斷重複
- provider.tf 這裡描述使用的 provider，這邊只有使用 gcp provider，所以是完全一樣重複
- variable.tf 是定義的參數
- terraform.tfvars 是傳入的參數，也就是實際各專案各自的執行參數
- national-team-5g 的專案下，又各自拆分多個執行環境，每個環境獨立，所以又有許多重複的 code

這邊的目的，是有系統化的處理這些重複的代碼

```
gcp
├── terraform.tfvars        # gcp 共用的參數
├── terragrunt.hcl          # gcp 共用的程式碼
├── national-team-5g/
│   ├── terraform.tfvars    # national-team-5g 共用的參數
│   ├── terragrunt.hcl      # national-team-5g 共用的程式碼
│   ├── dev
│   │   ├── terraform.tfvars  # dev 的參數
│   │   └── terragrunt.hcl    # dev 環境自己的程式碼
│   ├── staging
│   │   ├── terraform.tfvars  # staging 的參數
│   │   └── terragrunt.hcl    # staging 環境自己的程式碼
│   └── prod
│       ├── terraform.tfvars  # prod 的參數
│       └── terragrunt.hcl    # prod 環境自己的程式碼
```

差異非常多是吧，但這邊只是從資料目錄結構看，其實如果從 tf 檔案內部的程式碼看，裡面的代碼更是精簡到不行，用起來非常的爽XD

# 安裝

- 去 release 頁面找適合的執行檔案
- 下載

```
chmod u+x terragrunt
mv terragrunt /usr/local/bin/terragrunt
```

[詳細文件請見](https://terragrunt.gruntwork.io/docs/getting-started/quick-start/)

# 範例

Terragrunt 的 DRY feature，其實內容都大同小異

├── national-team-5g/
│   ├── dev
│   │   ├── terraform.tfvars  # staging 的參數
│   │   └── provider.tf
│   ├── stag
│   │   ├── terraform.tfvars  # staging 的參數
│   │   └── provider.tf
│   └── prod
│       ├── terraform.tfvars  # prod 的參數
│       └── provider.tf

例如

national-team-5g/dev/provider.tf
```
provider "google" {
  version = "~>v3.25.0"
  credentials = file(var.credential_json)
  project = var.project
  region  = var.region
}
```

改成

national-team-5g/dev/terragrunt.hcl
```
generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite"
  contents = <<EOF
provider "google" {
  version = "~>v3.25.0"
  credentials = file(var.credential_json)
  project = var.project
  region  = var.region
}
EOF
}
```

執行
```
cd national-team-5g/dev
terragrunt plan
```

關於參數
- var.region 是本地參數，可以依據 dev/staging/prod 參數各自設定
- var.project 這個是整個 national-team-5g 都共用的參數，可以進一步提高到更上層
  - i.g. 放在 national-team-5g/terraform.tfvars 檔案裡面，透過 terragrunt.hcl 傳遞。

# Functions

tf 檔案，在許多 block 中禁止使用 variable，這層限制有其考量，但是缺點是造成許多 hard coded 的程式碼。

Terragrunt 產生的程式碼，由於是在 terragrunt 執行後，terraform 執行前，因次沒有這層限制，可以做許多事情，例如 code generate 以及 function 運算，terragrunt 提供許多內建 function，這邊只介紹常用幾個。

- [find_in_parent_folder()]()
- [path_relative_to_include()]()

範例兩個檔案

project/dev/terraform.hcl
```
include {
  path = find_in_parent_folders()
}
```

project/terraform.hcl
```
env = path_relative_to_include()
```

最後 parse 後的結果

project/dev/terraform.hcl
```
env = "dev"
```

做了兩件事
- 要求 project/dev 去上層尋找 terraform.hcl，並且引入其中的設定 (env="")
  - 子專案可以 include 母資料夾的程式碼
- 匯入上層 project 時，寫入相對的路徑 (dev)，並且帶入 (env="dev")
  - 母專案可以為各個子目錄配置相對路徑

[其他內建 function 請見官方文件](https://terragrunt.gruntwork.io/docs/reference/built-in-functions/)

# 小結

Terragrunt 可以精簡程式碼，大福提升生產效率，然而在還不熟悉 terraform 核心功能之前，不建議過早導入，會導致多餘的學習成本。
