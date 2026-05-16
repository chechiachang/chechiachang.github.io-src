# LLM O11y：從 Observability 到 Decision System

- Source: `content/slides/2026-07-01-langfuse-ai-ent/_index.md`
- Slide: `https://chechia.net/slides/2026-07-01-langfuse-ai-ent/`
- Date: `2026-07-02T15:30:00Z`
- Tags: `llm, agent, observability, langfuse, evaluation, aiops`
- Categories: `aiops, observability`
- Description: `從 Langfuse observability 出發，補上 evaluation、dataset、regression 與 decision gate，建立可落地的 LLM Decision System。`

## Pages (Section | Summary)

1. `(frontmatter)` | Frontmatter metadata for reveal-hugo settings and slide metadata.
2. `LLM O11y：從 Observability 到 Decision System` | LLM O11y：從 Observability 到 Decision System
3. `核心問題` | 核心問題
4. `Goals` | Goals
5. `現況問題：我們其實在用「感覺」做決策` | 現況問題：我們其實在用「感覺」做決策
6. `關鍵誤解` | 關鍵誤解
7. `LLM-as-a-judge：有用，但有限` | LLM-as-a-judge：有用，但有限
8. `正確做法：建立 feedback system` | 正確做法：建立 feedback system
9. `Observability（發生了什麼）` | 1. Observability（發生了什麼）
10. `Evaluation（好不好）` | 2. Evaluation（好不好）
11. `Dataset（從 production 來）` | 3. Dataset（從 production 來）
12. `Regression（關鍵缺口）` | 4. Regression（關鍵缺口）
13. `Decision（真正價值）` | 5. Decision（真正價值）
14. `LLM SLO（工程化核心）` | LLM SLO（工程化核心）
15. `Failure Taxonomy（讓 debug 可控）` | Failure Taxonomy（讓 debug 可控）
16. `為什麼現在工具還不夠` | 為什麼現在工具還不夠
17. `LLM O11y 的定位（PoC）` | LLM O11y 的定位（PoC）
18. `核心結論` | 核心結論
19. `最終訊息` | 最終訊息
20. `LLM O11y 的本質` | LLM O11y 的本質

## Time-to-Syntax

- Markdown:
- `p8:code-fence`
- Hugo shortcode:
- none.
- Reveal-hugo syntax:
- none.

## Time-to-Sentence

- Markdown:
- `p1:title: "LLM O11y：從 Observability 到 Decision System"`
- `p1:description: "從 Langfuse observability 出發，補上 evaluation、dataset、regression 與 decision gate，建立可落地的 LLM Decision System。"`
- `p1:tags: ["llm", "agent", "observability", "langfuse", "evaluation", "aiops"]`
- `p2:LLM O11y：從 Observability 到 Decision System`
- `p3:目前多數團隊在導入 LLM / AI Agent 時，已經具備：`
- `p3:各種 agent framework（LangChain / AutoGen / 各種新 repo）`
- `p3:> 這次 model 或 framework 升級，到底該不該上 production？`
- `p4:control llm -> do exactly what we want`
- `p4:control cost -> avoid unexpected cost increase`
- `p6:trace（prompt / response / tool calls）`
- `p6:> 發生了什麼？`
- `p6:> 我應不應該改？`
- `p6:> 這個改動是不是變好？`
- `p7:有 bias（偏好 verbose / certain patterns）`
- `p7:> LLM judge 是 heuristic，不是 truth`
- `p8:observability -> evaluation -> dataset -> regression -> decision`
- `p11:trace -> detect failure -> promote to dataset`
- `p19:Evaluation tells you how good it is`
- `p19:Regression tells you if it got better`
- `p19:Decision tells you what to do`
- `p20:一個 AI 系統的 feedback control system`
- Hugo shortcode:
- none.
- Reveal-hugo syntax:
- none.
