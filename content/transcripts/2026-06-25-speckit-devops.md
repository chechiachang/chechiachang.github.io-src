---
title: "規格驅動的 AI 強化 DevOps - 演講逐字稿"
description: "DevOpsDay 演講逐字稿：以 Spec-driven development 結合 AI 與 Spec-kit，把 SOP 與 Runbook 轉成可執行規格，建立可驗證、可回饋的 DevOps 自動化流程。"
date: 2026-06-25
tags: ["speckit", "sdd", "devops", "ai", "transcript"]
---

# 規格驅動的 AI 強化 DevOps 演講逐字稿

## 開場

今天要分享的主題是「規格驅動的 AI 強化 DevOps」，副標是「篩選適合的情境，SDD 成為你的平台開發神器」。我是 Che-Chia Chang。

---

## 議程概述

在這場議程中，我會告訴各位三個重點：

第一，Spec-kit 跑起來是什麼樣子。我會用實際的例子展示工作流程。

第二，我會提供四個實務情境，說明哪些任務適合 SDD，哪些不適合。

第三，Spec-kit 帶來的代價是什麼，以及我們如何應對。

---

## 情境 1：跨平台，稽核內部平台帳號

讓我們從第一個情境開始。在許多企業中，都有一個共同的痛點：所有內部帳號需要定期稽核，確保沒有過期離職的帳號存在。

面對這類需求，有幾個重要的考量：

首先，如果有現成工具就直接用工具，不用閉門造車。但如果現成工具需求不符合，用 AI 閉門造車現在非常的快又便宜。

但這裡出現了一個大哉問——後續維護是否好維護？這個疑問很關鍵。

---

## 實際 Spec-kit 工作流程展示

讓我們看一下，實際的 Spec-kit 會長怎樣。假設我們在 VSCode Chat（Copilot）中啟用 spec-kit，流程會是這樣：

### 第一步：產生 Spec

使用 `/speckit.specify` 命令，我們描述需求：
- 寫一個工具，列出所有內部平台帳號
- 工具需要根據條件檢查帳號狀態與權限
- 包含單元測試，模擬帳號的整合測試
- 還要有 e2e 測試，產出符合稽核格式的結果

### 第二步：釐清 Spec

然後使用 `/speckit.clarify` 命令，不斷釐清模糊的地方，直到沒有歧義：
- 平台包含 AWS、GitHub、Jenkins 等
- 帳號狀態包含 active、expired、pending
- 權限包含 admin、write、read-only

這個過程非常重要，因為清楚的規格是後續成功的基礎。

### 第三步：規劃實作

使用 `/speckit.plan` 根據 Spec 產生 Plan，列出實作步驟，檢查相依性，準備 checklist。

### 第四步：拆分任務

使用 `/speckit.tasks` 將任務拆成多個獨立的子任務，可以分配給不同的 agent。

### 第五步：分析可行性

使用 `/speckit.analyze` 檢查產生的 Task：
- 是否可行？
- 有沒有遺漏的步驟？
- 有沒有不合理的地方？
- 是否存在相互衝突的地方？

### 第六步：平行實作

使用 `/speckit.implement`，啟動多個 agent 平行下去實作。Agent 根據 Task 來實作，直到達成 Spec 的所有要求。

### 最後一步：驗收

完成後進行驗收確認。

這些流程圖展示了 Plan、Task 以及 Implement 的實際樣貌。

---

## 什麼是 Spec-kit

Spec-kit 是 GitHub 開發的一個 SDD（Spec-driven development）工具包。

它的三個核心特點：

第一，它是一個 SDD 流程框架。不只是提供 prompt 技巧，而是一個可重複的工程流程。

第二，它的核心價值在於：把需求、驗收、交付串成同一條線。這樣做的好處是，整個流程變得可追蹤、可驗證、可協作。

---

## 什麼是 Spec-driven development

Spec-driven development 的核心理念是：

**避免模糊需求，產生精準的可執行規格。** 這是第一步，也是最重要的一步。

接著，**Agent 會自動滿足 Spec 實作。** 一旦 Spec 清楚了，Agent 就知道該做什麼。

最後，**Feedback > 修改 Spec > 循環。** 這是一個持續反饋的過程。

Spec-kit 就是 SDD 的工具，提供標準流程與格式，產出可驗證、可協作的規格。Agent 根據規格實作。

---

## SDD vs Chat Coding

讓我們比較一下 SDD 和 Chat Coding 的區別：

