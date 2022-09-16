---
title: "14th iThome ironman-01 IaC best practice workshop on aws" # Title of the blog post.
date: 2022-09-12T14:31:48+08:00 # Date of post creation.
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

[iThome 鐵人賽好讀版](https://ithelp.ithome.com.tw/articles/10290931)

[賽後文章會整理放到個人的部落格上 http://chechia.net/](http://chechia.net/)

[追蹤粉專可以收到文章的主動推播](https://www.facebook.com/engineer.from.scratch)

![https://ithelp.ithome.com.tw/upload/images/20210901/20120327NvpHVr2QC0.jpg](https://ithelp.ithome.com.tw/upload/images/20210901/20120327NvpHVr2QC0.jpg)

--

AWS 為例，實現 production framework 的最佳實踐的 30 天 workshop

# 準備 Production environmtn Devops 面臨的問題

DevOps 的工作內容繁雜
- 今天想要 Deploy 一個 backend API deployment 到 k8s 上
- 一轉眼發現自己在修 port / servie / ingress / alb
- 一轉眼發現自己在修 tls certificate
- 一轉眼發現自己在修 node linux 上的一個 bug
- 一轉眼發現自己在修 monitoring / metrics + alert / log collection
...
- 我只是想 deploy 一個 backend deployment
  - 修infra 花了好幾天，而寫 deployment 只要 2 hr
  - Devops 的工作，是處理 developer 與 operator 中間的繁雜的細節

換個角度思考：上面這些元件全都是存在許久的功能，應該有一套統一介面隨叫即用這些服務，ex.
- 今天想要 Deploy 一個 backend API deployment 到 k8s 上

承上，同值性高，coding 講求 DRY 原則 (Don't Repeat Youself)，infra 管理上卻會有大量重複的工作
- 開一個 Restful API deployment
- 開一個 GRPC deployment
- 開一個 Kafka message Queue / redis / RDS / ...
- 希望這些元件都有寫好的 unit 可以重複使用
- 但實務上還是會有細節需要調整

自動化
- 標準化功能後，應該要可以自動部署
- 甚至是當 Backend API deployment 部署上去時，自動調用產生對應的元件
- Backend API deployment 有變化時應該要跟據 deployment 需求去做 reconcile (k8s controller)

缺乏測試
- VM / alb / RDS / ... 等公有雲服務需要測試嗎
  - A: AWS / Google / Azure 都測過了，我們不用再測
    - 然而 SRE 卻發現時常需要花時間 debug 這些元件
      - 不是 functional issue，而是 configuration 問題，或是不同元件設定造成交互作用
  - B: 要上 production 的元件都要測試
    - 使用 terraform provision 一台 EC2 後，在使用 terratest (Golang) 打 aws API 進行測試
- 標準化，自動化後，應該有大量的自動化測試，來確保每一個元件的 configuration 都是正確的，而且有信心維持穩定度

infra 時常改變
- 技術元件時常改變：terraform 升級，aws 升級，k8s 升級，linux 升級與 patch
  - infra 沒有射後不理這種事，都需要時常且穩定的更新
- 為了滿足上游服務(前後端/DB/...)的需求
  - 調整 VM spec / networking / routing / security rules /
- 不斷的改變耗費大量的人工時間

production ready 需要準備的
- production -> 真金白銀，公司的業務與名聲
- production ready 應該是有明確的表準 True / False，而不是『我覺得現在是 production ready 了』
  - DevOps / SRE 都知道 production ready 的標準，只是沒有把他明確寫出來
- production ready 應該就跟 unit test 一樣，一個 checklist 跑下去檢查，通過就是 production-ready，不通過就是 not-ready，且會說明不通過的原因
- [Gruntwork production ready checklist](https://gruntwork.io/devops-checklist/)

人工介入工作太多
- 新增元件需要人工處裡
- 定期的 patch & update / 安全性更新 / deploy 都需要人工介入的話就太浪費時間了
- 人工工作太多容易造成人為錯誤(human error) 

多環境
- SRE 需要提供大量的環境 dev / qa / stag / prod ...
- 或是提早 scan 到更前面的工作流程，例如在 code base / reposiroty 中就先 scan


# Gruntwork solution

為何要使用 gruntwork framework

[Why you need a framework](https://docs.gruntwork.io/guides/production-framework)

[Gruntwork 提出兩個 solution](https://docs.gruntwork.io/intro/next-steps)
- [Reference Architecture](https://docs.gruntwork.io/guides/reference-architecture/example-usage-guide)
- [Build your own architecture](https://docs.gruntwork.io/guides/build-it-yourself)


# Prerequisites
由於本次分享不希望有多餘的費用，所以內容依據 gruntwork 公開網站與開源的 repository 內容講解使用
- 不會涉及付費版的 terraform code library 內容與教材(subscription $795/month)
- aws 服務也盡量使用 free tier 中的額度

Prerequisites
- 基本 Terraform 經驗，或是參考[2021 年的鐵人賽系列文章: 30 天學 Terraform on Azure]()
- 基本 AWS 服務的觀念
都沒有也沒關係，會沿路在幫各位複習

# 30 天的目標

- 使用 terraform 設定所有 aws account 的 resource
- 參考 gruntwork-io 的開源 repository，設定
  - 如果是測試或學習，可以參考
https://github.com/gruntwork-io/terraform-aws-service-catalog

學習目標
- 熟悉 terraform 基本觀念
- 學會使用 terraform IaC 控制所有 aws service


# Repository

NOTE: 如果是有購買 gruntwork subscription 的朋友，請使用私有的 IaC library repository，有更完整且經過測試的架構

本課程使用 [gruntwork 開源的 repository 架構](https://github.com/gruntwork-io/terragrunt-infrastructure-live-example)

請 copy 需要的部分（而不要 fork，因為這裡不需要過去的 commit history 與未來的 update)
- [去年iThome 鐵人賽使用的範例 repository](https://github.com/chechiachang/terraform-30-days)
- [我自己使用的 repo](https://github.com/chechiachang/terraform-azure)
- [今年 iThome 會使用的 repository](https://github.com/chechiachang/terragrunt-infrastructure-live-example)

# 今天要做的事

請準備好以下 prerequisite

- 設定 / 註冊 aws account 併取得 aws 12-month free-tier (預期是免費的預期 12-month free tier 即可包含所有內容)
  - 然而成本控制也是課程的一環，各位要注意使用的資源，不要超過 aws free tier 太多，理論上也是最多幾美金的花費
- 安裝與設定 terraform tools
  - terraform 1.2.9
  - terragrunt 0.38.9
  - 使用舊版本的朋友請盡量使用 terraform >1.x 與 terragrunt >0.35.8 的版本

Aws account

- 如果已經有 aws cloud service account 可以直接使用，本課程會使用全新的 aws account
- 使用 email 註冊 aws cloud service
  - email 認證
  - 信用卡登記
  - 手機認證

Install terraform
  - terraform 1.2.9
  - terragrunt 0.38.9

# 設定 Github repository

準備一個 github repository 來存放ㄏ的 terraform code

- 可以使用[我的範例 repository](https://github.com/chechiachang/terragrunt-infrastructure-live-example)，也是 fork 底下 gruntwork 的 repository 稍作整理
- 或參考 [gruntwork Github repository example](https://github.com/gruntwork-io/terragrunt-infrastructure-live-example)

```
git clone git@github.com:chechiachang/terragrunt-infrastructure-live-example.git
```

# 明天

帶著大家在 terraform code 中設定 aws account 與 IAM 權限

# 參考資源

不熟悉 terraform 的朋友不妨參考去年的佳作 [Terraform Workshop - Infrastructure as Code for Public Cloud 疫情警戒陪你度過 30 天](https://ithelp.ithome.com.tw/users/20120327/ironman/4057)，雖然是在 Azure 上
，但許多基本概念都是相通的

過去的鐵人賽文章
- 13th 佳作 [Terraform Workshop - Infrastructure as Code for Public Cloud 疫情警戒陪你度過 30 天](https://ithelp.ithome.com.tw/users/20120327/ironman/4057)
- 12th 佳作 [Kubernetes X DevOps X 從零開始導入工具 X 需求分析＊從底層開始研究到懷疑人生的體悟＊](https://ithelp.ithome.com.tw/users/20120327/ironman/3248)
- 11th 優勝 [其實我真的沒想過只是把服務丟上 kubernetes 就有這麼多問題只好來參加30天分享那些年我怎麼在 kubernetes 上踩雷各項服務](https://ithelp.ithome.com.tw/users/20120327/ironman/2444)
kkk

推薦一下 Gruntwork 他們家的 blog: [Gruntwork devops as a service](https://blog.gruntwork.io/)

# Q&A

過去參賽都會有許多朋友提出問題，今年若有疑問可以集中在第一篇文章，我會跟大家一起討論。有想要看的題目也可以留言，我們看時間做安排。

# references
- https://docs.gruntwork.io/intro/overview/how-it-works
