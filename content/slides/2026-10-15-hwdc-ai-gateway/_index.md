---
title: "AI Gateway：AI 治理的第一步"
description: "從團隊使用 LLM 的實際需求出發，整理模型存取、成本、路由、觀測、稽核與內容安全的管理邊界。"
tags: ["ai", "llm", "ai-gateway", "governance", "observability"]
categories: ["aiops", "observability"]
date: '2026-08-15T00:00:00Z'
outputs: ["Reveal"]
reveal_hugo:
  custom_theme: "reveal-hugo/themes/larger-font.css"
  margin: 0.2
  highlight_theme: "color-brewer"
  transition: "slide"
  transition_speed: "fast"
---

##### AI Gateway：AI 治理的第一步
##### 想用 LLM，就要先管理它

Che-Chia Chang

---

##### 同事問

- 我要 OpenAI，Anthropic，Gemini, <br>Kimi，cohere, ... <br>最新最強的 Model
- 如何存取控管？SSO，API Key，Security Filter
- 我還有多少額度？用完就下班了？
- Provider 壞了、變慢了

---

##### 主管問

- 哪個專案花了多少？
- 預算如何訂？是否會超支
- 導入 llm 後績效呈現

---

##### Anti-patterns：今天的狀況

- 「一個人就把公司預算燒完」
- 每個人手上都有 Api Key💀
- API 出問題，才問「是不是模型壞了」
- 成本只到 Provider 帳單總額
- 預算與績效用市場喊價

{{% note %}}
問題是原本由每個產品團隊重複處理的營運責任，沒有一致的控制點。
{{% /note %}}

---

##### 持續營運

- 開發團隊需要好用的入口
  - 簡單，安全，穩定
- 管理團隊需要查看使用情況
  - 成本、風險評估
  - 改進方向

> 需要 AI Gateway 作為共同管理層，大家用得順，營運管得住

{{% note %}}
今天不推銷任何 Gateway。先把問題講清楚：團隊想使用 LLM，工程上需要哪些共同能力，才能讓大家用得順、營運也管得住？
{{% /note %}}

---

##### 今天的大綱

- ✅為何需要共同管理層
- ?

---

{{< slide content="slides.about-me" >}}

---

##### 需求一：成本分攤（Chargeback）

- 每次 request 帶上 `team`、`project`、`environment`
- 記錄 Provider、Model、Input / Output Tokens
- 用量對應價格，依團隊與服務彙總
- 月底對帳，而不是猜誰用最多

{{% note %}}
沒有 consumer identity，就無法公平分攤。共享一把 API Key 只能看到一個大水桶，之後再怎麼畫圖也分不出各團隊的成本。
{{% /note %}}

---

##### 情境：每個 Team 都開始用 LLM

```text
客服摘要   → Model A
文件搜尋   → Embedding Model B
Coding Agent → Model C
內部助理   → Provider D
```

- 用量和權限沒有共通規則
- 每個人都要理解 Provider API
- 平台團隊無法回答整體使用狀況

---

##### 現在每個 Application 都自己處理

```text
App A ── Key A ── Provider A
App B ── Key B ── Provider B
App C ── Key C ── Provider C
```

- 認證、重試、路由、計費重複實作
- 每次 Provider API 變動都要逐一追
- 故障時沒有共同的觀測面

---

##### AI Gateway 是什麼？

在 Application 與 LLM Provider 之間<br>加入一個可管理的共同入口

```text
Applications → AI Gateway → LLM Providers
                   ├─ Identity / Policy
                   ├─ Routing / Limits
                   └─ Metrics / Logs / Traces
```

統一入口不是統一所有 Provider 的能力

---

##### Gateway 的目標不是「多一層 Proxy」

- 對工程師：少理解 Provider 差異，快速開始
- 對平台團隊：集中管理身份與政策
- 對維運團隊：看見用量、效能與失敗
- 對管理者：成本能歸屬，預算能控管

{{% note %}}
如果只是把流量轉發出去，團隊會多一個故障點，卻沒有解決治理問題。Gateway 的價值要回到這四種使用者的需求。
{{% /note %}}

---

##### 工程師需要簡單、穩定的呼叫方式

- 一組 SDK 或相容的 API
- 一個團隊管理的 Endpoint
- 使用邏輯 Model Alias，而非硬編 Provider Key
- 共用 timeout、錯誤處理與 retry 規則

```text
app → company-llm / fast-chat → Gateway
```

---

##### 把 Provider 差異收斂在邊界

應用程式指定需求：

- `fast-chat`：低延遲、一般問答
- `reasoning`：複雜分析
- `embedding`：向量化

Gateway 再對應實際 Provider 與 Model

{{% note %}}
Alias 不應該隱藏所有差異。Streaming、tool calling、JSON mode、context window、embedding 維度仍可能不同；要有明確的能力與相容性測試。
{{% /note %}}

---

##### Identity：知道誰在使用

- 使用者、Application、Team 都要能辨識
- API Key 存在 Gateway 或 Secret Manager
- 服務用自己的身份，不共用萬用 Key
- 依身份套用 Model、Provider、資料政策

```text
App → Virtual Key / Workload Identity → Policy
```


---

##### 超支保護：預算不是報表

