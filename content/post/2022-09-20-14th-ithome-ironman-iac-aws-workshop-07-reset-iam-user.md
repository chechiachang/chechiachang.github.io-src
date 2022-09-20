---
title: "2022 09 20 14th Ithome Ironman Iac Aws Workshop 07 Reset Iam User" # Title of the blog post.
date: 2022-09-20T18:30:06+08:00 # Date of post creation.
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

### TODO 與進度

- [x] 透過 root account 設定一組 IAM User
- [x] 透過 root account 設定多個 aws child accounts
- [x] root 中設定 IAM User
  - [x] 將手動產生的 Administrator 的 IAM User import terraform 中
  - [x] 補上 root account IAM Policy
  - [x] 補上 root account IAM Group
  - [ ] reset root account IAM user login profile & pgp key
- [ ] security 中設定 IAM User
  - [ ] security 設定 password policy
  - [ ] security 設定 MFA policy
- [ ] security 中設定 IAM Policy & Group
- [ ] dev 中設定 IAM role
- [ ] IAM cross account role 允許 security assume dev IAM role


[iThome 鐵人賽好讀版](https://ithelp.ithome.com.tw/articles/10290931)

[賽後文章會整理放到個人的部落格上 http://chechia.net/](http://chechia.net/)

[追蹤粉專可以收到文章的主動推播](https://www.facebook.com/engineer.from.scratch)

![https://ithelp.ithome.com.tw/upload/images/20210901/20120327NvpHVr2QC0.jpg](https://ithelp.ithome.com.tw/upload/images/20210901/20120327NvpHVr2QC0.jpg)

---

### Terraform fmt & lint

fmt 一下 commit 如下
- [terragrunt-infrastructure-modules commit](https://github.com/chechiachang/terragrunt-infrastructure-modules/commit/cab9fe72bafe8fa238ba04a17b7a60858ca2d27c)
- [terragrunt-infrastructure-live-example](https://github.com/chechiachang/terragrunt-infrastructure-live-example/commit/1810e1a28558937058e21feafa4a8c9d2c82fab3)

```
cd terragrunt-infrastructure-live-example
terragrunt hclfmt

cd terragrunt-infrastructure-modules


---

### 使用 aws module 的好處

為何許多開源的 terraform module 內部使用的都是其他的 module，而不是從 resource 單位開始？

[Terraform 官方文件，如何建立 module](https://www.terraform.io/language/modules/develop)

一個 module 會根據
根據最常出現的使用情劇與需求
最佳實踐
喜歡把好幾個經常一起使用，或是功能有關聯性的 resource 寫在同一個 module，透過 module 來使用
- 精簡 terragrunt.hcl 使用時要輸入的 input
- 透過 terraform function 與判斷式來產生

能符合需求，參數方便使用，內容邏輯清楚的 module 就是好 module

