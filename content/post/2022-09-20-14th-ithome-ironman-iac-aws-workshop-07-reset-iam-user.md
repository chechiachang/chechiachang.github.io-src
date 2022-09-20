---
title: "14th Ithome Ironman Iac Aws Workshop 07 Reset Iam User" # Title of the blog post.
date: 2022-09-20T18:30:06+08:00 # Date of post creation.
description: "Article description." # Description used for search engine.
featured: true # Sets if post is a featured post, making appear on the home page side bar.
draft: false # Sets whether to render this page. Draft of true will not be rendered.
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

昨天我們建立 IAM Group 與 policy，並說明 policy 管理原則。
- 然而昨天最後創建 user 時，我們關閉了 `create_login_profile = false` 的選項
  - 這是為了避免當前的登入機制被覆蓋掉，影響 root account Administrator 的使用
- 更改 login 方式，在某些極端的情形下，有可能讓 Administrator 自己覆蓋自己的 login 設定後，讓自己無法登入

如果你是管理員，在更改 admin 帳號的權限與登入設定時，一定要多加注意
- 如果不幸改壞，無法登入，就只能再去找出 root account root user 帳號來解救了
  - 如果是 root account root user 把自己的 login 改壞，就會很痛苦，要請 aws support 來救你

本日進度
- [x] root 中設定 IAM User
  - [x] 將手動產生的 Administrator 的 IAM User import terraform 中
  - [x] 補上 root account IAM Policy
  - [x] 補上 root account IAM Group
  - [ ] reset root account IAM user login profile & pgp key

