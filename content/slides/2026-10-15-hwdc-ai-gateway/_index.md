---
title: "AI Gateway：AI 治理的第一步"
description: "從團隊使用 LLM 的實際需求出發，整理模型存取、成本、路由、觀測、稽核與內容安全的管理邊界。"
tags: ["ai", "llm", "ai-gateway", "governance", "observability"]
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

##### AI Gateway：AI 治理的第一步

Che-Chia Chang

---

##### 同事問

- 我要最新最強的 Model
  <br>OpenAI Anthropic Gemini Cohere Jev ...
- API Key 如何管理？可以 SSO 嗎？
- 我還有多少額度？用完就下班了？
- xx Model 是不是壞了、變超慢

---

##### 主管問

- 哪個專案花了多少？
- 預算如何訂？是否會<span style="color: #1d4ed8;">超支</span>
- 安全嗎？會不會被攻擊
- 有存取紀錄與稽核軌跡嗎？
- 導入 LLM 後，長官要的<span style="color: #1d4ed8;">績效呈現</span>

---

##### 現實情境

- 「<span style="color: #1d4ed8;">一個人就把公司預算燒完</span>」💸💸💸
- 每個人手上都有 API Key💀
- API 出問題，才問「是不是模型壞了」
- 成本只到 Provider 帳單總額
- 預算與績效用市場喊價

{{% note %}}
問題是原本由每個產品團隊重複處理的營運責任，沒有一致的控制點
{{% /note %}}

---

{{< slide background-image="02-chaos.jpeg" background-size="100%" background-color="#000000" background-opacity="1" >}}

---

##### AI Gateway：<br>團隊治理 LLM 的共同入口

- 開發團隊需要好用的入口
  <br><span style="color: #1d4ed8;">簡單，安全，穩定</span>
- 管理團隊需要查看使用情況
  <br>成本、風險評估
  <br>績效、<span style="color: #1d4ed8;">持續改進方向</span>
- 多團隊、多 Provider 時<br>可用 AI Gateway 建立<span style="color: #1d4ed8;">共同管理層</span>

{{% note %}}
今天不推銷任何 Gateway。先把問題講清楚：團隊想使用 LLM，工程上需要哪些共同能力，才能讓大家用得順、營運也管得住？
{{% /note %}}

---

##### 今天的大綱

- ✅為何需要共同管理層
- 什麼是 AI Gateway
- 治理的第一步是成本
- 強化安全
- 監測穩定度
- 持續最佳化

---

{{< slide content="slides.about-me" >}}

---

##### 什麼是 AI Gateway

在 Application 與 LLM Provider 之間<br>加入一個共同管理層入口

---

{{< slide background-image="https://agentgateway.dev/img/architecture.svg" background-size="100%" background-color="#000000" background-opacity="1" >}}

<small style="position:fixed; bottom:0; background:#000; color:#fff;">Agentgateway 架構範例 · agentgateway.dev</small>

{{% note %}}
這是 Agentgateway 的架構範例，不是所有 AI Gateway 的標準架構
來源：https://agentgateway.dev/
{{% /note %}}

---

<pre style="width:100%; max-height:none; margin:0.25em auto; font-size:0.72em;"><code class="language-text" style="max-height:none; line-height:1.15;">
Apps / Agents
    │ request
    ▼
AI Gateway: AuthN/AuthZ → Policy → Budget / Rate Limit
             → Model Selection → Route / Load Balance / Failover
             ├─ Request Filter
             └─ Metrics / Logs / Traces / Audit
    │ routed request
    ▼
LLM Providers
    │ model response
    ▼
AI Gateway: Response Filter
    │ response
    ▼
Apps / Agents
</code></pre>

---

##### AI Gateways

