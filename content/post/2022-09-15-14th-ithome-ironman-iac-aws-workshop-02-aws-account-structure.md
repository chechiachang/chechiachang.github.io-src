---
title: "14th Ithome Ironman Iac Aws Workshop-02 AWS Account Struture" # Title of the blog post.
date: 2022-09-15T17:16:21+08:00 # Date of post creation.
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

AWS account structure 是 AWS IAM 提供的 feature 之一，可以讓用戶從一個 account login，然後透過授權操作其他 account 的元件。

然而有這個 feature 不代表用戶就要買單，有實際需求我們才來用 feature。使用 account structure 的理由是什麼？

# Account structure 的需求

[AWS 官方 whitepaper: 使用 multiple aws account 的好處](https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/benefits-of-using-multiple-aws-accounts.html)
- 依據職務需求將 workload 分組
- 為不同 environment 設定獨立的 security control
- 限制敏感資料的存取
- 提升創新與開發的敏捷
- 控制事故的影響程度與衝擊 impact
- 精細的拆分 IT 的工作
- 成本控管
- 分散 aws quotas 使用限額與 API rate limit 

[AWS 官方的 organization best practice](https://aws.amazon.com/organizations/getting-started/best-practices/)
[AWS 官方 OU 管理的 best practice](https://aws.amazon.com/blogs/mt/best-practices-for-organizational-units-with-aws-organizations/)

[Gruntwork Doc 建議的 IaC best practice 中的 aws account structure](https://docs.gruntwork.io/guides/build-it-yourself/landing-zone/core-concepts/what-is-an-aws-account-structure)，提到三個主要的目的
- Isolation (AKA compartmentalization)
  - 不同環境，事故發生時，影響範圍不會太大 (ex. 工程師 terraform 誤刪 infra)
  - 安全性，dev / stag 有安全性漏洞時，attacker 不會攻擊到 prod 環境
- Authentication and authorization
  - 把 user 都放在一起管理，透過更精細的 access control 去控制其他 account 內部的元件
- Auditing and reporting
  - 依據環境與用途拆分 account，讓監測與成本控制更精細

從實務上的經驗，有以下狀況就考慮要拆分 aws account
- 如果 IT 部門很大人數很多，那將所有工作內容不同的 user 都放在同一個 aws account 下導致管理麻煩
- 大多數的 incident 都是工程師 change 造成的，拆分 dev / stag 的 change 曾經影響到 prod
- 不同團隊對於負責的元件範圍區分不清
  - 工作掉球，該做的事沒人處理
  - 工作重功，做了一樣的事情導致衝突

# 小故事：技術問題解決人為問題（？）

iThome DevOpsDay 有一個聽眾聽完[2022 DevOpsDay PaC for IaC 演講](pfbid0DqcJsjuULbQ4KT7S9FQ312AJNuCtMoEZEnNcy8LFHd7ELfbSuUw8SHXCCzB2hpQxl) 後跑來找我，他問說：
講師你好，我們 terraform 常常誤刪東西，deploy dev / stag 結果 prod 壞掉（汗
如果不是技術的問題，是人的問題，不知道有沒有方法解？

要治本還是要加強內部教育訓練，很基礎的重大錯誤是很難用技術擋的
但短期要治標，可以
- 先區隔 dev stag 與 prod 的 terraform repo 跟 aws account
- 把 prod 權限鎖起來，先不要讓 junior 的成員去觸碰
- 所有 prod apply 都要兩到三個 senior 去 approve

也許你們的生活會快樂一點(好血淚)

# workshop

我們會根據 [Gruntwork Landing Zone Guide](https://docs.gruntwork.io/guides/build-it-yourself/landing-zone/deployment-walkthrough/pre-requisites) 的文字敘述來進行今天的 workshop

```
CAUTION
You must be a Gruntwork subscriber to access the Gruntwork Infrastructure as Code Library.
```

是的，這份 [Gruntwork Landing Zone Guide](https://docs.gruntwork.io/guides/build-it-yourself/landing-zone/deployment-walkthrough/pre-requisites) 內部的範例有使用許多 gruntwork-io 的 private repository，這部分是需要付費。gruntwork subscription 一個月 $795 起跳，有興趣的朋友可以參考 [Gruntwork subscription checkout](https://gruntwork.io/checkout)

我們這篇 workshop 並不使用 Gruntwork 的付費功能，所有 private repository 我們就會使用其他開源的 modules 來替代，例如使用 [aws + terraform team 官方維護的 aws modules](https://github.com/terraform-aws-modules)

由於缺少部分 repository 的內容，這份 [Gruntwork Landing Zone Guide](https://docs.gruntwork.io/guides/build-it-yourself/landing-zone/deployment-walkthrough/pre-requisites) 會常常看到很多 github external link 是 404 not found，表示是 private repository。看起來會有點不舒服，但沒關係我們就見招拆招自由發揮。

### 建立 workspace repository

repository 的內容可以[直接參照 Gruntwork Guide 的內容](https://docs.gruntwork.io/guides/build-it-yourself/landing-zone/deployment-walkthrough/prepare-your-infrastructure-live-repository)

本次 workshop 我們使用的 repository [https://github.com/chechiachang/terragrunt-infrastructure-live-example](https://github.com/chechiachang/terragrunt-infrastructure-live-example)
- terragrunt 都會在這個 repository 裡面運作
- 各位可以直接 copy 來改

### Root account

root account 是整個 account structure 最上層的 account，創世 account。由於是創世 account，權限也是最大，因此[會需要加上許多限制](https://docs.gruntwork.io/guides/build-it-yourself/landing-zone/deployment-walkthrough/lock-down-the-root-user):
- 使用高強度的密碼 
- 使用密碼儲存器保管密碼，ex 1password / lastpass / ...，這些密碼儲存器都有自動加密，且有通過安全風險測試
  - 不要存在電腦上 / email / google drive / 紙上 / 或是其他沒有經過安全驗證工具上
- 務必開啟 MFA
- 刪除 root account 的 aws access key，只允許透過 aws web console 存取
- 自己再也不要使用這個帳號，降低洩漏的風險
  - [AWS 官方建議，只有這些工作需要使用 root account](https://docs.aws.amazon.com/general/latest/gr/aws_tasks-that-require-root.html) ，其他工作都不應該使用 root account

### Root Account IAM user

我們使用 root account 的最後一件工作，就是建立一個 IAM User 作為 admin，之後使用這個 IAM User 操作。[文件與步驟在此](https://docs.gruntwork.io/guides/build-it-yourself/landing-zone/deployment-walkthrough/create-an-iam-user-in-the-root-account)
- Name: Administrator
- 勾選:
  - programmatic access
  - AWS Management Console access


![Root account IAM User: Name](https://ithelp.ithome.com.tw/upload/images/20220916/20120327tmntcNCOG5.png)

- Permission 頁面選擇 Attach existing policies to user directly
  - 勾選 AdministratorAccess policy.

![Root account IAM User: Attach existing policy](https://ithelp.ithome.com.tw/upload/images/20220916/20120327wrpyvOLW1h.png)

- 點下一步，直到產生出 IAM User
- 將登入資訊存在密碼儲存器
  - login url
  - name
  - password
  - Access key ID
  - Secret access key

![Root account IAM User: 1Password](https://ithelp.ithome.com.tw/upload/images/20220916/20120327EQGsL60PGH.png)

接著也是要鎖住 root account 的 IAM User 
- 使用高強度的密碼 
- 使用密碼儲存器保管密碼
- 務必開啟 MFA

# 為 Root account 設定 Security baseline

[依照 gruntwork guide](https://docs.gruntwork.io/guides/build-it-yourself/landing-zone/deployment-walkthrough/configure-the-security-baseline-for-the-root-account) 接下來需要設定底下的元件

- 建立所有的 child accounts
- 設定 AWS Organization
- IAM ROles
- IAM Users
- IAM Groups
- IAM Password Policies
- Amazon GuardDuty
- AWS CloudTrail
- AWS Config.

```
CAUTION
You must be a Gruntwork subscriber to access terraform-aws-service-catalog.
```

由於 [terraform-aws-service-catalog](https://github.com/gruntwork-io/terraform-aws-service-catalog) 是 private repository，需要付費訂閱才能使用，所以我們無法取得裡面的內容

為了避免這個 workshop 卡在這裡，我們就來自幹這些 module 吧ＸＤ
- 直接使用其他的開源 modules 替代
- 依照 guide 把元件生出來
- 然後依照自己的需求去客製化

NOTE: Gruntwork 的 security module 有其 enterprise solution 的經驗在裡面，其實公司有預算還是相當值得參考的。只是我們 workshop 為了壁面大家破費，先當一回免費仔。

### 我們自己的 module repository

- 開一個權限的 repository 
- fork [我自幹的 modules repository terragrunt-infrastructure-modules](https://github.com/chechiachang/terragrunt-infrastructure-modules)
- 上面這個是放 terraform module 的 repository，是兩個 repository
- 不要跟執行 terragrunt repository 搞混，是兩個 repository [https://github.com/chechiachang/terragrunt-infrastructure-live-example](https://github.com/chechiachang/terragrunt-infrastructure-live-example)

---

寫到這邊就 6000 字了，還沒開始碰 terragrunt
- aws account structure 與 terragrunt directory structure 的概念非常重要，有好的基礎會讓後面的工作快樂很多

明天會繼續今天的工作，把 aws account / iam policy / permission 配好
