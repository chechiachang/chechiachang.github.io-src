---
title: "Observing and Evaluating LLM Coding Agents"
description: "觀察 LLM coding agents 的行為，再建立 evaluation、dataset、regression 與 decision gate，讓模型與框架升級可驗證"
tags: ["llm", "agent", "observability", "evaluation", "aiops", "devops"]
categories: ["aiops", "observability"]
date: '2026-07-08T00:00:00Z'
outputs: ["Reveal"]
reveal_hugo:
  custom_theme: "reveal-hugo/themes/larger-font.css"
  margin: 0.2
  highlight_theme: "color-brewer"
  transition: "slide"
  transition_speed: "fast"
---

##### Observing and Evaluating LLM Coding Agents
##### 觀察，建立基礎，迭代驗證

Che-Chia Chang

---

##### Coding Agent 會動就好
##### 為何還需要 Observability 與 Evaluation？

---

- 紀錄 Coding Agent 效能 baseline
  - 效能劣化時告警
  - 紀錄原因：e.g. 上游 API 不穩定
  - Claude API Uptime 只有 99.4%
  - 沒有 o11y 就沒有 SLA

{{% note %}}

至少要知道他什麼時候是壞的

進行處置：切換 model 或 provider

至少要知道服務劣化

{{% /note %}}

---

