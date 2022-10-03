---
title: "14th Ithome Ironman Iac Aws Workshop 09 Modules and password security" # Title of the blog post.
date: 2022-09-21T00:01:14+08:00 # Date of post creation.
description: "Article description." # Description used for search engine.
featured: true # Sets if post is a featured post, making appear on the home page side bar.
draft: true # Sets whether to render this page. Draft of true will not be rendered.
toc: false # Controls if a table of contents should be generated for first-level links automatically.
# menu: main
featureImage: "/images/path/file.jpg" # Sets featured image on blog post.
thumbnail: "/images/path/thumbnail.png" # Sets thumbnail image appearing inside card on homepage.
shareImage: "/images/path/share.png" # Designate a separate image for social media sharing.
codeMaxLines: 10 # Override global value for how many lines within a code block before auto-collapsing.
codeLineNumbers: false # Override global value for showing of line numbers within code block.
figurePositionShow: true # Override global value for showing the figure label.
categories:
  - terraform
tags:
  - terraform
  - iac
  - aws
---

### 使用 aws module 的好處

為何許多開源的 terraform module 內部使用的都是其他的 module，而不是從 resource 單位開始？

[Terraform 官方文件，如何建立 module](https://www.terraform.io/language/modules/develop)

如何建立一個 module
- 根據最常出現的使用情劇與需求
- 專注於業務的需求與抽象，雃後把實作(terraform resource) 在 module 中組合實作出來
- module 也需要考慮 resource 之間的 architecture
- 也要考慮到觀禮是否方便？使用上是否安全？

ex. 我們需求是產生一個 IAM User
- 正常的實作就是寫一個 `resource.aws_iam_user` 達成需求
- 更好的實作是：除了 `iam_user` 外，加上
  - 一定會需要配權限，應搭配 `iam_group` + `iam_policy`
  - pgp encrypt 讓資料更安全
  - `password_policy` 增加密碼安全
  - ...等
- 比起單一一個 `iam_user` 思考的更全面，更接近最佳實踐

在這次的 Best Practice 追尋之旅中，我們會帶大家去看其他團隊所寫出的 terraform module
- 目前已經看了
  - aws 的 terraform module
  - gruntwork 的 terraform module design (我們沒看到 private module，只是跟隨文件自己刻)
- 這些有多年企業解決方案經驗的團隊，寫出來的 terraform module 都會考量許多 security 方面的問題
- 這也是我們前十篇都在專注的方向

一般來說，一個好 module 會帶來很多好處
- 精簡 .tf code，透過 terraform function 與判斷式來產生 resource
- 整合不同 resource 使用時要輸入的 input
- 可以引導使用者的 architecture 設計

能符合需求，參數方便使用，內容邏輯清楚的 module 就是好 module

然而要寫好一個 module 需要很多經驗，不僅要對 aws 元件，架構都很熟悉，還要考量管理與安全。我們有機會再來分享。

為什麼要花這麼多時間講 account / iam / security 的基礎設定？
因為人家寫出來的就是這麼的安全，開頭直接立於不被駭之地

---

昨天使用 reset root IAM user 的密碼，並使用 pgp key 加密保護，今天要進一步強化 IAM 的安全性，包括
- 強化 password policy
- 增加跨帳號 iam role 的 assume permission
- 增加 MFA

本日進度
- [x] root 中設定 IAM User
  - [x] 將手動產生的 Administrator 的 IAM User import terraform 中
  - [x] 補上 root account IAM Policy
  - [x] 補上 root account IAM Group
  - [x] reset root account IAM user login profile & pgp key
  - [ ] root account password policy
  - [ ] aws cross account iam role delegation
  - [ ] root account MFA policy

[iThome 鐵人賽好讀版](https://ithelp.ithome.com.tw/articles/10290931)

[賽後文章會整理放到個人的部落格上 http://chechia.net/](http://chechia.net/)

[追蹤粉專可以收到文章的主動推播](https://www.facebook.com/engineer.from.scratch)

![https://ithelp.ithome.com.tw/upload/images/20210901/20120327NvpHVr2QC0.jpg](https://ithelp.ithome.com.tw/upload/images/20210901/20120327NvpHVr2QC0.jpg)

### password policy

密碼強度的重要性不需要再強調，強迫 user 使用高強度的密碼並且定期更新，才能將地安全風險
想要透過 web console 修改 password policy 的朋友可以看[aws doc: setting account password policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_passwords_account-policy.html)。我們這邊會使用 terraform 配置

修改 terragrunt-infrastructure-modules
- 注意：昨天在 `module.iam_user` 設定的是 login profile 的 password，是管理員配給 user 的第一把 password，並且登入後必須更換密碼
- 今天要設置的是之後的重設密碼都要遵循的規範

如果想要強化密碼管理
- 更長的密碼
- 更多限制
- 定期更新

首先先更改 terraform module，開啟 password policy
- 增加 `resource.aws_iam_account_password_policy`
- 增加 input variable，將 variable 往從上層 input variable 接進來，讓我們可以在最上層調整
  - 可以設定密碼壽命，default 90 天
  - 可以設定最小密碼長度，default 32 字元
- 其他 policy 參數都寫死固定
  - 需要數字，大小寫英文
  - 允許使用者在密碼過期前重設密碼
  - 密碼過期就鎖住帳號不給登入，要請 admin 來 reset
```
# aws_iam_account_password_policy.tf

resource "aws_iam_account_password_policy" "strict" {
  allow_users_to_change_password = true
  minimum_password_length        = var.minimum_password_length
  hard_expiry                    = true
  max_password_age               = var.max_password_age
  require_lowercase_characters   = true
  require_numbers                = true
  require_uppercase_characters   = true
  require_symbols                = true
  password_reuse_prevention      = 0
}

# variables.tf

variable "minimum_password_length" {
  type = number
  description = "The number of days that an user password is valid."
  default = 32
}

variable "max_password_age" {
  type = number
  description = "Minimum length to require for user passwords."
  default = 90
}
```

進行 terragrunt plan，沒問題的話就可以直接 apply
```
aws-vault exec terraform-30day-root-iam-user --no-session  --  terragrunt plan

Terraform used the selected providers to generate the following execution
plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # aws_iam_account_password_policy.strict will be created
  + resource "aws_iam_account_password_policy" "strict" {
      + allow_users_to_change_password = true
      + expire_passwords               = (known after apply)
      + hard_expiry                    = true
      + id                             = (known after apply)
      + max_password_age               = 90
      + minimum_password_length        = 32
      + password_reuse_prevention      = 0
      + require_lowercase_characters   = true
      + require_numbers                = true
      + require_symbols                = true
      + require_uppercase_characters   = true
    }

Plan: 1 to add, 0 to change, 0 to destroy.

aws-vault exec terraform-30day-root-iam-user --no-session  --  terragrunt apply
```

注意更改密碼的副作用
- 由於更改 password policy 是整個 account 通用的，所以也會影響到 administrator 的 password
  - 雖然影響 password，但不影響 access key，所以 terraform 可以正常工作

Apply passsword policy 後，我們使用原先的密碼走 aws web console 登入看看
- 可以使用現有密碼登入
- 嘗試從右上角 User -> security credentials -> change password，可以發現新的 password policy 已經更新了
- 我們便手動更改密碼，以符合新的 password policy
- 更改密碼完成記得存在密碼儲存器中
- 個人習慣耕買密碼完成後，都重新登入，再登入一次，確定密碼正確，權限也沒問題

![Password reset: new password policy enforced](https://ithelp.ithome.com.tw/upload/images/20220921/20120327iUWx24T3IH.png)

### MFA for me

接著我們可以為自己的 IAM User 啟用 MFA 裝置

在右上角 User -> security credentials -> MFA
- 點選 Assign MFA Device
- 選擇 virtual MFA Device，我們這邊示範使用 google authenticator app
  - 畫面上出現 MFA key 的 QRcode，這個 QRcode == key，不能洩漏，離開這個畫面就不會再出現了
  - 使用 google authenticator，新增一組 account，然後掃描 QRCode
  - 底下填入新 account 產生的 6 位數字 token
  - 等待 60 秒
  - 底下填入第二組新 account 產生的 6 位數字 token，確定真的能夠取得正確的 token
- 之後每次登入都需要輸入 MFA

![Enable MFA: Assign MFA Device](https://ithelp.ithome.com.tw/upload/images/20220921/20120327XlAMWxDvcc.png)
![Enable MFA: Assign Virtual MFA Device](https://ithelp.ithome.com.tw/upload/images/20220921/201203277eQhM3xCiI.png)
![Enable MFA: Complete](https://ithelp.ithome.com.tw/upload/images/20220921/20120327cMSbmpYG4o.png)

NOTE: 這裡是 IAM User login 時需要輸入 MFA，我們之後會設定 child account 下 iam-role assume 時都需要輸入 MFA

明天會前十篇的重點之一：cross account 的 iam role 配置 

### TODO 與進度

- [x] 透過 root account 設定一組 IAM User
- [x] 透過 root account 設定多個 aws child accounts
- [x] root 中設定 IAM User
  - [x] 將手動產生的 Administrator 的 IAM User import terraform 中
  - [x] 補上 root account IAM Policy
  - [x] 補上 root account IAM Group
  - [x] reset root account IAM user login profile & pgp key
  - [x] root account password policy
  - [ ] aws cross account iam role delegation
  - [ ] root account MFA policy
  - [ ] (Optional) Cloudtrail
  - [ ] (Optional) terraform aws config
- [ ] security 中設定 IAM User
  - [ ] security 設定 password policy
  - [ ] security 設定 MFA policy
- [ ] security 中設定 IAM Policy & Group
- [ ] dev 中設定 IAM role
- [ ] 允許 security assume dev IAM role
