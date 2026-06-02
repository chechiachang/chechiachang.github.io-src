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

公司有做 DevOps Platform Engineering 的舉手

{{% fragment %}} DevOps 要求 Coding skill 的手放下 {{% /fragment %}}

{{% fragment %}} 需要開發，但許多 DevOps 職缺並不要求 Coding skill 🤔 {{% /fragment %}}

{{% fragment %}} 用 SDD 可以解部分的 DevOps 開發需求 {{% /fragment %}}

---

### 本議程會告訴你

1. 什麼是 Spec-kit，跑起來是什麼樣子
1. SSD 為何適合 DevOps
1. 適合導入的情境

{{% /section %}}

---

{{< slide content="slides.about-me" >}}

---

{{% section %}}

##### 平台工程需求

ex. 所有內部平台帳號定期稽核，確保沒有過期或離職的帳號存在

{{% fragment %}} 如果有工具直接用工具，不用閉門造車 {{% /fragment %}}

{{% fragment %}} 需求不符合的話，現在閉門造車非常的快與便宜 {{% /fragment %}}

{{% fragment %}} 後續維護是否好維護 🤔 {{% /fragment %}}

---

##### 實際 Spec-kit 會長怎樣

{{% fragment %}} 產生 Spec > 修 Spec 到滿意 > 產生 Plan > 拆成 Task {{% /fragment %}}

{{% fragment %}} agent 根據 Task 實作，直到達成 Spec {{% /fragment %}}

```text
# specify init --integration copilot

/speckit.specify    寫一個工具，列出所有內部平台帳號
                    1. 根據條件檢查帳號狀態權限
                    2. 有單元測試，模擬帳號整合測試

/speckit.plan       根據 Spec 產生 Plan，列出實作步驟，檢查相依性，準備 checklist
/speckit.tasks      拆成獨立子任務，可分配給 subagent...
/speckit.implement
```

---

{{< slide background-image="specify-plan.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

{{< slide background-image="specify-tasks.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

{{< slide background-image="specify-implement.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

### What is [Spec-kit](https://github.com/github/spec-kit)

- Spec-kit 是 GitHub 的 SDD toolkit
- 是一個 SDD 流程框架
- 不是 prompt 技巧，是可重複工程流程
- 核心價值：把需求、驗收、交付串成同一條線

---

##### 更多資訊與細節請參考

- Workshop [Spec-driven development with Spec-kit](../../posts/2026-07-01-ws-speckit-ai-ent/)
- Session [從 Vibe Coding 到 Spec-driven AI Engineering](../../posts/2026-07-01-speckit-cloud-summit/)

{{% /section %}}

---

##### What is Spec-driven development

- 模糊需求 > 可執行規格 Spec
- Spec > Implementation
  - 能滿足 Spec 就是好的實作
- Feedback > 修改 Spec > (loop)

{{% fragment %}}
Spec-kit 是 SDD 的工具，提供標準流程與格式

產出可驗證、可協作的規格。agent 根據規格實作
{{% /fragment %}}

---

##### SDD vs Chat Coding

| 面向 | SDD | Chat Coding |
| --- | --- | --- |
| 方式 | 先寫需求/設計，再實作 | 先寫程式，邊聊邊修 |
| 短期 | 較慢 | 很快 |
| 長期 | 通常更穩，返工少 | 累積技術債後期變慢 |
| 一致性 | 高，有明確規格 | 看操作者，波動大 |
| 維護性 | 高，文件、決策、邊界清楚 | 中低，脈絡常散在聊天紀錄 |
| 協作 | 好，可 review spec | 較難，知識偏個人化 |
| 風險 | 好，先定義約束與測試 | 較弱，容易漏邊界條件 |
| 適合 | 中大型專案、多人協作 | PoC、腳本、小功能 |

---

#### SSD 為何適合 DevOps

任務驗收標準明確，流程固定，重複性高
- SOP/Runbook 步驟完成率 -> %
- CI/CD Pipeline / 工具串接成功率 -> %

{{% fragment %}}
完成步驟就達成需求，這類任務非常適合 SDD

因為驗收標準明確，流程固定
{{% /fragment %}}

---

llm 產出是一個機率分布

需要釐清規格，邊界條件寫清楚，agent 實作結果才會收斂

{{% fragment %}}
未來改需求，甚至產生矛盾的需求，會讓 agent 產出偏離預期
{{% /fragment %}}

{{% fragment %}}
Drift (Context Drift)
{{% /fragment %}}

{{% note %}}
如果你的 DevOps 任務
- 需求變異很大
- 驗收條件不明確
- 被其他服務依賴
- 那麼先導入 SDD 可能不適合
{{% /note %}}

---

#### 找到第一個適合的任務

- 人工例行事務
- 固定流程/SOP/Runbook
- 低風險
- 沒有被其他服務依賴

---

#### 實際導入流程

- 挑題目：低風險，高人工，需求清楚
- 規格化：Spec-kit 需求寫成 Spec，確定驗收標準
- 拆任務：Spec-kit Spec -> Plan -> Task
- 實作：Task 已定義驗收條件，agent 會努力達成

---

##### 情境分享：所有內部平台帳號定期稽核

- ✅挑題目
- 規格化
  - 平台列表 aws, github, jenkins...
  - /user /permission api 規格
- 驗收標準
  - 測試：單元測試，模擬帳號整合測試
  - 結果：帳號總數，帳號權限，違反條件的帳號數量
  - 格式：符合稽核格式

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

#### Spec-kit 的盡頭是組合拳

- 新功能新 pkg 用 Spec-kit 開發
- 舊專案舊 pkg：補 Test 保護既有功能，再疊 Spec 上去
- 卡住的半成品重新分析問題，重寫 Spec，讓 agent 從頭實作
- 關鍵 pkg 重構，用 Spec-kit 把舊 Code 當成 Spec reference，全部重寫成 v2

{{% fragment %}}
其實是在用各種方法，捕捉虛幻的 Spec 讓他落地

這不是 Best Practice，而是 Working Practice
{{% /fragment %}}

---

#### 你可以帶走的重點

- DevOps 任務，許多已有明確的 Spec
- 選對題目：高人工、低風險，跨平台，被依賴性低的任務
- 從 vibe/chat coding 走向 Spec-kit
  - 標準化流程，分工協作

{{% fragment %}}
Speckit 不是終點，同志仍須努力
{{% /fragment %}}

---

##### Q&A 不是演講的終點

下週 Cloud Summit 會有一場 Workshop，會帶大家實際操作 Spec-kit，歡迎來玩！
- Workshop [Spec-driven development with Spec-kit](../../posts/2026-07-01-ws-speckit-ai-ent/)
- Session [從 Vibe Coding 到 Spec-driven AI Engineering](../../posts/2026-07-01-speckit-cloud-summit/)

Thank you.
