# LLM O11y：從 Observability 到 Decision System

- Source: `content/slides/2026-07-01-langfuse-ai-ent/_index.md`
- Slide: `https://chechia.net/slides/2026-07-01-langfuse-ai-ent/`
- Date: `2026-05-02T15:30:00Z`
- Tags: `llm, agent, observability, langfuse, evaluation, aiops`
- Categories: `aiops, observability`
- Description: `30 分鐘分享，從 Langfuse observability 出發，補上 evaluation、dataset、regression 與 decision gate，建立可落地的 LLM Decision System。`

## Pages (Section | Summary)

1. `(frontmatter)` | Frontmatter metadata for reveal-hugo settings and slide metadata.
2. `LLM O11y：從 Observability 到 Decision System` | 30 分鐘分享的標題與主題定位。
3. `痛點` | AI 工具很多，但缺的是數據化決策。
4. `今天的大綱` | 依照痛點、解法、效率定義與逐步收斂變因展開。
5. `需求` | 想要的是 Coding Agent 效能更好、更穩定、成本可控。
6. `解法` | 先落實 o11y，觀測 prompt、response、tool call 與成本。
7. `什麼叫效率` | 先把 AI 產出公式講清楚。
8. `變因太多` | model、instruction、tools、workload 與 evaluation 都會影響結果。
9. `先做 baseline` | Action 0：先收 tracing，建立 workload baseline。
10. `Langfuse 可以看什麼` | 以 Langfuse 收集 metadata 與 metrics。
11. `Action 1` | 先精簡 Agent tools usage 與 instruction。
12. `Action 2` | 用 llm-as-a-judge 做快速 evaluation。
13. `Issue` | multi-turn agent 很難直接評估。
14. `Action 3` | 用 observation 評估單一步驟，先縮小評估範圍。
15. `Dataset` | 從 daily work tracing 生成 input / output dataset。
16. `Action 4` | 用 dataset 做 experiment，比較不同變因。
17. `Human Decision` | 最後仍然要人做決定與負責。
18. `核心結論` | 流程要從觀測走到收斂、評估、實驗與人類決策。
19. `LLM O11y 的本質` | 這不是 logging tool，而是 feedback control system。
20. `Q&A` | 收尾，帶出下一步工程化方向。

## Time-to-Syntax

- Markdown:
- `p7:code-fence`
- Hugo shortcode:
- none.
- Reveal-hugo syntax:
- none.

## Time-to-Sentence

- Markdown:
- `p1:title: "LLM O11y：從 Observability 到 Decision System"`
- `p1:description: "30 分鐘分享，從 Langfuse observability 出發，補上 evaluation、dataset、regression 與 decision gate，建立可落地的 LLM Decision System。"`
- `p1:tags: ["llm", "agent", "observability", "langfuse", "evaluation", "aiops"]`
- `p3:AI 工具很多，選擇也很多。`
- `p4:1. 痛點：AI 工具的抉擇，缺乏數據化決策`
- `p5:我們想要的其實很直接：`
- `p6:### 落實 o11y，觀測所有`
- `p7:efficiency = useful output / time / cost / iteration`
- `p8:model 版本`
- `p9:trace -> baseline`
- `p10:trace`
- `p11:先精簡 Agent。`
- `p12:用 llm-as-a-judge 做快速 evaluation。`
- `p13:multi-turn agent 很難直接評估。`
- `p14:用 llm-as-a-judge 先評估觀測到的單一步驟`
- `p15:從 daily work tracing 生成 dataset。`
- `p16:model 5.4 -> 5.5`
- `p17:最後還是要人做決定。`
- `p18:流程要變成：`
- `p19:它是一個 AI 系統的 feedback control system。`
- `p20:如果你們現在已經有 Langfuse 或 tracing，但還缺決策流程，下一步就是把 baseline、judge、dataset 和 experiment 接起來。`
- Hugo shortcode:
- none.
- Reveal-hugo syntax:
- none.
