# COSCUP 2025: 初探 Model Context Protocol 與 AI Agent Protocol：快速打造多工 AI Agent

- Source: `content/slides/2025-08-09-coscup-mcp-agent/_index.md`
- Slide: `https://chechia.net/slides/2025-08-09-coscup-mcp-agent/`
- Date: `2025-08-01T00:45:00Z`
- Tags: `rag, devops`
- Categories: `devops`
- Description: `Model Context Protocol（MCP）是一項由 Anthropic 推出的開放標準，旨在為大型語言模型（LLMs）提供一種標準化的方式，以連接和操作各種資料來源（如本地檔案、資料庫）和工具（如 GitHub、Google Maps）。MCP 的目標是簡化 AI 應用與外部資源的整合過程，類似於 USB-C 為實體設備提供通用連接介面。隨著 AI 技術的快速發展，AI 助手需要與各種資料來源和工具進行互動，以提供更豐富和個性化的服務。Model Context Protocol（MCP）作為一種開放標準，為 AI 應用提供了一種統一的方式，連接到不同的資料來源和工具。本場演講將介紹 MCP 的架構、設計原則與實作範例，並展示如何使用開源 mcp-server 快速打造一套具備上下文共享、工具調用與多模型協作能力的 Agent Server。最後將透過實機 Demo 展現 MCP 在真實 AI Workflow 中的應用潛力。`

## Pages (Section | Summary)

1. `(frontmatter)` | Frontmatter metadata for reveal-hugo settings and slide metadata.
2. `COSCUP 2025` | COSCUP 2025
3. `(frontmatter)` | No textual content.
4. `🤖 我們今天要聊什麼` | 🤖 我們今天要聊什麼
5. `Demo 🚀🌕` | Demo 🚀🌕
6. `(frontmatter)` | 我寫了 main.py (~100Lines) L26-L42🔗接上 3 個 mcp-server
7. `Source Code` | Source Code
8. `Notes` | Notes
9. `MCP 看起來是什麼？` | MCP 看起來是什麼？
10. `Tool vs MCP` | Tool vs MCP
11. `(frontmatter)` | 爆炸性的 mcp-server https://github.com/modelcontextprotocol/servers/pulse🔗
12. `MCP 是什麼？` | MCP 是什麼？
13. `為何需要MCP？🤔` | 為何需要MCP？🤔
14. `不用 MCP 時` | 不用 MCP 時
15. `透過 MCP 整合資料源` | 透過 MCP 整合資料源
16. `為什麼需要 MCP？` | 為什麼需要 MCP？
17. `說白話一點` | 說白話一點
18. `MCP 解決哪些痛點？` | MCP 解決哪些痛點？
19. `MCP 如何使用？` | MCP 如何使用？
20. `無情工商，超缺人` | 無情工商，超缺人
21. `Demo 🚀🌕` | Demo 🚀🌕
22. `什麼是 AI Agent Protocol？` | 什麼是 AI Agent Protocol？
23. `MCP 和 Agent Protocol 的關係` | MCP 和 Agent Protocol 的關係
24. `小結一下概念差異` | 小結一下概念差異
25. `小結 ✨` | 小結 ✨
26. `延伸閱讀 & 原始碼` | 延伸閱讀 & 原始碼
27. `感謝大家 🙌` | 感謝大家 🙌
28. `無情工商，超缺人` | 無情工商，超缺人

## Time-to-Syntax

- Markdown:
- `p2:link`
- `p6:link`
- `p7:link`
- `p11:image`
- `p11:link`
- `p12:link`
- `p14:link`
- `p15:code-fence`
- `p16:link`
- `p17:link`
- `p19:link`
- `p20:image`
- `p24:table`
- `p26:link`
- `p28:image`
- Hugo shortcode:
- `p3:{{< slide content="slides.about-me" >}}`
- `p5:{{% section %}}`
- `p8:{{% /section %}}`
- `p12:{{% section %}}`
- `p15:{{% /section %}}`
- `p22:{{% section %}}`
- `p24:{{% /section %}}`
- Reveal-hugo syntax:
- none.

## Time-to-Sentence

