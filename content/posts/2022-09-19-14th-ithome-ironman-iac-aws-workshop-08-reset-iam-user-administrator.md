---
title: "Reset Iam User Administrator" # Title of the blog post.
date: 2022-09-20T23:56:47+08:00 # Date of post creation.
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

tags: ["terraform", "iac", "aws", "鐵人賽2022"]
categories: ["terraform"]
---

昨天處理完 Accounting 的 reset password，今天要來 reset root account Administrator 的權限

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

### Reset IAM root user Administrator Password

依照上面的步驟，我們確定可以正常登入，於是可以來可以新建 Administrator 的 login profile
- 由於 Administrator 會需要 access key，所以我們也把他設成 true

```
# terragrunt.hcl
  users = {
    Administrator = {
      groups               = ["full-access"]
      pgp_key              = "keybase:chechiachang"
      create_login_profile = true
      create_access_keys   = true
    },
    Accounting = {
      groups               = ["billing"]
      pgp_key              = "keybase:chechiachang"
      create_login_profile = true
      create_access_keys   = false # accounting always use web console, won't use access key
    }
  }
```

記得更改 module/output.tf，增加 secret key 的 output，而不要只留在 terraform state 裡面

```
# output.tf
output "keybase_secret_key_decrypt_command" {
  description = "Decrypt access secret key command"
  value       = {
     for key, value in module.iam_user : key => value.keybase_secret_key_decrypt_command
  }
}

output "keybase_secret_key_pgp_message" {
  description = "Encrypted access secret key"
  value       = {
     for key, value in module.iam_user : key => value.keybase_secret_key_pgp_message
  }
}
```

試著 plan 一下，預期
- Administrator 會產生一組新的 login profile
- Administrator 會產生一組新的 access key

```
aws-vault exec terraform-30day-root-iam-user --no-session  --  terragrunt plan

Terraform used the selected providers to generate the following execution
plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # module.iam_user["Administrator"].aws_iam_access_key.this[0] will be created
  + resource "aws_iam_access_key" "this" {
      + create_date                    = (known after apply)
      + encrypted_secret               = (known after apply)
      + encrypted_ses_smtp_password_v4 = (known after apply)
      + id                             = (known after apply)
      + key_fingerprint                = (known after apply)
      + pgp_key                        = "keybase:chechiachang"
      + secret                         = (sensitive value)
      + ses_smtp_password_v4           = (sensitive value)
      + status                         = "Active"
      + user                           = "Administrator"
    }

  # module.iam_user["Administrator"].aws_iam_user_login_profile.this[0] will be created
  + resource "aws_iam_user_login_profile" "this" {
      + encrypted_password      = (known after apply)
      + id                      = (known after apply)
      + key_fingerprint         = (known after apply)
      + password                = (known after apply)
      + password_length         = 20
      + password_reset_required = false
      + pgp_key                 = "keybase:chechiachang"
      + user                    = "Administrator"
    }

Plan: 2 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + iam_access_key_id = {
      + Accounting    = ""
      + Administrator = null -> (known after apply)
    }
  ~ keybase_password_decrypt_command   = {
      ~ Administrator = null -> (known after apply)
        # (1 unchanged element hidden)
    }
  ~ keybase_password_pgp_message       = {
      ~ Administrator = null -> (known after apply)
        # (1 unchanged element hidden)
    }
  + keybase_secret_key_decrypt_command = {
      + Accounting    = null
      + Administrator = (known after apply)
    }
  + keybase_secret_key_pgp_message     = {
      + Accounting    = null
      + Administrator = (known after apply)
    }
```

符合預期!! 可喜可賀

但是我們已經有 access key 在使用了，我又不想要走 day 3 aws-vault add key 的步驟換一組新的，這時該怎辦

