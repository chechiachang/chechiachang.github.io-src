---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Terraform Infrastructure as Code: Example repository"
subtitle: ""
summary: ""
authors: []
tags: ["kubernetes", "terraform"]
categories: ["kubernetes", "terraform"]
date: 2020-10-02T11:15:48+08:00
lastmod: 2020-10-02T11:15:48+08:00
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

上面講了很多 terraform 的操作範例，應該看到這裡，對於 terraform 基本上是什麼東西，應該有些概念了。然而這樣還不能算是學會 terraform，這種工具的東西一定要有實際操作過的經驗才算是學會。

可以直接參考 Terraform 官方的 Get-started 文件來操作學習，我這邊也提供一個 Git repository 讓大家上手，當作初次操作的框架。

### 提供做為範例的原始碼

這個 Github Repository 是我給社群演講所使用的範例，第一次使用的可以參考

https://github.com/chechiachang/terraform-playground
```
tree
├── README.md
├── SOP.md
├── aws/
├── azure/
└── gcp/
```

### TL;DR

選擇使用的雲平台，這邊提供三家範例，例如我這邊使用 gcp，當然你就要準備 GCP 的帳號，並且下載有執行權限的用戶 credential json key 等等。

雖然我沒收 gcp 錢，這邊還是推廣一下 gcp 的 free credit 試用。阿要用 Azure Cloud 的 free credit 來執行這個範例也是完全沒問題，非常夠用。唯有 AWS 的試用方案跟剩下兩家不太一樣，這個 repository 起的服務可能會超過 AWS 的免費額度涵蓋範圍，總之請自己注意。

```
git clone https://github.com/chechiachang/terraform-playground
cd gcp
DIR=my-new-project make project

cd my-new-project
vim *tf

terraform init
terraform plan
terraform apply
```

這樣應該就會跑完。然後我們講解幾個地方。

### 工作目錄

Terraform 預設是以當下執行的目錄作為基準，掃描資料夾中的 .tf 檔案。所以可以把一個一個獨立的專案先用資料夾裝好，彼此內容互不干涉。

我們這邊創建新的 subdirectory，這邊是以 my-new-project 為範例。這邊指的 project 只是一個 terraform resource 範圍，可以但不用是一個真實的 gcp project。terraform 執行是以一個 directory 為範圍，不同 project directory 可以透過不同 terraform 指令控制。如果是獨立的服務希望獨立管理也可以切開。

我寫了一個簡單的 Makefile，進一步封裝基本的指令，基本上不需要 Makefile 以外的操作。
make project 是其中一個指令，幫忙創建資料夾、布置 Makefile 與基本的 terraform 設定等等。

如果團隊有多人協作，非常推薦使用統一 Makefile / 或是 bash script 封裝，統一這些編輯的雜事，降低不同人編輯出錯的風險。

### 目錄結構

總之我們現在 cd 到 my-new-project 的工作目錄下，這個目錄代表一個專案。其他的 gke-playgound 與 national-team-5g 也是其他的專案，先忽略他。

```
gcp
├── README.md
├── Makefile
├── my-new-project/
├── gke-playground/
├── national-team-5g/
├── templates/
└── modules/

cd my-new-project
```

進入 my-new-project 下，可以看到裡面已經有一些檔案，我們首先要編輯的是這個 `terraform.tf`
```
my-new-project
├── Makefile
├── provider.tf
├── terraform.tf
└── variables.tf

vim terraform.tf
```

### terraform.tf 是 terraform 本身的設定

