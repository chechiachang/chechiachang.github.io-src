---
title: "14th Ithome Ironman Iac Aws Workshop-03 Provision Child AWS Accounts" # Title of the blog post.
date: 2022-09-16T17:16:21+08:00 # Date of post creation.
description: "Article description." # Description used for search engine.
featured: true # Sets if post is a featured post, making appear on the home page side bar.
draft: true # Sets whether to render this page. Draft of true will not be rendered.
toc: false # Controls if a table of contents should be generated for first-level links automatically.
# menu: main
featureImage: "/images/path/file.jpg" # Sets featured image on blog post.
#thumbnail: "/images/path/thumbnail.png" # Sets thumbnail image appearing inside card on homepage.
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

今天要使用 terraform 設定 AWS account structure

[iThome 鐵人賽好讀版](https://ithelp.ithome.com.tw/articles/10290931)

[賽後文章會整理放到個人的部落格上 http://chechia.net/](http://chechia.net/)

[追蹤粉專可以收到文章的主動推播](https://www.facebook.com/engineer.from.scratch)

![https://ithelp.ithome.com.tw/upload/images/20210901/20120327NvpHVr2QC0.jpg](https://ithelp.ithome.com.tw/upload/images/20210901/20120327NvpHVr2QC0.jpg)

--

# AWS Account structure

---

### 我們自己的 module repository

- 開一個權限的 repository 
- fork 我自幹的 modules repository terragrunt-infrastructure-modules [https://github.com/chechiachang/terragrunt-infrastructure-modules](https://github.com/chechiachang/terragrunt-infrastructure-modules)

### Terragrunt

使用 Root Account IAM User 執行
把 

```
aws-vault add terraform-30day-root-iam-user
Enter Access Key Id: XXXXXXXXXXXX
Enter Secret Key: YYYYYYYYYYYY

aws-vault exec terraform-30day-root-iam-user -- terragrunt init
```

### Terragrunt plan


```
Terraform will perform the following actions:

  # module.iam_account["dev"].aws_iam_account_alias.this will be created
  + resource "aws_iam_account_alias" "this" {
      + account_alias = "chechia-dev"
      + id            = (known after apply)
    }

  # module.iam_account["dev"].aws_iam_account_password_policy.this[0] will be created
  + resource "aws_iam_account_password_policy" "this" {
      + allow_users_to_change_password = true
      + expire_passwords               = (known after apply)
      + hard_expiry                    = false
      + id                             = (known after apply)
      + max_password_age               = 0
      + minimum_password_length        = 37
      + password_reuse_prevention      = (known after apply)
      + require_lowercase_characters   = true
      + require_numbers                = true
      + require_symbols                = true
      + require_uppercase_characters   = true
    }

  # module.iam_account["logs"].aws_iam_account_alias.this will be created
  + resource "aws_iam_account_alias" "this" {
      + account_alias = "chechia-logs"
      + id            = (known after apply)
    }

  # module.iam_account["logs"].aws_iam_account_password_policy.this[0] will be created
  + resource "aws_iam_account_password_policy" "this" {
      + allow_users_to_change_password = true
      + expire_passwords               = (known after apply)
      + hard_expiry                    = false
      + id                             = (known after apply)
      + max_password_age               = 0
      + minimum_password_length        = 37
      + password_reuse_prevention      = (known after apply)
      + require_lowercase_characters   = true
      + require_numbers                = true
      + require_symbols                = true
      + require_uppercase_characters   = true
    }

  # module.iam_account["prod"].aws_iam_account_alias.this will be created
  + resource "aws_iam_account_alias" "this" {
      + account_alias = "chechia-prod"
      + id            = (known after apply)
    }

  # module.iam_account["prod"].aws_iam_account_password_policy.this[0] will be created
  + resource "aws_iam_account_password_policy" "this" {
      + allow_users_to_change_password = true
      + expire_passwords               = (known after apply)
      + hard_expiry                    = false
      + id                             = (known after apply)
      + max_password_age               = 0
      + minimum_password_length        = 37
      + password_reuse_prevention      = (known after apply)
      + require_lowercase_characters   = true
      + require_numbers                = true
      + require_symbols                = true
      + require_uppercase_characters   = true
    }

  # module.iam_account["security"].aws_iam_account_alias.this will be created
  + resource "aws_iam_account_alias" "this" {
      + account_alias = "chechia-security"
      + id            = (known after apply)
    }

  # module.iam_account["security"].aws_iam_account_password_policy.this[0] will be created
  + resource "aws_iam_account_password_policy" "this" {
      + allow_users_to_change_password = true
      + expire_passwords               = (known after apply)
      + hard_expiry                    = false
      + id                             = (known after apply)
      + max_password_age               = 0
      + minimum_password_length        = 37
      + password_reuse_prevention      = (known after apply)
      + require_lowercase_characters   = true
      + require_numbers                = true
      + require_symbols                = true
      + require_uppercase_characters   = true
    }

  # module.iam_account["shared"].aws_iam_account_alias.this will be created
  + resource "aws_iam_account_alias" "this" {
      + account_alias = "chechia-shared"
      + id            = (known after apply)
    }

  # module.iam_account["shared"].aws_iam_account_password_policy.this[0] will be created
  + resource "aws_iam_account_password_policy" "this" {
      + allow_users_to_change_password = true
      + expire_passwords               = (known after apply)
      + hard_expiry                    = false
      + id                             = (known after apply)
      + max_password_age               = 0
      + minimum_password_length        = 37
      + password_reuse_prevention      = (known after apply)
      + require_lowercase_characters   = true
      + require_numbers                = true
      + require_symbols                = true
      + require_uppercase_characters   = true
    }

  # module.iam_account["stage"].aws_iam_account_alias.this will be created
  + resource "aws_iam_account_alias" "this" {
      + account_alias = "chechia-stage"
      + id            = (known after apply)
    }

  # module.iam_account["stage"].aws_iam_account_password_policy.this[0] will be created
  + resource "aws_iam_account_password_policy" "this" {
      + allow_users_to_change_password = true
      + expire_passwords               = (known after apply)
      + hard_expiry                    = false
      + id                             = (known after apply)
      + max_password_age               = 0
      + minimum_password_length        = 37
      + password_reuse_prevention      = (known after apply)
      + require_lowercase_characters   = true
      + require_numbers                = true
      + require_symbols                = true
      + require_uppercase_characters   = true
    }

Plan: 12 to add, 0 to change, 0 to destroy.
```
