---
title: "Workshop: LLM O11y 從 Observability 到 Decision System"
description: "90 分鐘 hands-on workshop，從 Langfuse observability 到 evaluation、dataset、regression 與 decision gate。"
tags: ["llm", "langfuse", "observability", "evaluation", "workshop", "aiops"]
categories: ["aiops", "workshop"]
date: '2026-05-02T13:30:00Z'
outputs: ["Reveal"]
reveal_hugo:
  custom_theme: "reveal-hugo/themes/robot-lung.css"
  margin: 0.2
  highlight_theme: "color-brewer"
  transition: "slide"
  transition_speed: "fast"
---

{{% section %}}

### Workshop 行前準備

Workshop 以 coding agent 為例

串接 ai gateway 與 observability stack

改善 token 花費與除錯

🔽

---

### Workshop 行前準備

- 攜帶筆電，可上網
- 安裝好操作環境
  - [VS Code](https://code.visualstudio.com/)
- 下載 [workshop 範例程式碼](https://github.com/chechiachang/llm-o11y)
- 講師會提供 Azure OpenAI API Key
- 已經會用其他 agent CLI（如 codex CLI）用習慣的即可

---

### VS Code

- 安裝 VS Code：[https://code.visualstudio.com/](https://code.visualstudio.com/)
- 打開 VS Code，底下 Terminal
  - git clone 程式碼 speckit-playground
  - File > Open Folder > 選擇 clone 的 資料夾

```
git clone https://github.com/chechiachang/llm-o11y.git
```
---

{{< slide background-image="git-clone.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

### 打開 VS Code，底下 Terminal

```
cd llm-o11y
docker compose config

name: llm-o11y
services:
  bifrost:
    environment:
      AZURE_ENDPOINT: ""
      AZURE_OPENAI_API_KEY: ""
      LANGFUSE_OTEL_AUTH: Basic cGs6c2s= # fake key: pk:sk
      LANGFUSE_OTEL_INGESTION_VERSION: "4"
...

docker compose pull
[+] pull 23/23
 ✔ Image docker.io/redis:7.4.8                            Pulled                                        6.4s
 ✔ Image docker.io/clickhouse/clickhouse-server:26.2.15.4 Pulled                                        6.4s
 ✔ Image minio/minio:RELEASE.2025-09-07T16-13-09Z         Pulled                                        5.4s
 ✔ Image docker.io/postgres:17.9                          Pulled                                       26.8s
 ✔ Image maximhq/bifrost:v1.5.3-arm64                     Pulled                                        6.4s
 ✔ Image docker.io/langfuse/langfuse-worker:3.172.1       Pulled                                        5.4s
 ✔ Image docker.io/langfuse/langfuse:3.172.1              Pulled                                        5.4s
```

---

{{< slide background-image="docker-compose-config.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

{{< slide background-image="docker-compose-pull.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

### 啟動服務

```
# VS Code Terminal
docker compose up -d
```

- 透過 http://localhost:8080/ 存取 bifrost ai gateway
- 透過 http://localhost:3000/ 存取 langfuse UI
```
chechia@chechia.net / password
```
- 透過 http://localhost:9001/ 存取 minio UI
```
chechia / password
```

---

{{< slide background-image="bifrost-gateway.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

{{< slide background-image="langfuse-ui.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

{{< slide background-image="minio-ui.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

### VSCode 使用 bifrost gateway

- VS Code 右側 Secondary Sidebar > Chat
  - 底下 Model (ex Auto, GPT-5.4) > 跳出可用 Model 列表
- Model 右上角齒輪 > Manage Model Settings
  - Add Models > Azure OpenAI
  - Group Name: Bifrost
  - Azure API Key 填入 123，不能空白
  - 跳出 chatLanguageModels.json 編輯

---

{{< slide background-image="manage-model-settings.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

{{< slide background-image="chat-language-models-json.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

### 設定 Model 使用 bifrost gateway

- chatLanguageModels.json 填入: id, name, url
- cmd + s 儲存
- 回到 Model 列表，選擇剛剛新增的 Azure GPT-5.4 Nano
  - 跟 Bifrost Azure say hi，預期 bifrost 沒填 api key 不可用
  - 選回去選擇其他 Model，可以先用免費版

```
[
  {
    "name": "Bifrost",
    "vendor": "azure",
    "apiKey": "${input:chat.lm.secret.-3df80c78}",
    "models": [
      {
      	"id": "azure/gpt-5.4-nano",
      	"name": "azure/gpt-5.4-nano",
      	"url": "http://localhost:8080/v1/responses",
      	"toolCalling": true,
      	"vision": true,
      	"maxInputTokens": 272000,
      	"maxOutputTokens": 128000
      }
    ]
  }
]
```

---

{{< slide background-image="azure-openai-settings.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

{{< slide background-image="select-azure-gpt54-nano.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

### 最重要的行前準備: Mindset

- 先自己思考，再問 chatGPT
  - 大多時候chatGPT是對的，性能優於講師
- 如何確定 chatGPT 是對或錯的

> workshop 重點在累積動手的經驗

---

### Workshop 行前準備結束

- VSCode 已安裝
- VSCode 設定 model
- Docker Compose 已 pull 好 image

{{% /section %}}

---

##### LLM O11y：從 Observability 到 Decision System
##### 90 分鐘 workshop
##### ~ Che Chia Chang @ [chechia.net](https://chechia.net) ~

---

{{< slide content="slides.about-me" >}}

---

### 大綱

1. ai gateway & o11y stack
1. finops: token 算錢與省錢
1. rtk
1. 講解：Observability != Decision System
1. LAB2：為 traces 加上 evaluation
1. LAB3：從 traces 產生 dataset
1. LAB4：跑 regression 與 decision gate
1. 驗收、回顧、Q&A

---

### 把 observability stack 跑起來

到 workshop.chechia.net 取得 Azure OpenAI API Key

```
export AZURE_ENDPOINT=https://chechia-ws.services.ai.azure.com/
export AZURE_OPENAI_API_KEY=...

docker compose up -d
[+] up 7/7
 ✔ Container llm-o11y-clickhouse-1      Healthy 1.4s
 ✔ Container llm-o11y-minio-1           Healthy 1.4s
 ✔ Container llm-o11y-redis-1           Healthy 1.4s
 ✔ Container llm-o11y-bifrost-1         Started 1.0s
 ✔ Container llm-o11y-postgres-1        Healthy 1.4s
 ✔ Container llm-o11y-langfuse-web-1    Running 0.0s
 ✔ Container llm-o11y-langfuse-worker-1 Running 0.0s
```

---

##### 測試 Bifrost gateway 是否可用

- VSCode Chat > Azure GPT-5.4 Nano Model
- 跟 Bifrost say hi
- 預期 bifrost 有回應

---

##### Bifrost gateway 是什麼？

http://localhost:8080/ 到 bifrost ai gateway

- 左手工具列 Observability
- Dashboard 觀察 Token Usage，包含 Input / Output token、Cached
- LLM Logs 點一筆，看到 User Prompt、Model Response、Tools
- 點 More details，看到時間，token 數、費用估算
- [Complete Guide to O11y in Bifrost](https://www.getmaxim.ai/articles/complete-guide-to-llm-logging-otel-tracing-and-observability-in-bifrost/)

---

{{< slide background-image="bitfrost-dashboard.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

{{< slide background-image="bitfrost-trace.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

##### Bifrost gateway 是什麼？

Models - Model Providers
- 可以看到已經配置 Azure，這是現在 VSCode 使用的模型
- OpenAI 則沒有配置 API key，所以不可用

Bifrost AI Gateway 提供團隊或公司 LLM Proxy 服務
- 支援多種模型，Routing，預算設定，並及時計價
- 人員與團隊管理，配發虛擬 api key，設定團隊預算
- OTel tracing，串接 o11y 工具（如 Langfuse）

---

##### Langfuse 是什麼？

http://localhost:3000/ 到 langfuse UI
- Organizations > chachia > default project

---

{{< slide background-image="langfuse-dashboard.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

{{< slide background-image="langfuse-trace.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

##### Bifrost 跟 Langfuse 的關係？

- AI Gateway 提供團隊模型管理功能
- Observability 提供團隊 trace 收集與分析功能

o11y 的功能看起來一樣，為何不用 Bifrost 就好?
- Bifrost 的進階 o11y 功能都需要 Enterprise
- Langfuse 的 LLM-as-a-judge，Datasets，Evaluation 都是 OSS (MIT license))

---

##### 根據不同 CLI 需求做 o11y 設定

Coding Agent 可能內建 trace 功能，或需額外設定
- codex 支援 otel ，但功能不完整
- Gemini CLI 支援 otel，但需要額外設定
- 透過 AI Gateway 收集 trace 是最方便的方式

LLM Application 需要自己串接 otel/langfuse SDK

收集更細節的 trace 與 custom metric

---

CLI - AI Gateway - Observability

{{< mermaid >}}
graph LR

    A["VSCode Chat
    Copilot"]
    B["Bifrost
    AI Gateway
    localhost:8080"]
    C["(Open Telemetry)"]
    D["Langfuse
    localhost:3000"]
    E["ClickHouse
    MinIO"]
    
    A --> B
    B --> C
    C --> D
    D --> E
{{< /mermaid >}}

---

### Workshop 以 Langfuse 為主

有空或無聊也可以去玩 Bifrost 的其他功能

---

### Task 1: Session overhead

- 請 VSCode Chat 說一個笑話，產生一筆 trace
- 找到這筆 trace
  - 總共花了多少 token？
  - 花在什麼東西上面？
  - 有沒有 cached token？
- 打開 trace detail
- 對照 input / output / cached

---

#### Task 2: Session & Cached token

- 請 VSCode Chat 說第二個笑話，以及第三個笑話
  - 第二筆與第三筆 trace 的 token 花費有什麼不同？
- 打開 trace detail
- 對照 input / output / cached
- Use /compact 或 /clear 指令，第四個笑話的 token 花費有什麼不同？

---

#### Task 3: 調整 VSCode enabled tools

`gen_ai.request.tools` 是 agent cli 的低消，會保證每次呼叫至少花這麼多 token

- /clear 指令清除 session
- 找到工具設定，試圖停用不必要的工具
- 哪些工具是你不需要的？
- 哪些工具是必要的？
- 停用後新的 session
- token 花費有沒有下降？

---

#### Tools

- 同一 Session 重複相同 prompt，Cached token 降低成本
- 然而很多工具是不會用到，浪費 token
- 建議停用工具: Browser，VSCode extension，Notebooks，Github，Terminal 等
- 不建議停用的：Agent，Read，Write
- 看情況：Web search，Github search 建議可以拆成獨立 Plan Agent 使用
- https://code.visualstudio.com/docs/copilot/agents/agent-tools

省 10000 token 沒多少錢，想像他是 gpt-5.4-pro （nano 的 x150 倍）

---

#### 有需要計較 token 的花費嗎

人月神話/Parkinson's Law，「工作會自動膨脹，填滿可用的時間」

人Token神話：給員工多少 Token 預算，就會用完多少 Token

面對問題，有人在等更未來強大模型來解決，有人在試圖用更便宜的模型現在解決

---

#### Task 4: Long-running Agent

模擬真實 Code Agent 進行長時間任務

- 參考上午 Lab [Spec-driven development with Spec-kit](../../posts/2026-07-01-ws-speckit-ai-ent/)
- 不用跑完，重點在觀察 trace 與 token 花費

```
specify init --here --integration copilot
/speckit.constitution 為專案建立一套憲法，重點在簡潔性和測試覆蓋率。
/speckit.specify 建立一個 Terminal 應用：台北市 YouBike 2.0 即時站點查詢器。
核心需求：
 1. 自動從政府 API 抓取 JSON 站點資訊。
 2. Input：可依據「站點地址」或「名稱」過濾。
 3. 列表呈現：站點名稱、可用車輛、剩餘空位。
/speckit.plan
/speckit.tasks
/speckit.implement
```
---

#### Task 5: rtk

https://github.com/rtk-ai/rtk

---

### Task 4: 寫下你的評分規則

- 把「好答案」寫成 3 條可檢查規則
- 每條規則都要能判斷 pass / fail
- 用這份 rubric 評分剛剛那筆 trace

---

### Task 5: 讓 judge 幫你打分

- 先自己猜這筆 trace 會得幾分
- 再跑一次 judge
- 比較：
  - 你的分數
  - judge 的分數
  - 哪一條規則最容易吵架

---

### 模擬 Code Agent 開發流程

參考上午 Lab [Spec-driven development with Spec-kit](../../posts/2026-07-01-ws-speckit-ai-ent/)

```
specify init --here --integration copilot
/speckit.specify 建立一個單頁 Web 應用：台北市 YouBike 2.0 即時站點查詢器。
核心需求：
 1. 自動從政府 API 抓取 JSON 站點資訊。
 2. 搜尋框：可依據「站點地址」或「名稱」過濾。
 3. 列表呈現：站點名稱、可用車輛、剩餘空位。
/speckit.plan
/speckit.tasks
/speckit.implement
```

---

### bootstrap llm-as-a-judge workflow

- 先用自己的標準猜一次這筆 trace 好不好
- 再讓 judge 跑一次
- 比較人類判斷和 judge 分數有沒有一致
- 如果不一致，回頭修 rubric

```
export AZURE_ENDPOINT=https://chechia-ws.services.ai.azure.com/
export AZURE_OPENAI_API_KEY=xxx
./scripts/bootstrap-langfuse.sh

verify llm-as-a-judge workflow
base_url=http://localhost:3000
config=data/langfuse/bootstrap.json
langfuse.version=3.172.1
auth=ok
Upserting 1 LLM connection(s) to http://localhost:3000
Upserted connection: provider=azure adapter=azure
Done: success=1 skipped=0 total=1
Updated score config: llm_judge_correctness (39a27360-ae53-448e-9a59-3f66b2535b21)
unstable_evaluators_api=ok
default_evaluator_model=missing
Set default evaluator model in UI: http://localhost:3000/project/chechia-project/evals/new
retry_create_evaluator=ok provider=azure model=gpt-5.4-nano
warning: default_evaluator_model still missing (explicit model works)
score_config=ok id=39a27360-ae53-448e-9a59-3f66b2535b21
create_evaluator=ok name=ci-answer-correctness-1779889505_30996
create_rule=ok id=cmpo49bb7000qoy08rw4zvxeg
get_rule=ok
delete_rule=ok
PASS: llm-as-a-judge workflow verified
```

---

## 核心問題

多數團隊已經有：

- trace / logging
- prompt 管理
- agent framework（LangChain / AutoGen / others）
- observability 工具（Langfuse）

但仍無法回答：

> 這次 model 或 framework 升級，該不該上 production？

---

## 關鍵誤解

### Observability != Decision System

Observability 只能回答：

> 發生了什麼？

Decision System 需要回答：

> 我應不應該改？  
> 這次改動是不是變好？

---

{{% section %}}

### LAB1：啟動 LLM O11y Stack

目標：把本地端觀測平台跑起來，先確保 trace 能收集。

```bash
cd llm-o11y
cp .env.example .env
docker compose up -d
```

---

### LAB1：確認服務健康

請確認：

- Langfuse UI 可開啟
- Gateway / API 可回應
- demo app 能發送一筆 trace

```bash
docker compose ps
```

---

### LAB1：做第一筆 trace

```bash
make demo-trace
```

觀察重點：

- prompt / response
- token usage
- latency

{{% /section %}}

---

## Evaluation：把主觀變可比較

建議組合：

- LLM-as-a-judge（快速、可擴）
- rule-based checks（格式、schema、constraints）
- task rubric（符合業務定義的好壞）

---

{{% section %}}

### LAB2：加入 LLM-as-a-judge

目標：針對既有 traces 自動評分。

```bash
make eval-run
```

---

### LAB2：加上 Rule-based Checks

常見檢查：

- JSON schema 是否合法
- 必要欄位是否存在
- 關鍵關鍵字是否命中

```bash
make eval-rules
```

{{% /section %}}

---

## Dataset：從真實流量累積

不是 benchmark 優先，而是 production-like data：

- 真實 query
- 真實 failure cases
- 真實 edge cases

流程：

`trace -> triage -> label -> dataset`

---

{{% section %}}

### LAB3：從 traces 產生 dataset

```bash
make dataset-export
```

輸出目標：

- baseline dataset
- failure-focused dataset

---

### LAB3：資料集分層

最低限度建議分三層：

- smoke（快速）
- core（關鍵流程）
- edge（高風險案例）

{{% /section %}}

---

## Regression：比較不能靠感覺

固定同一份 dataset 比較不同：

- model
- prompt strategy
- agent framework

輸出指標：

- quality delta
- latency delta
- cost delta

---

{{% section %}}

### LAB4：跑 regression

```bash
make regression-run
```

---

### LAB4：設定 Decision Gate

只有同時滿足才允許 deploy：

- quality >= baseline
- no critical regression
- latency within SLO
- cost within budget

```bash
make decision-gate
```

{{% /section %}}

---

## Failure Taxonomy

先分類，再修復：

- hallucination
- tool misuse
- reasoning error
- format/schema break

---

## 最小可行架構

```text
Agent Runtime
  -> Tracing (Langfuse)
  -> Evaluation
  -> Dataset Store
  -> Regression Runner
  -> Decision Policy
```

---

## 核心訊息

沒有 evaluation：

**LLM upgrade = gambling**

有 feedback loop：

**Observe -> Evaluate -> Regress -> Decide**

---

## Thank you

下午本堂 Session 歡迎參考
- Session: 15:30 - 16:00 [LLM O11y：從 Observability 到 Decision System](../../posts/2026-07-01-langfuse-ai-ent/)

謝謝大家。
