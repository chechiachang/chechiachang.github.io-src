# Slide Outline

## Talk Type

- Standard (30-40 min)
- Target: 35 min
- Target slide count: 20
- Style: Conference talk + short guided demo flow (non-live coding heavy)

## Sections and Timing

- Opening + problem framing: 5 min
- SDD fundamentals + fit for DevOps: 8 min
- Spec-kit workflow + demo flow: 10 min
- Adoption boundaries + pitfalls: 7 min
- Wrap-up + Q&A: 5 min
- Buffer: 2 min (for interaction or demo lag)

## Slides

1. 規格驅動的 AI 強化 DevOps（標題）
- Time: 1 min
- Goal: 建立主題與受眾期待。
- Detail: 先定義今天不是「哪個工具/模型最強」，而是「哪些 DevOps 任務 SpecKit 是神器」。

2. 大綱
- Time: 1 min
- Goal: 告知今天路線圖。
- Detail: 先問題、再方法、再流程、再邊界，最後給可立即帶回去的做法。

3. DevOps 現場痛點：碎片化與高重複
- Time: 2 min
- Goal: 讓聽眾對齊問題背景。
- Detail: 例子包含一份 SOP 場常用但需要人工，一個服務沒有自動維運工具靠手動。
- Detail: 點出「有文件」不等於「可驗證執行」。

4. What is Spec-driven Development
- Time: 2 min
- Goal: 給出 SDD 定義與核心元素。
- Detail: 定義為「先定義可檢查規格，再讓 agent 按規格實作與驗收」。
- Detail: 核心元素：需求、限制、驗收、回饋循環。

5. Why SDD fits DevOps (輸入/輸出/驗收)
- Time: 2 min
- Goal: 說明 DevOps 任務多為可規格化。
- Detail: DevOps 任務常有明確輸入/輸出（命令、狀態、數值 threshold）。
- Detail: 驗收可落在 Boolean/Number（成功率、時延、錯誤率）比 UI 審美更可控。

6. 對比 Dev 實作 vs DevOps 實作
- Time: 2 min
- Goal: 說明兩者驗收型態差異。
- Detail: Dev 偏功能/體驗驗收，DevOps 偏流程/穩定性/風險驗收。
- Detail: 強調不是誰比較簡單，是驗收維度不同。
- Detail: DevOps 很像動物園一堆服務健康就好，Dev 是養一隻動物要會動會叫還要長得美

7. LLM 產出差異：Boolean/Number 任務更可控
- Time: 2 min
- Goal: 說明為何先從 DevOps 類任務切入。
- Detail: 用 incident triage、health check、deploy guard 當例子。
- Detail: 強調先選「低風險高頻率可量測」題目，成功率最高。

8. Spec-kit 是什麼
- Time: 1 min
- Goal: 介紹工具定位。
- Detail: 一套把 SDD 流程標準化的工具，而不是單一 prompt 技巧。

9. Prompt vs Spec（聊天 vs 工程）
- Time: 2 min
- Goal: 打核心記憶點。
- Detail: Prompt 解單次問題；Spec 管長任務與多輪改動一致性。
- Detail: 金句重複：Vibe 是聊天，Spec 是工程。

10. Spec-kit 核心流程：specify -> plan -> tasks
- Time: 2 min
- Goal: 說清流程骨架。
- Detail: 補完整鏈路：`/speckit.specify -> /speckit.plan -> /speckit.tasks -> /speckit.implement -> /speckit.analyze -> /speckit.checklist`。
- Detail: 規則：需求變更先回 spec，不直接改 code。

11. SOP 到可驗證交付閉環（流程圖）
- Time: 2 min
- Goal: 展示執行與回饋如何串起來。
- Detail: SOP/Runbook -> 規格 -> 任務 -> 實作 -> 分析 -> checklist -> 回寫規格。
- Detail: 每一步都有 checkpoint，避免 late surprise。

12. Step 1: 選題（低風險/高頻/可量測）
- Time: 1.5 min
- Goal: 提供導入起點。
- Detail: 題目模板：可重跑、可比較前後結果、出錯可回滾。
- Detail: 範例：站點資料抓取、告警分級、每日巡檢摘要。

13. Step 2: 規格化（前置條件/步驟/驗收/回滾）
- Time: 1.5 min
- Goal: 說明規格內容要件。
- Detail: 用 workshop 格式：user stories + acceptance criteria + non-goals。
- Detail: 加入 constitution 概念：命名、test coverage、極簡，閱讀便利性優先。

14. Step 3: 接上執行（CI/CD + Metrics + Incident）
- Time: 2 min
- Goal: 連到平台工程落地。
- Detail: plan.md 固定技術棧與邊界，tasks.md 拆可驗證任務。
- Detail: implement 階段要求按 tasks 順序，避免隨意跳步。

15. Demo 流程（Runbook -> Spec -> Pipeline）
- Time: 2 min
- Goal: 讓流程具體可想像。
- Detail: Demo 題目：YouBike 2.0 站點查詢器（API 抓取 + 搜尋 + 低庫存警示）。
- Detail: 展示不斷調整需求，實作時一次完成所有步驟，最後回到 spec 調整驗收標準。

9. Context management：Prompt vs Spec
- Time: 2 min
- Goal: 說明為何 Spec 更適合長期任務管理。
- Detail: Vibe 越長 context 越大，需要在對話中 compact context，容易忘記更早的細節
- Detail: Spec drift 持續累積，造成規格與實作脫節
- Detail: SpecKit 使用 template 與 checkpoint 管理 context，確保規格與實作保持同步。

16. 適合先導入情境
- Time: 2 min
- Goal: 幫聽眾判斷 where to start。
- Detail: 高重複、流程固定、可量測、跨班別需一致執行。
- Detail: 例如：oncall 例行檢查、部署前驗證、事故後標準化修復。

17. 先不要導入情境
- Time: 2 min
- Goal: 設定風險邊界。
- Detail: 高探索性研究題、需求高度模糊、驗收標準未定。
- Detail: 若業務規則還在變，先整理 domain language 再導入。

18. 加深印象：先不要導入情境
- Time: 2 min
- Goal: 重複關鍵風險點，避免誤入。
- Detail: 「重複且可規格化」的任務，若不符合這兩點，成功率會大幅下降。
- Detail: 「隕石頻率高」，SpecKit 修完「實作過的規格」，直接重頭實作

18. 面對不適合的任務
- Time: 2 min
- Goal: 提供應對策略提供嘗試，避免完全放棄。
- Detail: 規格一直變動「隕石頻率高」。SpecKit 修完「實作過的規格」，直接重頭實作
- Detail: 「上次實作程式碼」加上「新需求」，修正產生「新的規格」
- Detail: 完成規格後的實作成本低，「勝敗乃兵家常事也，大俠請重新來過吧」

19. 常見踩雷與實務建議
- Time: 3 min
- Goal: 避免失敗模式。
- Detail: 雷點：spec 檢視不踏實、驗收標準不明確。
- Detail: 修正：可以多用不同模型，PR 中自動針對規格來回驗證。
- Detail: 「AI 挑出小錯誤的能力很強」產出高品質的規格來驅動實作品質。

20. 你可以帶走的重點 + Q&A
- Time: 3.5 min
- Goal: 收斂重點並啟動交流。
- Detail: 帶走三句話：
  1) 選對任務，全自動化，時間用在更有價值的工作上
  2) 規格優先，避免返工，高品質的規格驅動實作品質
  3) Speckit 絕非完美，但在特定任務是神器。用在那些任務上
- Detail: 與其問工具強不強，不如問工具對不對。

## Total

- Planned total: 35 min
