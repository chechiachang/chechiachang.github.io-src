+++
title = "Manage and Schedule GPU Computing Tasks on Kubernetes"

# Talk start and end times.
#   End time can optionally be hidden by prefixing the line with `#`.
date = 2018-05-16T11:00:00+08:00
date_end = 2018-05-16T17:00:00+08:00
all_day = false

# Schedule page publish date (NOT talk date).
publishDate = 2018-05-10T18:46:23+08:00

# Authors. Comma separated list, e.g. `["Bob Smith", "David Jones"]`.
authors = []

# Location of event.
location = ""

# Name of event and optional event URL.
event = "iThome Cloud & Edge Summit 2018"
event_url = "https://cloudsummit.ithome.com.tw/2018/"

# Abstract. What's your talk about?
abstract = ""

# Summary. An optional shortened abstract.
summary = ""

# Is this a featured talk? (true/false)
featured = false

# Tags (optional).
#   Set `tags = []` for no tags, or use the form `tags = ["A Tag", "Another Tag"]` for one or more tags.
tags = ["kubernetes", "gpu-computing", "cloud-computing", "container", "automation"]

# Markdown Slides (optional).
#   Associate this page with Markdown slides.
#   Simply enter your slide deck's filename without extension.
#   E.g. `slides = "example-slides"` references 
#   `content/slides/example-slides.md`.
#   Otherwise, set `slides = ""`.
slides = ""

# Optional filename of your slides within your talk folder or a URL.
url_slides = "https://www.slideshare.net/CheChiaChang/automated-containerdeploymentonkubernetes"

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

Manage and Schedule GPU Computing Tasks on Kubernetes

使用Kubernets管理集群GPU機器，靈活的分配調度GPU資源，並自動排程GPU運算工作。
使用者如資料科學家，只需將運算工作實施到Kubernetes上，Kubernetes便會檢視機器上可用的GPU資源，將運算工作分配到合適的機器
上，並監控工作的狀況。如資源不足Kubernetes會自動將工作加入排程，當前面的工作完成，GPU資源釋放後，Kubernetes會自動將運算
工作，配置到合適的機器上。管理者如系統工程師，只需透過Kubernetes，將機器上的GPU資源加入到Kubernetes。

1. Why we need Kubernetes for GPUs computing? Pros & Cons
2. How to deploy a GPU-enabled Kubernetes cluster
3. Run GPU computing on Kubernetes cluster