- [LiteLLM](https://github.com/BerriAI/litellm) 61.2k⭐ 非常棒，功能完整<br>直到被供應鏈攻擊💀
- [Bifrost](https://github.com/maximhq/bifrost) 8.8k⭐ Enterprise 方案
- [Agentgateway](https://agentgateway.dev/) 5.3k⭐ 最完整的開源方案<br>免費，K8s Native，HA<br>支持其他開源整合<br>架構較複雜😅

---

{{< slide background-image="01-litellm.png" background-size="100%" background-color="#000000" background-opacity="1" >}}

---

- ✅為什麼是 AI Gateway
- <span style="color: #1d4ed8;">治理的第一步是成本</span>💰
- 強化安全
- 監測穩定度
- 持續最佳化

---

##### 成本控管

- 營利公司必須考慮盈利
- 導入新工具，也要約定<span style="color: #1d4ed8;">預算與責任</span>
- 開發團隊：預估用量、設定上限
- 管理團隊：核定預算、處理超支
- 告警不是上限，還需要執行預算政策

誰能用？該花多少錢？避免超支

---

##### 成本：預算來自觀測（Observability）

- 鑑往知來，基於過去設定預算，不市場喊價
- <span style="color: #1d4ed8;">基於數據</span>，決定預算、成本、績效
- [Agentgateway Observability](https://agentgateway.dev/docs/standalone/latest/documentation/observability/)
- Metrics：Model, In/Out Tokens
- 用量 × 對應價格 → 成本估算
- Cache、折扣計費
- Traces: span, latency, route
- Access Logs：存取紀錄、稽核軌跡、<br>稽常告警

---

##### 成本：觀測是必備（Observability）

- [Agentgateway Observability](https://agentgateway.dev/docs/standalone/latest/documentation/observability/)
- Metrics > Prometheus > Alerting
- Traces > Langfuse
- Access logs > Security / Audit

<span style="color: #1d4ed8;">沒有 o11y 就沒有成本控管，告警，與資安</span>

---

##### 成本 Showback & Chargeback

- 用量對應價格，依團隊與服務彙總
- 由可信 Claims (Google OAuth2) 驗證身份
- 取得 Org, Unit, Team, Project, Env
- 存取 Gateway 時紀錄用量
- [OIDC Auth](https://agentgateway.dev/docs/standalone/latest/documentation/configuration/security/oidc/) / [JWT Auth](https://agentgateway.dev/docs/standalone/latest/documentation/configuration/security/jwt-authn/) 是身份入口
- 各部門團隊取得成本，進行成本分攤

<span style="color: #1d4ed8;">對齊團隊對成本的概念</span>

{{% note %}}
成本：Request 的管理流程

Identity → Policy → Budget Check → Route
         → Provider Call → Filter → Response
         → Metrics / Trace / Audit

每個階段都有明確的允許、拒絕或降級結果

用一個例子走過整條路徑：一個客服摘要服務帶自己的身份呼叫 `fast-chat`，先檢查資料政策與預算，再路由到健康的 Provider。回應經過輸出檢查，最後記錄用量、延遲、路由與決策。
{{% /note %}}

---

##### 節省成本：Semantic Routing

- 依任務動態選 Model
  - Routine → 小型、低成本 Model
  - 複雜推理 → 能力較強的 Model
- 對比全部使用高成本 Model
  - 同一組 Dataset，比成本與 Latency
  - 跑 Evaluation，確認品質沒掉
- 路由選對，不代表回答就對
- [案例與實驗方法](https://agentgateway.dev/blog/2026-07-17-semantic-routing-llm-costs/)

---

{{< slide background-image="https://agentgateway.dev/img/blog/cost-based-semantic-routing/semantic-routing-flow.svg" background-size="100%" background-color="#000000" background-opacity="1" >}}

---

##### 安全性：Provider Auth

- Provider API Key 集中管理
  - Vault / Secret Manager 儲存與派發
  - KMS 提供加密能力
- Client 不持有 Provider API Key
- 由 Provider 與 Secret 管理流程 Rotate
  - Gateway 更新憑證，配合撤銷舊 Key

在 AI Gateway 做 Security Hardening

---

{{< slide background-image="https://agentgateway.dev/img/blog/cb4a/cb4a-part2.gif" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

{{< slide background-image="https://agentgateway.dev/img/blog/cb4a/section01.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

##### 安全性：Client AuthN / AuthZ

- [OIDC Auth](https://agentgateway.dev/docs/standalone/latest/documentation/configuration/security/oidc/)：登入與身份整合
- [JWT Auth](https://agentgateway.dev/docs/standalone/latest/documentation/configuration/security/jwt-authn/)：驗證 JWT 格式的 Token
- 驗證簽章、Issuer、Audience 與有效期
- 再依身份與 Claims 執行存取政策

---

{{< slide background-image="https://developers.google.com/static/identity/protocols/oauth2/images/flows/authorization-code.png" background-size="40%" background-color="#000000" background-opacity="1" >}}

{{% note %}}
Access Token 不一定是 JWT，不應假設可以用 Google 公鑰驗證。登入整合與 API 授權是不同責任；依 Gateway 與 IdP 的支援方式設定 Token 類型、Issuer、Audience 與授權政策
{{% /note %}}

---

##### 穩定度：觀測（Observability）

- 如果 LLM 是對客戶（B2C）<br>不能等到客戶抱怨才知道
- Provider Status Page 可能延遲
- 根據 LLM provider 會有地區性問題
- 一定要<span style="color: #1d4ed8;">主動監測</span>並測量 metrics
  - Latency p50, p90, p99
  - Error Rate

---

{{< slide background-image="../2026-08-08-coscup-llm-o11y/05-claude-status.png" background-size="100%" background-color="#000000" background-opacity="1" >}}

---

##### 穩定度：主動監測與自動告警

- [Prometheus-compatible Metrics](https://agentgateway.dev/docs/standalone/latest/documentation/observability/metrics/overview/)
- Prometheus Stack: Prometheus + Alertmanager + Grafana
- 過去一季 xx Model / Provider 可用性高或偏低
- 透過 Dashboard 數據，<span style="color: #1d4ed8;">整合團隊共識</span>
- 基於數據不靠體感「我覺得 xx Model 很好用」
- 團隊可以選擇更適合的 Model

---

##### 穩定度：Retry / Failover

- [Load Balancing](https://agentgateway.dev/docs/kubernetes/latest/documentation/llm/load-balancing/)：分流到可用 Backend
- [Failover](https://agentgateway.dev/docs/kubernetes/latest/documentation/llm/failover/)：依失敗條件切換備援
- 可換 Provider，也可換 Model
- Retry：限制次數 Timeout 與 Backoff
- 429 依 Retry-After 與策略處理
- 使用者不會感受到 429 與 5xx
  - 已輸出串流、執行 Tool 的請求需另處理

{{% note %}}
下一頁圖示是依回應錯誤暫時移除 Backend，同組全數不可用時切換下一優先群組，不等同於主動 Health Check。重試可能重複計費或執行副作用，需要應用端的冪等性與串流恢復策略
{{% /note %}}

---

{{< slide background-image="03-model-failover.png" background-size="90%" background-color="#000000" background-opacity="1" >}}

---

##### 最佳化 Metrics

- 觀測取得 Metrics、Traces 與 Audit Log
- Metrics：哪個 Model / Provider<br>
  最快、穩定、便宜<br>
  哪個 Model 一直噴 Error
- Metrics 看速度與成本
- 回答品質要用 Dataset 與 Evaluation

---

##### 最佳化 Traces

- Traces 送到分析平台 ex langfuse
  - 整理 Dataset
  - 跑 <span style="color: #1d4ed8;">Experiment / Evaluation 針對產出內容做測試</span>
  - 哪個 Model 產出品質好
- 不會有一個超級 Model適合所有任務
  - 需求成長比 Model 快

---

##### LLM O11y 與最佳化

[AI Observability 投影片](../2026-10-15-hwdc-ai-o11y/)

從 Trace、Dataset 到 Evaluation<br>觀測到問題，再用實驗確認改動

---

##### 要不要用 AI Gateway？

<table style="width:100%; max-width:none; table-layout:fixed; font-size:0.58em; line-height:1.2;">
<colgroup><col style="width:17%;"><col style="width:41.5%;"><col style="width:41.5%;"></colgroup>
<thead><tr><th>面向</th><th>使用 AI Gateway</th><th>不使用 Gateway</th></tr></thead>
<tbody>
<tr><td>基礎設施</td><td>需部署或託管、監控、升級與 HA</td><td>少一層服務，不需 Gateway 算力</td></tr>
<tr><td>身份與治理</td><td>集中 Auth、Policy、Budget、Audit</td><td>靠 Provider 原生功能，或各 App 自行實作</td></tr>
<tr><td>路由與穩定</td><td>統一 Route、Retry、Failover（依產品能力）</td><td>用各家機制；跨 Provider 切換由 App 處理</td></tr>
<tr><td>客製化與相依</td><td>受 Gateway 支援的 API / Policy 限制</td><td>可用 Provider 完整功能；整合與移轉要改 App</td></tr>
<tr><td>使用體驗</td><td>單一 API / Portal、權限與用量一致</td><td>各 Provider 帳號、Console、Key 與流程分散</td></tr>
<tr><td>整體成本</td><td>多一份維運成本，換取用量可視與政策控管</td><td>少 Gateway 成本；整合、人工作業與超支風險仍在</td></tr>
</tbody>
</table>

多團隊、多 Provider 值得多維運一層
{{% note %}}
單一團隊、單一 Provider：直接串接可能更簡單
{{% /note %}}

---

##### Takeaways

- 多團隊、Providers 時務必 AI Gateway
- <span style="color: #1d4ed8;">O11y is a MUST</span>
- ChargeBack 讓團隊對成本有<span style="color: #1d4ed8;">共識</span>
- Metrics 讓長官對績效有共識
- 不妥協的安全性
- AI Gateway 提供共同管理入口

---

##### Q&A
