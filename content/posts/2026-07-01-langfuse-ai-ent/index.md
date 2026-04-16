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
### 📑 [投影片](https://chechia.net/slides/2025-10-23-k8sgpt-rag)

---

### Outline

這場分享改成「LLM/Agent 觀測資料管線實戰」：

1. 問題定義：為什麼傳統 APM 看不到 Agent 真正做了什麼
2. 架構藍圖：`LLM/Agent -> Bifrost -> OpenTelemetry -> Langfuse`
3. Bifrost 的角色：統一攔截多種 Agent/CLI 事件，標準化成 OTel Logs/Traces
4. Langfuse 的角色：把 prompt、trace、latency、cost 串起來做分析與評估
5. 為什麼不直接「LLM -> Langfuse」？
6. 實際踩坑：Codex CLI OTel 在不同模式下的可觀測性落差
7. 實作範例：從 CLI 事件到 Langfuse Trace 的映射方式
8. 企業落地：隱私遮罩、資料保留、告警與 SLO 設計
9. Q&A：如何從今天開始先上線最小可行觀測

### 為什麼不直接 LLM 到 Langfuse？

核心原因是很多 Agent CLI 對 OTel 的語意與完整性支援不一，直接對接 Langfuse 往往會遇到「資料不完整、語意不一致、難以跨工具關聯」。

- 例 1：社群已提出「希望 Codex CLI 直接整合 Langfuse tracing（含 input/output/timestamp）」需求，顯示目前不是開箱即用。
  - 參考：[openai/codex#1721 Add Langfuse Tracing Integration in Codex CLI](https://github.com/openai/codex/issues/1721)
- 例 2：`codex exec` / `codex mcp-server` 與互動模式在 OTel 支援程度曾出現落差，代表直接吃單一來源資料風險高。
  - 參考：[openai/codex#12913 codex exec emits no OTel metrics; codex mcp-server emits no OTel telemetry at all](https://github.com/openai/codex/issues/12913)
- 例 3：OTel 預設可能攜帶過多工具輸入輸出細節（如 patch body），隱私與治理要額外處理。
  - 參考：[openai/codex#17909 OTEL codex.tool_result logs full tool payloads by default](https://github.com/openai/codex/issues/17909)

因此實務上會用 Bifrost 先做一層標準化與治理，再送到 Langfuse，讓資料品質、隱私與可維運性可控。

### 主要收穫

- 了解如何用 Bifrost 把多來源 Agent/LLM 事件統一成 OTel，再送入 Langfuse。
- 知道直接整合單一 CLI 的風險，以及如何用中介層補齊資料語意與治理能力。
- 帶走一套可落地的最小觀測清單：prompt/response、latency、token、cost、error、tool call。

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
