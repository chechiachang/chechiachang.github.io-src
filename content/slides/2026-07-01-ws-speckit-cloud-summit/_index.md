---
title: "Cloud Summit Workshop: Spec-driven development with Spec-kit"
description: "90 分鐘 hands-on workshop，從 Vibe Coding 走向 Spec-driven Development（SDD），用 Spec-kit 完成從規格到實作的完整流程。"
tags: ["ai", "sdd", "spec-kit", "workshop", "devops", "agent"]
categories: ["ai", "workshop"]
date: '2026-05-02T09:00:00Z'
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

- 攜帶筆電，可上網
- 安裝好操作環境
  - [VS Code](https://code.visualstudio.com/)
  - [Spec-kit CLI](https://github.com/github/spec-kit#1-install-specify-cli)
- 下載 [workshop 範例程式碼](https://github.com/chechiachang/speckit-playground)
- 講師會提供 Azure OpenAI API Key，也可帶自己習慣的 llm
- 已經會用 VS Code + GitHub Copilot Chat，用自己的方式參加即可

🔽

---

### VS Code

- 安裝 VS Code：[https://code.visualstudio.com/](https://code.visualstudio.com/)
- 打開 VS Code，底下 Terminal
  - git clone 程式碼 `speckit-playground`
  - File > Open Folder > 選擇 clone 的 speckit-playground

```
git clone https://github.com/chechiachang/speckit-playground.git
```
---

{{< slide background-image="git-clone.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

### 安裝 Spec-kit CLI

- 打開 VScode 下方的 Terminal
- 確認 uv 可用，沒有的話[先裝 uv](https://github.github.com/spec-kit/install/uv.html)
- 安裝 [Spec-kit CLI](https://github.github.com/spec-kit/installation.html#installation)

```
# 確認 uv 可用
uv --version

# 沒有的話安裝 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安裝指定穩定版
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v0.8.9
```

---

{{< slide background-image="install-specify-cli.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

### API Key 設定

- 在 VS Code 右側 Secondary Sidebar 找到 Chat
  - 底下 Model 點一下，會跳出可用 Model 的列表
  - ex Auto, GPT-5, gpt-5.4 等等
- Model 右上角齒輪圖示，點一下選擇 Manage Model Settings
  - Add Models > Azure OpenAI
  - Group Name: Azure
  - Azure API Key 填入講師提供的 Key (當天提供可以先留白）
  - 跳出 chatLanguageModels.json 編輯

---

{{< slide background-image="manage-model-settings.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

{{< slide background-image="chat-language-models-json.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

### API Key 設定

- chatLanguageModels.json 填入: id, name, url
- cmd + s 儲存
- 回到 Model 列表，選擇剛剛新增的 Azure GPT-5.4 Nano
  - 跟 Azure say hi，確認可用

```
[
  {
    "name": "Azure",
    "vendor": "azure",
    "apiKey": "${input:chat.lm.secret.-3df80c78}",
    "models": [
      {
      	"id": "gpt-5.4-nano",
      	"name": "Azure GPT-5.4 Nano",
      	"url": "https://chechia-ws.cognitiveservices.azure.com/openai/responses?api-version=2025-04-01-preview",
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

### 行前準備結束

- Model 列表，選回去選擇其他 Model，可以先用免費版

{{% /section %}}

---

#### AI Enterprise Summit 2026
## 從零開始 Spec-kit 規格導向
##### 90 分鐘 workshop
##### ~ Che Chia Chang @ [chechia.net](https://chechia.net) ~

---

{{< slide content="slides.about-me" >}}

---

### 大綱

本次 workshop 以 hands-on 為主，講解為輔。

1. LAB1：第一個 Spec-kit 專案
1. 講解：什麼是Spec-kit
1. 講解：什麼時候 SDD 會優於 Vibe Coding
1. 講解：Spec-kit 經驗分享，適合與不適合的 use case
1. LAB2：自己想做的專案
1. 驗收、回顧、Q&A

---

{{% section %}}

### LAB1：第一個 Spec-kit 專案

還沒講什麼是 Spec-kit 之前，先讓大家實際體驗一次
- 先當 Spec-kit 是一個與 llm 對話的工具，目標是產生程式碼
- 打開瀏覽器到 https://github.com/github/spec-kit#-get-started
- 打開 VS Code 與 Spec-kit playground 的範例程式碼

---

### LAB1: 初始化專案

```bash
# VS Code Terminal

specify init --here --integration copilot

# 安裝為 skills 版本，而非整個 agent，來節省 spec-kit token overhead (spec-kit tax)
specify init --here --integration copilot --integration-options="--skills"

Warning: Current directory is not empty (7 items)
Template files will be merged with existing content and may overwrite existing files
Do you want to continue? [y/N]: y

specify check
```

---

### LAB1: 初始化專案

- specify init 在當前資料夾建立 copilot 整合的 Spec-kit 檔案
- 建立 .specify/ 資料夾，裡面有 specify agent 會用到的檔案
- .vscode/settings.json
  - 改成支援 Copilot Chat 的 prompt
  - 偷塞 chat.tools.terminal.autoApprove 給 .specify/scripts/bash/
- 🛠️ 打開 ./specify/templates 資料夾，看一下裡面的內容
- 🛠️ 在 Chat 中輸入 /spec 看看會發生什麼事

---

{{< slide background-image="specify-init-copilot.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

### LAB1: 建立 principles

- 在 Chat 輸入
- 等待 copilot 生成憲法（Constitution）
- 🛠️ 看一下 .specify/memory/constitution.md 內容，是否滿意
  - 如果不滿意，可以透過 chat 要求 copilot 修改，直到滿意為止

```
# 今天 workshop LAB1 先用中文，比較好理解
/speckit.constitution 為專案建立一套憲法，重點放在簡潔性和測試覆蓋率。

# 用英文 llm performance 會比較好，大概是 5-10% benchmark 提升（請見最後論文參考）
# 但如果英文會讓人類 performance 下降 10%，就請都用中文好了
/speckit.constitution Create principles focused on simplicity, and test coverage for our project.
```

---

{{< slide background-image="specify-constitution.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

> constitution 是 agent 的行為準則，會在每次 agent 行動時被參考

---

### LAB1: 建立 Spec

- 打開範例專案 example-ubike.md
- 如果你有準備其他題目，請用自己的題目
- Focus on the what and why
- agent 會產生 specs/001-branch-name/spec.md

```
# 清除之前的對話紀錄，讓 agent 從一個乾淨的狀態開始理解需求
/clear

/speckit.specify 建立一個單頁 Web 應用：台北市 YouBike 2.0 即時站點查詢器。
核心需求：
 1. 自動從政府 API 抓取 JSON 站點資訊。
 2. 搜尋框：可依據「站點地址」或「名稱」過濾。
 3. 列表呈現：站點名稱、可用車輛、剩餘空位。

/speckit.specify Create a specification for a single-page web application: Taipei YouBike 2.0 Real-time Station Query Tool. Specification should include: 1. Automatically fetch JSON station data from government API. 2. Search box: filter by "station address" or "name". 3. List display: station name, available bikes, remaining docks.
```

---

{{< slide background-image="specify-spec.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

### LAB1: Plan / Tasks / Implement

- 在 Chat 輸入 /speckit.plan，讓 agent 根據 spec 產生實作計畫
- agent 會產生 specs/001-branch-name/plan.md
- (optional) context management:
  - `/clear` 清除之前的對話紀錄，讓 agent 從一個乾淨的狀態開始讀取 plan.md & tasks.md
  - `/compact` 當前 session 會把之前的對話紀錄壓縮成一個 summary，讓 agent 可以讀取到之前的內容，但不會有太多 token 費用

```
/clear

/speckit.plan
/clear

/speckit.tasks
/clear

/speckit.implement
```

{{% /section %}}

---

### LAB1: Interruption

- agent 會遇到困難卡住，或是有疑問，會在流程中問你
- 檢視 agent 想要執行的 cmd，覺得合理的話選擇 allow
- 可以自己判斷或是再問 agent，或是直接叫 agent 自己決定
- 有些流程是 spec-kit 設定的，例如 branch name，可以使用 /speckit.git.feature 切換

```
I can’t start implementing yet because the repo is currently on main, and Spec Kit requires a feature branch for this workflow.

Please create or switch to a feature branch for 001-youbike-station-search using one of these patterns:

/speckit.git.feature
```

---

{{< slide background-image="specify-git-feature.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

### LAB1: Auto-approve

避免人類變成瓶頸，auto-approve 是需要的，但請注意安全性❗

- 只允許本 workspace 資料夾的存取（不允許存取本機其他目錄）
- 允許 readonly: git, bash, grep, ...
- write 只允許特定工具，arguments 也要限制
- 🛠️ 檢視目前的 setting，放在 .vscode/settings.json
  - Allow running command `xxx` in this workspace 會修改 settings.json
- ❗Allow all commands in this workspace 是相對危險的，也會提高費用

---

{{< slide background-image="auto-approve-constitution.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

### LAB1: Implementation

Implementation 需要時間，大家可以邊觀察邊做其他事情，等 agent 實作完再回來驗收
我會利用這段時間講解 Spec-kit 的概念，以及為什麼會有幫助，適合什麼 use case，等等

---

### Spec-kit 是什麼

- 一套 Spec-driven Development toolkit
- 定義 script, template, checklist 等等，讓 agent 可預測地產生Spec
- 把 workflow 拆解成 `/specify` `/plan` `/tasks` `/implement`
- 讓 agent 依標準流程工作，先完成 spec，再 plan，再 tasks，最後 implement
- 每流程都有需要完成的 checkpoint，才會進入下一步
- 支援長任務、多輪迭代

---

### 核心流程

```text
/specify -> /plan -> /tasks -> /implement
```

- 每一步都可回頭調整
- 改需求先改 spec，不先改 code

> 為何會有幫助？

---

### 為何會有幫助: 避免 Spec drift

「跟 llm 來回對話，一直補充資訊」，Spec 可能會越聊越清楚，也可能會越聊越模糊，到最後 llm 理解錯誤的需求，導致實作出來的東西不符合預期

「先產生 Spec」產生唯一的 source of truth，並持續修改，讓 agent 可以根據 Spec 來產生 Plan、Tasks、Implement，確保實作的東西是符合 Spec 的

「根據 Spec，有流程的產生程式」，透過分段實作或是拆分 task 來降低每次改動的成本，讓 agent 可以專注在當前的任務，而不是同時處理大量需求，帶來的額外複雜度

---

### 為何會有幫助: Context management

- Vibe Chat 如果描述複雜的需求，容易產生 long context
- long context 可能造成 llm performance 下降
- long context 會需要 compact 來壓縮，可能會有資訊遺失。
- [VSCode Official Doc: Context Compaction](https://code.visualstudio.com/docs/copilot/chat/copilot-chat-context#_context-compaction)
  - 不一定 compact 就會遺失，但會因為 compact 導致 context 不可控，llm 效能可能更好也可能更差

> 忽好忽壞的不可控，會增加未來改善措施的難度

---

### 為何會有幫助: Involve human in the loop

- Vibe Coding 沒有一個明確的 checkpoint，不容易多人協作
- 複雜需求的 Vibe Coding 流程拉長，更不容易 review
- 使用中間產物 Spec 檔案作為 source of truth
  - 可以讓其他 teammember 來 review，確保需求的正確性
  - 最終產物是 Spec + Code。Spec 作為未來改動的基準，確保 Spec 跟著需求改動

> 只有 Code 往往不足表達當初的需求細節
> 「誒我去年為何會這樣寫啊（問旁邊」

---

### Vibe Coding 常見狀況

Vibe 是聊天，Spec 是工程

- 同一需求每次改法不同
- QA 才發現需求漏掉
- 上線後才補規格

---

### SDD 適合 agent?

為何又紅起來

- 把需求變成可檢查文件
- 把實作順序固定下來
- 把驗收條件前移
- 把 agent 行為限制在 spec 內

---

### Why use nano (or mini) for Spec-kit?

- https://developers.openai.com/api/docs/pricing

```
  ┌──────────────┬──────────┬───────────┬────────────┬───────────┬───────────┬────────────┐
  │ Model        │    Short │     Short │      Short │      Long │      Long │       Long │
  │              │    Input │    Cached │     Output │     Input │    Cached │     Output │
  │              │          │     Input │            │           │     Input │            │
  ├──────────────┼──────────┼───────────┼────────────┼───────────┼───────────┼────────────┤
  │ gpt-5.4-pro  │   $30.00 │         - │    $180.00 │    $60.00 │         - │    $270.00 │
  │ gpt-5.4      │    $2.50 │     $0.25 │     $15.00 │     $5.00 │     $0.50 │     $22.50 │
  │ gpt-5.4-mini │    $0.75 │    $0.075 │      $4.50 │         - │         - │          - │
  │ gpt-5.4-nano │    $0.20 │     $0.02 │      $1.25 │         - │         - │          - │
  └──────────────┴──────────┴───────────┴────────────┴───────────┴───────────┴────────────┘
```

---

### Why use nano (or mini) for Spec-kit?

- https://openai.com/index/introducing-gpt-5-4-mini-and-nano/
- gpt-5.4-nano 有 gpt-5.4 `90%` 的 Coding, Tool-calling, Intelligence
- 但如果是 Long context 或 MM / Vision / CUA 效能只剩 `50%`

- Spec-kit Tax: 比起 Vibe Coding 的即時回饋，SDD 的流程會有額外的成本（Spec 產生、Plan 產生、Task 產生、Implement 產生）
- 使用 nano 費用 10% 或 mini 費用 16.7%
  - Tradeoff: 不適合 Long Context (>272K tokens) 的任務
  - 但是如果使用 gpt-5.4 來跑 long context 的任務，成本會變兩倍，變成 nano 的 18-36 倍
  - 要盡力把 context 壓縮不要變成 long context
- 可以用 5.4 來做 Spec，然後用 5.4-nano 來做 implement，這樣就能兼顧品質與成本

---

### LAB2

- 卡住很正常，先記錄問題
- 我們先求跑通，再求漂亮

```
/speckit.specify
/speckit.clarify
/speckit.plan
/speckit.analyze
/speckit.tasks
/speckit.implement
```


---

### Clarify

---

### 驗收（Analyze）

`/speckit.analyze`

- 看與 spec 的差距
- 看風險與遺漏
- 看是否需要回到 plan/tasks

---

### 今天的 LAB 題目

## 台北市 YouBike 2.0 即時站點查詢器

- 單頁靜態網頁
- 政府公開資料 API
- 要有搜尋與過濾

---

### LAB 目標

1. 可抓取站點資料
1. 可依站名或地址搜尋
1. 顯示可借車輛、可還空位
1. 可用低庫存警示（< 3）

---

### 資料來源

- API Endpoint  
`https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json`

---

### 安裝卡住怎麼辦

- 先確認 `uv` 可用
- 再確認 `specify version`
- 再跑一次 `specify check`
- 真的不行就切講師提供環境

---

### API Key 設定

- 選項 1：使用自己的 Azure OpenAI Key
- 選項 2：使用講師提供 Key
- 重點是先讓 agent 可用

---

### Workshop 規則

- 先做出可驗收版本
- 不要跳步驟
- 變更需求先改 spec
- 每階段都做 checkpoint

---

### Step 1: `/speckit.specify`

目標：把需求寫清楚，含 user stories 與驗收條件

```text
建立一個單頁 Web 應用：台北市 YouBike 2.0 即時站點查詢器。
需求：抓取 API、名稱/地址搜尋、列表顯示站點資訊、低庫存警示。
```

---

### Step 1 檢查點

- `spec.md` 是否可讀
- user stories 是否完整
- 模糊詞是否被移除
- 驗收標準是否可測

---

### Step 2: `/speckit.plan`

目標：固定技術棧與實作策略

```text
技術要求：index.html + main.js，Tailwind CDN，
用 Fetch API，不用 React/Vue，資料處理與 DOM 分離。
```

---

### Step 2 檢查點

- `plan.md` 有明確架構
- 模組邊界清楚
- 錯誤處理策略清楚
- RWD 與可維護性有被提到

---

### Step 3: `/speckit.tasks`

目標：拆成可執行任務

1. HTML 結構與 Tailwind 初始化
1. API fetch 與 error handling
1. Search filter
1. 列表渲染
1. 最後 UI/RWD 調整

---

### Step 3 檢查點

- 任務可獨立完成
- 任務順序合理
- 每個任務可驗證
- 無超大顆任務

---

### Step 4: `/speckit.implement`

目標：照 `tasks.md` 順序實作

```text
請依 tasks.md 順序實作。
先做 API 抓取邏輯，完成後提醒我手動測試。
```

---

### Step 4 檢查點

- 是否真的按 tasks 順序
- 是否偷改未定義需求
- 是否有最小可運行版本
- 每次改動是否可回推到 spec

---

### 常見失敗模式

1. 還沒寫 spec 就進 implement
1. 規格改了但 tasks 沒更新
1. 規格太模糊，agent 自由發揮
1. 驗收放最後，回頭成本很高

---

### 修正策略

- 發現偏移先回 `spec.md`
- `plan.md` 改完再重生 tasks
- 小步快跑，每步都驗
- 不要硬救一個壞的 task tree

---

### Live Demo Flow

1. 用 4 步驟 prompt 走完一輪
1. 故意改需求一次
1. 展示如何只改 spec 再重跑
1. 驗收後收斂成可交付版本

---

### LAB Review

- 你今天不是在練 prompt
- 你在練「讓 agent 可預測」
- spec 是 source of truth
- checklist 是交付品質底線

---

### 你可以帶走的 3 件事

1. `/specify -> /plan -> /tasks -> /implement` 是可落地流程
1. 規格優先能降低返工成本
1. AI agent 要穩定，必須有 spec + evaluate loop

---

## LAB 時間

- 大家可以繼續做自己的專案
- 閱讀 [Spec-kit 的概念文件](https://github.com/github/spec-kit/blob/main/spec-driven.md)
- 或閱讀今天有提到的論文
- 模型語言偏見
  - [Do Multilingual LLMs Think In English](https://www.alphaxiv.org/abs/2502.15603)
  - [Better To Ask in English?](https://www.alphaxiv.org/abs/2504.20022)

---

### 可以做的更好的地方

- o11y: 監測模型行為，找出失效跟錯誤的原因
  - 下午的 Lab 歡迎參考：LLM O11y：從 Observability 到 Decision System
  - [專案連結與投影片我也放上來]()

---

### 參考資源

- Spec-kit: https://github.com/github/spec-kit
- Spec-driven: https://github.com/github/spec-kit/blob/main/spec-driven.md
- Workshop playground: https://github.com/chechiachang/speckit-playground
- Session: https://aienterprise.ithome.com.tw/2026/session/4788

---

## Thank you

喜歡這種內容歡迎來找我聊天

[chechia.net](https://chechia.net)
