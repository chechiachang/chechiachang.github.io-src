---
title: "AI O11y：數據決策到技術選型"
description: "從 Langfuse Observability 與 Coding Agent 的實務案例出發，建立 evaluation、dataset、regression 與 decision gate"
tags: ["llm", "agent", "observability", "evaluation", "aiops", "devops"]
categories: ["aiops", "observability"]
date: '2026-08-15T00:00:00Z'
outputs: ["Reveal"]
reveal_hugo:
  slide_number: true
  custom_theme: "reveal-hugo/themes/larger-font.css"
  margin: 0.2
  highlight_theme: "color-brewer"
  transition: "slide"
  transition_speed: "fast"
---

##### AI O11y：數據決策到技術選型
##### Observability → Decision System

Che-Chia Chang

---

##### 同事在問

- Spec-kit SDD 好用，要不要試？
- rtk 省 Token，要不要導入？
- 新模型 Benchmark 更好，要不要換？

身為技術負責人，如何回答？

---

##### 面對 AI 工具快速迭代

- 全部試用
- 參考專家與供應商分享
- 採用代理商或雲端商推薦

試用是一種選擇；團隊更需要<span style="color: #1d4ed8;">數據化決策</span>

---

##### 新工具出現速度 > 研究速度

{{% fragment %}}
缺的不是更快研究，而是<span style="color: #1d4ed8;">量化評估系統</span>
{{% /fragment %}}

{{% fragment %}}
信任既有 Stack、免 FOMO、驗證改動成效
{{% /fragment %}}

---

##### Coding Agent 會動就好？
##### 為何需要 O11y / Evaluation？

---

- 建立效能 Baseline
- <span style="color: #1d4ed8;">劣化時告警</span>並追查原因
  - 例如上游 API 不穩
- Claude API Uptime 僅 99.4%
- 沒有 O11y，就沒有 SLA

{{% note %}}

至少要知道他什麼時候是壞的

進行處置：切換 model 或 provider

至少要知道服務劣化

{{% /note %}}

---

{{< slide background-image="05-claude-status.png" background-size="100%" background-color="#000000" background-opacity="1" >}}

---

##### Change Management

