# Slide Pages Pattern

Pattern observed from `wiki/slides/*.md` `## Pages (Section | Summary)`.

## Common Order

1. `(frontmatter)` metadata/transition page.
2. Cover/title.
3. Context (`About Me` or opening setup).
4. `Outline` / `大綱`.
5. Core content sections (concepts, issues, approaches).
6. Practical segment (`Demo`, workshop steps, tool usage).
7. Summary (`Summary` / `小結` / `總結` / `Takeaways` / `重點`).
8. Closing (`Q&A` / `Questions` / `Thank you` / `感謝`), often with hiring slide.

## Narrative Style

- Problem-first, then method, then implementation.
- Engineering flow: why -> what -> how -> operate -> conclude.
- Repeated section labels are intentional to reinforce progression.

## Overall Direction By Year

- 2019-2024: Kubernetes/platform infra heavy (Kafka, Vault, etcd, K8s operations, cost optimization).
- 2025: transition to AI + infra (`RAG`, `MCP`, `k8sgpt`) while keeping infra workshop tracks.
- 2026: AI engineering/systemization focus (`Spec-driven`, `LLM O11y`, `evaluation`, `decision system`).

## Notes For New Slide Outline

- Keep roadmap-first structure.
- Keep one practical section (demo or hands-on flow).
- End with explicit summary + Q&A.

## Useful snippets

Many code blocks are used for practical steps, commands, or code examples

```
```

Group pages if for a single topic or demo flow

{{% section %}}
---
Page 1
---
Page 1
---
{{% /section %}}
