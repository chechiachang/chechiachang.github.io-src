---
title: "14th Ithome Ironman Iac Aws Workshop 11 Terraform Github Action CI/CD" # Title of the blog post.
date: 2022-09-25T20:39:03+08:00 # Date of post creation.
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

AWS cross account delegation 依舊 WIP，今天延續昨天內容，使用 github action 做 terraform module 的 CI/CD

[iThome 鐵人賽好讀版](https://ithelp.ithome.com.tw/articles/10290931)

[賽後文章會整理放到個人的部落格上 http://chechia.net/](http://chechia.net/)

[追蹤粉專可以收到文章的主動推播](https://www.facebook.com/engineer.from.scratch)

![https://ithelp.ithome.com.tw/upload/images/20210901/20120327NvpHVr2QC0.jpg](https://ithelp.ithome.com.tw/upload/images/20210901/20120327NvpHVr2QC0.jpg)

---

### Terraform Github Action Jobs

我們可以在 terraform repository 中增加 tool checks 到 CI/CD 中，加強 code 的品質控管

[terragrunt-infrastructure-modules PR 在此](https://github.com/chechiachang/terragrunt-infrastructure-modules/pull/6)

這個 PR 包含幾個 Github Action Workflow

```
ls .github/workflows

checkov.yaml
format.yaml
plan.yaml
security-scan.yaml
validate.yaml
```

- format.yaml 中執行 terraform fmt -recursive，需求與目的已在昨天說明
- validate.yaml 中執行 terraform validate，用來驗證 module 內的 terraform syntax 是否符合語法
- checkov.yaml 是多語言的 policy as code 工具，在這邊執行掃描 terraform code 的安全性與 CVEs 檢查
- security-scan.yaml 中也是 Policy As Code 使用 tfsec 工具掃描
- plan.yaml 中在 pipeline 執行自動化 terraform plan
  - 由於 plan 需要存取 state 與 provider API，設定上有許多權限設定需要開啟，目前是一個 dummy workflow

policy as code 內容可以將一篇演講，有興趣請見底下投影片: [2022 DevOpsDay: Policy As Code for Terraform: https://docs.google.com/presentation/d/1yawazO1B_sP5Yiav-XLGJXW3ZS2JTV0wGuJwhrUKQ3A](https://docs.google.com/presentation/d/1yawazO1B_sP5Yiav-XLGJXW3ZS2JTV0wGuJwhrUKQ3A)

對於 Policy as Code 有興趣的朋友請見今年 DevOpsDay 的演講
https://devopsdays.tw/session-page/1146

![2022 DevOpsDay: 從零導入 Policy as Code 到 terraform 甘苦談](https://ithelp.ithome.com.tw/upload/images/20220925/201203277AyBGqc8Ly.png)

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

### cross account iam role

```
iam_cross_account_roles
```

### TODO 與進度

- [x] 透過 root account 設定一組 IAM User
- [x] 透過 root account 設定多個 aws child accounts
- [x] root 中設定 IAM User
  - [x] 將手動產生的 Administrator 的 IAM User import terraform 中
  - [x] 補上 root account IAM Policy
  - [x] 補上 root account IAM Group
  - [x] reset root account IAM user login profile & pgp key
  - [ ] root account password policy
  - [ ] aws cross account iam role delegation
  - [ ] root account MFA policy
  - [ ] Optional: Cloudtrail
  - [ ] Optional: terraform aws config
- [ ] security 中設定 IAM User
  - [ ] security 設定 password policy
  - [ ] security 設定 MFA policy
- [ ] security 中設定 IAM Policy & Group
- [ ] dev 中設定 IAM role
- [ ] 允許 security assume dev IAM role
