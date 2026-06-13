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

### 本議程會告訴你

- Spec-kit 跑起來是什麼樣子
- 提供 4 個實務情境，說明哪些適合 SDD
- Spec-kit 的代價與應對策略

---

{{< slide content="slides.about-me" >}}

---

##### 情境 1：跨平台，稽核內部平台帳號

所有內部帳號定期稽核，確保沒有過期離職的帳號存在

- 如果有現成工具就直接用工具，不用閉門造車
- 需求不符合的話，現在閉門造車非常的快與便宜
- 問題：後續維護是否好維護 🤔

---

##### 實際 Spec-kit 會長怎樣

```text
# VSCode Chat (Copilot) 中啟用 spec-kit
# specify init --integration copilot

# 產生 Spec
/speckit.specify    寫一個工具，列出所有內部平台帳號
                    1. 根據條件檢查帳號狀態權限
                    2. 有單元測試，模擬帳號整合測試
                    3. e2e 測試，產出符合稽核格式的結果

# 不斷釐清 Spec 到沒有模糊空間
/speckit.clarify    平台包含 aws, github, jenkins...
                    帳號狀態包含 active, expired, pending
                    權限包含 admin, write, read-only
 
# 根據 Spec 產生 Plan，列出實作步驟，檢查相依性，準備 checklist
/speckit.plan

# 拆成 Task，獨立子任務，可分配給 subagent...
/speckit.tasks

# 產生的 Task 是否可行？有沒有遺漏的步驟？有沒有不合理的地方？有無彼此衝突的地方？
/speckit.analyze

# 使用多個 subagent 平行下去實作
# agent 根據 Task 實作，直到達成 Spec
/speckit.implement

# 驗收
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

---

##### What is Spec-driven development

- 避免模糊需求，產生精準的可執行規格
- Agent 會自動滿足 Spec 實作
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

#### 情境 1: 為何適合 SDD

內部帳號定期稽核，確保沒有過期離職的帳號存在

- 任務驗收標準明確
  - 打平台 API，列出帳號，依照條件檢查狀態權限
  - 篩選離退名單，符合自動告警
  - 產出符合稽核格式的結果
- 流程固定
- Spec 變動不大
  - 可能平台增減，API 改版
  - 稽核需求與驗收標準不會變
- 自動化效益高
  - 人工做很痛苦，容易出錯
- 終端使用者，沒有被其他元件依賴
  - 被依賴會產生額外的 Spec 變動

---

#### 延伸情境 1: 跨平台人員管理

- 跨平台帳號定期稽核
- Access / Audit log 收集，整理，即時分析，可疑事件告警
- 權限稽核，驗證，更新
- Onboarding / Offboarding 自動化

使用 SDD 量身打造跨平台工具，進一步加速流程的驅動

---

##### 情境 2：工作流程自動化

Jira-Github-Coding: Developer 不想離開 Github

```text
[Human(PM)] 雜務/例行性事務排進 Jira
[Bot] 檢查DB，過去相關 Jira Ticket
[Bot] 檢查 Duplicated
[Bot] 開 Github Issue
[Bot] 指派 Coding Agent
[Bot] Coding Agent 產生 Spec

[Human(Developer)] Review Spec，Approve Spec

[Bot] Coding Agent 根據 Spec 實作 PR
[CI] 自動化測試 unit test + e2e test

[Human(Developer)] Review PR，Approve PR

