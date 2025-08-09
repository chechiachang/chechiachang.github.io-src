---
title: "COSCUP 2025: 初探 Model Context Protocol 與 AI Agent Protocol：快速打造多工 AI Agent"
description: Model Context Protocol（MCP）是一項由 Anthropic 推出的開放標準，旨在為大型語言模型（LLMs）提供一種標準化的方式，以連接和操作各種資料來源（如本地檔案、資料庫）和工具（如 GitHub、Google Maps）。MCP 的目標是簡化 AI 應用與外部資源的整合過程，類似於 USB-C 為實體設備提供通用連接介面。隨著 AI 技術的快速發展，AI 助手需要與各種資料來源和工具進行互動，以提供更豐富和個性化的服務。Model Context Protocol（MCP）作為一種開放標準，為 AI 應用提供了一種統一的方式，連接到不同的資料來源和工具。本場演講將介紹 MCP 的架構、設計原則與實作範例，並展示如何使用開源 mcp-server 快速打造一套具備上下文共享、工具調用與多模型協作能力的 Agent Server。最後將透過實機 Demo 展現 MCP 在真實 AI Workflow 中的應用潛力。
tags: ["rag", "devops"]
categories: ["devops"]
date: '2025-08-01T00:45:00Z'
outputs: ["Reveal"]
reveal_hugo:
  custom_theme: "reveal-hugo/themes/robot-lung.css"
  margin: 0.2
  highlight_theme: "color-brewer"
  transition: "slide"
  transition_speed: "fast"
  templates:
    hotpink:
      class: "hotpink"
      background: "#FF4081"
---

#### COSCUP 2025
### 初探 MCP 與 AI Agent Protocol
##### 快速打造多工 AI Agent
##### ~ Che Chia Chang @ [chechia.net](https://chechia.net)🔗~

---

{{< slide content="slides.about-me" >}}

---

### 🤖 我們今天要聊什麼

- 開場先 **Demo** 一波！🚀🌕
- 什麼是 Model Context Protocol（MCP）
  - 為何需要 MCP
  - MCP 的內容 (Scope & Projects)
    - 規格
    - 如何使用（SDK & Development Tools）
- 用開源 mcp-server 打造多工 AI Agent
  - OpenAI Agent SDK
  - FastMCP

---

{{% section %}}

### Demo 🚀🌕
🔽

---

