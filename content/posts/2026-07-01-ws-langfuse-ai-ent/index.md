---
title: "Workshop: LLM O11y 從 Observability 到 Decision System"
date: '2026-04-21T13:20:00Z'
tags: ["kubernetes", "openai", "aiops", "devops", "observability", "langfuse", "workshop"]
categories: ["kubernetes", "aiops", "observability", "workshop"]
description: "本工作坊將實作 llm-o11y：在 localhost 以 Docker Compose 啟動 Bifrost 與 Langfuse，串接 LLM AI Gateway 與 tracing，建立 evaluation 與 LLM-as-a-judge，抽取 dataset，並組成可重現的 AI 開發 workflow。"

showToc: true
TocOpen: false

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
---

### 📅 活動時間：2026-07-02 13:30-15:00
### 🔗 [活動連結](https://aienterprise.ithome.com.tw/2026/session/4790)
### 📑 [投影片](https://chechia.net/slides/2026-07-01-ws-langfuse-ai-ent/)

### 📘 Workshop Repo

- [chechiachang/llm-o11y](https://github.com/chechiachang/llm-o11y)

## Workshop Overview

這是一場 hands-on workshop，目標是把 LLM 應用從「可觀測」推進到「可評估、可決策」。
你會在自己的電腦上直接跑完整流程，從 tracing 到 evaluation，再到 workflow 落地。

## Agenda

1. Docker Compose 在 localhost 啟動 Bifrost 與 Langfuse
2. 串接 LLM AI Gateway 與 Langfuse tracing
3. 建立 evaluation 與 LLM-as-a-judge
4. 從實務觀測資料抽取 dataset
5. 串成可重現的開發 workflow

## What You Will Build

- 本地可執行的 observability stack（Bifrost + Langfuse）
- 一條可重跑的 evaluation pipeline
- 可持續擴充的 dataset 與 regression 基礎
- 能用於模型/框架決策的 workflow

## Prerequisites

- 自備筆電（must bring your own PC）
- 可連外網路（stable network required）
- 可使用 Docker / Docker Compose
- 可使用 Git 與 terminal

## Workshop Resources

- Azure OpenAI models will be provided by the workshop.

## Target Audience

- 正在導入或維運 LLM / Agent 系統的工程團隊
- 想建立 tracing + evaluation + decision flow 的 Tech Lead / SRE / Platform Team
- 想把 PoC 推進到可持續工作流的開發者