- 改變後，效能變好還是變差？
- [Spec-kit](https://github.com/github/spec-kit)：SDD 聽說好用
- [rtk](https://github.com/rtk-ai/rtk)：聽說省 Token
- [Opus 4.8](https://www.anthropic.com/claude/opus)：聽說很強
- <span style="color: #1d4ed8;">改變有成本</span>，也可能讓效能劣化

用數據決策，避免 FOMO

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

##### Cost Management

- 依本月用量，收斂下月預算
- <span style="color: #1d4ed8;">Chargeback</span>：讓團隊看見成本
- 分清哪些問題能用錢解決
- 需求演進比模型快
- <span style="color: #1d4ed8;">沒有單一模型能解決所有問題</span>
- 用合適預算與模型
- 有效率地解決能解的問題

---

##### 為何需要 Observability

- 建立 Baseline
- 管理改變（Change）
- 管理成本（Cost）

---

{{< slide content="slides.about-me" >}}

---

##### 今天的內容

- ✅ Change & Cost Management
- 建立 Baseline、完成第一次優化
- LLM-as-a-Judge
- Dataset & Experiment
- 釐清 Coding Agent 效能需求
- Decision System

---

##### 從 Observability 開始

- 用 Gateway / O11y Tool 收集 Tracing
- 建立流程：LLM O11y → Judge
- Dataset → Experiment
- [LLM O11y Workshop](../../slides/2026-07-01-ws-langfuse-ai-ent)
- [Observability → Decision System](https://chechia.net/posts/2026-07-01-ws-langfuse-ai-ent/)
- Agent 怎麼花 Token？
- 如何系統化評估輸出品質？

---

{{< slide background-image="00-langfuse-tracing.png" background-size="100%" background-color="#000000" background-opacity="1" >}}

---

##### 導入 Gateway / O11y Tool

- 看見 Observability Stack
- 量化 Token Usage、Latency、Error Rate
- <span style="color: #1d4ed8;">Chargeback</span>：讓團隊看見自己的成本
- 用監測數據控管預算，不只看市場喊價

- 建立 Cost / Token Usage Baseline
- 定義預算界線

---

##### Step 1｜Baseline 與第一次優化

- 先理解 CLI 行為
  - Copilot、Codex、OpenCode 各不同
- 停用不必要的 Tools
  - Copilot 內建 50+ 個 Tools
  - 實務上只用 10+ 個
  - VSCode Extension 也可能增加 Tools
- 透過 <span style="color: #1d4ed8;">AI Gateway</span> 增加控制點

控制你的 Coding Agent

---

{{< slide background-image="01-cli-baseline.png" background-size="100%" background-color="#000000" background-opacity="1" >}}

{{% note %}}
- User: "hi"
- Agent: "Hi! How can I help you today?"

- 這個簡單的互動就用了 20,000+ Input Tokens
- 成本約 0.1 USD（3 TWD；$5.00/1M Tokens）
{{% /note %}}

---

##### Step 1｜第一次優化成果

- Token Overhead：20,000+ → 1,000+
- 成本：$0.10 → $0.005（降至約 5%）
- 降低進入 Long Context 的機率
  - ≥272K Tokens 價格翻倍
- <span style="color: #1d4ed8;">把 Context Window 留給真正有用的內容</span>

[OpenAI API Pricing](https://developers.openai.com/api/docs/pricing)

{{% note %}}
Input Token Cache 只是折扣，不是免費；它可以改善 Model 在 Long Context 下的效能，
但不該因此被拿來浪費
{{% /note %}}

---

##### Step 2｜LLM-as-a-Judge

- 依 Tracing Metadata 優化成本
- 依 Input / Output 優化品質
- LLM 評估輸出品質
- 傳統測試難涵蓋多變情境

---

{{< slide background-image="02-llm-as-a-judge.png" background-size="100%" background-color="#000000" background-opacity="1" >}}

{{% note %}}
使用 Langfuse 收集 Tracing 資料，
先把 Input/Output 的品質量化，
再使用內建的 Evaluator Library，或自行撰寫 Prompt 評估品質
{{% /note %}}

---

##### Step 2｜Observation 評估

- 評估每次 API Call
- 看 Input、Output 與 Metadata
- 小範圍量化，觀察局部品質
- 不代表 Project 整體品質
- 從局部分析錯誤類型，<span style="color: #1d4ed8;">找出改進方向</span>

---

##### Step 2｜根據評估結果優化

- 依 LLM-as-a-Judge 結果持續調整
- 控制變因：
  - Token Usage、Latency、Cost
  - Model Version
- 調整 Prompt / Instruction
- 改善 Input / Output 品質

控制變因、調整變因，<span style="color: #1d4ed8;">提升局部評分</span>

---

##### Step 2｜Multi-turn Agent

Long-running Agent 不能只看最終答案：

```text
Input: 更新 README.md
讀取 → Plan → Apply Patch → 完成
Output: README.md 修改成功
```

改評估單一步驟<br>
例如 Plan 或 Apply Patch

---

{{< slide background-image="03-multi-turn-agent.png" background-size="100%" background-color="#000000" background-opacity="1" >}}

---

##### Step 3｜Dataset & Experiment

**Dataset**｜真實工作考題<br>
從 Daily Work Tracing 整理

```text
Input：真實工作需求
Output：Model 的回答
Judge Score：回答品質
```

**Experiment**｜同一份考題<br>
控制變因，重複執行

```text
Model：5.4 → 5.5
Tools / Instruction：改動前後
```

---

{{< slide background-image="04-dataset-experiment.png" background-size="100%" background-color="#000000" background-opacity="1" >}}

{{% note %}}
這是使用 Spec-kit 產生的 YouBike API app
{{% /note %}}

---

##### Step 3｜整理 Dataset

- Plan：Context Precision
- Coding：Answer Correctness
- 依 Judge 分數分類
- 高品質案例作為改進參考

注意：從 O11y 走進<span style="color: #1d4ed8;">Dataset，是個大坑</span>

---

##### Step 3｜Data Preprocessing

- 清理 Tracing 格式，挑選所需 Features
- 例如 `Output.tool_calls.args`
- 記錄呼叫哪些 Tools、帶哪些參數
- 用 Langfuse SDK 轉換格式
- Partition Dataset

持久化儲存，作為<span style="color: #1d4ed8;">測試題庫</span>

---

##### Step 3｜第三次優化：選擇最佳工具

- 用題庫測試不同選項：
  - Model：Pro、Mini、Nano
  - Model 版本：GPT-5.4、GPT-5.5
  - Thinking Effort
  - Agent：Codex、OpenCode、Copilot
- 不必等 Model 變強才解決問題
- <span style="color: #1d4ed8;">選適合的工具，平衡品質與成本</span>

---

##### Step 3｜Evaluation → Cost Estimate

- 測試題數與使用的 Model
- LLM API Metrics、Token 用量
- Quality Estimate

沒有<span style="color: #1d4ed8;">測試基礎</span>的預算，只是市場喊價

---

##### Step 0｜先釐清需求

需求應該先釐清

許多團隊卻先討論要不要換工具：
- 需求還不清楚
- 成員對 LLM 的<span style="color: #1d4ed8;">理解有落差</span>

{{% fragment %}}
先建立監測，讓團隊看見數據
{{% /fragment %}}

{{% fragment %}}
用數據調整認知，讓討論回到現實
{{% /fragment %}}

{{% note %}}
不能怪團隊不理解成本；要先讓大家容易看見成本，才會開始在意成本
{{% /note %}}

---

##### Step 0｜Coding Agent 效率

想提升團隊效率，先定義「效率」：

{{< math >}}
\text{Overall Efficiency} = \frac{\text{產出數量} \times \text{產出品質}}{\text{Token Cost} \times \text{花費時間}}
{{< /math >}}

{{% fragment %}}
降低 Cost、Latency、Error Rate<br>
控制 Context Window<br>
提升 Output Quality
{{% /fragment %}}

---

##### Step 0｜從需求走向 Action

依任務選工具：

- Model：
  - Mini、Nano
  - Low Latency、Low Error Rate
- Gateway Routing：
  - [AgentGateway](https://agentgateway.dev/)
  - [LiteLLM](https://docs.litellm.ai/docs/routing)
- Context Management：[rtk](https://github.com/rtk-ai/rtk)
- Greenfield：[Spec-kit](https://github.com/github/spec-kit)

---

##### Step 0｜讓團隊 On the Same Page

- Dev Team：<span style="color: #1d4ed8;">Chargeback</span>
- 選擇 Model 與 Tool
- 與 Stakeholders、管理者<span style="color: #1d4ed8;">對齊期待</span>
- 量化效能指標：
  - 正確率、Error Rate
  - Latency、Cost
- 有 AI，不代表產出就能提升十倍

有 Evaluation 後，可以說：

> 產出約提升 2–3 倍，<span style="color: #1d4ed8;">數據在此</span>

---

##### Takeaway｜從觀察到決策系統

- Step 1：Baseline、第一次優化
- Step 2：LLM-as-a-Judge 評估
- Step 3：Dataset、Experiment
- Step 0：先釐清需求
- Decision：釐清需求 → Action

---

##### Q&A

- Lab｜[LLM O11y Decision System](https://chechia.net/posts/2026-07-01-ws-langfuse-ai-ent/)
- Lab｜[Spec-kit SDD](https://chechia.net/posts/2026-07-01-ws-speckit-ai-ent/)