這邊是 Terraform Backend 的設定，如果不知道什麼是 terraform backend 這個我們明天的文章會講。這邊使用的 backend 是 terraform 官方自家的 [terraform cloud](https://app.terraform.io)，可以在網站上

- 註冊使用者，填到底下 `organization` 這裡
- 創建一個 workspace，填到 `workspace.name` 這裡

```
terraform {
  # Create a remote organization on https://app.terraform.io
  backend "remote" {
    # Provide terraform credential by
    # - terraform login (suggested)
    # - use User API Token
    #token        = ""
    hostname     = "app.terraform.io"
    organization = "chechia"

    workspaces {
      name = "terraform-playground"
    }
  }
}
```

### provider.tf 是 provider 的設定

terraform client 會把 tf 檔案拿來運算，透過 Provider ，將需求實際轉化成 API call ，然後送到公有雲或是其他目標。這邊就只講到這樣。

provider 為了工作，可能會需要提供一些參數，例如 google 的 provider 會需要在這裡提供 credential_json 的路徑，請把它放在適合的地方，然後用絕對路徑指向 google

NOTE: 不要 commit credential key 到 git repository 裡面。可以放到外層資料夾，或至少要 gitignore 掉。

```
provider "google" {
  version = "~>v3.25.0"

  credentials = file(var.credential_json)

  project = var.project
  region  = var.region
}
```

### variable.tf 做參數的存放點

雖然上面 tf 檔案使用了 terraform / provider / variable ，但 terraform 掃描檔案時，檔名本身並不會影響。也就是說，參數你想擺哪就擺哪。不過上面是常見的命名慣例，這樣擺人類比較容易找得到。

variable 這邊設定的參數，比較像是 arguments，也就是當其他位置的 tf 檔案，引用這個資料夾作為 module 的時候，作為參數輸入的 placeholder，其他 tf 檔案可以使用 variable 關鍵字定義的參數，例如: var.project，或是 provider.tf 裡的 var.credential_json。

variable 關鍵字也可以定義 default 預設值，如果沒有定義 default，也沒有從外部傳入 argument，會在 validate 時造成 error。

```
# Global
variable "project" {
  type    = string
  default = "myproject"
}

variable "credential_json" {
  type    = string
  default = "../credentials/gke-playground-0423-aacf6a39cc3f.json"
}

variable "region" {
  type    = string
  default = "asia-east1"
}
```

### Create

這裡我們試著創建一台 GCE，使用下列指令，會發現多了一個檔案 compute_instance.tf。

```
NAME=my-new-gce make gce

my-new-project
├── Makefile
├── compute_instance.tf
├── provider.tf
├── terraform.tf
└── variables.tf
```

內容大概是

```
module "my-new-gce" {
  source = "../modules/compute_instance"
  providers = {
    google      = google
  }

  project      = var.project
  name         = "my-new-gce"
  image        = "https://www.googleapis.com/compute/v1/projects/centos-cloud/global/images/centos-7-v20200429"
  machine_type = "n1-standard-1"

  network    = "projects/${var.project}/global/networks/myproject"
  subnetwork = "projects/${var.project}/regions/asia-east1/subnetworks/myproject"
}
```

module 關鍵字定義一組資源，[具體的內容是這裡](https://github.com/chechiachang/terraform-playground/tree/master/gcp/modules/compute_instance)，簡單來說可以把一堆 tf 檔案放在一塊，然後把需要的參數使用 variable.tf 拉出去，讓其他地方引用。

source = "" 是實際引用的 module 來源

底下是這個 module 需要用到的參數，例如 project, name, image, machine_type,... 等是 gce 這個 module 需要的參數。

### Makefile

NAME=my-new-gce make gce
這行指令與 terraform 無關，只是一個快速生成 compute_instance.tf 的小腳本。使用這個腳本可以

- 快速產生 tf 檔案
- 產生標準化的 tf 檔案，所有 project 的 compute_instance 都長一樣
- 抽換名子 name

使用 symbolic link 讓所有 project 資料夾使用同一個 Makefile，keep your code DRY。

最後就是常規的 plan 與 apply，這邊沒有什麼特別的。

```
terraform plan
terraform apply
```

### 小結

- 有規律地整理 project 可以降低維護成本
- 善用 module 封裝，可以提高整體的重用性與易用姓，提高開發效率
- 使用 template tf 可以加速重複的資源產生步驟

問題: 此時的資料夾中還是充滿大量重複的 code，例如到處都需要 provider、重複的 module，一大堆重複的東西。有沒有可能再讓我們的程式碼更 DRY 一點呢?

[Terragrunt](https://github.com/gruntwork-io/terragrunt) 幫我們實現這點，非常值得使用的工具。請見下篇分享。
