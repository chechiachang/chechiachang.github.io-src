---
title: "When Not to Vibe 從 Chat-driven coding 到 Spec-driven AI Engineering"
description: "以 Spec-driven development（SDD）結合 AI 與 Spec-kit，判斷何時不該 Vibe Coding，並把需求轉成可驗證、可回饋的工程流程。"
tags: ["openai", "generative", "ai", "kubernetes", "devops", "sdd", "spec-kit"]
categories: ["generative", "ai", "devops"]
date: '2026-05-02T12:00:00Z'
outputs: ["Reveal"]
reveal_hugo:
  custom_theme: "reveal-hugo/themes/robot-lung.css"
  margin: 0.2
  highlight_theme: "color-brewer"
  transition: "slide"
  transition_speed: "fast"
---

### When Not to Vibe

##### 從 Chat-driven coding 到 Spec-driven AI Engineering

Che-Chia Chang

---

{{% section %}}

寫扣使用 coding agent 有標準流程嗎？

可以多人開發，驗證，協作

---

如果還沒有，通常是

- 流程不固定
- 產出品質不穩
- 不知如何進行分工與驗證

---

##### 今天只講一件事

如果 Chat-driven coding 是團隊目前的方式

Try Spec-driven coding 的標準化流程

---

#### 本議程會告訴你

1. Chat-driven coding 的邊界
1. SDD 的核心概念
1. Spec-kit 落地流程
1. 何時切換與如何起步

{{% /section %}}

---

{{< slide content="slides.about-me" >}}

---

Chat-driven coding 的價值

- 快速探索，驗證想法，PoC
- 在短週期任務，Chat-driven 很有價值

---

Chat-driven Coding 的挑戰

- 輸出不穩定
- 團隊協作難追蹤
- 複雜需求 + 多輪對話，容易產生 long context

```
user: 幫我做一個功能，需求是...
user: 修這個錯誤
user: 新的需求...
user: 剛剛沒想到，現在改成這樣...
```

---

##### long context 可能造成 LLM 效能下降

