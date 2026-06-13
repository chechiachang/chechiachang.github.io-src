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

實際使用 Spec-kit 建立簡單的專案

讓大家體驗 Spec-driven Development

🔽

---

### Workshop 行前準備

- 攜帶筆電，可上網
- 安裝好操作環境
  - [VS Code](https://code.visualstudio.com/)
  - [Spec-kit CLI](https://github.com/github/spec-kit#1-install-specify-cli)
- 下載 [workshop 範例程式碼](https://github.com/chechiachang/speckit-playground)
- 講師會提供 Azure OpenAI API Key，也可帶自己習慣的 llm
- 已經會用 VS Code + GitHub Copilot Chat，用自己的方式參加即可

---

### VS Code

- 安裝 VS Code：[https://code.visualstudio.com/](https://code.visualstudio.com/)
- 打開 VS Code，底下 Terminal
  - git clone 程式碼 `speckit-playground`
  - File > Open Folder > 選擇 clone 的 speckit-playground

```bash
git clone https://github.com/chechiachang/speckit-playground.git
```
---

{{< slide background-image="git-clone.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

### 安裝 Spec-kit CLI

- 打開 VScode 下方的 Terminal
- 確認 uv 可用，沒有的話[先裝 uv](https://github.github.com/spec-kit/install/uv.html)
- 安裝 [Spec-kit CLI](https://github.github.com/spec-kit/installation.html#installation)

```bash
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
  - 跟 Azure say hi，預期沒填 api key 不可用
  - 選回去選擇其他 Model，可以先用免費版

```bash
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

### 最重要的行前準備: Mindset

- 先自己思考，再問 chatGPT
  - 大多時候chatGPT是對的，性能優於講師
- 如何確定 chatGPT 是對或錯的

> workshop 重點在累積動手的經驗

---

### Workshop 行前準備結束

- VSCode 已安裝
- Spec-kit CLI 已安裝
- VSCode 設定 model

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
1. 驗收、回顧、Q&A

---

{{% section %}}

### LAB1：第一個 Spec-kit 專案

還沒講什麼是 Spec-kit 之前，先讓大家實際體驗一次
- 先當 Spec-kit 是一個與 LLM 對話的工具，目標是產生程式碼
- 我們的目的：讓 Spec-kit 產生程式碼，且效果比 Vibe Coding 好
- 打開 VS Code 與 Spec-kit playground 的範例程式碼
- https://github.com/github/spec-kit#-get-started

🔽

---

### 核心流程

```bash
/specify -> /plan -> /tasks -> /implement
```

- SDD：先把需求寫成 Spec，Spec 是唯一 source of truth
- speckit：把 SDD 變成可執行流程（spec -> plan -> tasks -> implement），降低 drift 與返工成本
- 改需求先改 spec，不先改 code
- 為何先改需求，就會有幫助

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
- specify 初始化後
  - 建立 .specify 資料夾，裡面有 specify agent 會用到的檔案
  - .vscode/settings.json
  - 改成支援 Copilot Chat 的 prompt
  - 偷塞 chat.tools.terminal.autoApprove 給 .specify/scripts/bash/

```text
打開 .specify/templates 資料夾，看一下裡面的內容
在 Chat 中輸入 /spec 看看會發生什麼事
```

---

{{< slide background-image="specify-init-copilot.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

### LAB1: 建立 principles

```text
# 在 Chat 輸入指令，等待 copilot 生成憲法（Constitution）

# 今天 workshop LAB1 先用中文，比較好理解
/speckit.constitution 用zh-tw 專案建立憲法：規格從簡，程式簡潔，及早執行。

# 用英文 llm performance 會比較好，大概是 5-10% benchmark 提升（請見最後論文參考）
# 但如果英文會讓人類 performance 下降 10%，就請都用中文好了

# 看一下 .specify/memory/constitution.md 內容，是否滿意
# 如果不滿意，可以透過 chat 要求 copilot 修改，直到滿意為止
/speckit.constitution extreme compact constitution.
```

---

{{< slide background-image="specify-constitution.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

> constitution 是 agent 的行為準則，會在每次 agent 行動時被參考

---

### LAB1: 建立 Spec


```text
# 打開範例專案 example-ubike.md
# 如果你有準備其他題目，請用自己的題目
# agent 會產生 specs/001-branch-name/spec.md

# 清除之前的對話紀錄，讓 agent 從一個乾淨的狀態開始理解需求
/clear

/speckit.specify 建立一個單頁 Web 應用：台北市 YouBike 2.0 即時站點查詢器。
核心需求：
-  用 python + uv
-  自動從政府 API 抓取 JSON 站點資訊。https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json
-  搜尋框：可依據「站點地址」或「名稱」過濾。
-  列表呈現：站點名稱、可用車輛、剩餘空位。

# 其他需求可繼續補充
/speckit.specify ...

# 使用 clarify 檢查 Spec 是否有問題，或是有不清楚的地方
#   如果有，agent 會提出問題，讓你補充資訊
/speckit.clarify
```

---

{{< slide background-image="specify-spec.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

> SDD 要求 Spec 盡量接近最終需求，避免在實作過程中頻繁修改需求，導致返工成本增加

---

### LAB1: Auto-approve or Autopilot?

- 很快會感受到，如果每次都要 approve agent 想執行的 cmd，會非常卡
- 避免人類變成瓶頸，auto-approve 是需要的，但請注意安全性❗

```text
# 本 workshop 可以選擇 Auto Approve
#   VSCode Copilot 已設定基本 System Instruction：只允許本 workspace 資料夾的存取
#   （不允許存取本機其他目錄）

# 讓 agent 可以自動執行 cmd，不需要每次都問
Allow all commands in this session

# 或修改 settings.json 保留設定
# 檢視目前的 setting，放在 .vscode/settings.json
Allow running command `xxx` in this workspace

# 設定 auto-approve 的原則
#   允許 readonly: git, bash, grep, ...
#   write 只允許特定工具，arguments 也要限制

# 根據 agent 控制力，以及失控的損害程度，決定 auto-approve
```

---

{{< slide background-image="auto-approve-constitution.png" background-size="80%" background-color="#000000" background-opacity="1" >}}


---

### LAB1: Plan / Tasks / Implement

```text
# 清除之前的對話紀錄，讓 agent 從一個乾淨的狀態開始讀取 plan.md & tasks.md
#   可以每一步都清除一次，或是 agent 行為不符合預期時再清除
#   特別是 model 能力不足時（例如使用 nano），更需要頻繁清除，避免 context rot
/clear

# 在 Chat 輸入 /speckit.plan，讓 agent 根據 spec 產生實作計畫
#   預期會產生 specs/001-branch-name/plan.md
/speckit.plan

# 在 Chat 輸入 /speckit.tasks，讓 agent 根據 plan 產生實作任務
#   預期會產生 specs/001-branch-name/tasks.md
/speckit.tasks

# 在 Chat 輸入 /speckit.analyze，讓 agent 分析 plan 與 tasks 是否合理，是否有衝突
/speckit.analyze

# 根據分析結果，修改 plan 或是 tasks
#   不清楚的部分會導致 agent 實作出來的東西不符合預期，不建議直接進入 implement
#   可以直接請 agent 自己嘗試修復問題
根據建議修復

# 有調整後記得再次分析，看有無問題遺留
/speckit.analyze
```
---

{{< slide background-image="specify-analyze.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

```
# 確認 Spec、Plan、Tasks 都合理了之後，就可以開始實作了
# Agent 開始寫扣
/speckit.implement

# 實作過程中，agent 會持續根據 tasks.md 來產生程式碼，並且標記完成的 task
#   檢視實作過程中產生的程式碼，看看是否符合預期

# Agent 可能會做到一個段落就停下來，等待你確認是否繼續
繼續
# 或是直接讓 agent 自動繼續，直到完成
繼續直到完成可執行

# 完成後直接問 Agent 如何執行
如何執行
```
---

{{< slide background-image="specify-plan-tasks-implement.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

### 小結：Spec-kit 是什麼

- Spec-driven Development toolkit
- 定義 script, template, checklist 等等，讓 agent 可預測地產生Spec
- 把 workflow 拆解成 spec plan tasks implement
- 讓 agent 依標準流程工作，先完成 spec，再 plan，再 tasks，最後 implement
- 每流程都有需要完成的 checkpoint，才會進入下一步
- 支援長任務、多輪對話 session

---

### LAB1: Interruption & Error Handling

```text
# agent 會遇到困難卡住，或是有疑問，會在流程中問你
I can’t start implementing yet because the repo is currently on main, and Spec Kit requires a feature branch for this workflow.

# 檢視 agent 想要執行的 cmd，覺得合理的話選擇 allow
# 可以自己判斷或是再問 agent，或是直接叫 agent 自己決定

# 有些流程是 spec-kit 設定的，例如 Spec-Kit 會要求 branch name
Please create or switch to a feature branch for 001-youbike-station-search using one of these patterns:
# 可以使用 /speckit.git.feature 切換
/speckit.git.feature
```
---

{{< slide background-image="specify-git-feature.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

### LAB1: Interruption & Error Handling

```text
# Spec-kit 的流程中，agent 會遇到流程錯誤，導致走不下去
#   沒有滿足 plan 與 task，就無法 implement
#   沒有滿足 feature branch name 就無法 implement
# 可以請 agent 講 zh-tw 說明為什麼卡住了，該如何解決

# 某些情形會需要額外的清理
#   例如開了多個 spec/001 spec/002 資料夾與多個 feature branch
#   這時候可以請 agent 幫忙清理，或是自己手動刪除
#   「請協助 git reset spec 內容並清除 feature branch」
```

---

### LAB1: 驗收執行

- agent implement 時產生程式碼，會一邊把 tasks 標記完成
- 當完成所有 tasks 後，就可以開始驗收了
- 這次 LAB1 我們先手動驗收
- 執行是否成功？有無 error？功能是否符合 spec？
- 實務上會把驗收標準，測試覆蓋率，lint，style，都寫進 Spec
  - 讓 agent 產生測試程式碼，來自動驗收

```text
# 持續 implement 直到完成
/speckit.implement

# 新增新的 spec，或是修改 spec 來提高驗收標準
/speckit.specify 需要測試覆蓋率達到 80%，並且所有 lint 與 style 都必須通過
```

---

{{< slide background-image="manual-test.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

### LAB1: 錯誤處理

Spec-kit 的流程中，agent 會遇到各種錯誤，例如程式碼錯誤、測試失敗、驗收不過等等


```text

# 發現錯誤是 Spec，請回到修改 Spec，例如
/speckit.specify 改用xxx
/speckit.tasks

# 如果錯誤無關 Spec，例如程式碼錯誤，直接貼錯誤讓 agent 修正程式碼
# 例如發現網頁呈現不正確，直接把內容丟給 Chat agent
YouBike2.0_捷運科技大樓站
地址復興南路二段235號前
可用車輛0
剩餘空位0

# 或是
Error: xxx

# 提供驗證方法給 agent，讓 agent 可以自己驗證是否修正成功
# Spec-kit 會自動產生一些驗收需求，但需要人類去描述更精確的驗收需求
透過內建瀏覽器檢查網站內容

# 也可補充是否驗證要包含測試覆蓋率
/speckit.specify 需要測試覆蓋率達到 80%
```

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
  - 不可控會增加未來改善措施的難度

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

### SDD & Spec-kit

- Chat 是聊天，產出 Spec 是工程
- SDD 是方法
- speckit 是把方法落地，可重複執行 workflow 的工具

> Vibe Coding 就是療癒

---

### 為何用 nano or mini

```bash
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

https://openai.com/index/introducing-gpt-5-4-mini-and-nano/

{{% /section %}}

---

### 常見失敗模式

1. 還沒寫 spec 就進 implement
1. 規格改了但 tasks 沒更新
1. 規格太模糊，agent 自由發揮
1. 驗收放最後，回頭成本很高

---

### 你可以帶走的 3 件事

1. spec -> plan -> tasks -> implement 是可落地流程
1. 規格優先能降低返工成本
1. AI agent 要穩定，必須有 spec + 驗收標準 loop

---

### 回到 LAB，時間到最後 5 分鐘

- 大家可以繼續做自己的專案
- 卡住很正常，先問 agent 為什麼卡住了
- 或閱讀今天有提到的論文
- 模型語言偏見
  - [Do Multilingual LLMs Think In English](https://www.arxiv.org/abs/2502.15603)
  - [Better To Ask in English?](https://www.arxiv.org/abs/2504.20022)
- [Spec-kit 的概念文件](https://github.com/github/spec-kit/blob/main/spec-driven.md)

---

### 可以做的更好的地方

- 儘早引入 test suite、lint、pre-commit hooks、diff review
- o11y: 監測模型行為，找出失效跟錯誤的原因
  - 下午 Lab 歡迎參考：[LLM O11y：從 Observability 到 Decision System](../../posts/2026-07-01-ws-langfuse-ai-ent/)

---

### 參考資源

- Spec-kit: https://github.com/github/spec-kit
- Spec-driven: https://github.com/github/spec-kit/blob/main/spec-driven.md
- Workshop playground: https://github.com/chechiachang/speckit-playground
- Session: https://aienterprise.ithome.com.tw/2026/session/4788

---

## Thank you

下午歡迎參考
- Lab 13:30 - 15:00 [LLM O11y：從 Observability 到 Decision System](../../posts/2026-07-01-ws-langfuse-ai-ent/)
- Session: 15:30 - 16:00 [LLM O11y：從 Observability 到 Decision System](../../posts/2026-07-01-langfuse-ai-ent/)

喜歡這種內容歡迎來找我聊天

[chechia.net](https://chechia.net)
