---
title: "DevOpsDay: 規格驅動的 AI 強化 DevOps"
description: "以 Spec-driven development（SDD）結合 AI 與 Spec-kit，把 SOP 與 Runbook 轉成可執行規格，建立可驗證、可回饋的 DevOps 自動化流程。"
tags: ["openai", "generative", "ai", "kubernetes", "devops", "sdd", "spec-kit"]
categories: ["generative", "ai", "devops"]
date: '2026-06-25T09:00:00Z'
outputs: ["Reveal"]
reveal_hugo:
  custom_theme: "reveal-hugo/themes/robot-lung.css"
  margin: 0.2
  highlight_theme: "color-brewer"
  transition: "slide"
  transition_speed: "fast"
---

# 規格驅動的 AI 強化 DevOps

AI-powered Spec-driven DevOps Platform Engineering

Che-Chia Chang

---

{{% section %}}

{{< slide content="slides.about-me" >}}

---

## 大綱

1. DevOps 現場痛點：為什麼文件還是不夠
1. 什麼是 Spec-driven development（SDD）
1. Spec-kit 如何落地 SOP / Runbook / Platform automation
1. 什麼情境先導入，什麼情境先不要
1. 常見踩雷與可落地做法

{{% /section %}}

---

## DevOps 現場痛點

- 有 SOP / Runbook，但執行結果不一致
- 需求常常在口頭更新，沒有可追溯版本
- 出事時只能靠經驗，不是靠可驗證流程
- 「有文件」不等於「可重跑、可驗收」

---

## What is Spec-driven development

- Spec 是 source of truth
- 先定義目標、限制、驗收條件，再寫實作
- 把模糊需求轉成可執行規格
- 讓 AI 在明確邊界內產生可用輸出

---

## Why SDD 適合 DevOps

DevOps 任務常有明確輸入與產出
- 部署：程式碼 -> 服務狀態 -> health check
- 監測：指標數據 -> 警報
- 事故處理：事件 -> 解決方案
- 例行維護：狀態 -> 更新狀態

> 可重複 + 可觀測，通常就能規格化

---

## Dev vs DevOps：驗收型態不同

Dev 偏向功能與體驗
- 滿足規格後還要看效能、架構、可擴展性

DevOps 偏向流程與可靠性
- SOP/Runbook 完成步驟 -> 有/無完成
- Pipeline / 工具串接 -> 有通/沒通
- 成本與 SLO -> number

> 不是誰比較簡單，是驗收維度不同

---

## LLM 產出差異：先選可量測任務

- DevOps 任務常能用 Boolean / Number 驗收
- 更適合先導入 AI + SDD
- 先選低風險、高頻、可量測題目
- 先求可控與可驗證，再求覆蓋範圍

---

## What is Spec-kit

- Spec-kit 是 GitHub 的 SDD toolkit
- 不是 prompt 技巧，是可重複工程流程
- 核心價值：把需求、驗收、交付串成同一條線

---

## Prompt vs Spec

- Prompt 是聊天，解單次問題
- Spec 是工程，管多輪改動一致性

> Vibe 是聊天，Spec 是工程

---

## Spec-kit 核心流程

```text
/speckit.specify -> /speckit.plan -> /speckit.tasks -> /speckit.implement -> /speckit.analyze -> /speckit.checklist
```

- 需求改動時，先回 spec，再重跑後續步驟
- 不直接在 code 上硬修需求

---

## Flow: 從 SOP 到可驗證交付

{{< mermaid >}}
flowchart TD
  A[SOP / Runbook] --> B[specify]
  B --> C[plan]
  C --> D[tasks]
  D --> E[implement]
  E --> F[analyze + checklist]
  F --> G[CI/CD + Metrics]
  G --> B
{{< /mermaid >}}

---

## Step 1: 選題

- 先挑低風險、高頻、可量測任務
- 任務邊界要清楚，輸入輸出可定義
- 先小範圍試點，不要一次全改
- 指標先定義：Lead time、MTTR、錯誤率

---

## Step 2: 規格化

- 把流程拆成前置條件、步驟、輸出、驗收
- 把 Done 寫成可測試條件
- 明確列出失敗處理與回滾策略
- 規格版本化，讓變更可追溯

---

## Step 3: 接上執行

- 在 CI/CD 中執行規格對應任務
- plan 固定架構與邊界，tasks 拆可驗證任務
- implement 階段按 tasks 順序落地
- analyze/checklist 做交付品質保險絲

---

## Demo 流程（示意）

1. 以現有 Runbook 當輸入
1. 用 `specify` 產生 spec draft
1. 用 `plan` 補齊介面與驗收場景
1. 用 `tasks` 生成執行任務與檢查點
1. 用 `implement` 落地，`analyze/checklist` 驗收

---

## Demo 題目（示意）

YouBike 2.0 站點查詢器
- 自動抓政府開放資料 API
- 可用站名 / 地址搜尋
- 顯示可借車輛與可停車位
- 低庫存門檻告警（可量測）

---

## Demo 時要看哪三件事

- 規格是否完整覆蓋需求與限制
- 任務是否對應驗收條件
- 失敗時能否快速定位並回滾

---

## 哪些情境適合先導入

- SOP 與 Runbook 已存在
- 任務重複高且錯誤成本高
- 團隊願意用同一套規格語言協作
- 可以在 sandbox 或 staging 先驗證

---

## 哪些情境先不要

- 需求仍高速變動，尚未定義驗收
- 缺乏監控與回滾機制
- 高風險變更沒有審核流程
- 把 AI 當決策系統，而不是輔助系統

---

## 常見踩雷

- 規格太抽象，任務不可驗證
- 指標選錯，流程變快但結果沒變好
- 一次導入範圍過大，團隊吸收不了
- 只看成功路徑，忽略例外流程

---

## 實務建議

- 先做一條可跑通的最小閉環
- 每份規格都附驗收與回滾條件
- 規格與程式一樣進 code review
- 兩週一循環：回顧結果並更新規格

---

## 你可以帶走的重點

- 選對題目：高頻、可量測、可回滾
- 規格優先：需求改動先回 spec
- 流程閉環：analyze/checklist 不可省
- Prompt 是聊天，Spec 是工程

---

## References

- https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/
- https://github.com/github/spec-kit/blob/main/spec-driven.md

---

## Q&A

Thank you.