[iThome 鐵人賽好讀版](https://ithelp.ithome.com.tw/articles/10290931)

[賽後文章會整理放到個人的部落格上 http://chechia.net/](http://chechia.net/)

[追蹤粉專可以收到文章的主動推播](https://www.facebook.com/engineer.from.scratch)

![https://ithelp.ithome.com.tw/upload/images/20210901/20120327NvpHVr2QC0.jpg](https://ithelp.ithome.com.tw/upload/images/20210901/20120327NvpHVr2QC0.jpg)

---

### Enhance User Login Security

Gruntwork Guide 在完成 group 與 policy 設定後，下一個需要做的是加強 user 登入的安全性

需要做的事情有
- [啟用 MFA policy](https://docs.gruntwork.io/guides/build-it-yourself/landing-zone/production-grade-design/mfa-policy)
- [設定嚴格的 password policy](https://docs.gruntwork.io/guides/build-it-yourself/landing-zone/production-grade-design/password-policy)
- 建立 login profile: password 後，使用各個成員的 gpg key 加密 (encrypt) password，只有成員自己可以解開自己的 password

### [MFA Policy](https://docs.gruntwork.io/guides/build-it-yourself/landing-zone/production-grade-design/mfa-policy)

[Multi-factor authentication](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa.html) 是常用的認證方式
- 在使用 AWS API 的時候，除了帳號密碼 / access key 以外，需要第二層登入裝置做驗證
- AWS 支援許多不同形式的 MFA 裝置
  - 虛擬的 MFA 裝置 ex. 跟 google authenticator 一起使用
  - 硬體的 MFA 裝置 ex. 符合 FIDO2 標準的 YubiKey 等等
- 本 workshop 會實作虛擬的 MFA 裝置，讓使用者使用 Google Authenticator 登入才能使用 API

然而 [如 Gruntwork Guide 在 MFA Policy](https://docs.gruntwork.io/guides/build-it-yourself/landing-zone/production-grade-design/mfa-policy)所述，要 enforce MFA 到所有的 AWS API 會有諸多困難
- 如果我們要求所有 AWS API 都過 MFA，有些來源可能很難做 MFA
  - ex. EC2 VM 上的一個 application 也需要打 AWS API，但在 VM 上就很難取得 Google Authenticator 的認證碼
  - ex. 新的 IAM User 剛新建，沒有 MFA，也就無法登入設定自己的 MFA，變成雞生蛋蛋生雞

Gruntwork Guide 中建議在以下情境中啟用 MFA 就好
- security 以外的 child-account (dev/stag/prod) 的所有 iam-role 都開啟 MFA
  - 當我們要使用 security/iam-user assuem 到另外一個 account/iam-role 時，需要 MFA 認證才可 assume role
  - 然後把 security 以外的 child-account [開啟 global 的 trust policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa_configure-api-require.html#MFAProtectedAPI-user-mfa) ，這樣設定就很單純
    - 不會 block iam-user 登入，因為所有 user 都在 security 底下，其他 child-account 沒有 user
- 在 root 與 security account 內，才有 IAM User 與 IAM Group，在這邊啟用 MFA
  - 將 MFA 依據 policy 去設定，透過 policy - group - user 去 enforce user 使用 MFA
  - 新 user 建立時，需要額外建立 "self-management" permissions policy，讓新用戶可以不用 MFA，進行第一次的 MFA 設定


### [Password Policy](https://docs.gruntwork.io/guides/build-it-yourself/landing-zone/production-grade-design/password-policy)

Password Policy 指的是對於 user 自己設定的密碼要符合一定的規範
- [AWS official doc: 如何設定 password policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_passwords_account-policy.html)
- ex. 密碼至少要 32 字元長度
- ex. 密碼要包含英文，數字，大小寫，或特殊字元
- ex. 密碼多久需要更新一次
這些 password policy 可以大幅強化所有 User 的密碼安全性

由於我們使用的 external module terraform-aws-iam 已經整合了 password policy，所以我們這邊直接在 input 中開啟即可以使用

### PGP key

[pgp (Pretty Good Privacy)](https://zh.wikipedia.org/zh-tw/PGP) 是非常常用的非對稱加密工具
- 比較常用的工具如 [OpenPGP](https://www.openpgp.org/) 或是 [gpg (GnuPG)](https://www.gnupg.org/)

為何 iam user 創建會牽扯到 pgp？
- 不管是 gruntwork module 或是 aws terraform-aws-iam module 都支援 pgp
  - 在 admin 新建 User 與 login profile 後，aws api 產生 password，回傳給 admin terraform，這時 admin 需要把第一把 password 傳給 user，讓 user 做第一次登入
  - 這整個傳遞過程，不管從 aws api -> terraform state -> terraform output -> admin -> user，如果是明碼未加密的狀態下，實在不宜傳遞，很有可能被有心中中途攔截
  - 因此我們可以使用 pgp 相關工具來加密

admin 以 gpg(GnuPG) 為例非對稱加密 (local exposure)
- admin 取得新 user (ex. accounting 人員) 的 gpg public key
- admin 產生 user password 後，使用 gpg 工具，以 account 人員的 public key 加密 password
- 獲得一串 encrypted text，傳給 accounting 人員
- accounting 人員使用自己的 private key 用 gpg 工具解密，即可取得明碼 password
  - 只有有 private key 的人可以解開 encrypted text
- accounting 人員使用 password 登入後，會因為 login profile 要求，而被迫更改新密碼，捨棄 admin local 有曝險過的 password

上面的做法 terraform state 與 admin local 會看到明碼 password，不夠安全。

### PGP & keybase.io

[aws 提供一個改進的做法](https://github.com/terraform-aws-modules/terraform-aws-iam/tree/master/modules/iam-user#notes-for-keybase-users)，terraform state 只存 encrypted text
- 這樣可以避免在 terraform state 中與 admin local 的 password 曝險

pre-requisite
- gpg tool
- keybase.io 註冊

安裝 gpg
```
sudo port install gpg

gpg --version
```

[如果第一次使用，可以創建一對 key pair](https://docs.github.com/en/authentication/managing-commit-signature-verification/generating-a-new-gpg-key)
```
gpg --full-generate-key
```

列出自己有的 secret key (private key)
```
gpg --list-secret-keys --keyid-format=long
```

export public key
```
gpg --armor --export 3AA5C34371567BD2

-----BEGIN PGP PUBLIC KEY BLOCK-----
mQINBF9oN7ABEADeJ5BO3RsvfB0RpU3ZtI3AZmLmMfoaQ41QtkLoFEhF0XnSBNhH
....
ARFfAR39B4hHAnA+/+scVFdGT8i9kuYxk8Ocb7zHgULrOBfKEPEQ5XLmdiqAD+DN
jO2IFPM=
-----END PGP PUBLIC KEY BLOCK-----
```

NOTE: private key 是鑰匙，public key 是鎖頭，永遠不要把 private key 傳出去，而是把 public key 傳出去讓別人加密，用 public key 加密過的東西，只能用手上這把 private key 解開，也就是專屬你的

在 keybase.io 上面註冊後，上傳你的 pgp public key
- 依照指示完成步驟
- (optional) 認證 github / domain / 其他網站讓其他人確定這個是你本人

![keybase.io chechiachang 我本人](https://ithelp.ithome.com.tw/upload/images/20220921/20120327MIjudbzimM.png)

### 實際操作：password policy & pgp key

NOTE: 如果不啟用 pgp-key，admin terraform apply 新 user 後拿到的 password 就會是明碼，可以透過 gpg 工具加密，在透過網路傳給對方

這邊我們先使用 Accounting 先做測試，啟用 login profile

NOTE: 你知道自己是 admin，就請不要拿自己的 User 做測試，壞了很麻煩

將 terragrunt.hcl 改成
```
    Accounting = {
      groups               = ["billing"]
      pgp_key              = "keybase:chechiachang"
      create_login_profile = true
      create_access_keys   = false # accounting always use web console, won't use access key
    }
  }
```

接著要改 module 中的 code，將 module 的 output 接出來到上層的 root module

output.tf
```
# https://github.com/terraform-aws-modules/terraform-aws-iam/blob/master/modules/iam-user/outputs.tf
output "keybase_password_pgp_message" {
  description = "Encrypted password"
  value = {
    for key, value in module.iam_user : key => value.keybase_password_pgp_message
  }
}

output "keybase_password_decrypt_command" {
  description = "Decrypt user password command"
  value = {
    for key, value in module.iam_user : key => value.keybase_password_decrypt_command
  }
}
```

然後我們試著 plan
- 預期：產生 accounting login profile，產生 pgp encrypted password text (而不是明碼 password)

```
aws-vault exec terraform-30day-root-iam-user --no-session  --  terragrunt plan

Terraform will perform the following actions:

  # module.iam_user["Accounting"].aws_iam_user_login_profile.this[0] will be created
  + resource "aws_iam_user_login_profile" "this" {
      + encrypted_password      = (known after apply)
      + id                      = (known after apply)
      + key_fingerprint         = (known after apply)
      + password                = (known after apply)
      + password_length         = 20
      + password_reset_required = false
      + pgp_key                 = "keybase:chechiachang"
      + user                    = "Accounting"
    }

Plan: 1 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + keybase_password_decrypt_command = {
      + Accounting    = (known after apply)
      + Administrator = null
    }
  + keybase_password_pgp_message     = {
      + Accounting    = (known after apply)
      + Administrator = null
    }
```

符合預期！
- Output 中 `keybase_password_pgp_message` 的 ` Accounting    = (known after apply)` 應該是加密過的 output
- 應該要加密給 keybase:chechiachang，也就是用我的 gpg key 可以解開

那直接來 apply 試試看

```
aws-vault exec terraform-30day-root-iam-user --no-session  --  terragrunt apply


Outputs:

keybase_password_decrypt_command = {
  "Accounting" = <<-EOT
  echo "wcFMA4U4ylYlNYTfAQ/+KLtNeJqOqK/V3pNdcRh9nvyDw/huJfaYF7Ab/YdKqLKNVySBqc6HY8xedmER5Wn78RlG962/f772u8UlQN4XCOjOLjyOaNL8K0tkeoSVg+XXPx2qJO9Myc1d+74rG57biUD26XpwfS7+ryIjaHf+NzjisExZy2mgiMIzzAlfqTzRAc+jYP11wZcyFGwOe9pMq6BJy7FH5935ndVgNLCgYtSjgIV5b5kWQ3SDr0E9egAHnoAcHs8mni71x7OL7OCc/bS3nJSLz1jRkMoukWyQQ3+lM7Nwi36NSJneIKxW5f7lSxr7Bx+W3mx6gZgb18yRVIwbVW5iDFsAQOFb0zOHUf8tm3tAQ0F79Yeqy9sfLCfUUjVpCENEJe5FtwJkI8EbHKe8mGnYA4dbHaCkIDgVa8TZ4mdXl7yVZx0adlkKFIS48niwPHxMErZYqnRBitUCGdaH0bHcpPcnSVolLljZmXZUrntMjIEb9FGYbgl6hOiRF9MR3RQL5DNmpS7uSqU7V6TyhVbAOJO2oR01Z7hXdAMxZ54O+h06jN7fzvLrUSMWvUz/wp+JJnIDYNwu75Dvicn6NmXrP3fH3M8xmYIEPhpSvOldNzB4DMqQdD6tN+DphFFyvFwuLnWKWKOY+pbNXkd5q0H3A69owxgsONoOL1JqjZgOdcLtWTq+g9XqU5XSRQGo1ei5Ctv2f5yAHZuI2smwJkTA88SuyZqJNwRixw5OPpUDOuWxhK6xftsN7M1/TnioX8Ch3RTow7H0dvMFFD3ocvjG4A==" | base64 --decode | keybase pgp decrypt

  EOT
  "Administrator" = tostring(null)
}
keybase_password_pgp_message = {
  "Accounting" = <<-EOT
  -----BEGIN PGP MESSAGE-----
  Version: Keybase OpenPGP v2.0.76
  Comment: https://keybase.io/crypto

  wcFMA4U4ylYlNYTfAQ/+KLtNeJqOqK/V3pNdcRh9nvyDw/huJfaYF7Ab/YdKqLKNVySBqc6HY8xedmER5Wn78RlG962/f772u8UlQN4XCOjOLjyOaNL8K0tkeoSVg+XXPx2qJO9Myc1d+74rG57biUD26XpwfS7+ryIjaHf+NzjisExZy2mgiMIzzAlfqTzRAc+jYP11wZcyFGwOe9pMq6BJy7FH5935ndVgNLCgYtSjgIV5b5kWQ3SDr0E9egAHnoAcHs8mni71x7OL7OCc/bS3nJSLz1jRkMoukWyQQ3+lM7Nwi36NSJneIKxW5f7lSxr7Bx+W3mx6gZgb18yRVIwbVW5iDFsAQOFb0zOHUf8tm3tAQ0F79Yeqy9sfLCfUUjVpCENEJe5FtwJkI8EbHKe8mGnYA4dbHaCkIDgVa8TZ4mdXl7yVZx0adlkKFIS48niwPHxMErZYqnRBitUCGdaH0bHcpPcnSVolLljZmXZUrntMjIEb9FGYbgl6hOiRF9MR3RQL5DNmpS7uSqU7V6TyhVbAOJO2oR01Z7hXdAMxZ54O+h06jN7fzvLrUSMWvUz/wp+JJnIDYNwu75Dvicn6NmXrP3fH3M8xmYIEPhpSvOldNzB4DMqQdD6tN+DphFFyvFwuLnWKWKOY+pbNXkd5q0H3A69owxgsONoOL1JqjZgOdcLtWTq+g9XqU5XSRQGo1ei5Ctv2f5yAHZuI2smwJkTA88SuyZqJNwRixw5OPpUDOuWxhK6xftsN7M1/TnioX8Ch3RTow7H0dvMFFD3ocvjG4A==
  -----END PGP MESSAGE-----

  EOT
  "Administrator" = tostring(null)
}
```

上面的 PGP message 是加密過的 text，可以放心的傳遞
- 只有我的 private key 能解開，所以就算擴散也沒有什麼風險
- 沒有 private key 的人已經證明無法在有效的時間內解開
- 附上解密的 keybase command 很貼心，有使用 keybase tool 人可以直接解

但我是使用 gpg 而不是 keybase，也是可以解開
```
echo "wcFMA4U4ylYlNYTfAQ/+KLtNeJqOqK/V3pNdcRh9nvyDw/huJfaYF7Ab/YdKqLKNVySBqc6HY8xedmER5Wn78RlG962/f772u8UlQN4XCOjOLjyOaNL8K0tkeoSVg+XXPx2qJO9Myc1d+74rG57biUD26XpwfS7+ryIjaHf+NzjisExZy2mgiMIzzAlfqTzRAc+jYP11wZcyFGwOe9pMq6BJy7FH5935ndVgNLCgYtSjgIV5b5kWQ3SDr0E9egAHnoAcHs8mni71x7OL7OCc/bS3nJSLz1jRkMoukWyQQ3+lM7Nwi36NSJneIKxW5f7lSxr7Bx+W3mx6gZgb18yRVIwbVW5iDFsAQOFb0zOHUf8tm3tAQ0F79Yeqy9sfLCfUUjVpCENEJe5FtwJkI8EbHKe8mGnYA4dbHaCkIDgVa8TZ4mdXl7yVZx0adlkKFIS48niwPHxMErZYqnRBitUCGdaH0bHcpPcnSVolLljZmXZUrntMjIEb9FGYbgl6hOiRF9MR3RQL5DNmpS7uSqU7V6TyhVbAOJO2oR01Z7hXdAMxZ54O+h06jN7fzvLrUSMWvUz/wp+JJnIDYNwu75Dvicn6NmXrP3fH3M8xmYIEPhpSvOldNzB4DMqQdD6tN+DphFFyvFwuLnWKWKOY+pbNXkd5q0H3A69owxgsONoOL1JqjZgOdcLtWTq+g9XqU5XSRQGo1ei5Ctv2f5yAHZuI2smwJkTA88SuyZqJNwRixw5OPpUDOuWxhK6xftsN7M1/TnioX8Ch3RTow7H0dvMFFD3ocvjG4A==" | base64 --decode | gpg --decrypt
```

就取得 Accounting 的初次登入密碼的，趕快到 aws console 上面試試看

NOTE: 想要在 browser 同時多開 aws login session 的話，可以參考 chrome plugin session box

登入 aws web console
- 注意 account ID 是 root account ID
- user 是 Accounting
- password 是剛剛解密的密碼
  - password 尾端如果有 `%` 不是密碼的一部分，是 EOL (End of line) indicator，記得去掉
  - 前面的部分剛好 20 字元，符合我們 login profile 的密碼長度限制

順利登入拉
![Login success as Accounting](https://ithelp.ithome.com.tw/upload/images/20220921/20120327ZL24NpwgEX.png)

Accounting 的權限是不能動用 EC2 API 的，切到 EC2 頁面直接 API Error，也符合預期
![Accounting get permission denied](https://ithelp.ithome.com.tw/upload/images/20220921/20120327GDnxFXArEe.png)

---

上面的變更我們的 PR 如下
- [terragrunt-infrastructure-modules PR](https://github.com/chechiachang/terragrunt-infrastructure-modules/pull/3)
- [terragrunt-infrastructure-live-example PR](https://github.com/chechiachang/terragrunt-infrastructure-live-example/pull/3)

明天還有 Administrator 帳戶需要處理，會再更麻煩一些

---

### TODO 與進度

- [x] 透過 root account 設定一組 IAM User
- [x] 透過 root account 設定多個 aws child accounts
- [x] root 中設定 IAM User
  - [x] 將手動產生的 Administrator 的 IAM User import terraform 中
  - [x] 補上 root account IAM Policy
  - [x] 補上 root account IAM Group
- [ ] security 中設定 IAM User
  - [ ] security 設定 password policy
  - [ ] security 設定 MFA policy
- [ ] security 中設定 IAM Policy & Group
- [ ] dev 中設定 IAM role
- [ ] 允許 security assume dev IAM role
