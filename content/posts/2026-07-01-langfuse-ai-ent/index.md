---
title: "Observe and evaluate LLM applications with Langfuse"
date: '2026-04-23T13:20:00Z'
# weight: 1
# aliases: ["/test"]
tags: ["kubernetes", "openai", "aiops", "devops", "observability", "langfuse"]
categories: ["kubernetes", "aiops", "observability"]
description: "LLM（大型語言模型）應用的興起帶來了新的挑戰，尤其是在觀察性（observability）方面。傳統的監控工具無法有效捕捉和分析 LLM 的行為和性能指標，這使得開發者和運維團隊難以評估 LLM 應用的健康狀況和性能表現。Langfuse 是一個專為 LLM 應用設計的觀察性平台，提供了全面的監控、日誌分析和性能評估功能，幫助團隊更好地理解和優化他們的 LLM 應用。在本次演講中，我們將深入探討 Langfuse 的功能和優勢，以及如何利用它來提升 LLM 應用的可觀察性和性能。"
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

### 📅 活動時間：2026-07-01 21:20
### 🔗 [活動連結](https://k8s.ithome.com.tw/2025/session-page/4081)
### 📘 聯繫我 [Facebook](https://www.facebook.com/engineer.from.scratch)
### 📑 [投影片](https://chechia.net/slides/2026-07-01-langfuse-ai-ent/)

---

## Title

LLM O11y：從 Observability 到 Decision System

## Outline

1. 為什麼 observability 還不夠：Observability != Decision System
2. 常見誤區：用 impression 做 model/framework 選擇決策
3. LLM-as-a-judge 的價值與限制
4. 從 observability 到 closed-loop feedback system
5. evaluation / dataset / regression / decision gate 的實作框架
6. LLM SLO 與 failure taxonomy 的工程化方法
7. llm-o11y PoC：decision layer 最小可行實作
8. 總結：把 LLM 升級從 gambling 變成可驗證決策

## Target group

- 正在導入或維運 LLM / Agent 系統的工程團隊
- 關心品質、延遲、成本與上線風險的 Tech Lead / SRE / Platform Team
- 已有 tracing / logging / Langfuse，但缺乏 regression 與 deploy gate 的團隊

## Slides

- [完整投影片與講稿](https://chechia.net/slides/2026-07-01-langfuse-ai-ent/)

## Author

Che-Chia Chang 是一名專注於後端開發、開發維運、容器化應用及 Kubernetes 開發與管理的技術專家，同時也是 Microsoft 最有價值專業人士（MVP）。

活躍於台灣技術社群，經常在 CNTUG、DevOps Taipei、GDG Taipei、Golang Taipei Meetup 等社群分享 DevOps、SRE、Kubernetes 及雲端運算相關技術。致力於推動開發與維運的最佳實踐，並熱衷於研究與應用最新的雲端與 AI 技術。

個人部落格：https://chechia.net

Che-Chia Chang is a technology expert specializing in backend development, DevOps, site reliability engineering (SRE), containerized applications, and Kubernetes development and management. He is also recognized as a Microsoft Most Valuable Professional (MVP).

Actively engaged in the Taiwanese tech community, he frequently shares insights on DevOps, SRE, Kubernetes, and cloud computing at CNTUG, DevOps Taipei, GDG Taipei, and Golang Taipei Meetup. Passionate about promoting best practices in development and operations, he continuously explores and applies the latest advancements in cloud and AI technologies.

https://chechia.net
