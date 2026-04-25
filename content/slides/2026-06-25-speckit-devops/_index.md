---
title: "DevOpsDay: 以規格為核心的 AI 強化 DevOps 平台工程"
date: '2026-07-01T13:20:00Z'
outputs: ["Reveal"]
reveal_hugo:
  theme: "black"
  slide_number: true
  transition: "slide"
  custom_theme: "reveal-hugo/themes/robot-lung.css"
---

# 規格驅動的 AI 強化 DevOps 平台工程

AI-powered Spec-driven DevOps Platform Engineering

Che-Chia Chang

---

## Outline

1. DevOps 為何適合 Spec-driven Development
2. 如何用 Spec-kit 把 SOP 變成可執行規格
3. 如何串接 AI、CI/CD、監控形成閉環
4. 什麼情境適合導入，什麼情境先不要
5. 實務踩雷與可落地的導入路徑

---

## 為什麼是現在

- DevOps 任務範圍持續擴張，跨開發、測試、部署、維運、安全、合規
- 團隊同時面對高重複、低容錯、跨角色協作三種壓力
- 工具很多，但常常是流程配合工具，而不是工具配合流程
- 需要把可標準化工作轉為可驗證、可重複的執行方式

---

## DevOps 與 SDD 的契合點

- DevOps 本質重視「明確目標 + 可觀測結果」
- SDD 把需求、限制、完成定義先寫進規格
- 規格是跨角色共同語言，不是只給工程師的文件
- 當規格可執行，自動化就不只是腳本，而是流程資產

---

## 什麼工作最適合先導入

- 已有 SOP 或 Runbook，步驟與輸入輸出明確
- 高耗時、重複性高、出錯成本高的例行工作
- 依賴少、邊界清楚、可以獨立驗證的流程
- 例如：環境搭建、例行文件整理、跨工具資料同步

---

## 不適合直接導入的情境

- 需求尚未收斂，成功標準不明確
- 高風險變更且缺乏回滾或驗證機制
- 團隊對流程沒有共同語彙，規格無法對齊
- 把 AI 當萬能替代而非輔助，容易放大誤差

---

## DevOps 精神如何映射到 SDD

- Culture: 規格讓跨團隊協作有共同上下文
- Automation: 規格成為自動化流程的來源
- Lean: 聚焦最痛、最常發生、最可標準化工作
- Measurement: 先定義指標，再看自動化是否有效
- Sharing: 規格沉澱可複用知識，降低單點風險

---

## 三步導入法（Spec-kit）

1. 選題：找出最耗時且可量測的 DevOps 任務
2. 規格化：用 Spec-kit 範本定義需求、限制、驗收條件
3. 落地：接上 CI/CD 與監控，持續驗證與迭代

---

## Step 1：選題與定義目標

- 先對照業務目標與用戶影響，避免只做「看起來很酷」
- 盤點現況成本：人時、等待時間、失誤率、返工率
- 設定成功指標：Lead time、MTTR、變更失敗率、交付頻率
- 明確界定範圍：先小範圍試點，再擴大

---

## Step 2：把 SOP 轉成可執行規格

- 將流程拆成前置條件、輸入、步驟、輸出、驗收
- 把「Done」寫成可測試條件，而不是主觀描述
- 明確列出例外與失敗處理，避免 happy path 偏誤
- 用版本化方式管理規格，讓變更可追溯

---

## Step 3：接上執行與觀測

- 在 CI/CD 中執行規格驅動任務與驗證
- 以監控與告警收集結果，形成回饋資料
- 週期性檢視指標與誤差，更新規格而非堆腳本
- 把成功案例標準化，擴展到其他流程

---

## AI 在這裡扮演什麼角色

- 協助快速產出規格初稿與流程樣板
- 補足中低複雜度任務的開發與測試產能
- 對規格做一致性檢查，降低遺漏與矛盾
- 但決策與邊界仍需資深工程師把關

---

## 常見踩雷

- 規格太抽象，導致自動化結果不可驗證
- 指標定義錯誤，優化了流程卻沒提升業務價值
- 一次導入太大，造成團隊認知負擔過高
- 忽略例外流程，正式環境才暴露風險

---

## 實務建議

- 先做「低風險高頻」任務，快速建立信心
- 每份規格必附驗收條件與回滾策略
- 保持 Human-in-the-loop，特別是高風險變更
- 讓規格和程式一樣被 review、測試、版本控管

---

## 你可以帶走的重點

- SDD 不是替代工程判斷，而是放大工程紀律
- AI + Spec-kit 適合處理明確、重複、可驗證的 DevOps 工作
- 成效關鍵在於：規格品質、指標設計、持續回饋
- 先從小處落地，再把成功模式複製到平台工程體系

---

## References

- https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/
- https://github.com/github/spec-kit/blob/main/spec-driven.md

---

## Q&A

Thank you.