[Bot] 所有步驟回寫到 Jira，形成完整紀錄
[Bot] Index 到 Vector DB，提供未來類似任務參考
```

{{% note %}}
PM 不用離開 Jira
Developer 不用離開 Github

SDD Debug 會有極限
適用中型專案
{{% /note %}}

---

#### 可能適合 SDD 的條件

- 任務驗收標準明確，流程固定，重複性高
  - SOP/Runbook 步驟完成率
  - CI/CD Pipeline / 工具串接成功率
- 流程固定
- Spec 變動不大

{{% fragment %}}
完成步驟就達成需求，這類任務非常適合 SDD

因為驗收標準明確，流程固定
{{% /fragment %}}

---

#### 情境 3: 服務的 Sidecar

Stateful Backend 的維運輔助系統
- 提供 ops 對服務進行操作
- 重啟服務、調整資源
- 升版、回滾
- 切換 config
- Data Migration、Validation
- Snapshot、Backup、Restore

---

#### 情境 4: Debugging Runbook

[SRE] 除錯 Runbook / Incident Response

```text
[Alert] 某個為服務功能出錯
[Bot] 查架構文件，列出相關的微服務
[Bot] 查團隊文件，通知相關值班人員
[Bot] 收集所有相關微服務 Error log
[Bot] 查看 Monitoring、Tracing
[Bot] 統整資訊，分析問題
[Bot] readonly 再次存取相關服務，查看狀態、配置、版本
[Bot] 整理所有資訊與推論
[Bot] 提供解決方案，列出優缺點，建議下一步

[Human] 看到時已是完整的 Alert + 各方資訊 + 建議解決方案
[Human] Review 解決方案，Approve 後實作

[Bot] 指定時間內持續追蹤
[Bot] 定時主動回報團隊與主管，處理進度
```

---

#### 小結：找到第一個適合的任務

跨平台人員管理，Workflow 自動化

Sidecar，Debugging Runbook

- 人工例行事務：先解放人力
- 固定流程/SOP/Runbook
- 低風險
- 沒有被其他服務重度依賴

---

#### 實際導入流程

1. 挑題目：低風險，高人工，需求清楚
1. 從小開始：先從整個流程的一段步驟開始
1. 發現 Spec 不夠清楚，驗收條件不夠明確，流程遺漏
  1. 回到 Spec 修正，建立修正 Spec 的流程與經驗
1. 成功後再慢慢擴大範圍

---

#### Spec-kit 帶來的痛點

- 工作習慣改變
  - 痛點左移，寫扣時的痛苦提前到寫需求時
- Spec-kit Tax：Spec-kit 產生 Spec，會消耗額外 token
  - 貴模型寫 Spec
  - 便宜模型實作
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

#### SDD vs 需求改動

改需求，或是實作偏離太多

- 收集半成品(n) + 分析問題(n)
- 反饋給 Spec(n) -> 修改 Spec(n) -> 產出 Spec(n+1)
  - Spec(n+1)，比 Spec(n) 更清楚、更完整、更合理
- 退掉失敗 PR(n)，agent 從頭實作 Spec(n+1)

{{% note %}}
屍體產生新的 Spec 穢土轉生

可以相當程度的校正與需求的偏離，但無法抵抗與 Spec 的根本矛盾
{{% /note %}}

---

#### Spec-kit 的盡頭是組合拳

- 新專案直上 Spec-kit
- 舊專案舊 pkg：補 Test 保護既有功能，再啟用 Spec-kit
- 公司支持的話，請進行重構
  - code base 中的坑雷與技術債，人都不想解，Agent 也解不了
  - 把舊 Code 當成 Spec reference，重寫成 Spec v2，然後重構

{{% fragment %}}
其實是在用各種方法，讓虛幻的 Spec 落地

這不是 Best Practice，而是 Working Practice
{{% /fragment %}}

---

#### 你可以帶走的重點

- DevOps 任務，許多已有明確的 Spec
- 選對題目：高人工、低風險，跨平台，被依賴性低的任務
- 從 vibe/chat coding 走向 Spec-kit
  - 標準化流程，分工協作
- SDD 絕非萬能，需求合適的任務，才適合 SDD

{{% fragment %}}
Speckit 不是終點，同志仍須努力
{{% /fragment %}}

---

##### Q&A 不是演講的終點

下週 Cloud Summit 會有一場 Workshop，會帶大家實際操作 Spec-kit，歡迎來玩！
- Workshop [Spec-driven development with Spec-kit](../../posts/2026-07-01-ws-speckit-ai-ent/)
- Session [從 Vibe Coding 到 Spec-driven AI Engineering](../../posts/2026-07-01-speckit-cloud-summit/)

Thank you.
