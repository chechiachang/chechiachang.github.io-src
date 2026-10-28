---
title: "Platform Engineering 的 AI 實際落地案例"
description: "從三個工程案例理解 Vibe Coding、SDD 與 Coding Agent，並建立 AI 平台的安全與維運邊界"
tags: ["ai", "ai-engineering", "platform-engineering", "devops"]
categories: ["generative", "ai"]
date: '2026-10-29T00:00:00Z'
outputs: ["Reveal"]
reveal_hugo:
  slide_number: true
  custom_theme: "reveal-hugo/themes/larger-font.css"
  margin: 0.2
  highlight_theme: "color-brewer"
  transition: "slide"
  transition_speed: "fast"
---

##### Platform Engineering 的 AI 實際落地案例

從 Vibe Coding 到 AI Platform

Che-Chia Chang

---

##### Outline

- Project 1: Automation
- Project 2: 微服務與工具箱
- Project 3: Knowledge Agents
- Takeaways

---

##### Project 1｜Automation

**背景**

- 從早期自動化到開始使用 ChatGPT
- GPT-3.5（2022/11）→ GPT-4（2023/03）→ GPT-4o（2024/03）

**需求：Blockchain Full / Validator Node**

- 流程完整，有固定 SOP
  <br>但操作耗時
- 步驟繁瑣，低成就感，人工容易出錯
- 規格清楚

---

##### Project 1｜步驟

- 依據現有流程，設計流程、架構圖與開發階段
- Prompt Engineering + Spec-kit
  <br>參考既有的 Slides Workshop
- LLM 協作開發，產生程式碼與測試
- QA 手動測試，部分自動化測試

---

##### Project 1｜成果：大平台

- 自動化升級、維護、備份與備援
  <br>支援水平與垂直拓展
- 整合 Prometheus Metrics 與 Alertmanager 主動告警
- 大幅降低維運時間
- 提升團隊幸福度

---

##### Project 1｜限制

- 需要支援不同鏈，方案未必通用
- 各鏈持續升級 Hard Fork，無法完全免人工
- 功能增加，大平台驗證成本也隨之增加
- 需求改動導致維護成本上升

---

##### Project 1｜心得

- 選對題目比努力重要，跟畢業論文一樣
- 選好題目，追求 100% 自動化，享受成果
- 直到需求改變的那一天
- 100% 自動化只適用於規格固定的流程
  <br>明確規則交給程式，不把所有決策交給 LLM

---

##### Project 2｜微服務與工具箱

**需求：跨平台系統稽核軌跡**

- 所有系統操作都要有 Audit Log
  <br>並產出報告
- 抽查特定系統
- 人工定期抽查
- 自動化持續檢測與告警
- 流程大方向穩定，但細節模糊
  <br>輸入與輸出發散

---

##### Project 2｜MVP：標準化流程

- 人類提供過去大致的流程與方向
- LLM 會猜測並嘗試不同的 MCP 與 API 呼叫
- 紀錄 LLM 步驟，比對人類步驟

---

##### Project 2｜步驟：標準化自動化

- 寫一個小工具存取系統
- Hardcode 控制流程，Infra Policy 控制權限
- Hardcode 控制產出格式
- LLM 潤飾 Input / Output
- 最小權限
- LLM

---

##### Project 2｜成果

- 穩定提升報告品質
- 小工具都可讓 LLM 自動驗證輸入與產出
- 可以承受非預期的 API 改版或輸出調整
- 大幅降低人工時間，提升團隊幸福度
- 會有很多 Skills 與 Scripts

---

##### Project 2｜Evaluation

- 檢查結果品質與例外是否遺漏
- 比較節省的人工時間
- 確認失敗後能否復原與重試
- 計算 Token、API 與維護成本
- 用真實任務建立 Baseline
  <br>比較改動前後

---

##### Project 2｜安全問題

- Security Issues
- 開發者最小權限，以及 Infra / Hardcode Policy
- 如何控管 MCP 與 Agent Tools

---

##### Project 2｜Security Hardening

- 給 Skill 或 Goal，LLM 會做各種嘗試
- 移除探索步驟，用 Code 固定大部分流程
- 不用 Goal 讓 LLM 自由發揮產出報告
- LLM 填入 API 參數，再透過工具產出報告
- Decision Model：需要選擇題時，不提供問答題的可能

---

##### Project 2｜安全成果

- Least Privilege
- LLM Sandboxing
- Guardrails、Observability
- LLM 可用的 Tool 白名單，預設阻擋

---

##### Project 2｜安全成果（續）

- Secret 不放在 Prompt 或 Agent Context
- 破壞性操作需要人工 Approval
- API 呼叫設置逾時、重試與速率限制
- 保存 Audit Log，保護敏感資料

---

##### Project 2｜心得

- 從大平台到小工具
- 小工具更好開發與驗證
- 過去的努力不一定會有成果，但不會白費
- Security First 才走得遠

---

##### Project 3｜Knowledge Agents

**需求：自動化開發**

- Jira → PR → Review → Release
- 降低需要人類介入的環節
- 把專注力用在 Review 與驗證

---

##### Project 3｜步驟

- Infra：AI Gateway、Observability、Evaluation
- Identity 確認使用者與工作身份
  <br>Policy 限制可使用的資料與 Tools
- Execution 執行工作並處理錯誤
  <br>Evaluation 確認結果品質與回歸
- Knowledge Base、RAG

---

##### Project 3｜成果：Limited Agents

- 依照指定流程，安全地完成指定任務
- 使用便宜的模型
- FAQ Agent：問過的問題不要再問人類
- Orchestration Agent、Coding Agent
  <br>PR Review Agent、Debug Agent
- Validator

---

##### Project 3｜後續與心得

- 過去的努力不一定會有成果，但不會白費
- 安全第一，Security First 才走得遠
- 不要相信 LLM Security Instructions

---

##### Takeaways

- 挑對題目
- 安全第一
- 流程與安全需要 Hardcode
- 產出與潤飾委託 Agent
- 從小工具開始堆疊平台