| 面向 | SDD | Chat Coding |
| --- | --- | --- |
| **方式** | 先寫需求/設計，再實作 | 先寫程式，邊聊邊修 |
| **短期** | 較慢 | 很快 |
| **長期** | 通常更穩，返工少 | 累積技術債後期變慢 |
| **一致性** | 高，有明確規格 | 看操作者，波動大 |
| **維護性** | 高，文件、決策、邊界清楚 | 中低，脈絡常散在聊天紀錄 |
| **協作** | 好，可 review spec | 較難，知識偏個人化 |
| **風險** | 好，先定義約束與測試 | 較弱，容易漏邊界條件 |
| **適合** | 中大型專案、多人協作 | PoC、腳本、小功能 |

簡單來說，Chat Coding 短期快速，但長期容易累積問題。SDD 短期慢一點，但長期更穩定。

---

## 情境 1：為何適合 SDD

回到我們的第一個例子——內部帳號定期稽核。為什麼這特別適合 SDD？

**首先，任務驗收標準明確：**
- 需要打平台 API，列出帳號
- 依照條件檢查狀態權限
- 篩選離退名單，符合自動告警
- 產出符合稽核格式的結果

**其次，流程固定。** 這個任務的流程是明確的，每次都差不多。

**第三，Spec 變動不大。** 雖然可能平台會增減、API 會改版，但稽核需求與驗收標準不會變。

**第四，自動化效益高。** 人工做這件事非常痛苦，容易出錯。自動化能夠帶來很大的價值。

**最後，終端使用者，沒有被其他元件依賴。** 如果這個工具被其他系統重度依賴，會產生額外的 Spec 變動，增加複雜性。

---

## 延伸情境 1：跨平台人員管理

第一個情境可以延伸到更多的場景：

- 跨平台帳號定期稽核
- Access / Audit log 收集、整理、即時分析、可疑事件告警
- 權限稽核、驗證、更新
- Onboarding / Offboarding 自動化

使用 SDD 量身打造跨平台工具，可以進一步加速流程的驅動。

---

## 情境 2：工作流程自動化

情境 2 是工作流程自動化——Jira-Github-Coding。

在實務中，開發者不想離開 GitHub，PM 不想離開 Jira。我們如何打通這個流程呢？

流程會是這樣：

1. **Human(PM)** 把雜務、例行性事務排進 Jira
2. **Bot** 檢查 Database，查詢過去相關的 Jira Ticket
3. **Bot** 檢查是否有重複的 Ticket
4. **Bot** 開啟對應的 GitHub Issue
5. **Bot** 指派 Coding Agent
6. **Bot** Coding Agent 產生 Spec

此時，**Human(Developer)** 會 Review Spec，Approve Spec

7. **Bot** Coding Agent 根據 Spec 實作 PR
8. **CI** 自動化測試 unit test + e2e test

**Human(Developer)** Review PR，Approve PR

9. **Bot** 所有步驟回寫到 Jira，形成完整紀錄
10. **Bot** Index 到 Vector DB，提供未來類似任務參考

這樣，PM 不用離開 Jira，Developer 不用離開 GitHub，流程完全自動化。

需要注意的是，SDD Debug 會有極限，這個方案比較適用於中型專案。

---

## 可能適合 SDD 的條件

綜合來看，哪些條件的任務適合 SDD？

- **任務驗收標準明確，流程固定，重複性高**
  - 例如 SOP/Runbook 步驟完成率
  - CI/CD Pipeline / 工具串接成功率
- **流程固定**
- **Spec 變動不大**

**一個金律是：完成步驟就達成需求，這類任務非常適合 SDD。** 因為驗收標準明確，流程固定。

---

## 情境 3：服務的 Sidecar

情境 3 是服務的 Sidecar 系統。

這是指 Stateful Backend 的維運輔助系統。Sidecar 為 ops 提供對服務進行操作的能力：

- 重啟服務、調整資源
- 升版、回滾
- 切換 config
- Data Migration、Validation
- Snapshot、Backup、Restore

這類操作通常流程明確，驗收標準清楚，非常適合 SDD。

---

## 情境 4：Debugging Runbook

情境 4 是除錯 Runbook / Incident Response。

流程如下：

1. **Alert** 某個服務功能出錯
2. **Bot** 查架構文件，列出相關的微服務
3. **Bot** 查團隊文件，通知相關值班人員
4. **Bot** 收集所有相關微服務的 Error log
5. **Bot** 查看 Monitoring、Tracing
6. **Bot** 統整資訊，分析問題
7. **Bot** 用 read-only 權限再次存取相關服務，查看狀態、配置、版本
8. **Bot** 整理所有資訊與推論
9. **Bot** 提供解決方案，列出優缺點，建議下一步

此時，**Human** 看到的已經是完整的 Alert + 各方資訊 + 建議解決方案

