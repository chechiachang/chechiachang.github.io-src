---
title: "Observe and evaluate LLM Coding Agents"
description: "從 LLM coding agent observability 出發，建立 evaluation、dataset、regression 與 decision gate，讓模型與框架升級可驗證。"
tags: ["llm", "agent", "observability", "evaluation", "aiops", "devops"]
categories: ["aiops", "observability"]
date: '2026-08-08T00:00:00Z'
outputs: ["Reveal"]
reveal_hugo:
  custom_theme: "reveal-hugo/themes/robot-lung.css"
  margin: 0.2
  highlight_theme: "color-brewer"
  transition: "slide"
  transition_speed: "fast"
---

## Observe and evaluate LLM Coding Agents

COSCUP 2026  
Che-Chia Chang

---

## Problem Statement

團隊導入 coding agents 後，常見三個痛點：

- 品質波動，難以預測
- 模型升級，缺乏客觀依據
- 回歸風險，無法在上線前量化

---

## 現況：用 impression 做決策

常見決策模式：

- 看社群熱度就升級 model
- 看 demo 成果就換 framework
- 用少量 case 做結論

結果：

- 品質退化發生在 production 才知道
- latency / cost 默默上升

---

## 關鍵誤解

### Observability != Decision System

Observability 可以回答：

- 發生了什麼（trace、latency、cost）

但不能直接回答：

- 這次變更是否值得上線
- 變更是否比 baseline 更好

---

## 先從 Trace 開始

要蒐集的不只 log，而是完整執行脈絡：

- 任務上下文
- prompt / response
- tool calls 與結果
- error path 與重試行為

---

## Evaluation：把主觀變可比較

建議組合：

- LLM-as-a-judge（快速、可擴）
- rule-based checks（格式、schema、關鍵約束）
- task-specific rubric（對齊團隊定義的「好」）

---

## LLM-as-a-judge 的價值與限制

價值：

- 快速建立 feedback loop
- 支援大量樣本自動評估

限制：

- 有 bias
- 一致性不穩
- 不等於 ground truth

結論：judge 是 heuristic，不是 truth。

---

## Dataset：從真實工作流長出來

高價值 dataset 來源：

- daily coding tasks
- 真實失敗案例
- 邊界條件與高風險任務

流程：

`trace -> triage -> label -> dataset`

---

## Regression：比較不是靠感覺

固定同一份 dataset，比較不同：

- model
- agent framework
- prompt/runtime strategy

輸出應包含：

- quality delta
- latency delta
- cost delta
- failure pattern delta

---

## Decision Gate（上線前最後一關）

只有同時滿足才允許 deploy：

- quality >= baseline
- no critical regression
- latency within SLO
- cost within budget

---

## Failure Taxonomy

先分類錯誤，再對症下藥：

- hallucination
- tool misuse
- reasoning error
- format/schema break

沒有 taxonomy，很難系統化改善。

---

## Minimal Architecture

```text
Agent Runtime
  -> Tracing
  -> Evaluation Service
  -> Dataset Store
  -> Regression Runner
  -> Decision Policy
```

把 decision layer 補上，才是真正可控。

---

## Demo / PoC

- repo: https://github.com/chechiachang/llm-o11y
- trace local coding agents
- build evals with LLM-as-a-judge
- run regression for model/framework changes

---

## What Teams Can Start This Week

1. 先定義 10~20 個關鍵任務作為 baseline dataset
2. 對每次 model/framework 變更跑固定 regression
3. 設定簡單 decision gate（quality/latency/cost）

---

## 核心訊息

沒有 evaluation：

**Agent upgrade = gambling**

有 feedback loop：

**Observe -> Evaluate -> Regress -> Decide**

---

## Q&A

Thank you.
