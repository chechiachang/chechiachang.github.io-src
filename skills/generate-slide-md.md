---
name: generate-slide-md
description: "Generate slide markdown at content/slides/<date>-<slug>/_index.md with repository style and ordering."
---

# Generate Slide MD Skill

## Scope

- Create or update `content/slides/<date>-<slug>/_index.md`.
- Keep output concise, practical, and workshop/talk ready.

## Required Inputs

- Talk title.
- Audience.
- Core problem to solve.
- 2-4 takeaways.

## Required Reference

Before drafting `Outline`, read:

- `wiki/slide-pages-pattern.md`

Use its structure/order as default unless user requests a different order.

## Outline Rule

Generate `Outline` in this order:

1. Problem/context
2. Core concept or method
3. Implementation/demo/workshop
4. Limits/risks
5. Summary and Q&A

## Slide Skeleton

1. Frontmatter (`outputs: ["Reveal"]` + `reveal_hugo`).
2. Cover slide.
3. Outline slide.
4. Main sections.
5. Practical demo/hands-on section.
6. Summary.
7. Q&A.

## Writing Rules

- Traditional Chinese primary, keep key technical terms in English.
- Short headings and short bullets.
- Prefer problem-first and demo-first progression.
