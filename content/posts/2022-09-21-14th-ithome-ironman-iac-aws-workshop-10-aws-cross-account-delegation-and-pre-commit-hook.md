---
title: "Aws Cross Account Delegation & pre-commit hook" # Title of the blog post.
date: 2022-09-21T22:55:41+08:00 # Date of post creation.
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

### TODO 與進度

- [x] root 中設定 IAM User
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

[iThome 鐵人賽好讀版](https://ithelp.ithome.com.tw/articles/10290931)

[賽後文章會整理放到個人的部落格上 http://chechia.net/](http://chechia.net/)

[追蹤粉專可以收到文章的主動推播](https://www.facebook.com/engineer.from.scratch)

![https://ithelp.ithome.com.tw/upload/images/20210901/20120327NvpHVr2QC0.jpg](https://ithelp.ithome.com.tw/upload/images/20210901/20120327NvpHVr2QC0.jpg)

### AWS cross account with iam roles

要做跨 AWS account 的 IAM Roles access control，我們先看官方文件理解這個功能

[https://docs.aws.amazon.com/IAM/latest/UserGuide/tutorial_cross-account-with-roles.html](
https://docs.aws.amazon.com/IAM/latest/UserGuide/tutorial_cross-account-with-roles.html)

回憶我們在 day-04 提到的 multi-accounts 架構
- account/security 有所有 iam-users
- 其他 child-account ex. account/test 中會有 iam-roles
- 需求：security/iam-user 可以使用 test/iam-role 的身份，存取 test 底下的 resource ex.test/ec2
- 好處
  - admin 不需要到每一個 child-account 下面去開每一個人的 iam user，統一到 account/security 管理
  - user 只要登入一個 security 帳號，就可以控制多個 child-account，不用登出又登入不同 account

在 aws official doc 上，也是舉幾個 account 作為 cross account delegation 的範例。由於本 workshop 已經有現存的 child-account，我們會直接使用 workshop 的 accounts 做說明。完成這次 iam role delegation 的設定後，我們會得到以下成果
- account/security 下面 IAM User 可以 assume 到 account/test 下面的特定的 IAM role
- account/test 下面有一個 IAM role 可以存取 S3 Bucket
- 工程師可以使用 web console 登入 security/user，然後 assume role 為 test/role，取得查看 s3 bucket 的權限
- 工程師也可使用以 security/user 的身份， call aws API 取得 test/role 的暫時的 credential

### 步驟

我們會先過一次 aws 官方文件上所述的步驟，讓大家了解整個設定步驟，弄清整個 delegation 的流程與概念。之後會轉而使用 Terraform 設定所有的元件。
- 首先要在 test (child-account) 設定 iam role
  - 將 account/security 作為 trusted entity
  - 設定 role 的 policy，增加可以存取 s3 bucket 的權限給 test/role
- 調整 iam role，可以設定需要給予權限，或是 deny 某些權限
- 最後做測試，是否可以完成 switch role

AWS 的範例使用 aws web console 做範例，這個 workshop 後面我們會使用 terraform 來實作。

### 外出取材

上面的範例還在 WIP，請當作者外出取材一天，今天先講另外一個工具

---

### Terraform fmt & lint

要提升 terraform code 品質，有許多工具非常值得在 CI/CD 過程中使用

例如 terraform 內建的 fmt 與 terragrunt 內建的 hclfmt
- 在 module 的 repository 中會需要跑 terraform fmt，確保每個 module release 出去前都有經過 fmt
- 在使用 terragrunt 的 root module 會需要 hclfmt .hcl 檔案

```
cd terragrunt-infrastructure-modules
terraform fmt -recursive

cd terragrunt-infrastructure-live-example
terragrunt hclfmt
```

fmt 對於程式碼的品質是基礎但十分重要的
- 沒有固定 format 的程式碼會造成 git 使用出現過多 diff，造成團隊協作的困難
- format 也會影響自動化，例如 templating / variable expension

fmt / lint 是我們第一個帶入 CI/CD 的工具

### 手動 fmt

fmt 一下

```
cd terragrunt-infrastructure-modules
terraform fmt -recursive

cd terragrunt-infrastructure-live-example
terragrunt hclfmt
```

commit 如下
- [terragrunt-infrastructure-modules commit](https://github.com/chechiachang/terragrunt-infrastructure-modules/commit/cab9fe72bafe8fa238ba04a17b7a60858ca2d27c)
- [terragrunt-infrastructure-live-example](https://github.com/chechiachang/terragrunt-infrastructure-live-example/commit/1810e1a28558937058e21feafa4a8c9d2c82fab3)

### Git precommit hook

既然是 code 品質的基礎，應該每次 commit 之前都觸發檢查，這個階段適合使用 git pre-commit hook 前執行

[https://github.com/antonbabenko/pre-commit-terraform](https://github.com/antonbabenko/pre-commit-terraform)

以 terragrunt-infrastructure-live-example 為例
- [PR 在此](https://github.com/chechiachang/terragrunt-infrastructure-modules/pull/5)
- 啟用前需要 install remote script 到本地
- git add 後，使用 run 來手動觸發 pre-commit hook
  - 會根據 commit hook 執行腳本，以這邊的範例會執行
    - id: terraform-fmt
    - id: terraform-validate
    - id: tflint
    - id: terraform_checkov
    - id: terrascan
    - id: terraform_tfsec
    - id: infracost_breakdown
  - 除了 fmt 有說明過以外，其他的 tool 我們後續再說明

```
pre-commit install

pre-commit install
pre-commit installed at .git/hooks/pre-commit

pre-commit run
```

- 如果通過 run 測試，就可以進行 git commit
  - commit 之前會在跑一次 script，所以稱作 pre-commit hook
  - 如果通過測試變化自動 commit
  - 如果沒有通過，則退回這次 commit
  - 如果想要跳過 pre-commit check，可以使用 git commit --no-verify

通過上述步驟，來確保工程師在本地發出的 commit 有經過基礎的驗證，非常值得團隊導入

---

### Github Action

