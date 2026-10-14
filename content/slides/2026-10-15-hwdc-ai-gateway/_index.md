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

##### 現實情境

- 「一個人就把公司預算燒完」🔥
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
- 需要 AI Gateway 作為共同管理層<br>大家用得順，營運管得住

{{% note %}}
今天不推銷任何 Gateway。先把問題講清楚：團隊想使用 LLM，工程上需要哪些共同能力，才能讓大家用得順、營運也管得住？
{{% /note %}}

---

##### 今天的大綱

- ✅為何需要共同管理層
- ✅什麼是 AI Gateway
- 治理的第一步是成本
- 強化安全
- 監測穩定度
- 持續最佳化

---

{{< slide content="slides.about-me" >}}

---

##### AI Gateway 是什麼？

在 Application 與 LLM Provider 之間<br>加入一個共同管理層入口

```text
Apps → AI Gateway → LLM Providers
       ├─ Identity, Auth, Policy
       ├─ Routing, Budgets, Limits
       └─ O11y: Metrics, Logs, Traces
```

---

##### AI Gateways

- [liteLLM](https://github.com/BerriAI/litellm) 61.2⭐ 非常棒，功能完整<br>直到被供應鏈攻擊
- [Bifrost](https://github.com/maximhq/bifrost) 8.8k⭐ Enterprise 方案
- [Agentgateway](https://agentgateway.dev/) 5.3k⭐ 最完整的開源方案<br>免費, k8s Native, HA, 支持其他開源整合

我沒收錢所以大家自己選

---

screenshot

---

##### 成本控管

- 身為營利公司，不考慮盈利是不負責任的
- 身為開發團隊，不做預算與成本，就導入新工具，是不負責任的
  - 「xxx 公司一個人燒掉全公司預算」天理難容

第一個問題就是：誰能用？該花多少錢？如何避免超支？

---

##### 成本：觀測（Observability）

- 簡往知來，不要市場喊價
  - 過去紀錄需要監測
  - 未來需要預測
- 基於數據，決定預算、成本、績效
  - o11y 是必備 (non-negotiable)

---

##### 成本：觀測（Observability）

- 14:15-15:00 講AI O11y [link]
- [Agentgateway Observability](https://agentgateway.dev/docs/standalone/latest/documentation/observability/)
  - Metrics -> Prometheus-stack -> Alerting
  - Traces -> Langfuse
  - Access logs

{{ %note %}}
有來的舉個手讓我知道一下
{{ %/note %}}

---

##### 成本分攤（Chargeback）

- 用量對應價格，依團隊與服務彙總
- 記錄 Provider、Model、Input / Output Tokens
- 每次 request 帶上 `team`、`project`、`environment`
  - 整合 [OIDC Auth](https://agentgateway.dev/docs/standalone/latest/documentation/configuration/security/oidc/) 或 [JWT Auth](https://agentgateway.dev/docs/standalone/latest/documentation/configuration/security/jwt-authn/)

---

##### 安全性

- API Key 存在 Gateway 保護（ex vault or secret manager）
- Gateway 提供 [OIDC Auth](https://agentgateway.dev/docs/standalone/latest/documentation/configuration/security/oidc/) 或 [JWT Auth](https://agentgateway.dev/docs/standalone/latest/documentation/configuration/security/jwt-authn/)
  - 使用者 Google 登入，取得短效期 token
  - 使用者不存取 Provider API key
- Gateway 定期 rotate API Key

---

##### 穩定度：觀測（Observability）

- 即時主動監測
  - 如果 llm 是對客戶，等到客戶抱怨才知道
  - 等 provider status page 都是落後指標
- [Provider Load Balancing](https://agentgateway.dev/docs/kubernetes/latest/documentation/llm/load-balancing/)
  - 主動 health check
  - health check 不過，主動切換備援 model

---

##### 最佳化

觀測取得 Metrics, Traces, Audit Log

- Metrics
  - 哪個 model / provider 最快、穩定、便宜
  - 哪個 model 一直噴 error
- Traces 送到分析平台 ex langfuse
  - 跑 Experiment/Evaluation，針對產出內容做測試
  - 那個 model 慢，但產出品質好
- 決定 model 各自適合的任務

> 不會有一個超級 model 適合所有任務，且需求成長比 model 快

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

##### Gateway 做不到所有事

- 不能保證 Model 回答正確
- 不能替代 Application 的 Evaluation
- 不能自動決定資料是否可送到外部
- 不能把不同 Provider 的 API 差異變不見
- 不能取代 Provider 帳單與合約檢查

Observability 不是 Decision System

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
