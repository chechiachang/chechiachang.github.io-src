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
##### LLM O11y：從 Observability 到 Decision System
##### ~ Che Chia Chang @ [chechia.net](https://chechia.net) ~

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
##### 量化並提升 Coding Agent 效率
##### ~ Che Chia Chang @ [chechia.net](https://chechia.net) ~

---

{{< slide content="slides.about-me" >}}

---

### 大綱

1. AI Gateway & Observability stack
1. Tracing & token 花費，Agent 如何花 token
1. Case 1: 導入 rtk 是否有助減少 token
1. Llm-as-a-judge evaluator
1. Dataset & Experiment based on past tracing
1. Case 2: Evaluate multi-turn agent

---

{{% section %}}

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
- Observability 提供團隊 tracing 收集與分析功能

o11y 的功能看起來一樣，為何不用 Bifrost 就好?
- Bifrost 的進階 o11y 功能都需要 Enterprise
- Langfuse 的 LLM-as-a-judge，Datasets，Evaluation 都是 OSS (MIT license))

---

##### 不同 CLI 需求做 o11y 設定

Coding Agent 可能內建 tracing 功能，或需額外設定
- codex 支援 otel ，但功能不完整
- Gemini CLI 支援 otel，但需要額外設定
- 透過 AI Gateway 收集 tracing 是最方便的方式

LLM Application 需要自己串接 otel/langfuse SDK

收集更細節的 tracing 與 custom metric

---

CLI - AI Gateway - Observability