10. **Human** Review 解決方案，Approve 後實作
11. **Bot** 指定時間內持續追蹤
12. **Bot** 定時主動回報團隊與主管，處理進度

這樣，人類可以更快地做出決策，Bot 幫助收集資訊和分析。

---

## 小結：找到第一個適合的任務

我們梳理了四個情境：跨平台人員管理、Workflow 自動化、Sidecar、Debugging Runbook。

選擇第一個適合 SDD 的任務時，要注意：

- **人工例行事務**：先解放人力，選擇人工工作量大、容易出錯的任務
- **固定流程/SOP/Runbook**：流程不能太多變
- **低風險**：不要一上來就選最複雜的
- **沒有被其他服務重度依賴**：避免 Spec 頻繁變動

---

## 實際導入流程

當你決定採用 SDD 時，導入流程應該是這樣的：

1. **挑題目**：低風險，高人工，需求清楚
2. **從小開始**：先從整個流程的一段步驟開始，而不是全量
3. **發現與改進**：在實踐中發現 Spec 不夠清楚，驗收條件不夠明確，流程遺漏
   - 回到 Spec 修正，建立修正 Spec 的流程與經驗
4. **成功後再擴大範圍**：不要一次性全部換成 SDD

---

## Spec-kit 帶來的痛點

現在讓我們談談實施 Spec-kit 的代價和痛點：

### 工作習慣改變

首先，**工作習慣要改變**。原本的痛苦會左移——寫程式時的痛苦提前到寫需求時。你需要花更多時間在釐清需求上。

### Spec-kit Tax

第二，**Spec-kit Tax：Spec-kit 產生 Spec，會消耗額外 token。**

我們通常會用更好、更貴的模型來寫 Spec，然後用便宜的模型來實作。這會增加成本。

### 不適合舊專案

第三，**不適合舊專案**：Greenfield vs. Brownfield 的問題。

- 無法從舊程式碼逆向產生 Spec
- 對於舊專案，從頭寫 Spec 會燒時間和 token

---

## 改需求的成本變高

SDD 的一個重大挑戰是：**改需求的成本變高。**

當 Spec 寫好、Code 實作後，結果改需求了。你需要改 Spec、改 Plan、改 Task，agent 也要重跑。

**小改動** 可以像 git commit 一樣，疊上去 Spec。

但是 **大改動或需求矛盾**，就要重寫 Spec。Spec-kit 會幫你掃出 conflict，但不會幫你解決。當 Spec 衝突時，之前的 Code 都不能用，要重零開始。

**所以，需求變動頻繁的任務不適合 Spec-kit，反而會變得笨重。**

---

## SDD vs 需求改動

改需求或實作偏離太多時，流程會是：

1. 收集半成品(n) + 分析問題(n)
2. 反饋給 Spec(n) -> 修改 Spec(n) -> 產出 Spec(n+1)
   - Spec(n+1) 比 Spec(n) 更清楚、更完整、更合理
3. 退掉失敗 PR(n)，agent 從頭實作 Spec(n+1)

可以相當程度的校正與需求的偏離，但無法抵抗與 Spec 的根本矛盾。這是一個重要的認知。

---

## Spec-kit 的盡頭是組合拳

Spec-kit 的終局策略是「組合拳」：

- **新專案直上 Spec-kit**：如果是新專案，直接使用 Spec-kit，會最有效率
- **舊專案舊 pkg**：補 Test 保護既有功能，再啟用 Spec-kit
- **公司支持的話，請進行重構**
  - Codebase 中的坑雷與技術債，人都不想解，Agent 也解不了
  - 把舊 Code 當成 Spec reference，重寫成 Spec v2，然後重構

其實是在用各種方法，讓虛幻的 Spec 落地。**這不是 Best Practice，而是 Working Practice。**

---

## 你可以帶走的重點

在這場議程的最後，我想總結幾個重點：

1. **DevOps 任務，許多已有明確的 Spec**。不是所有事情都模糊。

2. **選對題目**：高人工、低風險，跨平台，被依賴性低的任務。這是成功的關鍵。

3. **從 vibe/chat coding 走向 Spec-kit**
   - 標準化流程
   - 分工協作
   - 更容易擴展和維護

4. **SDD 絕非萬能，需求合適的任務，才適合 SDD。**

最後一句：**Spec-kit 不是終點，同志仍須努力。**

---

## 結語

Q&A 不是演講的終點。下週 Cloud Summit 會有一場 Workshop，會帶大家實際操作 Spec-kit，歡迎來玩！

我提供了兩個資源連結供大家進一步學習：
- Workshop：Spec-driven development with Spec-kit
- Session：從 Vibe Coding 到 Spec-driven AI Engineering

感謝各位的聆聽。
