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

1. 攜帶筆電，可上網
1. 安裝好操作環境
    1. [VS Code](https://code.visualstudio.com/) + [Codex Extension](https://developers.openai.com/codex/ide#extension-setup)
    1. [Spec-kit CLI](https://github.com/github/spec-kit#1-install-specify-cli)
1. 下載 [workshop 範例程式碼](https://github.com/chechiachang/speckit-playground)
1. 講師會提供 Azure OpenAI API Key，也可帶自己習慣的 llm
1. 已經會用 VS Code + Codex，用自己的方式參加即可

🔽

---

### VS Code

- 安裝 VS Code：[https://code.visualstudio.com/](https://code.visualstudio.com/)
  - Terminal 或命令提示字元開啟 VS Code
- VS Code 中
  - git clone 程式碼 `speckit-playground`
  - 開啟資料夾

```
code .

git clone https://github.com/chechiachang/speckit-playground.git

# File > Open Folder > 選擇 clone 的 speckit-playground
```

---

{{< slide background-image="git-clone.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

### VS Code Extension

1. 安裝 Codex Extension
  1. https://developers.openai.com/codex/ide#extension-setup
  1. cmd + shift + x，搜尋 Codex，安裝
1. 在 VS Code 右側 Secondary Sidebar 找到 Codex
  1. 跟 Codex say hi，使用免費額度，或登入個人的 OpenAI 帳號

- 認明官方網址，其他來源的 extension 可能不安全
- Codex – OpenAI’s coding agent
- OpenAI 打勾勾 openai.com 下載 8,885,127 評價(377)

---

{{< slide background-image="install-codex-extension.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

### 安裝 Spec-kit CLI

1. 打開 VScode 下方的 Terminal
1. 確認 uv 可用，沒有的話[先裝 uv](https://github.github.com/spec-kit/install/uv.html)
1. 安裝 [Spec-kit CLI](https://github.github.com/spec-kit/installation.html#installation)

```
# 確認 uv 可用
uv --version

# 安裝指定穩定版（建議：把 vX.Y.Z 換成最新 release tag）
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v0.8.9
```

---

{{< slide background-image="install-specify-cli.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

### Workshop 行前完成
{{% /section %}}

---

{{% section %}}

### API Key 設定

1. 備份原本的 config.toml，以免覆蓋到自己的設定
1. codex-config.toml 複製到 codex 的 config.toml

```
cp ~/.codex/config.toml ~/.codex/config.toml.bak

cp codex-config.toml ~/.codex/config.toml
```

{{% note %}}

1. 打開檔案 `speckit-playground/codex-config.toml`
1. 全選複製
1. VS Code Extension 右上角齒輪 > Codex settings
1. Configuration > Open config.toml
1. 貼上複製的內容，存檔
1. 如果已經有自己的 config.toml，請把內容貼在檔案的上面

{{% /note %}}

🔽

---

{{< slide background-image="copy-config-toml.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

```
# 關掉 VS Code，重新用 Terminal 開啟，讓環境變數生效

export AZURE_OPENAI_API_KEY="講師提供的 api key"

# 啟動 vscode
code .
```
---

### VS Code Extension: Linux/MacOS

1. cmd + space，輸入 Terminal，開啟終端機

```
export AZURE_OPENAI_API_KEY="講師提供的 api key"
code .
```

---

{{< slide background-image="export-and-code.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

### VS Code Extension: Windows

1. Win + R，輸入 cmd，開啟命令提示字元

```
set AZURE_OPENAI_API_KEY="講師提供的 api key"
code .
```

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

1. 講解：什麼是Spec-kit
1. LAB：第一個 Spec-kit 專案
1. 講解：為什麼不 Vibe Coding
1. LAB：YouBike 2.0 需求到實作
1. 講解：Spec-kit 經驗分享，適合與不適合的 use case
1. LAB：YouBike 2.0 需求到實作
1. 驗收、回顧、Q&A

---

### 今天我們要做一件事

把「跟 llm 來回對話，一直補充資訊」
變成
「先產生 Spec，根據 Spec，有流程的產生程式」

---

### 什麼是Spec-kit

---

### 如何進行 workshop

- 講師在台上示範
- 參與者跟著做，或超前也可以
- 卡住很正常，先記錄問題
- 我們先求跑通，再求漂亮

---

### 先定義問題

- LLM 很會補 pattern
- 但不會讀你的腦
- Prompt 是聊天
- Spec 是工程

---

### Vibe Coding 常見狀況

- looks right, but does not quite work
- 同一需求每次改法不同
- QA 才發現需求漏掉
- 上線後才補規格

---

### SDD 在解什麼

- 把需求變成可檢查文件
- 把實作順序固定下來
- 把驗收條件前移
- 把 agent 行為限制在 spec 內

---

### Spec-kit 是什麼

- 一套 Spec-driven Development toolkit
- 提供 `/specify` `/plan` `/tasks` `/implement`
- 讓 agent 依規格工作
- 支援長任務、多輪迭代

---

### 核心流程

```text
/specify -> /plan -> /tasks -> /implement
```

- 每一步都可回頭調整
- 改需求先改 spec，不先改 code

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

### 環境準備（Spec-kit）

Option 1: Persistent installation（推薦）

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v0.8.9
specify version
```

---

### 初始化專案

```bash
specify init --here --integration codex
# 或
specify init --here --integration copilot

specify check
```

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

### 憲法（Constitution）在做什麼

`/speckit.constitution`

- 設定命名規範
- 設定錯誤處理底線（例如必須 `try-catch`）
- 設定團隊共識，避免每次重講

---

### 憲法範例

- 變數命名使用 `camelCase`
- 所有資料抓取都要有 `try-catch`
- 不允許 silent failure
- UI 錯誤訊息要可見

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

### Demo Command Cheat Sheet

```bash
specify version
specify check

# 在 agent 中
/speckit.specify
/speckit.plan
/speckit.tasks
/speckit.implement
/speckit.analyze
/speckit.checklist
```

---

### 進度落後怎麼辦

- 先完成 Step 1 + Step 2
- Step 3 可先用最小任務集合
- Step 4 先完成核心功能
- UI polish 放最後

---

### 驗收（Analyze）

`/speckit.analyze`

- 看與 spec 的差距
- 看風險與遺漏
- 看是否需要回到 plan/tasks

---

### 驗收（Checklist）

`/speckit.checklist`

- 功能是否對齊需求
- 錯誤處理是否完整
- 邊界條件是否覆蓋
- 是否準備好 demo / 交付

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

### 參考資源

- Spec-kit: https://github.com/github/spec-kit
- Spec-driven: https://github.com/github/spec-kit/blob/main/spec-driven.md
- Workshop playground: https://github.com/chechiachang/speckit-playground
- Session: https://aienterprise.ithome.com.tw/2026/session/4788

---

### 延伸作業

1. 把自己的題目寫成 100-200 字需求
1. 用同一流程做第 2 個小專案
1. 加一條 constitution 規範，再跑一輪

---

## Q&A

有問題先問 AI
再來問我

---

## Thank you

喜歡這種內容歡迎來找我聊天

[chechia.net](https://chechia.net)

