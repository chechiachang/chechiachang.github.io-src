---
title: "Provision Iam User" # Title of the blog post.
date: 2022-09-19T11:59:27+08:00 # Date of post creation.
description: "Article description." # Description used for search engine.
featured: true # Sets if post is a featured post, making appear on the home page side bar.
draft: false # Sets whether to render this page. Draft of true will not be rendered.
toc: false # Controls if a table of contents should be generated for first-level links automatically.
# menu: main
featureImage: "/images/path/file.jpg" # Sets featured image on blog post.
#thumbnail: "/images/path/thumbnail.png" # Sets thumbnail image appearing inside card on homepage.
shareImage: "/images/path/share.png" # Designate a separate image for social media sharing.
codeMaxLines: 10 # Override global value for how many lines within a code block before auto-collapsing.
codeLineNumbers: false # Override global value for showing of line numbers within code block.
figurePositionShow: true # Override global value for showing the figure label.

tags: ["terraform", "iac", "aws", "鐵人賽2022"]
categories: ["terraform"]
---

昨天我們為每個環境(dev / stag / prod ...) 設定一個 aws organization account

今天要使用 terraform 設定 AWS IAM User
- [ ] root 中設定 IAM User
  - [ ] 將手動產生的 Administrator 的 IAM User 加到 terraform 中
- [ ] security 中設定 IAM User
  - [ ] security 設定 password policy
  - [ ] security 設定 MFA policy