{{< mermaid >}}
graph LR
    A["VSCode
    Copilot "]
    B["Bifrost
    AI Gateway "]
    C["OTel "]
    D["Langfuse "]
    A --> B
    B --> C
    C --> D
{{< /mermaid >}}

---

### Workshop 以 Langfuse 為主

有空或無聊也可以去玩 Bifrost 的其他功能

{{% /section %}}

---

### Task 1: Reduce Overhead

- 請 VSCode Chat 說一個笑話，產生一筆 tracing
- Langfuse > Tracing > Observations
- 找到這筆 observation
  - 總共花了多少 token？
  - 花在什麼東西上面？
  - 有沒有 cached token？
- 打開 observation detail
- 對照 input / output / cached

---

#### Task 2: Understand Cached token

- 請 VSCode Chat 說第二個笑話，以及第三個笑話
  - 第二筆與第三筆 observation 的 token 花費有什麼不同？
- 打開 observation detail
- 對照 input / output / cached
- Use /compact 或 /clear 指令，第四個笑話的 token 花費有什麼不同？

---

{{% section %}}

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
- 然而很多工具是不會用到
- VSCode 與 CLI 甚至 ai gateway 都會注入工具
  - VSCode default 有 40+ tools
  - 例如 bifrost 的 `session_store_sql`

- 建議拆分不同 agent 分配工具
  - 規劃時使用 Plan agent (readonly)
  - 實作時切換 Write Agent (read file, write file)
- 停用: Browser，VSCode extension，Notebooks，Github，Terminal 等
- 不建議全關，例如 Agent 與 search，Read File 等是 coding agent 的核心

---

#### Task 4: 調整 Instruction

就算 VSCode Tools 全關，也大概剩下 2000+ token 的基礎花費

- langfuse observation: type=GENERATION name=llm.call
  - observation detail，找到 token 的來源
- AGENTS.md
  - 是否夠精簡? VScode 是否有讀取 AGENTS.md 內容?
  - VSCode `cmd + ,` 開啟設定，chat.useAgentsMdFile=true
- .github/copilot-instructions.md
  - 是否夠精簡? 是否有讀取 copilot-instructions.md 內容?
- role=system instruction 的來源是哪裡？

---

#### Agent Instruction

- 許多 CLI system instruction 是固定的，無法修改
  - 包含權限與安全性設定
  - 例如資料夾權限，Sandbox 設定，工具使用權限等
- 極簡或自由的 CLI 允許修改 system instruction
  - 需要額外設定來保障安全

---

#### CLI debug 模式

VSCode Chat 中，`/debug` 指令開啟 debug 模式
- 點 title [tokens tks][latency ms][timestamp]
  - 使用小模型為對話命名 ex. gpt-4o-mini
- copilotLanguageModelWrapper 檢視以下內容
  - Metadata
  - System Instruction
  - User 可能有多輪內容
  - Assistant

---

{{< slide background-image="vscode-chat-debug.png" background-size="80%" background-color="#000000" background-opacity="1" >}}  

{{% /section %}}

---

##### 小結：Know Your Agent

進入全自動 Agent 前，確定 Agent 設定符合需求

- 手動運行浪費錢 -> 自動運行花式燒錢
- 以 team 為單位 review agent 設定
- 10000 token ，想像他是 gpt-5.4-pro （nano 的 x150 倍）
- 人Token神話：給員工多少 Token 預算，就會用完多少 Token

{{% note %}}
人月神話/Parkinson's Law，「工作會自動膨脹，填滿可用的時間」
面對問題，有人在等更未來強大模型來解決，有人在試圖用更便宜的模型現在解決
{{% /note %}}

---

#### Case 1: 導入 rtk 是否有幫助

repo 1
repo 2


---

##### 目標：提升團隊 Coding Agent 效率

但是 Coding Agent 效率到底是什麼？

{{< math >}}
\text{整體效率 Efficiency} = \frac{\text{產出數量} \times \text{產出品質}}{\text{Token Cost} \times \text{花費時間}}
{{< /math >}}

{{% fragment %}}
- 團隊產出數量：完成的功能模組數、修復 Bug 數
- 團隊產出品質：測試通過率、Linter 分數、Code Review 評分
- 團隊 Token Cost
- 團隊工作時間
{{% /fragment %}}

---

#### LLM-as-a-Judge Evaluators

Langfuse > Evaluation > LLM-as-a-Judge
- Create Evaluator
- 右邊 Set up
- Add LLM connection

```
LLM adapter=azure
Provider name=azure
API Key=xxx
API Base URL=https://chechia-ws.services.ai.azure.com/openai/deployments
Custom models=gpt-5.4-nano
```
- Create Connection
- 選擇 Azure / gpt-5.4-nano > Save

---

{{< slide background-image="create-llm-connection.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

{{< slide background-image="default-model.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

#### LLM-as-a-Judge Evaluators

Helpfulness
- Run on Observations

```
Type any of GENERATION
And Environment any of default
And Name any of llm.call
```

最右下 Execute

---

#### LLM-as-a-Judge Evaluators

指派工作給 Agent，並觀察評分。以下是範例

```
檢查 ./github/agents/caveman.agent.md，潤飾措辭，並保持精簡

幫我寫 README.md，內容包含專案介紹、安裝說明、使用說明、貢獻指南。

上網搜尋 rtk 並且參考官方文件，並檢視本專案是否適用

上網搜尋 speckit 並檢視本專案是否適用

幫我查 ubike 2.0 officla API，並且寫一個 Python 程式碼範例查詢台北市的 ubike 站點資訊。
```

---

#### Task 5: LLM-as-a-Judge Evaluators

- 觀察 Helpfulness 分數
- 人類判斷是否合理
- 觀察分數後 LLM 的評分理由
- Evaluator 是否有正確取得 Input / Output 的內容

---

{{< slide background-image="judge-helpfulness.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

#### Task 5: LLM-as-a-Judge Evaluators

Evaluators 除錯
- 看起來評分不合理
- Evaluator > Logs View，看看 LLM 的評分理由
- Target Trace 是抽出 Input Output 的 Trace
- 點 Execution Trace 檢查 LLM 的思考過程與評分依據
- 發現 LLM reasoning 說「沒有看到 output」

實際上有 output，但只有部分 Observation 有 output，其他 Observation 裡面的 output 是空的，導致評分不合理

---

{{< slide background-image="evaluator-debug-logs.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

#### 觀測多步驟 Agent

Coding Agent Session 包含多個步驟，每步有不同的 input / output / tools

- 增加 filter，先以單一步驟 tool call 為單位建立 Evaluator
- 觀察每個步驟的表現
- 再逐步擴大到整個 Agent 的評分

---

{{< slide background-image="judge-helpfulness.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

#### Task 6: 建立自己的 Evaluator


Langfuse > Evaluation > LLM-as-a-Judge
- 右邊 Set up Evaluator
- Create Custom Evaluator
- Name: Apply Patch Safely
- Prompt:
```
Evaluate the safety of applying the following patch to the codebase. 

Request Input:
{{input}}
Apply Patch Description:
{{description}}
```

---

#### Task 6: 建立自己的 Evaluator

```
Where Type any of GENERATION
And Environment any of default
And Called Tool Names: apply_patch
```

Variable mapping
- 邊修改，邊觀察 Prview 的變化
```
{{input}}
    Object Field: input
{{description}}
    Object Field: Output
    JsonPath: $[0].tool_calls.[0].args
```

---

{{< slide background-image="custom-evaluator-filter-tool-call.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

{{< slide background-image="custom-evaluator-field-mapping.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

#### Task 6: 建立自己的 Evaluator

回到 VSCode，觸發 Agent 執行 apply patch
```
Review ./github/agents/caveman.agent.md, polish the wording, and keep it compact.
```
- 開啟 /debug 模式，找到這筆 observation 有觸發 apply patch 工具
- 回到 Langfuse Evaluation 觀察評分
- 觀察 Evaluator Logs View，看看 LLM 的評分理由

---

{{< slide background-image="vscode-chat-debug-apply-patch.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

{{< slide background-image="custom-evaluator-after-filtering.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

#### 小結：LLM-as-a-Judge Evaluators

llm-as-a-judge 只是開頭，重點是建立可持續修正的規則
- rule-based checks（格式、schema、constraints）
- task rubric（符合業務定義的好壞）

對你的團隊，什麼樣的 output 是好答案
- 要能用文字寫成可檢查規則
- 每條規則都要能判斷 pass / fail
- 用這份 rubric 評分剛剛那筆 trace

---

##### Observability 到 Decision System

LLM as a Judge Evaluator 是顯微鏡：避免以管窺天

小 scope 內的量化分數
- 侷限在 trace level，無法直接反映到 feature level 或 release level
- 絕對值不重要，重點在相對變化趨勢

人類的感覺是重要的評分
- 提供 o11y 量化結果，團隊的感覺會做修正，標準會統一
- 看過 o11y 後在進行團隊問券

---

##### 避免兩種以管窺天

- 人類只憑感覺，忽略量化分數
- 量化分數推翻人類的感覺

獲取更多客觀量化評分，加強人類觀察力，作為 Decision Gate 的依據

---

{{% section %}}

### Dataset 與 Regression

收集 gpt-5.4 的 Input / Output / 分數作為回歸測試資料

例如：相同的 Input，gpt-5.5 是否效能更好
  - 整體費用是否維持或降低
  - latency 維持或降低
  - 整體 (gpt-5.4-nano) judge 分數更高
  - 失敗率更低

---

### Dataset

嘗試使用 coding agent tracing 產生資料集

```
./scripts/create-langfuse-dataset-from-observations.sh
dataset=ok name=test id=cmprza7dv0067qi06zi7ccrc9
done dataset=test added=50 skipped_existing=0 skipped_invalid=146
```

---

{{< slide background-image="dataset-export.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

##### Data preprocessing
##### 清理格式

tracing 原始資料不適合直接使用

用 script 只收集 input / Expected Output / metadata

- 讀取既有資料集項目，收集它們的 sourceObservationId 用於去重。
- 依 START_PAGE 開始逐頁抓取 observations：
- 從 observation 解析並提取可用的 input 與 expectedOutput
- 跳過缺失/重複/解析無效的資料
- 將有效項目 POST 到 /api/public/dataset-items
- 直到新增 LIMIT 筆為止。

---

{{< slide background-image="dataset-preprocessing.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

##### script 只是示範實務的步驟

實務資料整理相當複雜

需要根據 use case 調整，才能整理出堪用的資料

這裡僅僅簡單帶過

資料集整理就是一門講不完的課

---

##### Data preprocessing
##### 挑選內容

現在的 dataset 是「日常工作的tracing」，但有包含有效跟無效的紀錄

我們想要挑選高效的 tracing 來訓練模型，或是挑選失敗的 tracing 來修正模型

可以進一步使用 llm-as-a-judge 評分篩選，挑選出可用的 input / expected output

---

##### 使用 dataset 進行 experiment

先建立 Prompt，Prompts > 右上角 New Prompt

```
Name: Coding agent vs LLM 
prompt: Chat
System: You are a coding agent.
```
點 +Message
```
User: {{input}}
取消 Set the "production" label
```
Create Prompt

---

##### 使用 dataset 進行 experiment

測試不同 model / agent / tool 的表現

Dataset > test > 右上角 Run Experiment
- via User Interface > Configure
```
Prompt: Coding agent vs LLM
Model
Provider: azure
Model name: gpt-5.4-nano # 或是測試新模型 gpt-5.5
```
- Next
- Dataset: test
- Valid configuration

```
Matches between dataset items and prompt variables/placeholders
input: 100 / 100
```
---

{{< slide background-image="experiment-valid-configuration.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

##### 使用 dataset 進行 experiment

- Next
- Select Evaluators (Optional)
  - Helpfulness
- Next
- Run Experiment
- 可以到 Dataset > test > Experiments 看進度與結果

---

{{< slide background-image="experiment-run.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

{{< slide background-image="experiment-details.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

{{% /section %}}

---

##### Observability 到 Decision System

- LLM call metadata（token usage, latency）：客觀數據
- LLM-as-a-Judge Evaluator：狹隘但便利的量化評分
- Dataset Experiment：基於具體 Input / Expected Output 的比較
- 最後加上人類意見，作為 Decision Gate

---

## Thank you

沒有 evaluation，LLM upgrade = gambling or faith

Observe -> Evaluate -> Regress -> Decide

下午本堂 Session 歡迎參考
- Session: 15:30 - 16:00 [LLM O11y：從 Observability 到 Decision System](../../posts/2026-07-01-langfuse-ai-ent/)

---

#### Case 2: Coding Agent

輸入給 VSCode Chat，並觀察 llm-as-a-judge 評分

```
建立一個 Terminal 應用：台北市 YouBike 2.0 即時站點查詢器。
核心需求：
 1. 自動從官方 YouBike 2.0 API 抓取 JSON 站點資訊。
 2. Input：可依據「站點地址」或「名稱」過濾。
 3. 列表呈現：站點名稱、可用車輛、剩餘空位。
 4. 使用 pytest 測試，mypy 類型檢查，ruff test lint

...(後續開發過程中對答）
```

---

#### Case 3: Monitoring & Evaluate long running agent

Single Turn vs Multi Turn o11y

重點在模擬開發，觀察 trace 與 token 花費

- 參考上午 Lab [Spec-driven development with Spec-kit](../../posts/2026-07-01-ws-speckit-ai-ent/)
- 現在可以跑 /speckit.specify，之後可以稍後再跑

```
/clear # 清除 session，開始新的對話
specify init --here --integration copilot
/speckit.constitution 為專案建立一套憲法，重點在簡潔性和測試覆蓋率。
/speckit.specify 建立一個 Terminal 應用：台北市 YouBike 2.0 即時站點查詢器。
核心需求：
 1. 自動從官方 YouBike 2.0 API 抓取 JSON 站點資訊。
 2. Input：可依據「站點地址」或「名稱」過濾。
 3. 列表呈現：站點名稱、可用車輛、剩餘空位。
/speckit.plan
/speckit.tasks
/speckit.implement
```
