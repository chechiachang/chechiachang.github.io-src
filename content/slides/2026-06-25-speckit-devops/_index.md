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

1. DevOps 現在的痛點
1. 為什麼要用 Spec-driven development
1. Spec-kit 怎麼落地到 SOP / Runbook
1. 怎麼接上 CI/CD 與監控形成閉環
1. 什麼情境先導入，什麼情境先不要

{{% /section %}}

---

## DevOps 的日常，不是只有部署

- 開發、測試、部署、維運、安全、合規全部都要顧
- 任務高頻、跨角色、低容錯
- 工具愈來愈多，但上下文愈來愈碎
- 太晚發現才是問題

---

## 常見卡點

- SOP 有寫，但每個人做法不同
- Runbook 在文件裡，incident 當下找不到
- 交接靠口頭，知識容易斷層
- 例行工作反覆做，人力被鎖在低價值任務

---

## 這題為什麼 AI 以前做不好

- Prompt 是聊天，不是工程契約
- LLM 會補 pattern，但不會讀你的腦
- 看起來對，不一定真的能在流程裡穩定運行
- 缺少可驗證邊界，就很難持續改善

---

## 解法：Spec-driven development

- Spec 是 source of truth
- 先定義目標、限制、驗收條件，再寫實作
- 把模糊需求轉成可執行規格
- 讓 AI 在明確邊界內產生可用輸出

---

## DevOps 與 SDD 的契合點

- DevOps 重視可重複與可觀測
- SDD 重視可定義與可驗證
- 兩者結合後，自動化流程可以被 review、測試、回歸
- 規格成為跨團隊共同語言

---

## Spec-kit 核心流程

```text
/speckit.specify -> /speckit.plan -> /speckit.tasks -> implement
```

- `specify`: 把需求變成結構化規格
- `plan`: 定義架構、資料模型、介面契約
- `tasks`: 拆成可執行任務與驗證順序

---

## Flow: 從 SOP 到可驗證交付

{{< mermaid >}}
flowchart TD
  A[SOP / Runbook] --> B[specify]
  B --> C[plan]
  C --> D[tasks]
  D --> E[Implement in CI/CD]
  E --> F[Test + Metrics + Incident]
  F --> B
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
- 自動回報測試結果與流程指標
- Incident 回寫規格，避免同錯重演
- 保留 Human-in-the-loop，尤其高風險變更

---

## Live Demo 流程（示意）

1. 以一份現有 Runbook 當輸入
1. 用 `specify` 產生 spec draft
1. 用 `plan` 補齊介面與驗收場景
1. 用 `tasks` 生成執行任務與檢查點
1. 在 pipeline 跑一次並看結果

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

- 需求還在快速變動
- 缺乏監控與回滾機制
- 高風險變更沒有審核流程
- 把 AI 當決策系統，而不是輔助系統

---

## 常見踩雷

- 規格太抽象，導致任務不可驗證
- 指標選錯，優化了流程但沒提升結果
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

- Prompt 是聊天，Spec 是工程
- SDD 適合 DevOps 的高頻可標準化工作
- Spec-kit 讓 AI 自動化更可控、更可驗證
- 成功關鍵是規格品質與回饋閉環

---

## References

- https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/
- https://github.com/github/spec-kit/blob/main/spec-driven.md

---

## Q&A

Thank you.
