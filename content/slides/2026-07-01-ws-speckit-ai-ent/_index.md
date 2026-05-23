---
title: "AI Enterprise Workshop: Spec-driven development with Spec-kit"
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
  - Azure API Key 填入講師提供的 Key (當天會提供，可以先填123）
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
  - ❓什麼是 maxInputTokens 與 maxOutputTokens❓

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

### Note

- Model 列表，選回去選擇其他 Model，可以先用免費版

---

### 最重要的行前準備: Mindset

- 講師不會總是對的，鼓勵懷疑簡報的內容
- 標記❓的地方，請練習懷疑/思考為什麼會有這個問題
- 先自己思考，再問 chatGPT
- 大部分時候chatGPT是對的，且性能優於講師
- 要知道怎麼確定 chatGPT 是對或錯的

> workshop 重點在累積動手的經驗

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
- 我們的目的：讓 Spec-kit 產生程式碼效果比 Vibe Coding 好
- 打開瀏覽器到 https://github.com/github/spec-kit#-get-started
- 打開 VS Code 與 Spec-kit playground 的範例程式碼

🔽

---

### LAB1: 初始化專案

```bash
# VS Code Terminal

specify init --here --integration copilot

Warning: Current directory is not empty (7 items)
Template files will be merged with existing content and may overwrite existing files
Do you want to continue? [y/N]: y

specify check
```

---

### LAB1: 初始化專案

- specify init 在當前資料夾建立 copilot 整合的 Spec-kit 檔案
  - Selected script type: sh or ps (Windows user 建議選 ps)
- 建立 .specify 資料夾，裡面有 specify agent 會用到的檔案
- .vscode/settings.json
  - 改成支援 Copilot Chat 的 prompt
  - ❓偷塞 chat.tools.terminal.autoApprove 給 .specify/scripts/bash/
- 🛠️ 打開 .specify/templates 資料夾，看一下裡面的內容
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
  - ❓為何要管理 context❓

```
/clear

/speckit.plan
/clear

/speckit.tasks
/clear

/speckit.implement
# implement 完成部分 task 後也可以 /clear
```
---

{{< slide background-image="specify-plan-tasks-implement.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

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
- Allow all commands in this workspace 是相對危險的，也會提高費用
- ❓根據 agent 控制力，以及失控的損害程度，決定 auto-approve

---

{{< slide background-image="auto-approve-constitution.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

### LAB1: 驗收執行

- agent implement 時產生程式碼，會一邊把 tasks 標記完成
- 當完成所有 tasks 後，就可以開始驗收了
- 這次 LAB1 我們先手動驗收
- 執行是否成功？有無 error？功能是否符合 spec？
- 實務上會把驗收標準，測試覆蓋率，lint，style，都寫進 Spec
  - 讓 agent 產生測試程式碼，來自動驗收

---

{{< slide background-image="manual-test.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

### LAB1: 錯誤處理

Spec-kit 的流程中，agent 會遇到各種錯誤，例如程式碼錯誤、測試失敗、驗收不過等等

- 如果錯誤是 Spec，請回到 /speckit.specify 修改 Spec
- 如果錯誤無關 Spec，例如程式碼錯誤，請讓 agent 修正程式碼
  - 提供錯誤訊息給 agent，讓 agent 可以根據錯誤訊息來修正程式碼
  - 提供驗證方法給 agent，讓 agent 可以自己驗證是否修正成功
  - ❓是否驗證方法或是測試覆蓋率，就需要寫在 Spec 中

---

{{< slide background-image="error-handling.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

### LAB1: Implementation

- Implementation 需要時間，大家可以邊觀察邊做其他事情
- agent 實作完（app 可以執行了）再回來驗收
- 我會利用這段時間講解
  - Spec-kit 的概念
  - 為什麼會比 Vibe Coding 有幫助
  - 適合什麼 use case

{{% /section %}}

---

{{% section %}}

### Spec-kit 是什麼

- Spec-driven Development toolkit
- 定義 script, template, checklist 等等，讓 agent 可預測地產生Spec
- 把 workflow 拆解成 spec plan tasks implement
- 讓 agent 依標準流程工作，先完成 spec，再 plan，再 tasks，最後 implement
- 每流程都有需要完成的 checkpoint，才會進入下一步
- 支援長任務、多輪對話 session

🔽

---

### 核心流程

```text
/specify -> /plan -> /tasks -> /implement
```

- SDD：先把需求寫成 Spec，Spec 是唯一 source of truth
- speckit：把 SDD 變成可執行流程（spec -> plan -> tasks -> implement），降低 drift 與返工成本
- 改需求先改 spec，不先改 code
- ❓為何先改需求，就會有幫助

---

### 為何有幫助

避免 Context rot，drift，Spec drift

- 對話 Vibe Coding 常見問題：一直持續聊到後面，agent 好像開始混亂了，聽不懂需求，一直來回做錯
  - context rot: llm 會忘記之前的對話內容，或是把之前的對話內容搞混，導致理解錯誤
  - context compact 後，agent 會「照比較新的對話」做事

{{% note %}}
「跟 llm 來回對話，一直補充資訊」，Spec 可能會越聊越清楚，也可能會越聊越模糊，到最後 llm 理解錯誤的需求，導致實作出來的東西不符合預期

「先產生 Spec」產生唯一的 source of truth，並持續修改，讓 agent 可以根據 Spec 來產生 Plan、Tasks、Implement，確保實作的東西是符合 Spec 的

「根據 Spec，有流程的產生程式」，透過分段實作或是拆分 task 來降低每次改動的成本，讓 agent 可以專注在當前的任務，而不是同時處理大量需求，帶來的額外複雜度
{{% /note %}}

---

### 為何會有幫助: Context management

- Vibe Chat 如果描述複雜的需求，容易產生 long context
- 但每個 llm 的 context window 都是有限的
- long context 可能造成 llm performance 下降
- long context 會需要 compact 來壓縮，可能會有資訊遺失。
- [VSCode Official Doc: Context Compaction](https://code.visualstudio.com/docs/copilot/chat/copilot-chat-context#_context-compaction)
  - ❓可能的不可控，會增加未來改善措施的難度（SOP 中要不要 compact 還是 clear）❓

---

### 為何會有幫助: 平行分工

- 複雜需求中，Vibe Coding 沒有一個明確的 checkpoint
  - 不易 review，Involve Human in the loop
  - 不易多人協作，或是拆分成多個任務
- 使用中間產物 Spec 檔案作為 source of truth
  - 讓其他 teammember 來 review
  - 根據 Spec 來產生 Plan、Tasks，進行平行分工
  - 最終產物是 Spec + Code。Spec 作為未來改動的基準
- 只有 Code 往往不足表達當初的需求細節

> 「誒我去年為何會這樣寫啊（問旁邊」

---

### Code 不是更精準的 Spec 展現嗎

- 過去 Code 為王，Coding 壁壘
  - Code 是最精確的需求表達，Spec 是服務 Code 的文件
- ai 時代 gen code 的速度，實現 Spec 的速度太快，成本太低
  - Spec 變成 executable spec
- Idea -> 產生 Spec -> 實作 Spec -> Spec 驗收交付 -> 上線
  - 整合服務根據 Spec 對接，而不是根據 Code 細節
  - 某個範圍內，相對不在乎 Code 是怎麼寫的

> 過去領先的 Code base，現在對手幾分鐘就 gen 出來。反而是 Spec 的優劣決定競爭力

---

### Code 逆向產生 Spec？

那我直接逆向工程產生 Spec 那不就可以繼續 SDD了嗎

- 實務上 code base 總量 token 會比 Spec 多
  - Spec -> Code 在 context window 內，Code -> Spec 就會超出 context window
  - 用相同等級的 model ，無法 Code to Spec
- Code 比較多行，不一定能讀到正確的資料夾，檔案，行數
- 失真：agent read 時會用 grep 跳著讀，有可能跳掉關鍵的邏輯

---

### SDD & Spec-kit

- Chat 是聊天，產出 Spec 是工程
- SDD 是方法
- speckit 是把方法落地，可重複執行 workflow 的工具

> Vibe Coding 就是療癒

---

### 為何用 nano or mini

```
# Prices per 1M tokens.
  ┌──────────────┬────────┬────────┬─────────┬────────┬────────┬─────────┐
  │ Model        │  Short │  Short │   Short │   Long │   Long │    Long │
  │              │  Input │ Cached │  Output │  Input │ Cached │  Output │
  │              │        │  Input │         │        │  Input │         │
  ├──────────────┼────────┼────────┼─────────┼────────┼────────┼─────────┤
  │ gpt-5.4      │  $2.50 │  $0.25 │  $15.00 │  $5.00 │  $0.50 │  $22.50 │
  │ gpt-5.4-mini │  $0.75 │ $0.075 │   $4.50 │      - │      - │       - │
  │ gpt-5.4-nano │  $0.20 │  $0.02 │   $1.25 │      - │      - │       - │
  │ gpt-5.4-pro  │ $30.00 │      - │ $180.00 │ $60.00 │      - │ $270.00 │
  └──────────────┴────────┴────────┴─────────┴────────┴────────┴─────────┘
# 只有 gpt-5.4 時，Spec-kit 請用 mini 或 nano
# Spec-kit 的核心流程（specify, plan, tasks）對於模型的能力要求不高
# 使用 mini 或 nano 就能達到 90% 的效果，但成本只有 10-20%，非常划算
```

https://developers.openai.com/api/docs/pricing

---

### 為何用 nano or mini

- nano 有 gpt-5.4 `90%+` 的 Coding/Tool-calling/Intelligence
  - Long context/MM/Vision/CUA 效能剩 `50%`
- Spec-kit Tax: 比起 Vibe Coding，Spec-Kit 流程有額外成本（Spec、Plan、Task、Implement 產生）
- 使用 nano 費用 10% 或 mini 費用 16.7% （假設使用相同 context)
  - Tradeoff: 不適合 Long Context (>272K tokens) 的任務
- 使用 gpt-5.4 來跑 long context，成本變兩倍，變成 nano 的 18-36 倍
  - 實務上應盡力控制 context
  - 用 5.4 來做 Spec，用 5.4-mini 來做 implement，兼顧品質與成本
  - ❓reasoning effort 應該如何設定？

https://openai.com/index/introducing-gpt-5-4-mini-and-nano/

{{% /section %}}

---

### 常見失敗模式

1. 還沒寫 spec 就進 implement
1. 規格改了但 tasks 沒更新
1. 規格太模糊，agent 自由發揮
1. 驗收放最後，回頭成本很高

---

### LAB Review

- 你今天不是在練 prompt
- 你在練「讓 agent 可預測」
- spec 是 source of truth
- checklist 是交付品質底線

---

### 你可以帶走的 3 件事

1. spec -> plan -> tasks -> implement 是可落地流程
1. 規格優先能降低返工成本
1. AI agent 要穩定，必須有 spec + 驗收標準 loop

---

### 回到 LAB

- 大家可以繼續做自己的專案
- 卡住很正常，先問 agent 為什麼卡住了
- 或閱讀今天有提到的論文
- 模型語言偏見
  - [Do Multilingual LLMs Think In English](https://www.alphaxiv.org/abs/2502.15603)
  - [Better To Ask in English?](https://www.alphaxiv.org/abs/2504.20022)
- [Spec-kit 的概念文件](https://github.com/github/spec-kit/blob/main/spec-driven.md)

---

### LAB 到最後 5 分鐘

```
/speckit.specify
/speckit.clarify # 問 agent 這是什麼
/speckit.plan
/speckit.analyze # 問 agent 這是什麼
/speckit.tasks
/speckit.implement
```

---

### 可以做的更好的地方

- o11y: 監測模型行為，找出失效跟錯誤的原因
  - 下午的 Lab 歡迎參考：LLM O11y：從 Observability 到 Decision System
  - [TODO] [專案連結與投影片我也放上來]()

---

### 參考資源

- Spec-kit: https://github.com/github/spec-kit
- Spec-driven: https://github.com/github/spec-kit/blob/main/spec-driven.md
- Workshop playground: https://github.com/chechiachang/speckit-playground
- Session: https://aienterprise.ithome.com.tw/2026/session/4788

---

## Thank you

[TODO] add link to 下午的 session https://aienterprise.ithome.com.tw/2026/lab/4790 與投影片永久網址

喜歡這種內容歡迎來找我聊天

[chechia.net](https://chechia.net)
