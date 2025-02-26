---
title: "Workshop: RAG打造企業AI知識庫：把一甲子功力傳給新人"

event: DevOpsDay Taipei 2025
event_url: https://devopsdays.tw/2025/

location: 臺北文創大樓6樓ABC會議室
address:
  street: 台北市信義區光復南路133號
  city: Taipei
  region: Taiwan
  postcode: '110'
  country: Taiwan

summary: 學員將學會如何利用 RAG 技術，結合 OpenAI、LangChain、Qdrant 向量數據庫，構建企業內部文檔的智能知識庫，並能設計與實作一個基於自然語言處理（NLP）的查詢系統，來提升開發團隊的效率與知識管理能力。
abstract: 學員將學會如何利用 RAG 技術，結合 OpenAI、LangChain、Qdrant 向量數據庫，構建企業內部文檔的智能知識庫，並能設計與實作一個基於自然語言處理（NLP）的查詢系統，來提升開發團隊的效率與知識管理能力。

# Talk start and end times.
#   End time can optionally be hidden by prefixing the line with `#`.
date: '2025-06-05T12:45:00Z'
date_end: '2025-06-06T13:30:00Z'
all_day: false

# Schedule page publish date (NOT talk date).
publishDate: '2025-05-01T00:00:00Z'

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

學員將學會如何利用 RAG 技術，結合 OpenAI、LangChain、Qdrant 向量數據庫，構建企業內部文檔的智能知識庫，並能設計與實作一個基於自然語言處理（NLP）的查詢系統，來提升開發團隊的效率與知識管理能力。

- 什麼是 RAG？
  - 介紹 RAG（Retrieval-Augmented Generation）技術如何結合檢索與生成提升問答準確性。
  - 為什麼企業需要智能知識庫？
  - RAG 的應用場景：知識庫建立、開發支援、技術決策等。
- Python 與 OpenAI：
  - 使用 OpenAI API 架構與語言模型，快速構建生成模型
- LangChain：介紹 LangChain 框架如何簡化 RAG 實現
- 如何利用 LangChain 整合多種數據源與生成模型
- Qdrant 向量數據庫：
  - 向量數據庫的概念與作用
  - 如何利用 Qdrant 儲存與檢索內部文檔的嵌入向量
- 構建 RAG 系統：實作步驟與演示
  - 數據預處理與文檔轉換
  - 將處理後的文本轉換為向量表示（embedding）
  - 利用 Qdrant 向量數據庫儲存這些嵌入並執行檢索
- 使用 LangChain 結合 OpenAI 模型與 Qdrant，製作自動化問答系統

# Target group

本次工作坊會提供參與者一個簡單的環境，讓參與者可以透過遠端操作來實作基本 RAG AI Agent。參與者必備個人筆電，透過 SSH 操控遠端機器。

必備知識：Linux 操作基本知識，Docker 操作基本知識，會使用 SSH 連線 / Bash / docker。

工作坊結束後，學員將能夠：
- 理解並實作 RAG 技術，將內部文檔轉化為智能知識庫
- 使用 Python、LangChain 和 OpenAI 構建基於檢索的問答系統
- 利用 Qdrant 向量數據庫進行高效檢索，提升開發流程中的知識管理效率。
- 這樣的工作坊結構能夠平衡理論與實踐，並為學員提供實際動手操作的機會。

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
