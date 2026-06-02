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

公司使用 coding agent 有標準流程的舉個手

可以多人開發，驗證，協作

{{% fragment %}} 流程不固定，產出品質不穩，不知如何進行分工與驗證 {{% /fragment %}}

---

如果 Chat-driven coding 是團隊目前的方式

Try Spec-driven coding 的標準化流程

---

#### 本議程會告訴你

1. Chat-driven coding 的邊界
1. SDD 的核心概念
1. Spec-kit 落地流程
1. 何時切換與如何起步

---

{{< slide content="slides.about-me" >}}

{{% /section %}}

---

Chat-driven coding 的價值

- 快速探索，驗證想法，PoC
- 在短週期任務，Chat-driven 很有價值

---

Chat-driven Coding 的挑戰

- 輸出不穩定
- 團隊協作難追蹤
- 複雜需求 + 多輪對話，容易產生 long context
- 對話拉長，模型偏移，容易 context drift

```
user: 幫我做一個功能，需求是...
user: 修這個錯誤
user: 新的需求...
user: 剛剛沒想到，現在改成這樣...
```

---

##### long context 可能造成 LLM 效能下降

```
# https://www.arxiv.org/abs/2404.06654v3
┌───────┬─────────────┬──────────────┬───────────────┬─────────────────┐
│ Model │ 4K Accuracy │ 32K Accuracy │ 128K Accuracy │ Claimed Context │
├───────┼─────────────┼──────────────┼───────────────┼─────────────────┤
│ GPT-4 │       ~90%+ │        ~85%+ │          ~75% │            128K │
└───────┴─────────────┴──────────────┴───────────────┴─────────────────┘
```

{{% fragment %}}
模型的 context window 理論值，實際可用的 context 更短

[Theoretical vs. Effective Context Window](https://www.arxiv.org/abs/2509.21361v2)
{{% /fragment %}}

{{% fragment %}}
最前跟最後的 Input ，模型比較能使用

["Lost in the Middle" Effect](https://www.arxiv.org/abs/2307.03172v3) / [Positional Biases](https://www.arxiv.org/abs/2508.07479v1)
{{% /fragment %}}

---

#### Chat-driven Coding 的挑戰總結

- 不易控制 context
- context 前後有出入，導致 context drift
- 模型更記得最前面跟最後面的訊息

> Spec-kit 流程實際是不斷整理 context

---

#### Chat-driven Coding vs SDD

假設需求寫出來是十萬字

- Chat-driven 是透過多輪對話，一萬字分散一段一段給模型
- SDD 是 Plan 時把一萬字整理一個結構化的 Spec
  - 實作時讓模型一次讀進結構化的 Spec

---

#### What is SDD

Spec-driven development

- Spec > source of truth
- Spec > Implementation
- Feedback > Spec
- 模糊需求 > 可執行規格

---

#### Spec 需要可驗收任務

驗收標準明確
- SOP/Runbook 步驟完成率 -> %
- CI/CD Pipeline 成功率 -> %
- Lead Time -> 分鐘
- Infra / Cloud 成本 -> 每月金額
- SLO 達成率 -> %

---

#### SDD 導入第一步

找第一個切換題目

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
/speckit.specify 列出所有內部平台帳號...
                 根據條件檢查帳號狀態...權限...

/speckit.plan    修改先後順序...

/speckit.tasks   拆成獨立子任務，可分配給 subagent...
/speckit.analyze 檢查 Task 依賴性

/speckit.implement
```

---

{{< slide background-image="specify-plan.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

{{< slide background-image="specify-tasks.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

{{< slide background-image="specify-implement.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

#### 細節請參考

今天早上的 workshop

- Lab 09:00 - 10:30 [Spec-driven development with Spec-kit](../../posts/2026-07-01-ws-speckit-ai-ent/)

---

#### 情境落地

- ✅挑題目
- ✅規格化
- ✅驗收標準
- ✅拆任務：每個平台一組 task，平行實作
- 實作：subagent 分工，主流程整合

---

#### Spec-kit 帶來的痛點

- 工作習慣改變
  - 痛點左移，寫扣時的痛苦提前到寫需求時
- Spec-kit tax：Spec-kit 產生 Spec，會消耗額外 token
  - 用貴模型寫 Spec，便宜模型實作，降低成本
- 不適合舊專案：Greenfield vs. Brownfield
  - 無法從舊程式碼逆向產生 Spec
  - 從頭寫 Spec，燒時間跟token

---

#### 改需求的成本變高

- Spec 寫好 Code，結果改需求，改 Spec、Plan、Task，agent 也要重跑
- 小改動可以像 git commit 一樣，疊上去 Spec
- 大改動或需求矛盾，就要重寫 Spec
  - Spec-kit 會幫你掃出 conflict，但不會幫你解決
  - Code 都不能用，要重零開始
- 需求變動頻繁的任務不適合 Spec-kit，反而會變得笨重

---

#### Spec-kit 解決了什麼，沒解決什麼

- 解決：需求結構化、任務拆解、協作流程
- 無法解決
  - 需求變動頻繁的任務
  - 舊專案的 Spec 產生

---

#### 你可以帶走的重點

- Chat-driven 適合探索，不適合所有正式交付
- When Not to Chat-driven：高風險、可驗收、多人協作場景
- SDD + Spec-kit 讓 AI 開發流程可工程化
- 加上 Eval + Loop，才能穩定落地

---

#### Q&A

Thank you.