- 為 Team、Project、Key 設定 Budget
- 設定 Token / Request Rate Limits
- 接近門檻：通知負責人
- 超過門檻：拒絕、降級或改走核准流程

要先定義：誰能突破限制？

---

##### 預算控制要處理延遲與進行中的請求

- Provider 用量與帳單可能延遲回報
- 長回應開始前，最終成本還不知道
- 多個並行請求可能同時消耗額度
- 設軟門檻、硬門檻與保留額度

沒有任何 Budget 可以取代帳單對帳

---

##### 智慧路由：依需求選路

- Capability：支援工具呼叫或長 Context
- Latency：互動請求優先選低延遲
- Cost：簡單工作先用較低成本 Model
- Availability：避開不健康的 Provider
- Policy：資料區域與允許清單優先

不是所有 Request 都要跑最貴的 Model

---

##### 備援切換不等於盲目切換

- 遇到 timeout、429、5xx，評估是否重試
- 符合條件時，切到同等能力的備援
- 保留 request id 與路由決策紀錄
- 超過重試預算就快速失敗

權限、資料邊界與 Model 能力不能被 Fallback 繞過

---

##### LLM 需要新的效能指標

- Request：成功率、錯誤類型、Retry 次數
- Latency：首 Token 時間、完整回應時間
- Throughput：Tokens / sec、並行請求數
- Usage：Input / Output Tokens、Cache Tokens
- Cost：每次、每個 Team、每種任務的成本

只看 HTTP 200，不代表回答有用

---

##### 監測與告警

- Provider Error Rate 突升
- p95 Latency 或 Time to First Token 劣化
- Budget 使用率接近上限
- Token 用量異常成長
- Fallback、429、Timeout 過多

告警要能連到值班人與處置方式

---

##### 追蹤（Trace）：一個回答怎麼產生？

```text
Request → Policy → Route → Provider → Response
             │        │          │
           Team     Model     Tokens / Latency
```

- 保留 Request ID 與路由結果
- 串接 Application Trace 與 Provider Call
- 依需要記錄內容，不是預設保存所有 Prompt

---

##### 稽核（Audit）：誰在什麼時候改了什麼？

- Key 建立、撤銷與權限異動
- Routing、Budget、Guardrail 政策變更
- 誰核准了例外？何時生效？
- Request metadata 能否追到呼叫者？

Access Log ≠ Audit Log

---

##### 內容安全防護：要有明確位置

- Input：敏感資料、惡意指令、違規內容
- Output：個資、機密、危險或不允許的內容
- 可選擇規則、分類器或 Provider Guardrail
- 記錄命中原因與處置結果

Filter 會誤判；要有例外流程與人工檢視

---

##### 一個 Request 的管理流程

```text
Identity → Policy → Budget Check → Route
         → Provider Call → Filter → Response
         → Metrics / Trace / Audit
```

每個階段都有明確的允許、拒絕或降級結果

{{% note %}}
用一個例子走過整條路徑：一個客服摘要服務帶自己的身份呼叫 `fast-chat`，先檢查資料政策與預算，再路由到健康的 Provider。回應經過輸出檢查，最後記錄用量、延遲、路由與決策。
{{% /note %}}

---

##### 讓開發團隊容易開始

1. 申請 Application Identity
2. 選一個允許的 Model Alias
3. 使用共用 SDK / Endpoint
4. 本地測試，部署後檢查 Dashboard

開發者不必每次申請 Provider API Key

---

##### 實務情境：流量如何被治理？

- `team=search` 呼叫 `fast-chat`
- 預設 Model 降價，但仍符合品質需求
- Provider timeout，切換合格的備援
- 月度預算到門檻，通知負責人
- Prompt 不進一般 Log，保留必要 Metadata

這是政策流程，不是特定產品操作教學

---

##### Gateway 做不到所有事

- 不能保證 Model 回答正確
- 不能替代 Application 的 Evaluation
- 不能自動決定資料是否可送到外部
- 不能把不同 Provider 的 API 差異變不見
- 不能取代 Provider 帳單與合約檢查

Observability 不是 Decision System

---

##### 導入時要一起想的事

- Gateway 自己也要有 HA、容量與升級策略
- Gateway 掛了，Application 怎麼處理？
- Prompt / Output 的保存與遮罩政策
- Streaming、Tool Call、Batch 的相容性
- 用量、價格與 Provider 帳單如何對帳

先管理最重要的流量，再擴大範圍

---

##### 參考能力，不是產品推薦

- [Agentgateway Standalone Docs](https://agentgateway.dev/docs/standalone/latest/)
  - Routing、rate limits、cost controls、guardrails、metrics / traces
- [Bifrost Overview](https://docs.getbifrost.ai/overview)
  - Virtual Keys、routing / failover、budget、rate limits、metrics、guardrails

設計需求先於選型

---

##### 重點｜把「想用 LLM」變成可管理的服務

- 給工程師：一個入口、清楚的 Model 介面
- 給平台：Identity、Policy、Routing
- 給財務與 Team：Chargeback、Budget、Alerting
- 給維運：Metrics、Trace、Audit
- 給使用者：內容安全與明確的失敗行為

從最痛的問題開始，逐步建立共同管理層

---

##### Q&A

我們想用 LLM<br>接下來要先管理什麼？