{{< slide background-image="05-claude-status.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

Change Management

- 改變後，效能是變好還是變差
- [Spec-kit](https://github.com/github/spec-kit) SDD 聽說好用要不要試
- [rtk](https://github.com/rtk-ai/rtk) 聽說省 Token，要不要導入
- [Opus 4.8](https://www.anthropic.com/claude/opus) 聽說很強
- 改變可能會劣化
- 改變需要成本
- 需要數據化的決策流程，避免 FOMO

{{% note %}}

- 把每個工具都試用一遍
- 閱讀專家的分享與供應商的文章
- 採用代理商或公有雲的推薦

每個都試用的確是一種選擇，但不太實際；團隊產出會大打折扣，也可能因此失去信心

我們也很難區分宣傳文案與真正的技術分享

雲服務商提供各種產品，本質上也在推銷產品

這些問題的核心，是缺乏以數據為基礎的決策流程
{{% /note %}}

---

Cost Management

- 根據監測控管預算，本月花費收斂下月預算
- charge back 團隊看見自己的成本
- 哪些問題用錢解決，哪些不能
- 需求進化比模型快
  - 不會有一個超強模型解決所有問題
- 剛好的預算，選適合的模型，選適合的問題
  - 有效率的解決能解的問題

---

為何需要 Observability
- Baseline
- change management
- cost management

---

{{< slide content="slides.about-me" >}}

---

今天的內容

- ✅ Change & Cost Management
- 建立 baseline 與第一次優化
- LLM as a Judge
- Dataset & Experiment
- 釐清需求：提升 Coding Agent 效能
- Decision System

---

##### 從 Observability 開始

- 透過 AI Gateway 或 Observability Tool 收集 Tracing
- 建立 LLM O11y、LLM-as-a-Judge，以及 Dataset 與 Experiment 流程
- 技術細節請見 [LAB Cloud Summit 2026: LLM O11y](../../slides/2026-07-01-ws-langfuse-ai-ent) 或是 [LLM O11y：從 Observability 到 Decision System](https://chechia.net/posts/2026-07-01-ws-langfuse-ai-ent/)

「我的 Agent 到底怎麼花 Token 的」「如何系統化評估 Agent 輸出品質」

---

{{< slide background-image="00-langfuse-tracing.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

##### 導入 Gateway 或 Observability Tool 後

- 觀察到 Observability Stack
- 看見量化數據：Token Usage、Latency、Error Rate
- Chargeback 讓團隊成員看見自己的成本
- 根據監測紀錄控管預算，而不是只看市場喊價

先建立 Cost 與 Token Usage baseline，定義什麼是符合預算、什麼是超出預算

---

##### Step 1: 建立 Baseline，完成第一次優化

- 先理解正在使用的 CLI
  - VSCode Copilot、Codex、OpenCode 的行為都不相同
- 停用不必要的 Tools
  - VSCode Copilot 內建 50+ 個 Tools，但實務上只用到 10+ 個
  - VSCode Extension 也可能增加 Tools
  - AI Gateway 提供額外的控制點

控制你的 Coding Agent

---

{{< slide background-image="01-cli-baseline.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

{{% note %}}
- User: "hi"
- Agent: "Hi! How can I help you today?"

- 這個簡單的互動就用了 20,000+ Input Tokens
- 成本約 0.1 USD（3 TWD；$5.00/1M Tokens）
{{% /note %}}

---

##### Step 1: 完成第一次優化

- Token Usage Overhead 從 20,000+ 降到 1,000+
- 成本從 0.1 USD 降到 0.005 USD（約為原本的 5%）
- 降低進入 Long Context 的機率（>=272K Tokens 會變成兩倍價格）
- 把 Context Window 留給真正有用的 Context

https://developers.openai.com/api/docs/pricing

{{% note %}}
Input Token Cache 只是折扣，不是免費；它可以改善 Model 在 Long Context 下的效能，
但不該因此被拿來浪費
{{% /note %}}

---

##### Step 2: 用 LLM 作為 Judge

- 前一步根據 Tracing Metadata 優化成本
- 接著根據 Tracing 的 Input/Output 優化品質
  - 讓 LLM 根據 Input 與 Output 評估結果品質
  - 傳統程式碼測試的場景有限，難以涵蓋 LLM 多變的使用情境

---

{{< slide background-image="02-llm-as-a-judge.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

{{% note %}}
使用 Langfuse 收集 Tracing 資料，
先把 Input/Output 的品質量化，
再使用內建的 Evaluator Library，或自行撰寫 Prompt 評估品質
{{% /note %}}

---

##### Step 2: 以 Observation 為單位評估

以 Observation 為單位，評估每次 API Call 的品質

- 針對 Input、Output、Metadata 或部分資料進行評估
- 先在小 scope 內進行量化，以管窺天
  - 反映局部品質
  - 但無法代表 Project 的整體品質

先從局部開始，分析錯誤類型並找出改進方向

---

##### Step 2: 根據評估結果完成第二次優化

LLM-as-a-Judge 的評估結果，持續調整

- 控制其他變因，例如
  - Metadata：Token Usage、Latency、Cost
  - Model Version
- 優化 Input/Output 品質
  - Prompt 與 Instruction

控制變因，調整變因，持續提升局部分數

---

##### Step 2: Multi-turn Agent

Long-running Agent 很難只看最終答案來評估，例如

```text
Input: 更新 README.md
- Assistant: 先看 README.md 內容
- Assistant: [tool] cat README.md -> README.md 內容
- Assistant: [tool] plan -> plan
- ...
- Assistant: 根據 README.md 內容，修改 README.md
- Assistant: [tool] apply patch -> 修改後 README.md 內容
Output: README.md 修改成功
```

針對單一步驟評估，例如 Plan 或 [tool] Apply Patch

---

{{< slide background-image="03-multi-turn-agent.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

##### Step 3: 建立 Dataset，執行 Experiment

Dataset：從 Daily Work Tracing 整理出的真實考題

```text
Input 反映真實工作需求
Output 反映 Model 上次的回答
LLM-as-a-Judge 的分數反映回答品質
```

Experiment：使用同一份考題，控制不同變因重複執行

```text
Model：5.4 -> 5.5
Tools：改動前後
Instruction：改動前後
```

---

{{< slide background-image="04-dataset-experiment.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

{{% note %}}
這是使用 Spec-kit 產生的 YouBike API app
{{% /note %}}

---

##### Step 3: 整理 Dataset

先根據更細緻的需求定義分類 Dataset

- Plan 著重 Context Precision
- Coding 著重 Answer Correctness

再根據 LLM-as-a-Judge 分類 Dataset
- 高分高品質的案例，作為未來改進的參考

Warning: o11y 走進 Dataset 是一個大坑

---

##### Step 3: 進行 Data Preprocessing

- 清理 Tracing 資料格式
- 根據需求，挑出有意義的 Features
  - 例如 `Output.tool_calls.args`
  - Model 收到 Input 時呼叫哪些 Tools，帶什麼參數
- 用 Langfuse SDK Transform 成其他格式
- Partition Dataset

儲存到持久化儲存系統，作為測試題庫

---

##### Step 3: 完成第三次優化

針對題庫中的特定題目，測試最佳 Model

- Pro, Mini, Nano
- Thinking Effort
- GPT-5.4, GPT-5.5
- Codex, OpenCode, Copilot

不要等待 Model 變強來解決問題

選擇最佳的工具，在品質與成本之間取得平衡

---

##### Step 3: Evaluation 後，就取得 Cost Estimate

- 完成多少題目
- 使用的 Model 與 metrics
  - LLM API metrics，使用多少 Token
- Quality Estimate

沒有測試做基礎的預算，其實是市場喊價

---

##### Step 0: 先釐清需求

釐清需求，應該是第一件要做的事

實務上，很多團隊還沒做到前兩件事
- 沒有清楚定義需求
- 成員對 LLM 的理解存在落差
- 就開始討論要不要更換工具

{{% fragment %}}
建議「先建立監測」：先看見顯微鏡下的世界，再相信微生物存在，會比較容易接受

用數據調整團隊認知，後續討論才更容易回到現實
{{% /fragment %}}

{{% note %}}
不能怪團隊不理解成本；要先讓大家容易看見成本，才會開始在意成本
{{% /note %}}

---

##### Step 0: 定義 Coding Agent 的效率

我們想提升團隊使用 Coding Agent 的效率

但 Coding Agent 的效率到底是什麼？

{{< math >}}
\text{整體效率 Efficiency} = \frac{\text{產出數量} \times \text{產出品質}}{\text{Token Cost} \times \text{花費時間}}
{{< /math >}}

{{% fragment %}}
降低 Cost、Latency、Error Rate
控制 Context Window
提升 Output Quality
{{% /fragment %}}

---

##### Step 0: 從需求走向 Action

依照不同任務選工具

- Model: Mini, Nano, Low Latency, Low Error Rate
- AI Gateway Routing
  - [AgentGateway](https://agentgateway.dev/) ✅
  - [LiteLLM](https://docs.litellm.ai/docs/routing)👻
- Context Management -> [rtk](https://github.com/rtk-ai/rtk)
- 加速 Greenfield 專案開發 -> [Spec-kit](https://github.com/github/spec-kit)

---

##### Step 0: 讓團隊 On the Same Page

- Dev Team: Chargeback
  - Model & Tool Choice
- Stakeholders 與管理者對齊期待
  - 量化效能指標：正確率、Error Rate、Latency、Cost
  - 有 AI 不代表就能十倍產出

有 Evaluation 後，可以明確講出「我們產出大概 2-3 倍，數據在此」

---

##### Takeaway: 從觀察到決策系統

- Step 1: 建立 Baseline，完成第一次優化
- Step 2: 使用 LLM-as-a-Judge 評估品質
- Step 3: 建立 Dataset，執行 Experiment
- Step 0: 先釐清需求
- Decision: 釐清需求 -> Take Action

---

##### Q&A

- Lab [LLM O11y：從 Observability 到 Decision System](https://chechia.net/posts/2026-07-01-ws-langfuse-ai-ent/)
- Lab [Spec-driven development with Spec-kit](https://chechia.net/posts/2026-07-01-ws-speckit-ai-ent/)
