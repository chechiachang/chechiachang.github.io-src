---
title: "Workshop: LLM O11y 從 Observability 到 Decision System"
description: "90 分鐘 hands-on workshop，從 Langfuse observability 到 evaluation、dataset、regression 與 decision gate。"
tags: ["llm", "langfuse", "observability", "evaluation", "workshop", "aiops"]
categories: ["aiops", "workshop"]
date: '2026-05-02T13:30:00Z'
outputs: ["Reveal"]
reveal_hugo:
  custom_theme: "reveal-hugo/themes/robot-lung.css"
  margin: 0.2
  highlight_theme: "color-brewer"
  transition: "slide"
  transition_speed: "fast"
---

{{% section %}}

### Workshop 行前準備

- 攜帶筆電，可上網
- 安裝好 Docker Desktop
- 安裝好 Git 與 VS Code
- 下載 [workshop 範例程式碼](https://github.com/chechiachang/llm-o11y)
- 講師會提供範例 `.env` 與測試資料

🔽

---

### Workshop Repo

- SSH: `git@github.com:chechiachang/llm-o11y.git`
- HTTPS: `https://github.com/chechiachang/llm-o11y`

```bash
git clone git@github.com:chechiachang/llm-o11y.git
cd llm-o11y
```

---

### Workshop 目標

- 建立 local observability stack（Bifrost + Langfuse）
- 讓 traces 進入 evaluation flow（含 LLM-as-a-judge）
- 從 traces 產生 dataset，跑 regression 比較
- 建立可執行的 decision gate（是否可 deploy）

{{% /section %}}

---

#### AI Enterprise Summit 2026
## LLM O11y：從 Observability 到 Decision System
##### 90 分鐘 workshop
##### ~ Che Chia Chang @ [chechia.net](https://chechia.net) ~

---

{{< slide content="slides.about-me" >}}

---

### 大綱

本次 workshop 以 hands-on 為主，講解為輔。

1. LAB1：把 observability stack 跑起來
1. 講解：Observability != Decision System
1. LAB2：為 traces 加上 evaluation
1. LAB3：從 traces 產生 dataset
1. LAB4：跑 regression 與 decision gate
1. 驗收、回顧、Q&A

---

## 核心問題

多數團隊已經有：

- trace / logging
- prompt 管理
- agent framework（LangChain / AutoGen / others）
- observability 工具（Langfuse）

但仍無法回答：

> 這次 model 或 framework 升級，該不該上 production？

---

## 關鍵誤解

### Observability != Decision System

Observability 只能回答：

> 發生了什麼？

Decision System 需要回答：

> 我應不應該改？  
> 這次改動是不是變好？

---

{{% section %}}

### LAB1：啟動 LLM O11y Stack

目標：把本地端觀測平台跑起來，先確保 trace 能收集。

```bash
cd llm-o11y
cp .env.example .env
docker compose up -d
```

---

### LAB1：確認服務健康

請確認：

- Langfuse UI 可開啟
- Gateway / API 可回應
- demo app 能發送一筆 trace

```bash
docker compose ps
```

---

### LAB1：做第一筆 trace

```bash
make demo-trace
```

觀察重點：

- prompt / response
- token usage
- latency

{{% /section %}}

---

## Evaluation：把主觀變可比較

建議組合：

- LLM-as-a-judge（快速、可擴）
- rule-based checks（格式、schema、constraints）
- task rubric（符合業務定義的好壞）

---

{{% section %}}

### LAB2：加入 LLM-as-a-judge

目標：針對既有 traces 自動評分。

```bash
make eval-run
```

---

### LAB2：加上 Rule-based Checks

常見檢查：

- JSON schema 是否合法
- 必要欄位是否存在
- 關鍵關鍵字是否命中

```bash
make eval-rules
```

{{% /section %}}

---

## Dataset：從真實流量累積

不是 benchmark 優先，而是 production-like data：

- 真實 query
- 真實 failure cases
- 真實 edge cases

流程：

`trace -> triage -> label -> dataset`

---

{{% section %}}

### LAB3：從 traces 產生 dataset

```bash
make dataset-export
```

輸出目標：

- baseline dataset
- failure-focused dataset

---

### LAB3：資料集分層

最低限度建議分三層：

- smoke（快速）
- core（關鍵流程）
- edge（高風險案例）

{{% /section %}}

---

## Regression：比較不能靠感覺

固定同一份 dataset 比較不同：

- model
- prompt strategy
- agent framework

輸出指標：

- quality delta
- latency delta
- cost delta

---

{{% section %}}

### LAB4：跑 regression

```bash
make regression-run
```

---

### LAB4：設定 Decision Gate

只有同時滿足才允許 deploy：

- quality >= baseline
- no critical regression
- latency within SLO
- cost within budget

```bash
make decision-gate
```

{{% /section %}}

---

## Failure Taxonomy

先分類，再修復：

- hallucination
- tool misuse
- reasoning error
- format/schema break

---

## 最小可行架構

```text
Agent Runtime
  -> Tracing (Langfuse)
  -> Evaluation
  -> Dataset Store
  -> Regression Runner
  -> Decision Policy
```

---

## 核心訊息

沒有 evaluation：

**LLM upgrade = gambling**

有 feedback loop：

**Observe -> Evaluate -> Regress -> Decide**

---

## Thank you

下午本堂 Session 歡迎參考
- Session: 15:30 - 16:00 [LLM O11y：從 Observability 到 Decision System](https://chechia.net/posts/2026-07-01-langfuse-ai-ent/)

謝謝大家。
