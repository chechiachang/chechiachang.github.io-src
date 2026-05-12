# Presentation Skill

Generate and maintain presentation content in two places:

- post: `content/posts/<date>-<slug>/index.md`
- slides: `content/slides/<date>-<slug>/_index.md`

Keep `<date>-<slug>` aligned between post and slides.

## Event Post Rule

If a post includes all three:

- `活動時間`
- `活動連結`
- `投影片`

then it is an event post.

Date rule for confirmed sessions:

- If `活動連結` exists (session confirmed):
- Keep post directory date (`content/posts/<date>-<slug>/`) as `活動時間` date.
- Set `date` in index.md` frontmatter (visible date) to 2 months before `活動時間`.

Event post must contain:

- `Title`
- `Outline`
- `Target group`
- `Takeaways`
- `References`
- `Author`

Event post must link to its slide URL.

Example link pattern:

- `https://chechia.net/slides/<date>-<slug>/`

## Post vs Slide Responsibility

Post is concise agenda/info page:

- event info (`活動時間`, `活動連結`, `聯繫我`, `投影片`)
- presentation title
- short outline list
- target audience and expected takeaways
- author section

Slides hold full talk/workshop content:

- full narrative
- deep technical details
- diagrams, demos, commands
- section-by-section speaker flow

Do not duplicate full slide content into post.

## Slide File Convention

Use `content/slides/<date>-<slug>/_index.md` with reveal frontmatter:

- `outputs: ["Reveal"]`
- `reveal_hugo` settings (theme, transition, etc.)

Use `---` to split slides.

Use concise slide headings and short bullets.

## Distilled Structure From Existing Content

Observed post pattern:

1. frontmatter
2. event metadata lines (`活動時間`, `活動連結`, `聯繫我`, `投影片`)
3. `Title`
4. `Outline`
5. `Target group`
6. `Author`

Observed slide pattern:

1. reveal frontmatter
2. title/cover slide
3. agenda slide
4. main technical sections
5. demo and examples
6. conclusion / Q&A

## Generation Workflow

1. Define talk title and target audience.
2. Draft full slides in `content/slides/<date>-<slug>/_index.md`.
3. Create/update post in `content/posts/<date>-<slug>/index.md` as agenda-only summary.
4. Add `投影片` link in post to `https://chechia.net/slides/<date>-<slug>/`.
5. Ensure event post includes `Title`, `Outline`, `Target group`, `Author`.
6. Keep frontmatter date/title/tags coherent across post and slides.
7. If session is confirmed with `活動連結`, keep post dir date as `活動時間` and set frontmatter `date` to 2 months before `活動時間`.

## Writing Style

- Keep post short, actionable, and scan-friendly.
- Keep outline as numbered list.
- Keep target group specific (role + context).
- Keep slide bullets short; one idea per bullet.
- Prefer practical flow: problem -> approach -> demo -> limits -> next steps.
