---
title: "O11y day 2026: Observe and evaluate LLM applications with Langfuse"
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

### 📅 活動時間：2026-04-23 21:20
### 🔗 [活動連結](https://k8s.ithome.com.tw/2025/session-page/4081)
### 📘 聯繫我 [Facebook](https://www.facebook.com/engineer.from.scratch)
### 📑 [投影片](https://chechia.net/slides/2025-10-23-k8sgpt-rag)

---

### Outline

Langfuse 是一個專為 LLM（大型語言模型）應用設計的觀察性平台，提供了全面的監控、日誌分析和性能評估功能，幫助團隊更好地理解和優化他們的 LLM 應用。在本次演講中，我們將深入探討 Langfuse 的功能和優勢，以及如何利用它來提升 LLM 應用的可觀察性和性能。

Langfuse 的核心功能包括：
1. **全面監控**：提供對 LLM 應用的實時監控，捕捉關鍵性能指標（KPIs）和行為模式。
2. **日誌分析**：收集和分析 LLM 應用的日誌數據，幫助團隊識別問題和優化性能。
3. **性能評估**：提供詳細的性能評估報告，幫助團隊了解 LLM 應用的運行狀況和潛在瓶頸。
4. **可視化工具**：提供直觀的可視化工具，幫助團隊更好地理解和分析 LLM 應用的數據。
5. **自定義警報**：允許團隊設置自定義警報，及時通知他們有關 LLM 應用的異常行為或性能問題。

本次演講將通過實際案例展示如何使用 Langfuse 來提升 LLM 應用的可觀察性和性能，並討論在實際應用中遇到的挑戰和解決方案。更好地管理和優化他們的 LLM 應用。

### 主要收穫

了解哪些 Langfuse 信號與提示品質、延遲與成本相關，讓你能優先進行觀察性儀表板的部署。將 prompt、embeddings 與 metrics 導入 Langfuse

### 為什麼這場演講重要

- 我有在大規模 Kubernetes 與 LLM 工作負載環境中運營的經驗，曾推動將 Langfuse 作為生產 AI 服務的觀察性管線，降低延遲波動並挖掘出隱藏的失敗模式。
- Langfuse 能將提示、嵌入向量與系統指標關聯起來，補足傳統監控的盲點，這種視角與會議「現代 AI 的可觀察性」主題高度契合。
- 與會者將帶走一份清單，明確指出應追蹤哪些指標、如何呈現在儀表板上，以及在部署下個 LLM 特性前該寫哪些防護腳本。

參考資料
- [Langfuse 官方網站](https://www.langfuse.com/)

## Author

Che-Chia Chang 是一名專注於後端開發、開發維運、容器化應用及 Kubernetes 開發與管理的技術專家，同時也是 Microsoft 最有價值專業人士（MVP）。

活躍於台灣技術社群，經常在 CNTUG、DevOps Taipei、GDG Taipei、Golang Taipei Meetup 等社群分享 DevOps、SRE、Kubernetes 及雲端運算相關技術。致力於推動開發與維運的最佳實踐，並熱衷於研究與應用最新的雲端與 AI 技術。

個人部落格：https://chechia.net

Che-Chia Chang is a technology expert specializing in backend development, DevOps, site reliability engineering (SRE), containerized applications, and Kubernetes development and management. He is also recognized as a Microsoft Most Valuable Professional (MVP).

Actively engaged in the Taiwanese tech community, he frequently shares insights on DevOps, SRE, Kubernetes, and cloud computing at CNTUG, DevOps Taipei, GDG Taipei, and Golang Taipei Meetup. Passionate about promoting best practices in development and operations, he continuously explores and applies the latest advancements in cloud and AI technologies.

https://chechia.net
