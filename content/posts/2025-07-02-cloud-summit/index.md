---
title: "Cloud Summit 2025: 用 RAG 打造企業可對話 AI 知識庫。有問題問過 AI 後再來問我"
date: '2025-06-09T12:45:00Z'
# weight: 1
# aliases: ["/test"]
tags: ["openai", "generative", "ai", "kubernetes", "devops"]
categories: ["generative", "ai"]
description: 透過 RAG（檢索增強生成）技術，將企業內部文件轉為智能知識庫，提升資訊檢索與決策效率。本演講將探討 RAG 應用、技術架構與落地實踐，幫助開發團隊與企業更高效利用內部知識。企業內部文件往往分散於 Confluence、Google Drive、Notion 等平台，傳統關鍵字搜尋難以快速獲取準確資訊，導致溝通成本高、開發流程受阻。本演講將介紹如何運用 RAG（Retrieval-Augmented Generation）技術，結合 OpenAI 及向量數據庫，將企業內部文檔轉為智能知識庫。我們將探討文件解析、嵌入索引、AI 問答系統的技術架構與實作，幫助開發團隊構建高效 AI 助手，節省溝通成本，加速開發流程，提升決策與問題解決能力
#canonicalURL: "https://canonical.url/to/page"

showToc: true
TocOpen: false
#UseHugoToc: true

draft: false

hidemeta: false
comments: true
disableHLJS: false

hideSummary: false
ShowReadingTime: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
ShowWordCount: true
ShowRssButtonInSectionTermList: true

searchHidden: false
disableShare: false

#cover:
#    image: "" # image path/url
#    alt: "" # alt text
#    caption: "" # display caption under cover
#    relative: false # when using page bundles set this to true
#    hidden: false # only hide on current single page
---

- 活動時間: 2025-07-03T12:45:00Z
- [活動連結](https://cloudsummit.ithome.com.tw/2024/session-page/2620)
- [Facebook](https://www.facebook.com/engineer.from.scratch)
- [Twitter](https://twitter.com/chechiachang)
- [投影片 WIP](../../slides/2025-06-05-devops-rag-internal-ai)

---

## Info

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

## Target group

## Author

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
