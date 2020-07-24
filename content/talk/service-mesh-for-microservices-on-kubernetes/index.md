---
title: "Ithome Cloud Summit 2019: Service Mesh for Microservices on Kubernetes"

# Talk start and end times.
#   End time can optionally be hidden by prefixing the line with `#`.
date: 2019-05-15T12:00:00+08:00
date_end: 2019-05-15T12:30:00+08:00
all_day: false

# Schedule page publish date (NOT talk date).
publishDate: 2019-04-02T17:10:57+08:00

# Authors. Comma separated list, e.g. `["Bob Smith", "David Jones"]`.
authors: []

# Location of event.
location: "台北國際會議中心 (TICC)：110台北市信義區信義路五段1號"

# Name of event and optional event URL.
event: "IThome Cloud Summit 2019"
event_url: "https://cloudsummit.ithome.com.tw/"

# Abstract. What's your talk about?
abstract: "當眾多的為服務同時運作，產生複雜的依賴與交流，網路層不再只是有『有通就好』，而是需要精細且彈性的流量管理與監控，來提供穩定的效能。本次主題將基於 Kubernetes 平台上的 Istio ，探討 Service Mesh 的概念與相關應用。"

# Summary. An optional shortened abstract.
summary: "基於 Kubernetes 平台上的 Istio ，探討 Service Mesh 的概念與相關應用。"

# Is this a featured talk? (true/false)
featured: false

# Tags (optional).
#   Set `tags: []` for no tags, or use the form `tags: ["A Tag", "Another Tag"]` for one or more tags.
tags: ["kubernetes", "istio", "service-mesh"]

# Markdown Slides (optional).
#   Associate this page with Markdown slides.
#   Simply enter your slide deck's filename without extension.
#   E.g. `slides: "example-slides"` references 
#   `content/slides/example-slides.md`.
#   Otherwise, set `slides: ""`.
slides: ""
#slides: "service-mesh-with-istio"

# Optional filename of your slides within your talk folder or a URL.
url_slides: "https://docs.google.com/presentation/d/1Myn9v2OrWtrnzHIk_5KrKhE0f-rW51lxZMaX6IlYfak/edit?usp=sharing"

# Projects (optional).
#   Associate this talk with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects: ["deep-learning"]` references 
#   `content/project/deep-learning/index.md`.
#   Otherwise, set `projects: []`.
projects: []

# Links (optional).
url_pdf: ""
url_video: ""
url_code: "https://github.com/istio/istio"

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder. 
image:
  # Caption (optional)
  caption: "cncf/istio.png"

  # Focal point (optional)
  # Options: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight
  focal_point: ""

menu:
  main:
    parent: "Talks"
    weight: 1
---

### Outlines

傳統的 Monolith被分解為分散的微服務，以取得更高的效能與更彈性的管理。當眾多的為服務同時運作，產生複雜的依賴與交流，網路層不再只是有『有通就好』，而是需要精細且彈性的流量管理與監控，來提供穩定的效能。本次主題將基於 Kubernetes 平台上的 Istio ，探討 Service Mesh 的概念與相關應用。

1. 何為 Service Mesh ？為何需要 Service Mesh ？
2. Service Mesh 基本概念
3. 如何Service-to-Service的網路層管理監控
4. 導入 Istio 到 Kubernetes

### 目標聽眾

1. 微運大量微服務，希望導入Service Mesh 的Operator
2. 想了解微服務生態中竄紅的 Service Mesh

### 收穫

1. 了解為服務的優勢與Cloud Native應用發展趨勢
2. 了解 Service Mesh 與 Istio 觀念
3. 能使用 Istio 於 Kubernetes，進行服務網路的管理。

---

### 你有聽過 Microservice / Istio有聽過嗎？

今天來介紹一款好藥：Istio。如果你有以下問題：

- 維運大量(成千上百)微服務
- 需要服務對服務的流量控制，監控，管理

---

談 Service Mesh 之前，不免的要先談一下 Microservice，這個目前好像很夯的一個技術名詞。

如果手上有一個 App，會希望依照 Monolith 的架構，或是 Microservices？
Microservices 聽起來又新又潮。相對於 Monolith有許多明顯的好處：

- Decoupling
- Scalability
- Performance

也有明顯的壞處：

- Development Complexity
- Operation Cost

> 沒事別挖坑跳

---

何為 Service Mesh？

- Service Mesh: Model / Pattern
- Implementations: linkerd, istio, ...
- 基於底層的網路服務，在複雜的 topology 中可靠的傳遞

使用Microservie 可能會遇到的問題：

- Traffic control
- Monitoring
- A/B Testing
