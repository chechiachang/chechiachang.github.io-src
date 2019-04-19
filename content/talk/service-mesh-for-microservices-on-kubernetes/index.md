+++
title = "Service Mesh for Microservices on Kubernetes"

# Talk start and end times.
#   End time can optionally be hidden by prefixing the line with `#`.
date = 2019-05-15T12:00:00+08:00
date_end = 2019-05-15T12:30:00+08:00
all_day = false

# Schedule page publish date (NOT talk date).
publishDate = 2019-04-02T17:10:57+08:00

# Authors. Comma separated list, e.g. `["Bob Smith", "David Jones"]`.
authors = []

# Location of event.
location = "台北國際會議中心 (TICC)：110台北市信義區信義路五段1號"

# Name of event and optional event URL.
event = "IThome Cloud Summit 2019"
event_url = ""

# Abstract. What's your talk about?
abstract = "當眾多的為服務同時運作，產生複雜的依賴與交流，網路層不再只是有『有通就好』，而是需要精細且彈性的流量管理與監控，來提供穩定的效能。本次主題將基於 Kubernetes 平台上的 Istio ，探討 Service Mesh 的概念與相關應用。"

# Summary. An optional shortened abstract.
summary = ""

# Is this a featured talk? (true/false)
featured = false

# Tags (optional).
#   Set `tags = []` for no tags, or use the form `tags = ["A Tag", "Another Tag"]` for one or more tags.
tags = ["kubernetes", "istio"]

# Markdown Slides (optional).
#   Associate this page with Markdown slides.
#   Simply enter your slide deck's filename without extension.
#   E.g. `slides = "example-slides"` references 
#   `content/slides/example-slides.md`.
#   Otherwise, set `slides = ""`.
slides = ""

# Optional filename of your slides within your talk folder or a URL.
url_slides = ""

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
url_code = "https://github.com/istio/istio"

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder. 
[image]
  # Caption (optional)
  caption = "cncf/istio.png"

  # Focal point (optional)
  # Options: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight
  focal_point = ""
+++

### Outlines

微服務蓬勃發展，傳統的 Monolith被分解為分散的為服務，已取得更高的效能與更彈性的管理。當眾多的為服務同時運作，產生複雜的依賴與交流，網路層不再只是有『有通就好』，而是需要精細且彈性的流量管理與監控，來提供>穩定的效能。本次主題將基於 Kubernetes 平台上的 Istio ，探討 Service Mesh 的概念與相關應用。

1. 何為 Service Mesh ？為何需要 Service Mesh ？
2. Service Mesh 基本概念
3. 如何Service-to-Service的網路層管理監控
4. 導入 Istio 到 Kubernetes

### 收穫

了解為服務的優勢與Cloud Native應用發展趨勢，了解 Service Mesh 與 Istio 觀念，並能使用 Istio 於 Kubernetes。