[iThome 鐵人賽好讀版](https://ithelp.ithome.com.tw/articles/10290931)

[賽後文章會整理放到個人的部落格上 http://chechia.net/](http://chechia.net/)

[追蹤粉專可以收到文章的主動推播](https://www.facebook.com/engineer.from.scratch)

![https://ithelp.ithome.com.tw/upload/images/20210901/20120327NvpHVr2QC0.jpg](https://ithelp.ithome.com.tw/upload/images/20210901/20120327NvpHVr2QC0.jpg)

# Accounts & IAM Users

今天要使用 Terraform 設定 IAM Users。
- 未來所有的 User 都會透過 terraform 設定並管理
- Day02 設定的 root account IAM User: Administrator 雖然是手動建立的，我們一樣需要把他匯入到 terraform 中

然而上個 PR 中，我們的 terraform module 中並沒有設定 IAM User 的功能，也就是這段 code 是沒有發揮功能
[https://github.com/chechiachang/terragrunt-infrastructure-live-example/pull/1/files#diff-62920ff868733e1c625c23fe7ffd6c93bebd87ae16b865869bf682e29b082a99R54-R67](https://github.com/chechiachang/terragrunt-infrastructure-live-example/pull/1/files#diff-62920ff868733e1c625c23fe7ffd6c93bebd87ae16b865869bf682e29b082a99R54-R67)
```
  users = {
    alice = {
      groups               = ["full-access"]
      pgp_key              = "keybase:alice"
      create_login_profile = true
      create_access_keys   = false
    },
    bob = {
      groups               = ["billing"]
      pgp_key              = "keybase:bob"
      create_login_profile = true
      create_access_keys   = false
    }
  }
```

我們這邊一樣嘗試把這個 users (map) 的功能補上

### 使用開源 module 實作 IAM User

- 使用的開源 terraform module 是 [terraform-aws-modules/terraform-aws-iam](
https://github.com/terraform-aws-modules/terraform-aws-iam/tree/master/modules/iam-user)
  - 是 aws 官方維護的開源 terraform module，品質很好，放心使用

需求整理
- 要產生 IAM User
- input: 一個 map users = {}
- output: 多個 user
- 要產生 IAM Group 與 IAM Policy

增加 IAM User PR 的 commit 在此 [https://github.com/chechiachang/terragrunt-infrastructure-modules/pull/1](https://github.com/chechiachang/terragrunt-infrastructure-modules/pull/1)

於是我們試著執行 terraform plan
```
aws-vault exec terraform-30day-root-iam-user --no-session  --  terragrunt plan

Terraform used the selected providers to generate the following execution
plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # module.iam_group_with_policies_full_access.aws_iam_group.this[0] will be created
  + resource "aws_iam_group" "this" {
      + arn       = (known after apply)
      + id        = (known after apply)
      + name      = "full-access"
      + path      = "/"
      + unique_id = (known after apply)
    }

  # module.iam_group_with_policies_full_access.aws_iam_group_membership.this[0] will be created
  + resource "aws_iam_group_membership" "this" {
      + group = (known after apply)
      + id    = (known after apply)
      + name  = "full-access"
      + users = [
          + "Administrator",
        ]
    }

  # module.iam_group_with_policies_full_access.aws_iam_group_policy_attachment.custom_arns[0] will be created
  + resource "aws_iam_group_policy_attachment" "custom_arns" {
      + group      = (known after apply)
      + id         = (known after apply)
      + policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
    }

  # module.iam_group_with_policies_full_access.aws_iam_group_policy_attachment.iam_self_management[0] will be created
  + resource "aws_iam_group_policy_attachment" "iam_self_management" {
      + group      = (known after apply)
      + id         = (known after apply)
      + policy_arn = (known after apply)
    }

  # module.iam_group_with_policies_full_access.aws_iam_policy.iam_self_management[0] will be created
  + resource "aws_iam_policy" "iam_self_management" {
      + arn         = (known after apply)
      + id          = (known after apply)
      + name        = (known after apply)
      + name_prefix = "IAMSelfManagement-"
      + path        = "/"
      + policy      = jsonencode(
            {
              + Statement = [
                  + {
                      + Action   = [
                          + "iam:UploadSigningCertificate",
                          + "iam:UploadSSHPublicKey",
                          + "iam:UpdateUser",
                          + "iam:UpdateLoginProfile",
                          + "iam:UpdateAccessKey",
                          + "iam:ResyncMFADevice",
                          + "iam:List*",
                          + "iam:Get*",
                          + "iam:GenerateServiceLastAccessedDetails",
                          + "iam:GenerateCredentialReport",
                          + "iam:EnableMFADevice",
                          + "iam:DeleteVirtualMFADevice",
                          + "iam:DeleteLoginProfile",
                          + "iam:DeleteAccessKey",
                          + "iam:CreateVirtualMFADevice",
                          + "iam:CreateLoginProfile",
                          + "iam:CreateAccessKey",
                          + "iam:ChangePassword",
                        ]
                      + Effect   = "Allow"
                      + Resource = [
                          + "arn:aws:iam::706136188012:user/*/${aws:username}",
                          + "arn:aws:iam::706136188012:user/${aws:username}",
                          + "arn:aws:iam::706136188012:mfa/${aws:username}",
                        ]
                      + Sid      = "AllowSelfManagement"
                    },
                  + {
                      + Action   = [
                          + "iam:List*",
                          + "iam:Get*",
                        ]
                      + Effect   = "Allow"
                      + Resource = "*"
                      + Sid      = "AllowIAMReadOnly"
                    },
                  + {
                      + Action    = "iam:DeactivateMFADevice"
                      + Condition = {
                          + Bool            = {
                              + "aws:MultiFactorAuthPresent" = "true"
                            }
                          + NumericLessThan = {
                              + "aws:MultiFactorAuthAge" = "3600"
                            }
                        }
                      + Effect    = "Allow"
                      + Resource  = [
                          + "arn:aws:iam::706136188012:user/*/${aws:username}",
                          + "arn:aws:iam::706136188012:user/${aws:username}",
                          + "arn:aws:iam::706136188012:mfa/${aws:username}",
                        ]
                      + Sid       = "AllowDeactivateMFADevice"
                    },
                ]
              + Version   = "2012-10-17"
            }
        )
      + policy_id   = (known after apply)
      + tags_all    = (known after apply)
    }

  # module.iam_user["Administrator"].aws_iam_user.this[0] will be created
  + resource "aws_iam_user" "this" {
      + arn           = (known after apply)
      + force_destroy = true
      + id            = (known after apply)
      + name          = "Administrator"
      + path          = "/"
      + tags_all      = (known after apply)
      + unique_id     = (known after apply)
    }

  # module.iam_user["Administrator"].aws_iam_user_login_profile.this[0] will be created
  + resource "aws_iam_user_login_profile" "this" {
      + encrypted_password      = (known after apply)
      + id                      = (known after apply)
      + key_fingerprint         = (known after apply)
      + password                = (known after apply)
      + password_length         = 20
      + password_reset_required = false
      + pgp_key                 = "keybase:alice"
      + user                    = "Administrator"
    }

Plan: 7 to add, 0 to change, 0 to destroy.
```

會產生幾個東西
- `module.iam_user["Administrator"]` 是一個 module，裡頭產生 IAM User 與其他 resource
  - `module.iam_user["Administrator"].aws_iam_user_login_profile` 我們有開啟 create login file 的參數，所以 aws terraform module 便產生
- `module.iam_group_with_policies_full_access.aws_iam_policy.iam_self_management` 我們有開啟 create self management policy，所以 aws terraform module 便產生
  - `module.iam_group_with_policies_full_access.aws_iam_group_policy_attachment` 透過這個 attachment 將 IAM policy 關聯到 IAM group，也就是 group 中有 attach 此 full-access policy
- `module.iam_group_with_policies_full_access.aws_iam_group` 是 IAM Group: full-access
  - `module.iam_group_with_policies_full_access.aws_iam_group_membership` 將 IAM User 關聯到 IAM group 也就是 user/Administrator 屬於 group/full-access

AWS 許多資源的描述都用 attachment 的形式描述兩個元件的關聯
- user + group -> `group_membership`
- group + policy -> `group_policy_attachment`
- 像是 RMDBS 的關聯 table，更改關聯時並不會影響到兩個元件本身的內容，調整關聯很彈性

### Terraform Import

由於 Administrator 我們 Day02 已經透過 web console 建立，現在 terraform plan 出來的結果卻也是要 create 一個 new user，這個結果不是我們想要的
- 因為 web console 產生的 User 並沒有在 terraform 中管理，也就是雖然 AWS 上 User 確實存在，但 terraform 中並沒有 state 來描述這個 User，所以 Terraform 不知道這個 plan create 的 User 其實就是 AWS console 上已經存在的 Administrator
  - 不在 terraform state 的元件，terraform 便無法管理

要將已經存在的 AWS 元件，納入 terraform state 進行管理，這個行為我們稱作 import

現在我們要試著 terraform import 已經存在的 User/Administrator
- 首先，先到 terraform registry 去搜尋 aws provider import 的語法及參數
  - 直接 google 元件的名稱 `terraform aws iam user` 通常就會找到
  - [捲到頁面最底下就可以看到 import 語法](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_user#import)

```
# terraform import aws_iam_user.lb loadbalancer
terraform import <address> <username>
```

這邊的 address 需要填入 plan 時預計產生的 resource `aws_iam_user`
- 也就是 `module.iam_user["Administrator"].aws_iam_user.this[0]` 這個 address
- 剛開始學 terraform 可能會還不太清楚 address 為何會長這樣，久了就會了解

可以先從找到 resource 主體為目標慢慢看
- 所謂的 resource 的主體，其實就是 terraform 的基本單位
- 一個 terraform resource 可能就是對應一個 aws 元件
  - `aws_iam_user` -> `iam_user`
  - `aws_iam_policy` -> `iam_policy`

去掉前面的 module 與後面的 index 就可以找到 resource
```
# 其中 aws_iam_user 是 terraform resource
module.<module_name>.aws_iam_user.<iam_user_name>.<iam_user_index>

# 或是這個 address 中  aws_iam_policy 是 terraform resource
module.<module_name>.aws_iam_policy.<iam_user_name>.<iam_user_index>

# module 可以在包其他 module，所以架構複雜的 terraform module，resource address 就愈來越長
module.<module_name>.module.<module_name>.aws_iam_user.<iam_user_name>.<iam_user_index>
```

最上層的 resource 是 `module/iam_user[*]`，對應的 .tf code 是 [user.tf]()
```
module "iam_user" {
  source   = "terraform-aws-modules/iam/aws//modules/iam-user"
  for_each = var.users

  name          = each.key
  force_destroy = true

  create_iam_user_login_profile = each.value.create_login_profile
  create_iam_access_key         = each.value.create_access_keys
  pgp_key                       = each.value.pgp_key
  password_reset_required       = false
}
```
- `module/iam_user` 中包含了許多 terraform resource
  - `aws_iam_user` 是基本 resource
  - `aws_iam_user.this[0]` 後面多了 index suffix，是因為可能在 module 中有使用 `count` 或 `for_each`，造成一個 list 的 `aws_iam_user`，而其中 index 為 0 的就是 `aws_iam_user.this[0]`

terraform 支援許多好用的 build-in function 讓我們可以快速的使用，產生複雜的邏輯，這個之後有空會教大家。或是[參考 2021 iThome 的發文: infrastructure 也可以 for each 之一](https://ithelp.ithome.com.tw/articles/10263624)

回到 import，我們把 terraform import address name 數入後，發現出錯
```
# Bash syntax error
aws-vault exec terraform-30day-root-iam-user --no-session -- terragrunt import module.iam_user["Administrator"].aws_iam_user.this[0] Administrator

zsh: no matches found: module.iam_user[Administrator].aws_iam_user.this[0]
```

這是因為有些 address 字元 bash 中有其他意義的特殊字元，bash 先看不懂了，就無法執行，還沒跑到 terragrunt。我們把 address 前後都增加單引號，讓 bash 把 address 當作字串處理而不要展開 (expension)

```
# Add single quote to escape
taws-vault exec terraform-30day-root-iam-user --no-session -- erragrunt import 'module.iam_user["Administrator"].aws_iam_user.this[0]' Administrator

module.iam_user["Administrator"].aws_iam_user.this[0]: Importing from ID "Administrator"...
module.iam_user["Administrator"].aws_iam_user.this[0]: Import prepared!
  Prepared aws_iam_user for import
module.iam_user["Administrator"].aws_iam_user.this[0]: Refreshing state... [id=Administrator]

Import successful!

The resources that were imported are shown above. These resources are now in
your Terraform state and will henceforth be managed by Terraform.

Releasing state lock. This may take a few moments...
```

顯示為 Import Success 了，就表示我們已經把 aws 存在的 user import 到 terraform state 中

再次 plan，發現從 Plan: 7 to add，變成 Plan: 6 to add, 1 to change
- 表示 terraform 知道 plan 中的 address 要直接對應到 aws 現存的 user/Administrator
- change 中顯示 `+ force_destroy = true` 表示
  - aws 現存的 user/Administrator 沒有這個設定
  - .tf 的 `module.iam_user["Administrator"].aws_iam_user.this[0]` 有這行 code
  - terraform plan 發現 .tf 比現存的 user/Administrator 多設定，於是要多加設定
  - 我們可以依據需求，決定要
    - 更改 .tf，拿掉 `+ force_destroy = true`，這樣 plan 後 terraform 就會覺得兩邊的 user/Administrator 一模壹樣，不需要 change
    - 或是就直接 apply ，讓現存的 user/Administrator 增加 `+ force_destroy = true`

```
aws-vault exec terraform-30day-root-iam-user --no-session  --  terragrunt plan

  # module.iam_user["Administrator"].aws_iam_user.this[0] will be updated in-place
  ~ resource "aws_iam_user" "this" {
      + force_destroy = true
        id            = "Administrator"
        name          = "Administrator"
        tags          = {}
        # (4 unchanged attributes hidden)
    }

Plan: 6 to add, 1 to change, 0 to destroy.
```

### TODO 與進度

- [x] 透過 root account 設定一組 IAM User
- [x] 透過 root account 設定多個 aws child accounts
- [x] root 中設定 IAM User
  - [x] 將手動產生的 Administrator 的 IAM User import terraform 中
  - [ ] 補上 root account IAM Policy
  - [ ] 補上 root account IAM Group
- [ ] security 中設定 IAM User
  - [ ] security 設定 password policy
  - [ ] security 設定 MFA policy
- [ ] security 中設定 IAM Policy & Group
- [ ] dev 中設定 IAM role
- [ ] 允許 security assume dev IAM role
