---
title: 'DevOpsDay: HashiCorp Vault 自建金鑰管理最佳入坑姿勢'

event: DevOpsDay Taipei 2023
event_url: https://devopsdays.tw/2023/

location: 臺北文創大樓6樓ABC會議室
address:
  street: 台北市信義區光復南路133號
  city: Taipei
  region: Taiwan
  postcode: '110'
  country: Taiwan

summary: 從導入 HashiCorp Vault 作為起點，直接提供實務上經驗，分享建議的入坑設定
abstract: '本次演講從導入 HashiCorp Vault 作為起點，直接提供實務上經驗，分享建議的設定與路上可能有的雷。內容包含：Vault 入坑的困難，Vault + Terraform 一入坑就 IaC，mount path + role + policy 命名與管理，Vault 升級與維護。會依據企業需求提供實際用例 demo，當天提供 github code example。不會講太多非常基本介紹 vault 介紹。'

# Talk start and end times.
#   End time can optionally be hidden by prefixing the line with `#`.
date: '2023-09-26T13:20:00Z'
date_end: '2023-09-26T14:00:00Z'
all_day: false

# Schedule page publish date (NOT talk date).
publishDate: '2023-09-09T00:00:00Z'

authors: []
tags: []

# Is this a featured talk? (true/false)
featured: false

image:
  #caption: 'Image credit: [**Unsplash**](https://unsplash.com/photos/bzdhc5b3Bxs)'
  focal_point: Right

links:
  - name: 活動連結
    icon: calendar
    icon_pack: fa
    url: https://devopsdays.tw/2023/session-page/2279
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
slides: 2023-09-26-devopsday-2023-vault

# Projects (optional).
#   Associate this post with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects = ["internal-project"]` references `content/project/deep-learning/index.md`.
#   Otherwise, set `projects = []`.
projects:
  - example
---

HashiCorp Vault 自建金鑰管理最佳入坑姿勢

本次演講從導入 HashiCorp Vault 作為起點，直接提供實務上經驗，分享建議的設定與路上可能有的雷。

- Vault 入坑的困難
- Vault + Terraform 一入坑就 IaC
- mount path + role + policy 命名與管理
- 升級與維護
- 會依據企業需求提供實際用例 demo，當天提供 github code example

中階
- 預期聽眾是有 Vault 使用經驗，希望能更有效率管理 Vault 的人
- 不會講太多基本功能介紹 vault 介紹
