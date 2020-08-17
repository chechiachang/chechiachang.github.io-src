---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Ithome Cloud Summit 2020: Terraform Infrastructure as Code"
event: "2020 IThome Cloud Summit"
event_url: "https://cloudsummit.ithome.com.tw/agenda.html"
location: "台北國際會議中心 (TICC)"
summary: "Cloud Native Apache Kafka on Kubernetes"
abstract: "Infrastructure as code 的概念已經推廣許久，不是什麼新概念，本次分享以一步一步實際導入 Terraform 的經驗，描述如何針對需求對症下藥，帶領公司導入 infrastructure as code，內容包含實作步驟，心得感想，並紀錄沿路踩過的雷，希望能提供其他團隊導入經驗。"

# Talk start and end times.
#   End time can optionally be hidden by prefixing the line with `#`.
date: 2020-02-11T17:26:22+08:00
date_end: 2020-02-11T17:26:22+08:00
all_day: false

# Schedule page publish date (NOT talk date).
publishDate: 2020-02-11T17:26:22+08:00

authors: []
tags: ["kafka", "kubernetes", "devops", "stateful", "distributed"]

# Is this a featured talk? (true/false)
featured: false

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder. 
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: false

# Custom links (optional).
#   Uncomment and edit lines below to show custom links.
# links:
# - name: Follow
#   url: https://twitter.com
#   icon_pack: fab
#   icon: twitter

# Optional filename of your slides within your talk's folder or a URL.
url_slides:

url_code:
url_pdf:
url_video:

# Markdown Slides (optional).
#   Associate this talk with Markdown slides.
#   Simply enter your slide deck's filename without extension.
#   E.g. `slides = "example-slides"` references `content/slides/example-slides.md`.
#   Otherwise, set `slides = ""`.
slides: ""

# Projects (optional).
#   Associate this post with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects = ["internal-project"]` references `content/project/deep-learning/index.md`.
#   Otherwise, set `projects = []`.
projects: []

menu:
  main:
    parent: "Talks"
    weight: 1
---

Infrastructure as code 的概念已經推廣許久，不是什麼新概念，然而公司卻尚未導入。op 需要新環境都是透過 GUI 去開環境。

環境越開越多，漸漸浮現出幾個痛點：

「這個環境怎麼少一個設定」-> 環境沒標準化

「是誰改了這個設定」-> 環境的變更沒有 change log，無法 blame

「你環境開錯了吧」 -> 環境交付沒自動化測試

其他如：只看單一環境不在乎全局設定，環境數量多不易管理或更新維護，人工操作錯誤率高...等問題層出不窮。

本次分享以一步一步實際導入 Terraform 的經驗，描述如何針對需求對症下藥，帶領公司導入 infrastructure as code，內容包含實作步驟，心得感想，並紀錄沿路踩過的雷，希望能提供其他團隊導入經驗。