- 我寫了 main.py (~100Lines) [L26-L42](https://github.com/chechiachang/mcp-playground/blob/main/main.py#L26-L42)🔗接上 3 個 mcp-server
  - [yfinance-mcp](https://github.com/narumiruna/yfinance-mcp)
  - [firecrawl official mcp](https://github.com/mendableai/firecrawl-mcp-server)
  - [lymcp](https://github.com/narumiruna/ly-mcp) Open Fun LYAPI 立法院開放 api 2.0
- [FastMCP](https://github.com/jlowin/fastmcp/tree/main) framework 實做 MCP
  - 使用 decorator (@mcp.tool) 定義工具
  - FastMCP 會自動生成[符合 MCP 規格的 Tool](https://github.com/jlowin/fastmcp/blob/main/src/fastmcp/tools/tool.py#L133-L155)🔗
- client (main.py) 
  - 初始化時詢問 mcp-server list tools
  - query 時 LLM 決定要用哪個 tool

---

### Source Code

- [https://github.com/chechiachang/mcp-playground](https://github.com/chechiachang/mcp-playground)🔗
- [https://github.com/narumiruna/ly-mcp](https://github.com/narumiruna/ly-mcp)

---

### Notes

- 100 行程式碼就可以接上 3 個資料源
- Agent 內的 context 共用
  - ex. yfinance-mcp 可以查詢新聞，firecrawl-mcp 去爬新聞內容，爬完新聞再去查詢立法院的相關法案
- 調用 tool 時，LLM 會自動生成 request parameter

{{% /section %}}

---

### MCP 看起來是什麼？

- 不用寫扣就可以透過 mcp-server 接上資料源 api ❌
  - 這是 mcp-server 提供的 tool 功能，不是 MCP 本身❌
  - MCP 提供 SDK 可以開發符合標準的 mcp-server ✅
- 從 FastMCP 來看，MCP 定義了 tool, prompt, context 的結構 ✅
  - 這些結構可以被 LLM 使用 (ex. LLM 可以 list tools, read context)
- 上面的 context 可以於 OpenAI Agent SDK 中無縫使用 ✅
  - 其他 LLM SDK 也可以接上

---

### Tool vs MCP

- 現在 ChatGPT 也會使用 tool 如 function calling, WebSearch, File Search, ...，這些都是 OpenAI tool 的實作。
- MCP 不是提供 tool，而是提供一個統一的標準，讓 LLM 可以使用這些 tool 產生的結果，格式是統一的。
- 由於是統一的標準，各家 LLM 與資料源才會覺得「我只要做一套，全世界都可以用」所以才爆炸性的產生一堆 MCP server。

> 換句話說：因為有 USB 存在，各家硬體廠商才會覺得「我只要做一套 USB 接口，所有人都可以用」，所以才會有 USB 可以支援超多功能的感覺。

---

爆炸性的 mcp-server [https://github.com/modelcontextprotocol/servers/pulse](https://github.com/modelcontextprotocol/servers/pulse)🔗

![](images/2025-mcp-servers.jpeg)

---

{{% section %}}

### MCP 是什麼？

- [https://modelcontextprotocol.io/docs/learn/architecture](https://modelcontextprotocol.io/docs/learn/architecture)
- Anthropic 推出的開放標準
- 給大型語言模型（LLM）用的
- 用來「統一描述上下文 + 工具 + 記憶」
- 有點像是 LLM 的操作系統 API
🔽

---

### 為何需要MCP？🤔

---

### 不用 MCP 時

LLM 都有自己的 context 與 tool 格式，context 要自己整理

- 上古時代(2023) context 想怎麼寫就怎麼寫，曾流行把 context 塞進 prompt，然後再 prompt compression
- [OpenAI Agent SDK](https://openai.github.io/openai-agents-python/context/) 的 context management 建議用 Wrapper 包一層，調用 function tool 時傳入
- [FastMCP 提供更通用的 context 功能](https://gofastmcp.com/servers/context)
  - context 統一格式傳入 tool，讓 LLM 可以讀取
  - 包含 Logging, Progress, State, Request metadata, Server metadata,...
  - 只記得 response.text vs 記得 context 的差別🤔

---

### 透過 MCP 整合資料源

```
without-mcp/
├── main.py
├── openai/
│   ├── mysql.py
│   ├── ...
│   └── github.py
├── gemini/
│   ├── mysql.py
│   ├── ...
│   └── github.py
```

- 如果你是 LLM 提供者，要為每一個資料源API 寫一套接法，處理 api request 與 response 到 context
- 如果你是資料庫開發者，要為每一個 LLM 寫一套 sdk 
- 然後上面都沒有提供的話，使用者就要自己維護 LLM x 資料庫數量的程式碼🤮
- LLM 改版就要跟著改（不然沒有新功能直接變成上古時代🦖
  - 資料源(ex. GitHub)的 API 不會常大改，但 LLM 是急速更新🚀

{{% /section %}}

---

### 為什麼需要 MCP？

- context, prompt, tool, ... 都定義在規格中
- [MCP 的內容](https://modelcontextprotocol.io/specification/2025-06-18)
- Transport：如何傳輸 MCP context
- Schema
  - Resources (Context + data)
  - 什麼是 Server, Client, Tool, TextContext, AudioContext, [Prompt](https://modelcontextprotocol.io/specification/2025-06-18/schema#prompt) 🔗, Request, Response, ...
  - tools/call, tools/list
- Security and Trust & Safety

---

### 說白話一點

- [OpenAI: The Model context protocol (aka MCP) is a way to provide tools and context to the LLM.](https://openai.github.io/openai-agents-python/mcp/)

- [Gemini: Model Context Protocol (MCP) 是一項開放標準，可將 AI 應用程式連結至外部工具和資料。MCP 提供通用協定，供模型存取內容，例如函式 (工具)、資料來源 (資源) 或預先定義的提示。](https://ai.google.dev/gemini-api/docs/function-calling?hl=zh-tw&example=meeting#mcp)

---

### MCP 解決哪些痛點？

- 🔥 prompt, tool, resource 太亂 → 結構化表示
- 🤹‍♀️ 多任務切換 → 上下文一致
- 🛠️ 各步驟間 interface 接得很統一，不再 hardcode

---

### MCP 如何使用？

- LLM 提供商：OpenAI agent sdk 與 gemini sdk 都支援 MCP
  - 開源 LLM frameworks（如 LangChain, LlamaIndex）也支援 MCP
- 許多資料源提供商都支援 MCP
- 使用者直接使用
  - LLM sdk 或 LLM frameworks
  - official 資料源 MCP server
  - [MCP offifial sdk](https://modelcontextprotocol.io/docs/sdk) 寫 client 或 server

---

### 無情工商，超缺人

#福利佳 #薪優 #成長性高 #公司賺錢

![](./we-re-hiring.png)

> 想當個 sre，或是想當個會 MCP 的 sre 嗎？這邊都可以實現

---

### Demo 🚀🌕

---

{{% section %}}

### 什麼是 AI Agent Protocol？

- 一組設計模式
- 把 MCP context 拿去 dispatch 給適合的 agent
- Agent 間可以互相協作，完成一整個 workflow
🔽

---

### MCP 和 Agent Protocol 的關係

- MCP 是「一個 agent 的說明書」
- Agent Protocol 是「多個 agent 怎麼互動」
- MCP 負責上下文、Agent Protocol 負責流程

---

### 小結一下概念差異
| 概念 | 負責的事 |
|------|-----------|
| MCP | 一個 agent 的角色 + 工具 + 任務 |
| Agent Protocol | 多個 agent 的協作 + 任務分派 |

{{% /section %}}

---

### 小結 ✨

- MCP 是 AI 應用的通用「上下文 + 工具」描述法
- Agent Protocol 幫你 orchestrate 多個 Agent
- 用 mcp-server 可以快速打通各種 LLM + 工具實作出一套原型

---

### 延伸閱讀 & 原始碼

- MCP：[https://modelcontextprotocol.io/specification/2025-06-18](https://modelcontextprotocol.io/specification/2025-06-18)
- 開源實作：[https://github.com/chechiachang/mcp-playground/tree/main](https://github.com/chechiachang/mcp-playground/tree/main)
- 投影片與講稿：[https://chechia.net](https://chechia.net)

---

### 感謝大家 🙌
- 現場 Q&A 時間
- 喜歡這種內容歡迎來找我聊天！

---

### 無情工商，超缺人

#福利佳 #薪優 #成長性高 #公司賺錢

![](./we-re-hiring.png)
