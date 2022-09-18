---
title: "14th Ithome Ironman Iac Aws Workshop 04 AWS Multi-Accounts Structure" # Title of the blog post.
date: 2022-09-18T09:35:25+08:00 # Date of post creation.
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

昨天設定了多個 aws organization accounts，但我們還沒有說明為什麼要這樣做

今天會先講 Gruntwork 提出的 [Production-Grade Design: multi-account security strategy](https://docs.gruntwork.io/guides/build-it-yourself/landing-zone/production-grade-design/intro)
- 拆分多個 account 的用意
- 多 account 下如何統一管理 IAM User
- access control 與安全性控管

---

[iThome 鐵人賽好讀版](https://ithelp.ithome.com.tw/articles/10290931)

[賽後文章會整理放到個人的部落格上 http://chechia.net/](http://chechia.net/)

[追蹤粉專可以收到文章的主動推播](https://www.facebook.com/engineer.from.scratch)

![https://ithelp.ithome.com.tw/upload/images/20210901/20120327NvpHVr2QC0.jpg](https://ithelp.ithome.com.tw/upload/images/20210901/20120327NvpHVr2QC0.jpg)

# Production-grade Design IAM

Gruntwork 提出的 [Production-Grade Design: multi-account security strategy](https://docs.gruntwork.io/guides/build-it-yourself/landing-zone/production-grade-design/intro)，我們這邊一一講解

![Multi-account security strategy](https://ithelp.ithome.com.tw/upload/images/20220918/20120327GL49e7CTD0.png)

### [Root Account](https://docs.gruntwork.io/guides/build-it-yourself/landing-zone/production-grade-design/the-root-account) 的用途

- 位於 diagram 圖中的最上層
- 是整個架構的創世帳號，權限最大
- root account 裡面沒有任何 infrastructure 元件， i.e. aws ec2 不會長在裡面，是一個空 account
- root account 的存取最嚴格
  - 只有很少數的 admin 可以存取
    - i.e 只有 SRE 部門主管有自己的 IAM User，其他 SRE 沒有權限存取 root account
- root account 的工作最少
  - 設定 child account
  - 管理 billing

IAM policy 管理，不要把 policy 直接綁在 User 上，應該要
- 為不同權責的成員設定 IAM Group，ex. dev-admin / dev-user / stag-admin / qa / billing / ...
- 把 policy 綁在 Group 上，ex. ReadPermission -> dev-user / Read+Write -> dev-admin
- 把 User 加進 / 移除 Group，來管理人員權限
- Group 通常會接近公司團隊的職責分配
- root account 內部只會有
  - full-access 的管理員 group
  - billing 的會計出帳 group

### [Child Account](https://docs.gruntwork.io/guides/build-it-yourself/landing-zone/production-grade-design/child-accounts) 的用途

透過 root account 創建 child accounts 後，這裡說明各個 account 的設計用途

`Security` 用來管理 authentication 與 authorization
- 底下一樣沒有任何 infrastructure 元件
- 定義所有 IAM User 與 IAM Group，所有團隊成員的 User 在這邊設定
  - 所有的 User 放在 `Security` 底下統一管理
  - 其他的 child account 不會設定 IAM User，ex. dev / stag / prod 裡面都沒有 IAM User
    - child account 中設定 IAM roles，讓 security/user [assume role](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html) 存取其他 child account
    - ex. `security`/dev-admin/chechia assume role `dev`/admin，透過 aws STS(Security Token Service) 暫時取得 dev/admin 這個 role 的權限來控制 `dev`
- 團隊主管也會有一個 security IAM User，平時開發 infrastructure 使用這個 IAM User，只有需要調整 root account 時才會動用 root account IAM User。反正 root account 是能不用就不用

這個做法有非常多好處，但又不會造成工作上的負擔
- 使用方面：所有的團隊成員只會有一個 User，透過 `security` 登入。不會一個人有好幾個帳號密碼很煩
- 管理方面：管理員只要在 `security` 內管理 User，而不用一直切換 account 去調整 IAM User
- 安全方面：只要在 `security` 內落實安全性設定，就可以很好的控制所有 account 的存取權限

`dev` / `stag` / `prod` 用來存放 infrastructure 與跑 application
- 開發時使用 dev / stag 環境，測試都完成後，才自動推倒 `prod` 公開給用戶使用
- dev / stag 環境是內部環境，架構與 prod 類似，來模擬 prod 的環境方便開發與測試
  - 可能機器數量或規格比 prod 小很多，來節省成本
  - 有些團隊會有更多 account，例如 qa / uat / ...，都可以依照需求建立
- prod 有些團隊會有複數 prod 環境，可以供災難發生時做備援切換

`shared` 裡面放跨 application account 共用的元件
- 例如
  - AWS ECR 可能不想要每個 account 都開，想放一起的話可以放在 `shared`，然後讓其他 account 存取 `shared`
  - 版本控制系統 Git / github 可能會只有一組大家共用
  - CI/CD pipeline / Jenkins
  - ...等等跨環境共用的資源，可以放 `shared`
- 每個 account 都開也是有許多好處，例如更獨立更安全，這就看看各個團隊災安全與成本上的取捨
- 管理上由於 `prod` 會使用到 `shared` 的元件，建議要把 `shared` 的安全等級當作 `prod` 來管理，嚴格限制 `shared` 的存取，以保護 `prod` 環境的安全

很多個 `sandbox` account 讓工程師自由的測試功能
- 如果有需求與預算，一個完全獨立的 `sandbox` 讓工程師可以做各種實驗，對於促進團隊內部的創新會有非常大的幫助
  - 如果在 `dev` 上做這測試，有可能會影響到其他團隊成員，而覺得綁手綁腳的事情，都可以盡情在 `sandbox` 上操作
  - 可以為 `sandbox` 的帳號設定更嚴格的 billing / cost 設定，避免工程師玩太嗨超過預算
- 黃金準則是一個工程師一個 `sandbox` 來達到 100% 開發獨立

`testing` account 用來測試 infrastructure 的測試
- 如果有使用 [Gruntwork/Terratest](https://blog.gruntwork.io/open-sourcing-terratest-a-swiss-army-knife-for-testing-infrastructure-code-5d883336fcd5?gi=141873b58326) 來測試 terraform tf code 的朋友，應該知道 terratest 會把 terraform module 中的 infrastrcuture 真的在 aws 開出來，做功能測試，然後測試完成後再把 infrastrcture 全部刪掉
  - 是的 IaC terraform module 也是需要單元測試
- `testing` 就是用來讓 IaC 做自動化測試的環境，裡面的 infrastructure 都是常常 create + destroy，不會有常駐的服務
- 與 `sandbox` 不同的是
  - `testing` 是跑自動化 CI/CD pipeline 的測試
  - `sandbox` 是讓工程師做規模較小的手動測試與開發，因為我們也不希望一堆測試用 infrastructure 散落在 `sandbox` 裡面，感覺很貴

`logs` 用來收集 log 到單一 account 底下，方便查閱
- 所有 child account 的 log 都收到這裡，而不用跑到各個 account 去查 log
- aws account 內部的 log，cloud trail 都可以透過客訂與工具轉發，集中收集

如果公司規模很大，有多個 business unit 的話，也可以多建幾個 organization，來對應公司組織

### 透過 web console switch role

我是一個開發工程師（不是 admin），那在 multi-account 下的環境我應該如何工作？

如何存取 aws
- IAM User 可以透過帳號密碼來存取 aws web console，登入之後會發現自己處在 `security` account 底下
  - 第一次登入的話需要重設密碼，需要符合 [IAM Password Policy](https://docs.gruntwork.io/guides/build-it-yourself/landing-zone/production-grade-design/password-policy)
  - 會需要輸入 MFA，會需要符合 [IAM MFA Policy](https://docs.gruntwork.io/guides/build-it-yourself/landing-zone/production-grade-design/mfa-policy)
  - 兩面的安全性 policy 在實際公司帳號裡是必備，但在 workshop 中，我們還沒做，先留個坑之後來補
- programatic access 如同 [day03 的 root account IAM User 步驟](https://ithelp.ithome.com.tw/articles/10292900)，我們也是使用 aws-vault 搭配 aws access key，來讓 terraform 執行

web console 如何 switch role
- 可以在 aws web console -> 右上角 user -> switch role

![AWS Console: switch role](https://ithelp.ithome.com.tw/upload/images/20220918/20120327WzL2o9OCng.png)
![AWS Console: switch role](https://ithelp.ithome.com.tw/upload/images/20220918/20120327KR6vRGyAxe.png)

填入
- 目標 account ID (ex dev: 123456789012)
- 目標的 role
- 給自己看的好辨識名稱
如果 admin 有設定 IAM role 與 assume role 權限，就可以切換到 `dev` account 下的 IAM role 身分

![AWS Console: switch role](https://ithelp.ithome.com.tw/upload/images/20220918/20120327YSjdG8mJE1.png)

### 透過 web console switch role

如同 [day03 使用 root account IAM User](https://ithelp.ithome.com.tw/articles/10292900)，我們也是使用 aws-vault 搭配 aws access key，來讓 terraform 執行) 來跑 terraform 建立 child accounts 一樣，我們也需要設定 aws-vault，讓我們可以在 local 機上 assume 不同 account role，來使用各個 child account
- [aws-vault Roles and MFA](https://github.com/99designs/aws-vault#roles-and-mfa)

需要調整 `~/.aws/config` 的設定
- security 管理員設定完 iam role + assume policy 後，會提供登入資訊給其他團隊成員
```
cat ~/.aws/config

# 這是 root account IAM User 不要再拿來用了
# aws access key 收在本機的 aws-vault 內
[profile terraform-30day-root-iam-user]
region=ap-northeast-1

# 這是 security account (111111111111) IAM User（還沒建立）
# aws access key 收在本機的 aws-vault 內
[profile chechia-security-iam-user]
region=ap-northeast-1

# 這是 dev account (333333333333) IAM Role（還沒建立）
[profile dev-admin]
source_profile = chechia-security-iam-user
role_arn = arn:aws:iam::333333333333:role/dev-admin
mfa_serial = arn:aws:iam::111111111111:mfa/chechia-security-iam-user
```

上面這些都還沒建立，所以都還不能用，只是先說一下之後要怎麼操作

security 管理員要設定一大堆東西，但工程師使用非常簡單，只要透過 aws-vault 切換就可以在不同 account 下操作 terraform
```
aws-vault exec dev-admin -- aws sts get-caller-identity

{
    "UserId": "xxxxxxxxxxxxxxxx",
    "Account": "333333333333",
    "Arn": "arn:aws:iam::333333333333:role/dev-admin"
}

aws-vault exec dev-admin -- terragrunt plan
aws-vault exec stag-admin -- terragrunt plan
...

```

### 其他

Cloudtrail
- 12 month free-tier 是可以免費使用的
- log 存放在 s3 上，會需要收取 s3 的費用，12 month free-tier s3 是 5G，我們這個 workshop 不會超過
  - note: terraform state 也是放在 s3 上

### TODO 與進度

- [x] 透過 root account 設定一組 IAM User
- [x] 透過 root account 設定多個 aws child accounts
- [ ] security 中設定 IAM User
  - [ ] security 設定 password policy
  - [ ] security 設定 MFA policy
- [ ] security 中設定 IAM Policy & Group
- [ ] dev 中設定 IAM role
- [ ] 允許 security assume dev IAM role

