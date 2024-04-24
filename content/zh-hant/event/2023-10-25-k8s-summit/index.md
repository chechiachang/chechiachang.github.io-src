---
title: "Kubernetes Summit: Resource as Code for Kubernetes: Stop kubectl apply"

event: Kubernetes Summit 2023
event_url: https://k8s.ithome.com.tw/2023/

location: 臺北文創大樓
address:
  street: 台北市信義區光復南路133號
  city: Taipei
  region: Taiwan
  postcode: '110'
  country: Taiwan

summary: 將 k8s resource 以 code 管理，推上 vcs，並使用 argoCD, secret operator 等工具進行管理，來讓避免低級的人工操作錯誤，降低團隊整體失誤率，並降低 k8s admin 管理的成本，提高管理效率
abstract: 'Infrastrure as Code (IaC) 與 PaC，在萬物都該 as Code 得時代，你還在不斷的 kubectl apply 嗎？本次演講集合幾個管理 k8s 的範例，將 k8s resource 以 code 管理，推上 vcs，並使用 argoCD, secret operator, ... 等工具進行管理，來讓避免低級的人工操作錯誤，降低團隊整體失誤率，並降低 k8s admin 管理的成本，提高管理效率'

# Talk start and end times.
#   End time can optionally be hidden by prefixing the line with `#`.
date: '2023-10-25T13:20:00Z'
date_end: '2023-10-25T14:00:00Z'
all_day: false

# Schedule page publish date (NOT talk date).
publishDate: '2023-09-10T00:00:00Z'

authors: []
tags: ["vault", "iac", "aws", "terraform", "kubernetes"]
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
    url: https://k8s.ithome.com.tw/2023/session-page/2331
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
slides: 2023-10-25-k8s-resource-as-code

# Projects (optional).
#   Associate this post with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects = ["internal-project"]` references `content/project/deep-learning/index.md`.
#   Otherwise, set `projects = []`.
#projects:
#  - example

---
# Info

Title: Resource as Code for Kubernetes: stop kubectl apply

https://k8s.ithome.com.tw/CFP

Infrastrure as Code (IaC) 與 PaC，在萬物都該 as Code 得時代，你還在不斷的 kubectl apply 嗎？

手動 apply 的痛點：
- 人就是會忘：是誰 apply 這個在 k8s 上的？是誰上次漏 apply 所以壞了？
- 人就是會寫錯：能否 apply 
- 管理大量的 label, taint, annotation
- 安全：apply 變更內容是否有經過資訊安全的 review

當服務的 app code base 都已經用 chart 打包，使用 vcs 管理後，為何依賴的 k8s resource (namespace, secret, label, crd, ...) 不需要推上 vcs 管理的？

本次演講集合幾個管理 k8s 的範例，將 k8s resource 以 code 管理，推上 vcs，並使用 argoCD, secret operator, ... 等工具進行管理，來讓避免低級的人工操作錯誤，降低團隊整體失誤率，並降低 k8s admin 管理的成本，提高管理效率

# target group

Kubernetes User who want to increase performance in k8s management