- 最前跟最後的 Input ，模型比較能使用
  - ["Lost in the Middle" Effect](https://www.alphaxiv.org/abs/2307.03172v3) / [Positional Biases](https://www.alphaxiv.org/abs/2508.07479v1)
- 模型號稱的 context window 是理論值，實際可用的 context 可能更短
  - [Theoretical vs. Effective Context Window](https://www.alphaxiv.org/abs/2509.21361v2)

```
# https://www.alphaxiv.org/abs/2404.06654v3
┌───────┬─────────────┬──────────────┬───────────────┬─────────────────┐
│ Model │ 4K Accuracy │ 32K Accuracy │ 128K Accuracy │ Claimed Context │
├───────┼─────────────┼──────────────┼───────────────┼─────────────────┤
│ GPT-4 │       ~90%+ │        ~85%+ │          ~75% │            128K │
└───────┴─────────────┴──────────────┴───────────────┴─────────────────┘
```

---

##### long context 可能造成錢包縮水

```
# https://developers.openai.com/api/docs/pricing
# Prices per 1M tokens.
┌──────────────┬────────┬────────┬─────────┬────────┬────────┬─────────┐
│ Model        │  Short │  Short │   Short │   Long │   Long │    Long │
│              │  Input │ Cached │  Output │  Input │ Cached │  Output │
│              │        │  Input │         │        │  Input │         │
├──────────────┼────────┼────────┼─────────┼────────┼────────┼─────────┤
│ gpt-5.4      │  $2.50 │  $0.25 │  $15.00 │  $5.00 │  $0.50 │  $22.50 │
│ gpt-5.4-mini │  $0.75 │ $0.075 │   $4.50 │      - │      - │       - │
│ gpt-5.4-nano │  $0.20 │  $0.02 │   $1.25 │      - │      - │       - │
│ gpt-5.4-pro  │ $30.00 │      - │ $180.00 │ $60.00 │      - │ $270.00 │
└──────────────┴────────┴────────┴─────────┴────────┴────────┴─────────┘
# 使用 gpt-5.4 來跑 long context，成本變兩倍，變成 nano 的 18-36 倍
# 用 5.4 來做 Spec，用 5.4-mini 來做 implement，兼顧品質與成本
# 使用 mini 或 nano 就能達到 90% 的效果，但成本只有 10-20%，非常划算
```

---

##### Chat-driven Coding 的挑戰總結

實務上應盡力控制 context
- Spec-kit 流程（specify, plan, tasks）實際上是不斷整理 context 的過程
- 有完整 spec 實作時對於模型的能力要求不高
- 用 mini 就能達到 90% 效果，因此成本也大幅降低

---

### Chat-driven Coding vs SDD

假設需求寫出來是十萬字

- Chat-driven 是透過多輪對話，一萬字分散一段一段給模型
- SDD 是 Plan 時把一萬字整理一個結構化的 Spec
  - 實作時讓模型一次讀進結構化的 Spec

---

### When Not to Chat-driven

當任務符合以下條件

- 有明確規格或可定義規格
- 需要可驗證交付品質
- 需要多人分工與可追蹤
- 需要持續迭代與維護

---

### What is SDD

Spec-driven development

- Spec > source of truth
- Spec > Implementation
- Feedback > Spec
- 模糊需求 > 可執行規格

---

### 從 Chat-driven 到工程化

- Chat-driven：Prompt 主導
- SDD：Spec 主導
- Prompt 是畫一張水墨畫
  - Spec 是給你一張直角座標工程圖(template)，挖洞填坑

---

#### AI Engineering 需要可驗收任務

驗收標準明確
- SOP/Runbook 步驟完成率 -> %
- CI/CD Pipeline 成功率 -> %
- Lead Time -> 分鐘
- Infra / Cloud 成本 -> 每月金額
- SLO 達成率 -> %

---

### 找第一個切換題目

- 高人工成本
- 流程固定（SOP/Runbook）
- 低風險
- 被依賴性低

---

##### 情境分享：跨平台帳號與權限稽核

- 平台：aws, azure, gcp, github, jenkins...
- 需求清楚：列出帳號、檢查條件、輸出報告
- 高人工、重複性高、容易漏

---

### 實際導入流程

- 挑題目：低風險、高人工、需求清楚
- 規格化：把需求寫成 Spec 與驗收條件
- 拆任務：Spec -> Plan -> Task
- 實作：Task 具體可驗收，agent 才能穩定交付

---

### What is [Spec-kit](https://github.com/github/spec-kit)

- Spec-kit 是 GitHub 的 SDD toolkit
- 是一個 SDD 流程框架
- 不是 prompt 技巧，是可重複工程流程
- 把需求、驗收、交付串成同一條線

---

### Spec-kit 核心流程

```text
/speckit.specify 列出需求、邊界、驗收條件...
/speckit.clarify 釐清模糊點與衝突...
/speckit.plan    設計實作策略與順序...
/speckit.tasks   拆成可分配任務...
/speckit.analyze 檢查任務依賴與一致性...
/speckit.implement
```

---

### 情境落地：帳號稽核自動化

- ✅挑題目
- ✅規格化
- ✅驗收標準
- 拆任務：每個平台一組 task，平行實作
- 實作：subagent 分工，主流程整合

> 人類手動很痛苦 -> 變成可持續自動化

---

### 常見誤解

用了 Spec-kit 就會自動得到高品質？

答案：不一定

---

### Spec-kit 解決了什麼，沒解決什麼

- 解決：需求結構化、任務拆解、協作流程
- 未完全解決：品質評估、回歸驗證、持續收斂

---

### More than Chat-driven, More than Spec

你還需要三件事

```text
1. Evaluation
2. Iteration Loop
3. Automation Pipeline
```

---

### 1) Evaluation

- 不只測試有沒有過
- 還要看是否符合 Spec
- 還要看可維護性與可讀性

---

### 2) Iteration Loop

```text
fail -> fix -> rerun
```

> 讓流程可收斂，而不是每次重抽卡

---

### 3) Automation Pipeline

把流程 script 化、pipeline 化

- Spec
- Plan
- Tasks
- Implement
- Test + Eval + Loop

---

### 完整心智模型

```text
Chat-driven (探索) -> Spec (定義) -> Build (交付) -> Eval/Loop (收斂)
```

---

### 你可以帶走的重點

- Chat-driven 適合探索，不適合所有正式交付
- When Not to Chat-driven：高風險、可驗收、多人協作場景
- SDD + Spec-kit 讓 AI 開發流程可工程化
- 加上 Eval + Loop，才能穩定落地

---

### Q&A

Thank you.
