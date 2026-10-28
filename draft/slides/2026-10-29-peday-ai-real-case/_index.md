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

##### Project 1: Automation

**背景**

- 從史前時代到已知用 chatgpt
- gpt 3.5 (2022/11) gpt 4 (2023/03) gpt 4o (2024/03)

**需求: blockchain full/validator node**

- 流程完整，有固定SOP，但操作耗時
- 步驟繁瑣，低成就感，人工容易出錯
- 規格清楚

**步驟**

- 依據現有流程，設計流程，架構圖，與開發階段
- prompt engineering + speckit (參考已經有的 slides workshop)
- llm 協作開發，產生程式碼與測試
- QA 手動測試，部分自動化測試

**成果: 大平台**

- 自動化升級，維護，備份，備援，水平與垂直拓展
- 整合 prometheus metrics 與 alertmanager 主動告警
- 大幅降低維運時間
- 提升團隊幸福度

**限制**

- 需要支援不同鏈，不同鏈未必適用
- 不同鏈也會不斷升級 hardfork，無法完全去人工
- 功能增加，大平台驗證成本也增加
- 需求改動導致維護成本上升

**心得**

- 選對題目比努力重要，跟畢業論文一樣
- 選好題目，追求 100% 自動化，享受成果
- 直到需求改變的那天
- 100% 自動化只適用於規格固定的流程；明確規則交給程式，不把所有決策交給 LLM

##### Project 2: 微服務與工具箱

**需求: 跨平台系統稽核軌跡**

- 所有系統的操作都要有 audit log 並且產出報告
- 抽查特定系統
- 人工定期抽查
- 自動化持續檢測與告警
- 流程大方向穩定，但細節模糊，輸入與輸出發散

**MVP: 標準化流程**

- 人類提供過去大概的流程與方向
- LLM 會去猜測家嘗試不同的 MCP, API call
- 紀錄 LLM 步驟，比對人類步驟

**步驟: 標準化自動化**

- 寫一個小工具存取系統
- hardcode 控制流程，infra policy 控制權限
- hardcode 控制產出格式
- llm 潤飾 Input/Output 
- 最小權限
- llm 

**成果**

- 穩定提升報告品質
- 小工具都可讓 llm 自動驗證輸入產出
- 可以承受不預期的 api 改版或輸出調整
- 大幅降低人工時間，提升團隊幸福度
- 會有很多 skills, scripts

**Evaluation**

- 檢查結果品質與例外是否遺漏
- 比較節省的人工時間
- 確認失敗後能否復原與重試
- 計算 Token、API 與維護成本
- 用真實任務建立 baseline，比較改動前後

**安全問題**

- security issues
- 開發者最小權限與 infra/hardcode policy
- MCP 與 agent tools 要如何控管

**Security hardening**

- 給 skill 或是 goal，LLM 會去各種嘗試
- 把嘗試的部分去掉，用 code 固定大部分
- 不用 goal: 自由發揮產出報告
- LLM 填上這幾個 api 參數，透過工具就會產出這個報告
- decision model: 有時需要產出是選擇題，就不要給問答題的可能

**安全成果**

- least privilege
- llm sandboxing
- guardrails, observability
- llm 可以使用的 tool 白名單，預設阻擋
- Secret 不放在 Prompt 或 Agent Context
- 破壞性操作需要人工 Approval
- API 呼叫設置逾時、重試與速率限制
- 保存 Audit Log，保護敏感資料

**心得**

- 從大平台到小工具
- 小工具更好開發與驗證
- 過去的努力不一定會有成果，但不會白費
- security first 才走得遠

##### Project 3: Knowledge Agents

**需求: 自動化開發**

- Jira -> PR -> Review -> Release
- 降低人類需要干涉的環節
- 把專注力用在 review 與驗證

**步驟**

- infra: AI Gateway, Observability, Evaluation
- Identity 確認使用者與工作身份；Policy 限制可使用的資料與 Tools
- Execution 執行工作並處理錯誤；Evaluation 確認結果品質與回歸
- knowledge base, RAG

**成果: limited agents**

- 依照指定的流程，安全地完成指定的任務
- 使用便宜的模型
- FAQ Agent: 問過的問題不要再問人類
- Orchestration Agent, Coding Agent, PR Review Agent, Debug Agent
- validator

**然後**

**心得**

- 過去的努力不一定會有成果，但不會白費
- 安全第一，security first 才走得遠
- 不要相信 LLM security instruction

##### Takeaways

- 挑對題目
- 安全第一
- 流程與安全需要 hardcode
- 產出與潤飾委託 agent
- 從小工具開始堆疊平台

---
