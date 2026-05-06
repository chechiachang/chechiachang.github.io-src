---
title: "Observe and evaluate LLM Coding Agents"
date: '2026-08-08T00:00:00Z'
# weight: 1
# aliases: ["/test"]
tags: ["openai", "aiops", "devops", "observability", "langfuse", "agent"]
categories: ["aiops", "observability", "generative"]
description: "LLM Coding Agent 正在改變軟體開發流程，但團隊常缺少可驗證品質與風險的機制。本分享聚焦於如何觀測與評估 LLM Coding Agent，從 tracing、資料集抽取到 LLM-as-a-judge，建立可重複的評測流程與 decision gate，讓模型與框架選型不再是賭博，而是可量化、可回歸、可持續優化的工程決策。"
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

### 📅 活動時間：2026-08-08
### 🔗 [活動連結](https://coscup.org/2026/)
### 📘 聯繫我 [Facebook](https://www.facebook.com/engineer.from.scratch)
### 📑 [投影片](https://chechia.net/slides/2026-08-08-coscup-llm-o11y/)

---

## Title

Observe and evaluate LLM Coding Agents

## Outline

在導入 LLM Coding Agent 到日常開發後，很多團隊會遇到問題：品質不穩、風險難估、模型升級缺少客觀依據。本分享會從實務流程出發，介紹如何觀測 Agent 行為、把評估流程自動化，並建立可持續迭代的 decision system。

1. 為什麼 LLM Coding Agent 需要 O11y 與 Evaluation
1. 從 trace 開始：觀測 agent 任務、工具調用與失敗模式
1. Observability != Decision System：看得到不代表能決策
1. LLM-as-a-judge 在 coding 任務中的價值與限制
1. 從 daily coding logs 抽取 dataset
1. 建立 regression evaluation pipeline 與 quality gate
1. 用量化結果比較不同模型與 agent framework
1. 把模型升級與框架切換變成可驗證工程流程

## Demo & POC

https://github.com/chechiachang/llm-o11y

1. Trace and observe local coding agents
1. Build coding-task evals with LLM-as-a-judge
1. Extract datasets from real developer-agent interactions
1. Run regression tests for model / framework change decisions

## Target group

- 正在導入 AI coding workflow 的工程團隊
- 關心品質、成本、延遲與回歸風險的 Tech Lead / SRE / Platform Team
- 已有 tracing / logging，但缺少可執行評估與 deployment gate 的團隊

## Slides

- [完整投影片與講稿](https://chechia.net/slides/2026-08-08-coscup-llm-o11y/)

## Author

Che-Chia Chang 是一名專注於後端開發、開發維運、容器化應用及 Kubernetes 開發與管理的技術專家，同時也是 Microsoft 最有價值專業人士（MVP）。

活躍於台灣技術社群，經常在 CNTUG、DevOps Taipei、GDG Taipei、Golang Taipei Meetup 等社群分享 DevOps、SRE、Kubernetes 及雲端運算相關技術。致力於推動開發與維運的最佳實踐，並熱衷於研究與應用最新的雲端與 AI 技術。

個人部落格：https://chechia.net

Che-Chia Chang is a technology expert specializing in backend development, DevOps, site reliability engineering (SRE), containerized applications, and Kubernetes development and management. He is also recognized as a Microsoft Most Valuable Professional (MVP).

Actively engaged in the Taiwanese tech community, he frequently shares insights on DevOps, SRE, Kubernetes, and cloud computing at CNTUG, DevOps Taipei, GDG Taipei, and Golang Taipei Meetup. Passionate about promoting best practices in development and operations, he continuously explores and applies the latest advancements in cloud and AI technologies.

https://chechia.net