沒錯，我們可以像 Day3 一樣，使用 import 匯入已經存在的 resource 到 address 裡面
- google "terraform aws iam user access key"，[找到 aws iam user access key 的說明頁面](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_access_key#import)
- address 是 `module.iam_user["Administrator"].aws_iam_access_key.this[0]`
- access key ID
  - 可以在密碼管理器查看
  - 或是在 aws web console -> IAM -> User -> Administrator -> Security Credential -> Access Keys 查到

```
aws-vault exec terraform-30day-root-iam-user --no-session  --  terragrunt import 'module.iam_user["Administrator"].aws_iam_access_key.this[0]' AKIA1234567890

module.iam_user["Administrator"].aws_iam_access_key.this[0]: Importing from ID "AKIA2I2H7ERWKI4RIF4Z"...
module.iam_user["Administrator"].aws_iam_access_key.this[0]: Import prepared!
  Prepared aws_iam_access_key for import
module.iam_user["Administrator"].aws_iam_access_key.this[0]: Refreshing state... [id=AKIA2I2H7ERWKI4RIF4Z]

Import successful!

The resources that were imported are shown above. These resources are now in
your Terraform state and will henceforth be managed by Terraform.

Releasing state lock. This may take a few moments...
```

順便 [login profile 也 import 近來](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_user_login_profile#import)
```
aws-vault exec terraform-30day-root-iam-user --no-session  --  terragrunt import 'module.iam_user["Administrator"].aws_iam_user_login_profile.this[0]' Administrator
```

再次 plan 就不需要新建一把 access key 了...吧？！

```
aws-vault exec terraform-30day-root-iam-user --no-session  --  terragrunt plan

Terraform used the selected providers to generate the following execution
plan. Resource actions are indicated with the following symbols:
  + create
-/+ destroy and then create replacement

Terraform will perform the following actions:

  # module.iam_user["Administrator"].aws_iam_access_key.this[0] must be replaced
-/+ resource "aws_iam_access_key" "this" {
      ~ create_date                    = "2022-09-16T13:05:35Z" -> (known after apply)
      + encrypted_secret               = (known after apply)
      + encrypted_ses_smtp_password_v4 = (known after apply)
      ~ id                             = "AKIA2I2H7ERWKI4RIF4Z" -> (known after apply)
      + key_fingerprint                = (known after apply)
      + pgp_key                        = "keybase:chechiachang" # forces replacement
      + secret                         = (sensitive value)
      + ses_smtp_password_v4           = (sensitive value)
        # (2 unchanged attributes hidden)
    }

  # module.iam_user["Administrator"].aws_iam_user_login_profile.this[0] must be replaced
-/+ resource "aws_iam_user_login_profile" "this" {
      + encrypted_password      = (known after apply)
      ~ id                      = "Administrator" -> (known after apply)
      + key_fingerprint         = (known after apply)
      + password                = (known after apply)
      + password_length         = 20 # forces replacement
      + pgp_key                 = "keybase:chechiachang" # forces replacement
        # (2 unchanged attributes hidden)
    }

Plan: 2 to add, 0 to change, 2 to destroy.

Changes to Outputs:
  + iam_access_key_id = {
      + Accounting    = ""
      + Administrator = "AKIA2I2H7ERWARJJWIVK"
    }
  ~ keybase_password_decrypt_command   = {
      ~ Administrator = null -> (known after apply)
        # (1 unchanged element hidden)
    }
  ~ keybase_password_pgp_message       = {
      ~ Administrator = null -> (known after apply)
        # (1 unchanged element hidden)
    }
  ~ keybase_secret_key_decrypt_command = {
      ~ Administrator = null -> (known after apply)
        # (1 unchanged element hidden)
    }
  ~ keybase_secret_key_pgp_message     = {
      ~ Administrator = null -> (known after apply)
        # (1 unchanged element hidden)
    }
```

誒結果不符合預期，
- `aws_iam_access_key.this` 需要重建
  - 原因是我們更改了 `pgp_key = "keybase:chechiachang"` 造成 forces replacement
  - 因為
  - 想一想也很合理
    - 第一次創建 access key 的時候，keybase 是亂寫的，這時用 module 的 code 去跑，產生無加密的 access key 放在 state 中
    - 這次 import 後，module 中的 .tf code 已經改過，不再存無加密的 access key，而是加密後儲存 GPG Encrypted Message
    - 這個改變讓 provider 覺得沒有辦法符合，只好刪掉重建
- `.aws_iam_user_login_profile.this` 需要重建，原因也是一樣，因為我們改了 .tf code 邏輯，造成 provider 勢必要重建 login profile

執行 terraform apply

NOTE: 注意有 destroy 的 terraform plan 都要特別小心 review，因為很多 aws API delete 發出去就是無法復原了
- 例如 access key 與 password 刪掉後，是無法 recover 的
- 有些 API request 會有副作用
  - reset password 後，aws web console 會被登出
  - access key 換掉 terraform 就不能用，有可能導致 terraform 進行到一半被 permission denied (這個 apply 不會，只是提醒大家要注意)

有 destroy 的部分都要小心 review，看不懂就找 peering review
有 destroy 的部分都要小心 review，看不懂就找 peering review
有 destroy 的部分都要小心 review，看不懂就找 peering review

很重要所以說三次

```
aws-vault exec terraform-30day-root-iam-user --no-session  --  terragrunt apply

Apply complete! Resources: 2 added, 0 changed, 2 destroyed.

Outputs:

keybase_password_decrypt_command = {
  "Accounting" = <<-EOT
  echo "wcFMA4U4ylYlNYTfAQ/+KLtNeJqOqK/V3pNdcRh9nvyDw/huJfaYF7Ab/YdKqLKNVySBqc6HY8xedmER5Wn78RlG962/f772u8UlQN4XCOjOLjyOaNL8K0tkeoSVg+XXPx2qJO9Myc1d+74rG57biUD26XpwfS7+ryIjaHf+NzjisExZy2mgiMIzzAlfqTzRAc+jYP11wZcyFGwOe9pMq6BJy7FH5935ndVgNLCgYtSjgIV5b5kWQ3SDr0E9egAHnoAcHs8mni71x7OL7OCc/bS3nJSLz1jRkMoukWyQQ3+lM7Nwi36NSJneIKxW5f7lSxr7Bx+W3mx6gZgb18yRVIwbVW5iDFsAQOFb0zOHUf8tm3tAQ0F79Yeqy9sfLCfUUjVpCENEJe5FtwJkI8EbHKe8mGnYA4dbHaCkIDgVa8TZ4mdXl7yVZx0adlkKFIS48niwPHxMErZYqnRBitUCGdaH0bHcpPcnSVolLljZmXZUrntMjIEb9FGYbgl6hOiRF9MR3RQL5DNmpS7uSqU7V6TyhVbAOJO2oR01Z7hXdAMxZ54O+h06jN7fzvLrUSMWvUz/wp+JJnIDYNwu75Dvicn6NmXrP3fH3M8xmYIEPhpSvOldNzB4DMqQdD6tN+DphFFyvFwuLnWKWKOY+pbNXkd5q0H3A69owxgsONoOL1JqjZgOdcLtWTq+g9XqU5XSRQGo1ei5Ctv2f5yAHZuI2smwJkTA88SuyZqJNwRixw5OPpUDOuWxhK6xftsN7M1/TnioX8Ch3RTow7H0dvMFFD3ocvjG4A==" | base64 --decode | keybase pgp decrypt

  EOT
  "Administrator" = <<-EOT
  echo "wcFMA4U4ylYlNYTfAQ/+JcRNkO9SxMm9U196p2WuuXdSWo9ooktKJMp3q4Xf5xMG5z/ccphl5+fVDmkp2Pr76UJ9NmiBw8rzScFUEU4U+xZepNojSdN/rmZPWB6PKCdJMyItw6HOnn7OSa0i1arr0PHaC0bpVs4Bc+9Oqtw1SuU8uvwBpCeM+h33qOROnvKnGgvOHV2Zk1XcgT+sg7xMTv8q77KePoNLTK3joQL7fXdPWUGWCp8srWpxzJ8LD4aNMmsrjA/s/7sNbAAdhffRwwA6diuZfeYscZ6MlURUtrSx3iAuNV33kmhuyYimlmXstbfs/nIJVI5OfcVexPKzHK5O9DikXApAzbf/YACz0OebOcxnzh6+rQw9+XWwRtARcK3tViMhxqnEu4PHROmj1sNmLZLJqCniwN91J2iry7BAx2Zoyvvw7vd7Sw9LddaM+j2XHhSf21250sNMn/9R6beUlkWQgPci8mU51rnqBffbOJnvVh7QCTLssoMTgKRrgxb+oZbSsKLLQO/621ZcTY9rzC74w2kZWJTS7nx5G/0KQkwXP4NGRSTXYg3/6TcwT7LefQiJpWB2z92zT1sp5lPhtpNneqrtFFnirplfP5coeelRSlTEbHDwbHSX1LfHU7A5WHjf7oEHvn2hMhdgTlvGt4vL7rXiy9p8GWjcudGxZs+/WNs8CCkZd8j2gVvSRQEmNNtCd/U3jmq+o2VncJjBhetJ7eCyvKOAMwcCLHE0zleX77mXVtq7UVLXrcypxIbVjJAIko8y71fATyrRomcijS7Sgw==" | base64 --decode | keybase pgp decrypt

  EOT
}
keybase_password_pgp_message = {
  "Accounting" = <<-EOT
  -----BEGIN PGP MESSAGE-----
  Version: Keybase OpenPGP v2.0.76
  Comment: https://keybase.io/crypto

  wcFMA4U4ylYlNYTfAQ/+KLtNeJqOqK/V3pNdcRh9nvyDw/huJfaYF7Ab/YdKqLKNVySBqc6HY8xedmER5Wn78RlG962/f772u8UlQN4XCOjOLjyOaNL8K0tkeoSVg+XXPx2qJO9Myc1d+74rG57biUD26XpwfS7+ryIjaHf+NzjisExZy2mgiMIzzAlfqTzRAc+jYP11wZcyFGwOe9pMq6BJy7FH5935ndVgNLCgYtSjgIV5b5kWQ3SDr0E9egAHnoAcHs8mni71x7OL7OCc/bS3nJSLz1jRkMoukWyQQ3+lM7Nwi36NSJneIKxW5f7lSxr7Bx+W3mx6gZgb18yRVIwbVW5iDFsAQOFb0zOHUf8tm3tAQ0F79Yeqy9sfLCfUUjVpCENEJe5FtwJkI8EbHKe8mGnYA4dbHaCkIDgVa8TZ4mdXl7yVZx0adlkKFIS48niwPHxMErZYqnRBitUCGdaH0bHcpPcnSVolLljZmXZUrntMjIEb9FGYbgl6hOiRF9MR3RQL5DNmpS7uSqU7V6TyhVbAOJO2oR01Z7hXdAMxZ54O+h06jN7fzvLrUSMWvUz/wp+JJnIDYNwu75Dvicn6NmXrP3fH3M8xmYIEPhpSvOldNzB4DMqQdD6tN+DphFFyvFwuLnWKWKOY+pbNXkd5q0H3A69owxgsONoOL1JqjZgOdcLtWTq+g9XqU5XSRQGo1ei5Ctv2f5yAHZuI2smwJkTA88SuyZqJNwRixw5OPpUDOuWxhK6xftsN7M1/TnioX8Ch3RTow7H0dvMFFD3ocvjG4A==
  -----END PGP MESSAGE-----

  EOT
  "Administrator" = <<-EOT
  -----BEGIN PGP MESSAGE-----
  Version: Keybase OpenPGP v2.0.76
  Comment: https://keybase.io/crypto

  wcFMA4U4ylYlNYTfAQ/+JcRNkO9SxMm9U196p2WuuXdSWo9ooktKJMp3q4Xf5xMG5z/ccphl5+fVDmkp2Pr76UJ9NmiBw8rzScFUEU4U+xZepNojSdN/rmZPWB6PKCdJMyItw6HOnn7OSa0i1arr0PHaC0bpVs4Bc+9Oqtw1SuU8uvwBpCeM+h33qOROnvKnGgvOHV2Zk1XcgT+sg7xMTv8q77KePoNLTK3joQL7fXdPWUGWCp8srWpxzJ8LD4aNMmsrjA/s/7sNbAAdhffRwwA6diuZfeYscZ6MlURUtrSx3iAuNV33kmhuyYimlmXstbfs/nIJVI5OfcVexPKzHK5O9DikXApAzbf/YACz0OebOcxnzh6+rQw9+XWwRtARcK3tViMhxqnEu4PHROmj1sNmLZLJqCniwN91J2iry7BAx2Zoyvvw7vd7Sw9LddaM+j2XHhSf21250sNMn/9R6beUlkWQgPci8mU51rnqBffbOJnvVh7QCTLssoMTgKRrgxb+oZbSsKLLQO/621ZcTY9rzC74w2kZWJTS7nx5G/0KQkwXP4NGRSTXYg3/6TcwT7LefQiJpWB2z92zT1sp5lPhtpNneqrtFFnirplfP5coeelRSlTEbHDwbHSX1LfHU7A5WHjf7oEHvn2hMhdgTlvGt4vL7rXiy9p8GWjcudGxZs+/WNs8CCkZd8j2gVvSRQEmNNtCd/U3jmq+o2VncJjBhetJ7eCyvKOAMwcCLHE0zleX77mXVtq7UVLXrcypxIbVjJAIko8y71fATyrRomcijS7Sgw==
  -----END PGP MESSAGE-----

  EOT
}
keybase_secret_key_decrypt_command = {
  "Accounting" = tostring(null)
  "Administrator" = <<-EOT
  echo "wcFMA4U4ylYlNYTfARAAivQzF+bh6N6OH/3a1S7XQCrIceoLn9EXsc8Gr0p09TVieSqwwv1RojaCULjYXYu5UnxRFwaavN+ULxrl2c4hRBIMgNEAo1Nxy16vfDEj4W7S9l+yA/TU3ewbs8WqKHIFrO8+AcjxUV4Ol5cmziDu70UR0H1/f0w7lqC/s36Zqa1Rz5Mb1n7ATLfs4jiPDQiFlr+E6gSe+I23sAQqdDS/WEbwAVz6o2B9mvs+OznNzeDoTwd7nE2ca+jYDZKjEjD6+qfDAnVzftwSrJIb2yJYlKIeSKJLC9loEQk2wdR5fkKrPg//9S4gYQJjzkwWyJAQsc6AuOPZXjqVe5yV9EpG2r0938G/acR3SEjt53ckXjh6Fi0/EgOjfeTVMO0EH6Se/vurdXBRyMggTieyN76Ts8nnn32GBldTZBUgWTL1Udj6B9ueqFCFuB8LFGNNNoHYjp3hAeGEQdtgI9TQ9r+jRDKpO8zcDoRMFK7wv4DJ31Nl/aS++a8nFEwJp7D5XkiSPbJ9JE1MwvuufldAHqr8iRbt3LmKeB4qC3TFbIhNWY4gs2VZ5LTepIn18sQfQ4f5s9o1lpem4yQw2XeEA7Fd1sPVypVeOj4z8Y080duGES896LiGpsAZdQ3bm/RiuIMLSabArgWCP/0LgrOQU8SwrIdN3k4682nw41KVnhjY2IDSWQHfEUCTNkgNfdj8v7FiD/OHX5G6VX/NAOwiAQ7Qh9u6UOmyAVY3QTjgVYEF4+oUyX+zZWprhhJkvHRDTTTNqozxVBfbYqrKTxSa00MRwAFIwQJh3xXbvmlF" | base64 --decode | keybase pgp decrypt

  EOT
}
keybase_secret_key_pgp_message = {
  "Accounting" = tostring(null)
  "Administrator" = <<-EOT
  -----BEGIN PGP MESSAGE-----
  Version: Keybase OpenPGP v2.0.76
  Comment: https://keybase.io/crypto

  wcFMA4U4ylYlNYTfARAAivQzF+bh6N6OH/3a1S7XQCrIceoLn9EXsc8Gr0p09TVieSqwwv1RojaCULjYXYu5UnxRFwaavN+ULxrl2c4hRBIMgNEAo1Nxy16vfDEj4W7S9l+yA/TU3ewbs8WqKHIFrO8+AcjxUV4Ol5cmziDu70UR0H1/f0w7lqC/s36Zqa1Rz5Mb1n7ATLfs4jiPDQiFlr+E6gSe+I23sAQqdDS/WEbwAVz6o2B9mvs+OznNzeDoTwd7nE2ca+jYDZKjEjD6+qfDAnVzftwSrJIb2yJYlKIeSKJLC9loEQk2wdR5fkKrPg//9S4gYQJjzkwWyJAQsc6AuOPZXjqVe5yV9EpG2r0938G/acR3SEjt53ckXjh6Fi0/EgOjfeTVMO0EH6Se/vurdXBRyMggTieyN76Ts8nnn32GBldTZBUgWTL1Udj6B9ueqFCFuB8LFGNNNoHYjp3hAeGEQdtgI9TQ9r+jRDKpO8zcDoRMFK7wv4DJ31Nl/aS++a8nFEwJp7D5XkiSPbJ9JE1MwvuufldAHqr8iRbt3LmKeB4qC3TFbIhNWY4gs2VZ5LTepIn18sQfQ4f5s9o1lpem4yQw2XeEA7Fd1sPVypVeOj4z8Y080duGES896LiGpsAZdQ3bm/RiuIMLSabArgWCP/0LgrOQU8SwrIdN3k4682nw41KVnhjY2IDSWQHfEUCTNkgNfdj8v7FiD/OHX5G6VX/NAOwiAQ7Qh9u6UOmyAVY3QTjgVYEF4+oUyX+zZWprhhJkvHRDTTTNqozxVBfbYqrKTxSa00MRwAFIwQJh3xXbvmlF
  -----END PGP MESSAGE-----

  EOT
}
```

這時嘗試在使用 terraform plan，會無法取得 state s3 bucket
- 因為 access key 已經重建，現在 terraform 使用舊的 access key 連 s3 會 404 not found
```
aws-vault exec terraform-30day-root-iam-user --no-session  --  terragrunt plan

Remote state S3 bucket chechia-root-ap-northeast-1-terraform-state does not exist or you don't have permissions to access it. Would you like Terragrunt to create it? (y/n) n
ERRO[0004] remote state S3 bucket chechia-root-ap-northeast-1-terraform-state does not exist or you don't have permissions to access it
ERRO[0004] Unable to determine underlying exit code, so Terragrunt will exit with error code 1
```

取得 output 後，一樣做 gpg decrypt 取得
- password
- access key

完成後使用 aws-vault 移除舊的 profile + credential，再從新匯入 access key
```
aws-vault remove terraform-30day-root-iam-user
Delete credentials for profile "terraform-30day-root-iam-user"? (y|N) y
Deleted credentials.

aws-vault add terraform-30day-root-iam-user
Enter Access Key ID:
Enter Secret Access Key:
Added credentials to profile "terraform-30day-root-iam-user" in vault
```

完成後就可以正常使用 aws-vault plan 了
```
aws-vault exec terraform-30day-root-iam-user --no-session  --  terragrunt plan
```

上面的變更我們的 PR 如下
- [terragrunt-infrastructure-modules PR](https://github.com/chechiachang/terragrunt-infrastructure-modules/pull/3)
- [terragrunt-infrastructure-live-example PR](https://github.com/chechiachang/terragrunt-infrastructure-live-example/pull/3)

### TODO 與進度

- [x] 透過 root account 設定一組 IAM User
- [x] 透過 root account 設定多個 aws child accounts
- [x] root 中設定 IAM User
  - [x] 將手動產生的 Administrator 的 IAM User import terraform 中
  - [x] 補上 root account IAM Policy
  - [x] 補上 root account IAM Group
  - [x] reset root account IAM user login profile & pgp key
- [ ] security 中設定 IAM User
  - [ ] security 設定 password policy
  - [ ] security 設定 MFA policy
- [ ] security 中設定 IAM Policy & Group
- [ ] dev 中設定 IAM role
- [ ] 允許 security assume dev IAM role