- Markdown:
- `p1:title: "COSCUP 2025: 初探 Model Context Protocol 與 AI Agent Protocol：快速打造多工 AI Agent"`
- `p1:description: Model Context Protocol（MCP）是一項由 Anthropic 推出的開放標準，旨在為大型語言模型（LLMs）提供一種標準化的方式，以連接和操作各種資料來源（如本地檔案、資料庫）和工具（如 GitHub、Google Maps）。MCP 的目標是簡化 AI 應用與外部資源的整合過程，類似於 USB-C 為實體設備提供通用連接介面。隨著 AI 技術的快速發展，AI 助手需要與各種資料來源和工具進行互動，以提供更豐富和個性化的服務。Model Context Protocol（MCP）作為一種開放標準，為 AI 應用提供了一種統一的方式，連接到不同的資料來源和工具。本場演講將介紹 MCP 的架構、設計原則與實作範例，並展示如何使用開源 mcp-server 快速打造一套具備上下文共享、工具調用與多模型協作能力的 Agent Server。最後將透過實機 Demo 展現 MCP 在真實 AI Workflow 中的應用潛力。`
- `p2:初探 MCP 與 AI Agent Protocol`
- `p2:~ Che Chia Chang @ chechia.net🔗~`
- `p6:我寫了 main.py (~100Lines) L26-L42🔗接上 3 個 mcp-server`
- `p6:lymcp Open Fun LYAPI 立法院開放 api 2.0`
- `p8:調用 tool 時，LLM 會自動生成 request parameter`
- `p9:MCP 看起來是什麼？`
- `p9:這是 mcp-server 提供的 tool 功能，不是 MCP 本身❌`
- `p9:MCP 提供 SDK 可以開發符合標準的 mcp-server ✅`
- `p9:從 FastMCP 來看，MCP 定義了 tool, prompt, context 的結構 ✅`
- `p9:這些結構可以被 LLM 使用 (ex. LLM 可以 list tools, read context)`
- `p10:現在 ChatGPT 也會使用 tool 如 function calling, WebSearch, File Search, ...，這些都是 OpenAI tool 的實作。`
- `p10:MCP 不是提供 tool，而是提供一個統一的標準，讓 LLM 可以使用這些 tool 產生的結果，格式是統一的。`
- `p10:由於是統一的標準，各家 LLM 與資料源才會覺得「我只要做一套，全世界都可以用」所以才爆炸性的產生一堆 MCP server。`
- `p10:> 換句話說：因為有 USB 存在，各家硬體廠商才會覺得「我只要做一套 USB 接口，所有人都可以用」，所以才會有 USB 可以支援超多功能的感覺。`
- `p12:MCP 是什麼？`
- `p14:LLM 都有自己的 context 與 tool 格式，context 要自己整理`
- `p14:上古時代(2023) context 想怎麼寫就怎麼寫，曾流行把 context 塞進 prompt，然後再 prompt compression`
- `p14:OpenAI Agent SDK 的 context management 建議用 Wrapper 包一層，調用 function tool 時傳入`
- `p14:包含 Logging, Progress, State, Request metadata, Server metadata,...`
- `p14:只記得 response.text vs 記得 context 的差別🤔`
- `p15:│ ├── ...`
- `p15:│ ├── ...`
- `p15:如果你是 LLM 提供者，要為每一個資料源API 寫一套接法，處理 api request 與 response 到 context`
- `p15:資料源(ex. GitHub)的 API 不會常大改，但 LLM 是急速更新🚀`
- `p16:為什麼需要 MCP？`
- `p16:什麼是 Server, Client, Tool, TextContext, AudioContext, Prompt 🔗, Request, Response, ...`
- `p17:OpenAI: The Model context protocol (aka MCP) is a way to provide tools and context to the LLM.`
- `p17:Gemini: Model Context Protocol (MCP) 是一項開放標準，可將 AI 應用程式連結至外部工具和資料。MCP 提供通用協定，供模型存取內容，例如函式 (工具)、資料來源 (資源) 或預先定義的提示。`
- `p18:MCP 解決哪些痛點？`
- `p18:🔥 prompt, tool, resource 太亂 → 結構化表示`
- `p19:MCP 如何使用？`
- `p19:LLM 提供商：OpenAI agent sdk 與 gemini sdk 都支援 MCP`
- `p19:開源 LLM frameworks（如 LangChain, LlamaIndex）也支援 MCP`
- `p19:MCP offifial sdk 寫 client 或 server`
- `p20:> 想當個 sre，或是想當個會 MCP 的 sre 嗎？這邊都可以實現`
- `p22:什麼是 AI Agent Protocol？`
- `p22:把 MCP context 拿去 dispatch 給適合的 agent`
- `p24:| MCP | 一個 agent 的角色 + 工具 + 任務 |`
- `p24:| Agent Protocol | 多個 agent 的協作 + 任務分派 |`
- `p25:MCP 是 AI 應用的通用「上下文 + 工具」描述法`
- `p25:Agent Protocol 幫你 orchestrate 多個 Agent`
- `p25:用 mcp-server 可以快速打通各種 LLM + 工具實作出一套原型`
- `p27:喜歡這種內容歡迎來找我聊天！`
- Hugo shortcode:
- `p3:{{< slide content="slides.about-me" >}}`
- `p5:{{% section %}}`
- `p8:{{% /section %}}`
- `p12:{{% section %}}`
- `p15:{{% /section %}}`
- `p22:{{% section %}}`
- `p24:{{% /section %}}`
- Reveal-hugo syntax:
- none.
