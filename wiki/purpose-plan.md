# Wiki Purpose Plan

## Purpose

Turn `content/slides/*` into a maintainable, query-friendly knowledge base for talks, workshops, and reusable platform engineering guidance.

## Target Users

- You (author): quickly reuse past material when preparing new talks.
- Collaborators: find canonical slide references by topic.
- LLM agents: answer questions from structured wiki pages instead of raw slide markdown.

## Success Criteria

- Every slide deck has one wiki note in `wiki/slides/`.
- `wiki/index.md` stays topic-oriented and current.
- Answers can be generated from wiki pages with explicit source slide links.
- Updates are append-only in `wiki/log.md`.

## Content Model

1. Source of truth: `content/slides/*/_index.md` (immutable).
2. Compiled note: `wiki/slides/<slug>.md` (metadata + key sections + summary).
3. Navigation layer: `wiki/index.md` (topic entry points).
4. Operation log: `wiki/log.md` (chronological append-only).

## Next Layers (Inspired by Reference Wiki)

- `wiki/topic-map.md`: cross-deck concept clusters.
- `wiki/coverage.md`: ingest status and freshness checks.
- `wiki/query-playbook.md`: standard workflow for answering from wiki.
- `wiki/queries/*.md`: saved answers for repeated questions.

## Operating Loop

1. Ingest new slide deck to `wiki/slides/<slug>.md`.
2. Rebuild `wiki/index.md` topic grouping.
3. Refresh `wiki/topic-map.md` and `wiki/coverage.md`.
4. Append one log line to `wiki/log.md`.
5. For user questions, save high-value outputs to `wiki/queries/`.

## 3-Phase Rollout

1. Phase 1 (Now): keep `wiki/slides/`, `wiki/index.md`, `wiki/log.md` stable.
2. Phase 2: add `topic-map`, `coverage`, and `query-playbook`.
3. Phase 3: add query archive (`wiki/queries/`) and optional graph layer.

