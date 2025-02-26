---
title: "Cloud Summit: 用 RAG 打造企業可對話 AI 知識庫。有問題問過 AI 後再來問我"

event: Cloud Summit 2025
event_url: https://cloudsummit.ithome.com.tw/2025

location: 南港展覽館二館7樓
address:
  street: No. 2, Jingmao 2nd Rd, Nangang District, Taipei City, 115
  city: Taipei
  region: Taiwan
  postcode: '115'
  country: Taiwan

summary: 透過 RAG（檢索增強生成）技術，將企業內部文件轉為智能知識庫，提升資訊檢索與決策效率。本演講將探討 RAG 應用、技術架構與落地實踐，幫助開發團隊與企業更高效利用內部知識。
abstract: '企業內部文件往往分散於 Confluence、Google Drive、Notion 等平台，傳統關鍵字搜尋難以快速獲取準確資訊，導致溝通成本高、開發流程受阻。本演講將介紹如何運用 RAG（Retrieval-Augmented Generation）技術，結合 OpenAI 及向量數據庫，將企業內部文檔轉為智能知識庫。我們將探討文件解析、嵌入索引、AI 問答系統的技術架構與實作，幫助開發團隊構建高效 AI 助手，節省溝通成本，加速開發流程，提升決策與問題解決能力。'

# Talk start and end times.
#   End time can optionally be hidden by prefixing the line with `#`.
date: '2025-07-03T12:45:00Z'
date_end: '2025-07-03T13:30:00Z'
all_day: false

# Schedule page publish date (NOT talk date).
publishDate: '2025-06-01T00:00:00Z'

authors: []
tags: ["openai", "generative", "ai", "kubernetes", "devops"]
categories: ["generative", "ai"]

# Is this a featured talk? (true/false)
featured: false

image:
  #caption: 'Image credit: [**Unsplash**](https://unsplash.com/photos/bzdhc5b3Bxs)'
  focal_point: Right

links:
  - name: 活動連結
    icon: calendar
    icon_pack: fa
    url: https://cloudsummit.ithome.com.tw/2024/session-page/2620
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
slides: 2025-07-03-build-internal-rag-ai-agent

# Projects (optional).
#   Associate this post with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects = ["internal-project"]` references `content/project/deep-learning/index.md`.
#   Otherwise, set `projects = []`.
#projects:
#  - example

---

# Info

開發團隊需要將經驗與知識，透過文件化的方式保存下來，以便未來查詢與學習。然而，企業內部文件往往分散於 Confluence、Google Drive、Notion 等平台，傳統關鍵字搜尋難以快速獲取準確資訊，導致溝通成本高、開發流程受阻。又或是，當開發團隊需要查詢特定知識時，往往需要透過 Slack、Email 等方式詢問同事，這樣的溝通成本不僅浪費時間，也容易造成資訊不對稱。

本演講將介紹如何運用 RAG（Retrieval-Augmented Generation）技術，結合 OpenAI 及向量數據庫，將企業內部文檔轉為智能知識庫。

我們將探討文件解析、嵌入索引、AI 問答系統的技術架構與實作，幫助開發團隊構建高效 AI 助手，節省溝通成本，加速開發流程，提升決策與問題解決能力。

大綱：
- 為什麼企業知識管理難？
  - 文件分散（Confluence、Google Drive、Notion、SharePoint）
  - 搜索體驗不佳，開發者找不到關鍵資訊
  - 知識難以沉澱，員工流失即知識流失
- RAG 如何解決這些問題？
  - 透過檢索增強生成（Retrieval-Augmented Generation）提升答案準確性
  - 把內部文件轉為可查詢的知識庫
  - 讓 AI 提供具體、準確、即時的回覆
- 技術架構與實作指南
  - 文件解析與嵌入（HTML、Markdown、Confluence API）
  - 使用向量數據庫實現高效檢索
  - OpenAI API + LangChain 打造智能問答系統
- 案例分享與落地經驗

# Target group

# Author

Che-Chia Chang 是一名專注於後端開發、開發維運、容器化應用及 Kubernetes 開發與管理的技術專家，同時也是 Microsoft 最有價值專業人士（MVP）。

活躍於台灣技術社群，經常在 CNTUG、DevOps Taipei、GDG Taipei、Golang Taipei Meetup 等社群分享 DevOps、SRE、Kubernetes 及雲端運算相關技術。致力於推動開發與維運的最佳實踐，並熱衷於研究與應用最新的雲端與 AI 技術。

個人部落格：https://chechia.net

Che-Chia Chang is a technology expert specializing in backend development, DevOps, site reliability engineering (SRE), containerized applications, and Kubernetes development and management. He is also recognized as a Microsoft Most Valuable Professional (MVP).

Actively engaged in the Taiwanese tech community, he frequently shares insights on DevOps, SRE, Kubernetes, and cloud computing at CNTUG, DevOps Taipei, GDG Taipei, and Golang Taipei Meetup. Passionate about promoting best practices in development and operations, he continuously explores and applies the latest advancements in cloud and AI technologies.

https://chechia.net

- 2024 Ithome Kubernetes Summit
- 2024 Ithome Cloud Summit
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
