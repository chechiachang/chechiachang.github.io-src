---
title: "從 Model Context Protocol 初探 AI Agent Protocol：快速打造多工 Agent Server"

event: "COSCUP 2025"
event_url: https://coscup.org/2025/

location: 國立臺灣科技大學
address:
  street: 106 台北市大安區基隆路四段 43 號
  city: Taipei
  region: Taiwan
  postcode: '106'
  country: Taiwan

summary: '深入探索 Model Context Protocol（MCP），學習如何透過標準化協議打造支援多 Agent 協作與工具調用的進階 AI Agent Server。'
abstract: 'AI Agent 系統的發展正逐步邁向模組化與多 Agent 協作的新階段，而 Model Context Protocol（MCP） 正是促進模型、工具與本地資源之間有效協作的關鍵協議。透過 MCP，開發者可用統一且安全的方式讓 LLM 與本地/遠端服務互動，實現更穩定、可追蹤、可擴充的多工 Agent 架構。本場演講將深入解析 MCP 的架構、設計原則與實作範例，並展示如何使用開源 mcp-server 快速打造一套具備上下文共享、工具調用與多模型協作能力的 Agent Server。最後將透過實機 Demo 展現 MCP 在真實 AI Workflow 中的應用潛力。'

# Talk start and end times.
#   End time can optionally be hidden by prefixing the line with `#`.
date: '2025-08-09T12:45:00Z'
date_end: '2025-08-09T13:30:00Z'
all_day: false

# Schedule page publish date (NOT talk date).
publishDate: '2025-07-01T00:00:00Z'

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
    url: https://coscup.org/2025/
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

Model Context Protocol（MCP）是一項由 Anthropic 推出的開放標準，旨在為大型語言模型（LLMs）提供一種標準化的方式，以連接和操作各種資料來源（如本地檔案、資料庫）和工具（如 GitHub、Google Maps）。MCP 的目標是簡化 AI 應用與外部資源的整合過程，類似於 USB-C 為實體設備提供通用連接介面。

隨著 AI 技術的快速發展，AI 助手需要與各種資料來源和工具進行互動，以提供更豐富和個性化的服務。Model Context Protocol（MCP）作為一種開放標準，為 AI 應用提供了一種統一且安全的方式，連接到不同的資料來源和工具。

本場演講將介紹 MCP 的架構、設計原則與實作範例，並展示如何使用開源 mcp-server 快速打造一套具備上下文共享、工具調用與多模型協作能力的 Agent Server。最後將透過實機 Demo 展現 MCP 在真實 AI Workflow 中的應用潛力。

演講大綱
- 問題背景與動機
  - AI 助手在實際應用中面臨的挑戰：需要訪問多種資料來源和工具，現有整合方式的限制：開發成本高、維護困難
- 認識 Model Context Protocol（MCP）MCP 的定義與目標
  - MCP 的核心架構：主機、客戶端、伺服器
  - MCP 如何簡化 AI 應用與外部資源的整合
- MCP 的工作原理
  - MCP 如何建立 AI 應用與資料來源/工具之間的橋樑
  - MCP 的模組化設計如何支持功能擴展
- 使用 mcp-server 快速建立多工 Agent Server
  - mcp-server 的功能與架構
  - 如何使用 mcp-server 整合多個 Agent 和工具
  - 實作示範：建立一個能夠協作完成任務的多 Agent 系統
- 實際應用案例與未來展望
  - MCP 在企業助手、開發工具等領域的應用
  - MCP 的安全性與擴展性
  - 未來 AI 系統與 MCP 的整合趨勢

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

# References

- https://arxiv.org/pdf/2504.16736v2
