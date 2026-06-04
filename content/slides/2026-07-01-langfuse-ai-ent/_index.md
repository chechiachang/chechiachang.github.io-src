---
title: "LLM O11y：從 Observability 到 Decision System"
description: "30 分鐘分享，從 Langfuse Observability 出發，補上 Evaluation、Dataset、Regression 與 Decision Gate，建立可落地的 LLM Decision System。"
tags: ["llm", "agent", "observability", "langfuse", "evaluation", "aiops"]
categories: ["aiops", "observability"]
date: '2026-05-02T15:30:00Z'
outputs: ["Reveal"]
reveal_hugo:
  custom_theme: "reveal-hugo/themes/robot-lung.css"
  margin: 0.2
  highlight_theme: "color-brewer"
  transition: "slide"
  transition_speed: "fast"
---

##### LLM O11y：從 Observability 到 Decision System
##### 從監測到資料決策
##### ~ Che Chia Chang @ [chechia.net](https://chechia.net) ~

---

##### 同事問

- [Spec-kit](https://github.com/github/spec-kit) SDD 聽說很好用
- [rtk](https://github.com/rtk-ai/rtk) 聽說省 Token，我們要不要用 rtk?
- [Opus 4.8](https://www.anthropic.com/claude/opus) 聽說更強大，升級不加錢，為何不升級?
- xx 模型 Benchmark 贏現在用的，我們要不要換供應商?

身為團隊技術負責人，如何回答這些問題

---

##### 面對 AI 工具的快速迭代

- 每個都試用看看
- 看大大的分享文章，供應商的文章
- 給代理商或公有雲推薦

{{% note %}}
每個都試用看看的確是個選項，但不太實際，團隊產出會大打折扣，還可能因此失去信心。

如何區分宣傳文案和真正的技術分享

雲服務商提供各種產品，賣藥

這些問題的核心，是缺乏數據化決策流程
{{% /note %}}

---

##### 新工具冒出來的速度 > 人研究的速度

但需要的不是更快的研究速度

{{% fragment %}}
缺的是數據化決策，不是更多聽說
{{% /fragment %}}

{{% fragment %}}
真正缺的，是 LLM 解決方案的量化評估系統
{{% /fragment %}}

{{% fragment %}}
團隊信任現有的 Stack，不會 FOMO，並有能力驗證改動的影響
{{% /fragment %}}

---

## 今天的大綱

- ✅AI 時代的工具抉擇，缺乏數據化決策
- 建立 baseline 與第一次優化
- LLM as a Judge
- Dataset & Experiment
- 釐清需求：提升 Coding Agent 效能
- Decision System

---

##### 如何開始 O11y

- 透過 AI Gateway 或 Observability Tool 收集 Tracing
- 早上 Lab 13:30-15:00 分享本議程 Workshop
- 建立 LLM O11y，LLM-as-a-Judge，以及 Dataset 與實驗流程
- 技術細節請見 [LLM O11y：從 Observability 到 Decision System](https://chechia.net/posts/2026-07-01-ws-langfuse-ai-ent/)
  - 「我的 Agent 到底怎麼花 Token 的」
  - 「如何系統化評估 Agent 輸出品質」

---

{{< slide background-image="00-langfuse-tracing.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

##### 有了 Observability Stack 後

- 看到量化數據：Token Usage, Latency, Error Rate
- Chargeback 團隊使用者看到自己的成本
- 基於監測紀錄的預算控管，而非市場喊價

建立成本與 Token Usage baseline：什麼是符合預算與超過預算

--- 

##### Step 1: 建立 baseline 與第一次優化

- 理解使用的 CLI
  - VSCode Copilot, Codex, OpenCode 行為都不一樣
- 停用無用的 Tools
  - VSCode Copilot Built-in 50+ Tools，但實務上只用到 10+ 個
  - VSCode Extension 也會增加 Tools
  - AI Gateway
- 控制 CLI System Instruction 的內容

---

{{< slide background-image="01-cli-baseline.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

{{% note %}}
- User: "hi"
- Agent: "Hi! How can I help you today?"

- 就用了 20000+ Input Tokens
- 約 0.1 USD 的成本，3 TWD ($5.00/1M Tokens)
{{% /note %}}

--- 

##### Step 1: 第一次優化後

- Token Usage Overhead 從 20000+ 降到 1000+
- 成本從 0.1 USD 降到 0.005 USD (~5% 的成本)
- 降低 Long Context 機率（>=272K Tokens 變成兩倍價格）
- 節省 Context Window 給實際有用的 Context

https://developers.openai.com/api/docs/pricing

{{% note %}}
Input Token Cache 只是打折，不是不用錢，並且可以提高 Model 在 Long Context 下的效能
不該拿來浪費
{{% /note %}}

---

##### Step 2: LLM as a Judge

- 前面根據 Tracing Metadata 進行成本最佳化
- LLM-as-a-Judge 是根據 Tracing Input/Output 進行品質最佳化
  - LLM 收到 Input 後，根據 Output 評分效能
  - 傳統程式碼的測試，場景侷限，無法符合 LLM 多變的場景

---

{{< slide background-image="02-llm-as-a-judge.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

{{% note %}}
使用 Langfuse 收集到的 Tracing 資料
先把 Input/Output 的品質量化出來
使用內建的 Evaluator Library，或是自己寫 Prompt 來評估品質
{{% /note %}}

---

##### Step 2: LLM as a Judge

Observation 為單位，評估 API Call 的品質

- 針對 Input/Output/Metadata 或部分資料進行評估
- 小 scope 內的量化評估
  - 反應局部品質
  - 無法反映 Project 整體品質
- 暫且以管窺天，分析錯誤類型，找到改進的方向

---

##### Step 2: 第二次優化

根據 LLM-as-a-Judge 的評估結果

- 控制其他變因，例如
  - Metadata: Token Usage, Latency, Cost
  - Model Version
- 優化 Input/Output 的品質
  - Prompt 與 Instruction

Judge 不變，持續提升局部獲得的評分

---

##### Step 2: Multi-turn Agent

Long Running Agent 的評估很難直接看最終答案，例如

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

針對單一步驟做評估，例如 Plan，或是 [tool] Apply Patch

---

{{< slide background-image="03-multi-turn-agent.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

##### Step 3: Dataset & Experiment

Dataset: 從 Daily Work Tracing 挖出的考古題

```text
Input 反映真實工作需求
Output 反映上次 Model 的回答
LLM-as-a-Judge 的評分反映品質
```

Experiment: 同一份考古題，換不同變因來跑

```text
Model 5.4 -> 5.5
Tools 改動前後
Instruction 改動前後
```

---

{{< slide background-image="04-dataset-experiment.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

{{% note %}}
這個是 Spec-kit 產生 ubike API app
{{% /note %}}

---

##### Step 3: Dataset

根據更細節的需求定義，先把 Dataset 分類
- Plan 時在意 Context Precision
- Coding 時在意 Answer Correctness

根據 LLM-as-a-Judge 的評分，先把 Dataset 分類
- good: 評分高的，品質好的，作為未來改進的參考

{{% note %}}
Dataset 是個大坑
{{% /note %}}

---

##### Step 3: Data Preprocessing

- 清理 Tracing 資料格式
- 根據需求，從資料中挑出有意義的 Features
  - 例如 `Output.tool_calls.args`
  - Model 收到 Input 時呼叫哪些 Tools，帶什麼參數
- 透過 Langfuse SDK 做 Transform 其他格式
- Partition Dataset
- 存到持久化儲存

---

##### Step 3: 第三次優化

針對特定情境選擇最適合的工具與 Model
- Pro, Mini, Nano
- Thinking Effort
- GPT-5.4, GPT-5.5
- Codex, OpenCode, Copilot

不是等 Model 或工具變強來解決問題

而是選更適合的工具做品質與成本的平衡

---

##### Step 0: 釐清需求

釐清需求是第一件該做的事

然而實務上發現，很多團隊在
- 沒有清楚定義需求
- 對於 LLM 的理解知識有落差
- 就開始討論要不要換工具

{{% fragment %}}
建議「先有監測」先看到顯微底下的世界，再去相信微生物存在，比較容易接受

以數據調整團隊的認知，未來的討論也會較能接軌現實
{{% /fragment %}}

{{% note %}}
不能怪他們吃米不知米價，要讓團隊輕易看到米價，才會開始在意米價
{{% /note %}}

---

##### Step 0: 釐清需求

提升團隊 Coding Agent 效率

但是 Coding Agent 效率到底是什麼？

{{< math >}}
\text{整體效率 Efficiency} = \frac{\text{產出數量} \times \text{產出品質}}{\text{Token Cost} \times \text{花費時間}}
{{< /math >}}

{{% fragment %}}
降低 Cost，Latency，Error Rate
控制 Context Window
提升 Output Quality
{{% /fragment %}}

---

##### Step 0: 需求 -> Action

- 不同任務選用 Model
  - Mini, Nano, Low Latency, Low Error Rate
  - AI Gateway Routing [LiteLLM](https://docs.litellm.ai/docs/routing)，
- Context Management -> [rtk](https://github.com/rtk-ai/rtk) 
- 加速 Greenfield 專案開發 -> [Spec-kit](https://github.com/github/spec-kit)

---

##### Step 0: On the same page

- Dev Team
  - Cost Chargeback
  - Model & Tool Evaluation
- Stakeholders 對齊長官的期待
  - 效能量化指標：正確率，Error Rate，Latency，Cost
  - 不是有 AI 就可以十倍產出，開除人類員工

---

##### Takeaway: 從零開始的 Decision System

- Step 1: 建立 baseline 與第一次優化
- Step 2: LLM as a Judge
- Step 3: Dataset & Experiment
- Step 0: 釐清需求
- Decision: 釐清需求 -> Take Action

---

##### Q&A

- 早上 Lab [LLM O11y：從 Observability 到 Decision System](https://chechia.net/posts/2026-07-01-ws-langfuse-ai-ent/)
- 上週 Lab [Spec-driven development with Spec-kit](https://chechia.net/posts/2026-07-01-ws-speckit-ai-ent/)
