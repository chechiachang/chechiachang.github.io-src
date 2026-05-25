---
title: "DevOpsDay: 規格驅動的 AI 強化 DevOps"
description: "以 Spec-driven development（SDD）結合 AI 與 Spec-kit，把 SOP 與 Runbook 轉成可執行規格，建立可驗證、可回饋的 DevOps 自動化流程。"
tags: ["openai", "generative", "ai", "kubernetes", "devops", "sdd", "spec-kit"]
categories: ["generative", "ai", "devops"]
date: '2026-04-25T09:00:00Z'
outputs: ["Reveal"]
reveal_hugo:
  custom_theme: "reveal-hugo/themes/robot-lung.css"
  margin: 0.2
  highlight_theme: "color-brewer"
  transition: "slide"
  transition_speed: "fast"
---

### 規格驅動的 AI 強化 DevOps

##### 篩選適合的情境，SDD 成為你的平台開發神器

Che-Chia Chang

---

{{% section %}}

公司有在做或想做 DevOps Platform Engineering 的，歡迎舉手

---

如果還沒舉手，通常是兩種情況

- 目前優先度還不高
- 或覺得落地門檻很高

---

### DevOps 

Platform Engineering 需要開發，但許多 DevOps 職缺並不要求 Coding skill

{{% note %}}
DevOps 核心在於「自動化」與「維運」
既有工具無法滿足需求時，自然轉向自建平台工程
{{% /note %}}

---

### 本議程會告訴你

1. 平台工程的現實
1. 什麼是 SDD
1. Spec-kit 如何落地
1. 適合導入的情境

{{% /section %}}

---

{{< slide content="slides.about-me" >}}

---

### What is SDD

Spec-driven development

- Spec > source of truth
- Spec > Implementation
- Feedback > Spec
- 模糊需求 > 可執行規格

> 可執行Spec 讓 agent 有效率的實作

---

### SDD vs Vibe Coding

「使用 coding agent」為前提，比較 Vibe coding

- Vibe coding 是藝術
  - Prompt 好壞決定輸出品質
- SDD 是工程
  - 標準流程
  - 規格定義驗收條件
  - 產出可驗證、可協作的流程

{{% note %}}
不討論手刻程式，手刻是一種浪漫
{{% /note %}}

---

#### DevOps 有許多適合 SDD 的任務

驗收標準明確
- SOP/Runbook 步驟完成率 -> %
- CI/CD Pipeline / 工具串接成功率 -> %
- CI/CD Lead Time -> 分鐘
- Infra / Cloud 成本 -> 每月金額
- SLO 達成率 -> %

---

#### 先用這題判斷：流程是否已知？

| Spec 明確 | 釐清 Spec |
| --- | --- |
| SOP / Runbook 自動化 | 如何降低耗時、提升速度 |
| CI/CD Pipeline 標準化 | 如何降低成本 |
| 工具串接 / 整合 | 如何達成或提高 SLO |

> 需要釐清可行方法，才能定義規格

---

如果你的 DevOps 任務
- 需求變異很大
- 驗收條件不明確
- 被其他服務依賴
- 那麼先導入 SDD 可能不適合

---

### 找到第一個適合的任務

- 人工例行事務
- 固定流程/SOP/Runbook
- 低風險
- 沒有被其他服務依賴

---

##### 情境分享：所有內部平台帳號定期稽核

- 確保沒有過期或離職的帳號存在
- 需求清楚：產生帳號列表，檢查條件，回報格式
- 低風險，高人工，常常做

{{% note %}}
{{% /note %}}

---

### 實際導入流程

- 挑題目：低風險，高人工，需求清楚
- 規格化：Spec-kit 需求寫成 Spec，確定驗收標準
- 拆任務：Spec-kit Spec -> Plan -> Task
- 實作：Task 已定義驗收條件，agent 會努力達成

---

##### 情境分享：所有內部平台帳號定期稽核

- ✅挑題目
- 規格化
  - aws, azure, gcp, github, jenkins...
  - /user /permission api 規格
- 驗收標準
  - 測試：單元測試，模擬帳號整合測試
  - 結果：帳號總數，帳號權限，違反條件的帳號數量
  - 格式：符合稽核格式

---

### What is [Spec-kit](https://github.com/github/spec-kit)

- Spec-kit 是 GitHub 的 SDD toolkit
- 是一個 SDD 流程框架
- 不是 prompt 技巧，是可重複工程流程
- 核心價值：把需求、驗收、交付串成同一條線

---

### Spec-kit 核心流程

```text
/speckit.specify 列出所有內部平台帳號...
/speckit.specify 根據條件檢查帳號狀態...權限...

/speckit.clarify
/speckit.plan
/speckit.plan    修改先後順序...

/speckit.tasks   拆成獨立子任務，可分配給 subagent...
/speckit.analyze 檢查 Task 依賴性

/speckit.implement
```

---

##### 情境分享：所有內部平台帳號定期稽核

- ✅挑題目
- ✅規格化
- ✅驗收標準
- 拆任務：agent 準備平台 task，檢查相依性與 checklist
- 實作：發包 subagent 負責一個平台，平行實作
- 成果：人類做到很痛苦 -> 變成全自動化

{{% note %}}
如果有適合的工具，那不用閉門造車
但現在造車非常的快與便宜
{{% /note %}}

---

### 其他情境分享

- 除錯 Runbook：在多個內部維服務上來回收集資訊，分析問題
- 服務的 sidecar：提供業務邏輯的 API，讓 ops 對服務進行操作，或提供額外功能

---

### 你可以帶走的重點

- DevOps 任務，許多已有明確的 Spec
- 選對題目：高人工、低風險，跨平台，被依賴性低
- SpecKit 標準化流程，分工協作
- 適合處理複雜流程，跨平台的任務

{{% note %}}
有工具就不用閉門造車
- 但如果沒有，現在造車非常的快與便宜，而且有相當的品質
{{% /note %}}

---

### Q&A

Thank you.
