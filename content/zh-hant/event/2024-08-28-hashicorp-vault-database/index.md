---
title: "Hashicorp: managed database credentials with Hashicorp Vault"

event: Hashicorp Vault 2024
event_url: 

location: Webinar
address:
  street: 
  city: Taipei
  region: Taiwan
  postcode: '106'
  country: Taiwan

summary: 分享如何使用 Hashicorp Vault 管理資料庫的帳號密碼，並透過 AWS IAM Role 與 Kubernetes Service Account 進行驗證，以及如何連線到資料庫，監控與審查。
abstract: '資料庫管理是一個很大的議題：如何管理資料庫的帳號密碼，如何精確的用戶設定權限，傳遞密碼給用戶，並自動化定期更新密碼。本次演講將分享如何使用 Hashicorp Vault 管理資料庫的帳號密碼，並透過 AWS IAM Role 與 Kubernetes Service Account 進行驗證，如何安全的傳遞密碼，並安全地連線到資料庫。'

# Talk start and end times.
#   End time can optionally be hidden by prefixing the line with `#`.
date: '2024-08-03T13:20:00Z'
date_end: '2024-08-04T14:00:00Z'
all_day: false

# Schedule page publish date (NOT talk date).
publishDate: '2024-07-01T00:00:00Z'

authors: []
tags: ["iac", "aws", "terraform", "kubernetes", "vault"]
categories: ["kubernetes", "vault"]

# Is this a featured talk? (true/false)
featured: false

image:
  #caption: 'Image credit: [**Unsplash**](https://unsplash.com/photos/bzdhc5b3Bxs)'
  focal_point: Right

links:
  - name: 活動連結
    icon: calendar
    icon_pack: fa
    url: 
  - name: Facebook
    icon: facebook
    icon_pack: fab
    url: https://www.facebook.com/engineer.from.scratch
  - name: Twitter
    icon: twitter
    icon_pack: fab
    url: https://twitter.com/chechiachang
url_code: ''
url_pdf: ''
url_slides: ''
url_video: ''

# Markdown Slides (optional).
#   Associate this talk with Markdown slides.
#   Simply enter your slide deck's filename without extension.
#   E.g. `slides = "example-slides"` references `content/slides/example-slides.md`.
#   Otherwise, set `slides = ""`.
slides: 2024-04-26-saving-money-on-cloud-k8s

# Projects (optional).
#   Associate this post with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects = ["internal-project"]` references `content/project/deep-learning/index.md`.
#   Otherwise, set `projects = []`.
#projects:
#  - example

---

https://developer.hashicorp.com/vault/docs/secrets/databases

- database 帳號密碼管理的難題
- 簡介 Vault 與 database secret engine
- 在 vault 中設定 database secret engine
- vault 在需要時自動產生資料庫帳號密碼
- vault 透過安全來源認證 app 身份(使用 k8s service account 與 public cloud 認證(aws iam role))
- 完成 app 連線至 database 的工作週期
- monitoring / audit：vault audit log + prometheus / grafana dashboard / alert manager
- 範例：如何使用 terraform 設定 vault 與 database secret engine

---

cons
- not able to aquire the credentials if vault is down

# Info


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
