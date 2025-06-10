---
title: "Hashicorp: managed database credentials with Hashicorp Vault"
date: 2024-08-28T11:00:00Z
# weight: 1
# aliases: ["/test"]
tags: ["iac", "aws", "terraform", "kubernetes", "vault"]
description: "分享如何使用 Hashicorp Vault 管理資料庫帳號密碼，並透過 AWS IAM Role 與 Kubernetes Service Account 進行驗證與連線。"
#canonicalURL: "https://canonical.url/to/page"

showToc: true
TocOpen: false
#UseHugoToc: true

draft: false

hidemeta: false
comments: true
disableHLJS: false

hideSummary: false
ShowReadingTime: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
ShowWordCount: true
ShowRssButtonInSectionTermList: true

searchHidden: false
disableShare: false

#cover:
#    image: "" # image path/url
#    alt: "" # alt text
#    caption: "" # display caption under cover
#    relative: false # when using page bundles set this to true
#    hidden: false # only hide on current single page
---

- 活動時間: 2024-08-28T11:00:00Z
- [活動連結](https://www.omniwaresoft.com.tw/all-events/aicloud-webinar-20240814-0828/)
- [Facebook](https://www.facebook.com/engineer.from.scratch)
- [Twitter](https://twitter.com/chechiachang)
- [投影片](../../slides/2024-08-28-hashicorp-vault-database)

---

# Info

資料庫管理是一個很大的議題：如何管理資料庫的帳號密碼，如何精確的用戶設定權限，傳遞密碼給用戶，並自動化定期更新密碼。本場演講將分享如何使用 Hashicorp Vault 管理資料庫的帳號密碼，並透過 AWS IAM Role 與 Kubernetes Service Account 進行驗證，如何安全的傳遞密碼，並安全地連線到資料庫

涵蓋以下內容：

- database 帳號密碼管理的難題
- 簡介 Vault 與 database secret engine
- 在 vault 中設定 database secret engine
- vault 在需要時自動產生資料庫帳號密碼
- vault 透過安全來源認證 app 身份(使用 k8s service account 與 public cloud 認證(aws iam role))
- 完成 app 連線至 database 的工作週期
- monitoring / audit：vault audit log + prometheus / grafana dashboard / alert manager
- 範例：如何使用 terraform 設定 vault 與 database secret engine


# Target group

有資料庫管理需求的工程師，想要學習如何使用 Hashicorp Vault 管理資料庫的帳號密碼，並透過 AWS IAM Role 與 Kubernetes Service Account 進行驗證，如何安全的傳遞密碼，並安全地連線到資料庫。


# Author

Che-Chia Chang，專長的領域是後端開發，開發維運，容器化應用，以及Kubernetes開發管理。
Microsoft 最有價值從業人員 MVP。

目前為 Golang Taiwan Meetup Organizer，常出現於 CNTUG，DevOps Taipei，GDG Taipei， Golang Taipei Meetup。

Che-Chia Chang, an SRE specialize in container and Kubernetes operation. An active member of CNTUG, DevOps Taipei, GDS Taipei, Golang Taiwan Meetup.
Microsoft Most Valuable Professional since 2020.

https://chechia.net

- 2023 DevOpsDay
- 2023 Ithome Kubernetes Summit
- 2022 COSCUP
- 2022 Ithome Cloud Summit
- 2021 Ithome Cloud Summit
- 2020 DevOps Taiwan Meetup #26 - 從零開始導入 Terraform
- 2020 Cloud Native Taiwan 年末聚會
- 2020 Ithome Cloud Summit
- 2019 Ithome Cloud Summit
- 2018 Ithome Cloud Summit
- 2018 Ithome Kubernetes Summit
