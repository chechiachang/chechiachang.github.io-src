---
title: "LLM O11y：從 Observability 到 Decision System"
description: "從 Langfuse observability 出發，補上 evaluation、dataset、regression 與 decision gate，建立可落地的 LLM Decision System。"
tags: ["llm", "agent", "observability", "langfuse", "evaluation", "aiops"]
categories: ["aiops", "observability"]
date: '2026-07-02T15:30:00Z'
outputs: ["Reveal"]
reveal_hugo:
  custom_theme: "reveal-hugo/themes/robot-lung.css"
  margin: 0.2
  highlight_theme: "color-brewer"
  transition: "slide"
  transition_speed: "fast"
---

## LLM O11y：從 Observability 到 Decision System

---

## 核心問題

目前多數團隊在導入 LLM / AI Agent 時，已經具備：

- tracing / logging
- prompt 管理
- 各種 agent framework（LangChain / AutoGen / 各種新 repo）
- 基本 observability 工具（如 Langfuse）

但仍然無法回答一個關鍵問題：

> 這次 model 或 framework 升級，到底該不該上 production？

---

## Goals

- control llm -> do exactly what we want
- control cost -> avoid unexpected cost increase



---

## 現況問題：我們其實在用「感覺」做決策

常見現象：

- 新 LLM model 出來就想升級
- 看到熱門 AI Agent framework 就想導入
- 依賴 demo impression 做技術選型
- 沒有系統化 evaluation pipeline
- 沒有 regression baseline

結果是：

- 品質變差但沒人知道
- latency / cost 上升但難追原因
- system behavior 不可預測
- upgrade decision 完全依賴直覺

---

## 關鍵誤解

### Observability != Decision System

Observability（例如 Langfuse）可以提供：

- trace（prompt / response / tool calls）
- latency / token / cost
- debug 能力

但它只能回答：

> 發生了什麼？

無法回答：

> 我應不應該改？  
> 這個改動是不是變好？

---

## LLM-as-a-judge：有用，但有限

優點：

- scalable
- 可以做即時評估
- 可快速建立 feedback loop

但限制非常明確：

- 有 bias（偏好 verbose / certain patterns）
- 不穩定（不同 model judge 結果不同）
- 不等於 ground truth

結論：

> LLM judge 是 heuristic，不是 truth

---

## 正確做法：建立 feedback system

真正需要的是一個 closed-loop system：

```text
observability -> evaluation -> dataset -> regression -> decision
```

---

## 1. Observability（發生了什麼）

透過 tracing 收集：

- prompt / response
- tool calls
- latency / cost
- agent execution path

工具例：Langfuse

但這只是在「看系統」，不是在「控制系統」

---

## 2. Evaluation（好不好）

使用：

- LLM-as-a-judge
- rule-based scoring
- structured rubric

注意：evaluation 本身也是一個 model，需要被監控

---

## 3. Dataset（從 production 來）

最有價值的資料來源不是 benchmark，而是：

- real user queries
- real failure cases
- real edge cases

流程：

trace -> detect failure -> promote to dataset

---

## 4. Regression（關鍵缺口）

比較 model / framework 時不能靠感覺，而是：

- 同一 dataset
- 不同 model
- 比較差異

輸出應該是：

- quality change
- latency change
- cost change
- failure pattern change

---

## 5. Decision（真正價值）

最終要有明確 gate：

只有當：

- quality >= baseline
- no regression on critical cases
- latency within SLO
- cost within budget

才允許 deploy

---

## LLM SLO（工程化核心）

借用 SRE 思維：

- Quality SLO：correctness / helpfulness
- Latency SLO：p95 latency
- Cost SLO：cost per request

---

## Failure Taxonomy（讓 debug 可控）

不是所有錯誤都一樣：

- hallucination
- tool misuse
- reasoning error
- format / schema break

不同 failure -> 不同修法

---

## 為什麼現在工具還不夠

即使有 observability tools（如 Langfuse），仍然缺：

- dataset curation
- regression testing
- decision policy

所以現況是：

我們看得到 system，但無法控制 system

---

## LLM O11y 的定位（PoC）

本專案（llm-o11y）提供一個最小可行的：

LLM Decision System prototype

能力包含：

- trace collection
- basic evaluation
- dataset accumulation
- model comparison prototype

目標不是取代工具，而是補上：

decision layer

---

## 核心結論

沒有 evaluation：

LLM upgrade = gambling

有完整 feedback loop：

- 可觀測
- 可評估
- 可回歸
- 可決策

---

## 最終訊息

Observability tells you what happened

Evaluation tells you how good it is

Regression tells you if it got better

Decision tells you what to do

---

## LLM O11y 的本質

不是 logging tool

而是：

一個 AI 系統的 feedback control system
