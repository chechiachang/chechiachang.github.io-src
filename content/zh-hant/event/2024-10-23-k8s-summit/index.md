---
title: "Kubernetes Summit: Upgrade A VM Based Cluster"

event: Kubernetes Summit 2024
event_url: 

location: 台北文創大樓六樓
address:
  street:  台北市信義區菸廠路88號六樓
  city: Taipei
  region: Taiwan
  postcode: '110'
  country: Taiwan

summary: 分享如何升級 VM-based Kubernetes Cluster 的版本，包含 etcd，control plane，與 node。升級前如何規劃，升級步驟該如何操作，升級後應該如何檢查。
abstract: '升級 VM-based Kubernetes Cluster 的版本是一個複雜的工作，但是卻是必要的，而且每隔一段時間就需要進行。升級步驟會依據每個 cluster 當初部屬的方法而有相當大的落差。本篇演講會分享如何升級 VM-based Kubernetes Cluster 的版本（非公有雲託管），自行升級各個服務元件：包含 etcd，api-server，controller-manager，scheduler，與 node。本次演講會討論：升級的事前檢查，依據workload 型態的考量，升級前如何規劃，升級步驟該如何操作，升級後應該如何檢查。'

# Talk start and end times.
#   End time can optionally be hidden by prefixing the line with `#`.
date: '2024-10-23T13:20:00Z'
date_end: '2024-10-24T17:00:00Z'
all_day: false

# Schedule page publish date (NOT talk date).
publishDate: '2024-08-04T00:00:00Z'

authors: []
tags: ["iac", "aws", "terraform", "kubernetes", "vault"]
categories: ["kubernetes"]

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
slides: 2024-10-23-upgrade-k8s-cluster

# Projects (optional).
#   Associate this post with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects = ["internal-project"]` references `content/project/deep-learning/index.md`.
#   Otherwise, set `projects = []`.
#projects:
#  - example

---

# Presentation

Upgrade A VM Based Clustermin

### Target group 收穫

本次演講會講解升級操作，但不侷限在具體步驟，而是希望能講解更多 k8s 架構與設計，讓觀眾有以下收穫：如何升級 Kubernetes Cluster 的版本，升級時應考量的事項有哪些，有什麼工具可以協助升級流程，透過升級更了解 Kubernetes 的架構

# Author

Che-Chia Chang，專長的領域是後端開發，開發維運，容器化應用，以及Kubernetes開發管理。
Microsoft 最有價值從業人員 MVP。

目前為 Golang Taiwan Meetup Organizer，常出現於 CNTUG，DevOps Taipei，GDG Taipei， Golang Taipei Meetup。

Che-Chia Chang, an SRE specialize in container and Kubernetes operation. An active member of CNTUG, DevOps Taipei, GDS Taipei, Golang Taiwan Meetup.
Microsoft Most Valuable Professional since 2020.

https://chechia.net

- 2024 Cloud Summit
- 2024 SRE Conference
- 2023 DevOpsDay Taipei
- 2023 Kubernetes Summit
- 2022 COSCUP
- 2022 Cloud Summit
- 2021 Cloud Summit
- 2020 DevOps Taiwan Meetup #26 - 從零開始導入 Terraform
- 2020 Cloud Native Taiwan 年末聚會
- 2020 Cloud Summit
- 2019 Cloud Summit
- 2018 Cloud Summit
- 2018 Kubernetes Summit
