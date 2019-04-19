+++
title = "Kubernetes Networking"

# Talk start and end times.
#   End time can optionally be hidden by prefixing the line with `#`.
date = 2018-06-14T09:00:00+08:00
date_end = 2018-06-14T17:00:00+08:00
all_day = false

# Schedule page publish date (NOT talk date).
publishDate = 2018-06-10T18:35:07+08:00

# Authors. Comma separated list, e.g. `["Bob Smith", "David Jones"]`.
authors = []

# Location of event.
location = "台大醫院國際會議中心 台北市中正區徐州路 2 號"

# Name of event and optional event URL.
event = "2018 iThome Kubernetes Summit"
event_url = "https://summit.ithome.com.tw/kubernetes/"

# Abstract. What's your talk about?
abstract = "網路實作為Kubernetes核心架構，也是開發過程中容易出錯的部分。本次演講將從群集管理員的角度，說明Kubernetes 中網路的實作。"

# Summary. An optional shortened abstract.
summary = "從系統管理層面看Kubernetes的網路架構"

# Is this a featured talk? (true/false)
featured = false

# Tags (optional).
#   Set `tags = []` for no tags, or use the form `tags = ["A Tag", "Another Tag"]` for one or more tags.
tags = ["kubernetes", "networking", "docker", "flannel"]

# Markdown Slides (optional).
#   Associate this page with Markdown slides.
#   Simply enter your slide deck's filename without extension.
#   E.g. `slides = "example-slides"` references 
#   `content/slides/example-slides.md`.
#   Otherwise, set `slides = ""`.
slides = ""

# Optional filename of your slides within your talk folder or a URL.
url_slides = "https://www.slideshare.net/CheChiaChang/k8s-networks"

# Projects (optional).
#   Associate this talk with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects = ["deep-learning"]` references 
#   `content/project/deep-learning/index.md`.
#   Otherwise, set `projects = []`.
projects = []

# Links (optional).
url_pdf = ""
url_video = ""
url_code = ""

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder. 
[image]
  # Caption (optional)
  caption = ""

  # Focal point (optional)
  # Options: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight
  focal_point = ""
+++

從系統管理層面看Kubernetes的網路架構

網路實作為Kubernetes架構，也是開發過程中容易出錯的部分。本次演講將從群集管理員的角度，說明Kubernetes 中網路的實作。

大綱:

1. Docker 與 Kubernetes 的網路架構
2. 不同層級的網路溝通實作
  - 容器對容器
  - Pod對Pod
  - 集群內部與Service
  - 集群外部對Service
3. 以flannel為例講解網路實作
4. 開發過程中常遇到的網路問題

希望聽眾對Kubernetes的網路架構能有基礎的概念，並在開發過程中遇到問題時，有明確的除錯步驟來判定網路是否有問題。遇到網路的問題，也能明確的知道問題的核心，並找到解法。
