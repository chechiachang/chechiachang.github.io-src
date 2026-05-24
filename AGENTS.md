# AGENTS

Main instruction index for this repo.
All instructions and skills must be compact and extremely minimal.

## Hard Rules
- Keep outputs short, actionable, and minimal.
- Never ask approval. Execute directly with the safest reasonable default.
- Ask only if blocked by missing required secret/credential/account value.
- Use repo-local `./tmp` for temporary files; do not use OS-wide temp directories.

## Agents
- `ingest-agent`: Ingest `./content/*`.
- `output-agent`: Generate content.
- `review-agent`: Review content.

### ingest-agent Instructions

#### Raw Sources from `./content`
- `./content` is the source-of-truth layer.
- The LLM may read from raw sources, but should treat them as immutable.
- Raw data includes posts and slides.

#### Directory: `wiki/`
- The wiki is LLM-maintained markdown.
- The LLM owns the structure, summaries, cross-references, and organization.
- Humans read the wiki; the LLM writes and updates it.
- Before ingest work, read `wiki/purpose-plan.md`.
- `wiki/index.md` is content-oriented navigation.
- `wiki/log.md` is chronological and append-only.

#### Operation: Ingest

When new raw data is added to `./content`, the ingest-agent should:

1. Re-compile the wiki.
1. Append an entry to `wiki/log.md`.
1. Preserve old knowledge unless a newer source clearly supersedes it.

#### Slide Parsing
- Slide: a `content/slides/*/_index.md` file using markdown/hugo/reveal-hugo syntax.
- Page: a slide is split by `---`; each split is one page.

#### Slide Output Format
For each slide, output:

1. Title, description, metadata.
1. Pages (`## Pages (Section | Summary)`): one line per page in format `Section | Summary` (`count(pages) == count(page)`).
1. Use `(frontmatter)` as section name for pages without a heading.
1. Time-to-Syntax: list of `timing:syntax`, grouped by where the syntax appears in the slide (markdown/hugo/reveal-hugo).
1. Time-to-Sentence: list of `timing:sentence`, grouped by where the complete sentence appears in the slide.

## output-agent Instructions

1. Try fetch existing content with the same title from draft/<category>/ content/transcripts, content/slides, and content/posts. Use them as reference for style, voice, and structure.

##### markdown-slides

1. use ./markdown-slides for generating markdown slides.
1. use ./draft for generated contents.

##### Type of Presentation

1. Standard: A typical presentation with a Slide Deck. Time: 30-40 minutes. Slides about 20 pages. Focus on delivering key insights or explaining a specific topic.
1. Workshop: A hands-on session with exercises. Time: 60-90 minutes. Slides about 60 pages. Focus on teaching a skill or process, with step-by-step instructions and practical applications.

If conten/posts or slides path contains `workshop` or `ws`, the output-agent should assume the presentation is a Workshop. Otherwise, it should assume it's a Standard presentation.

##### Generate Post in `./content/posts`
- `skills/presentation.md`: Skills for drafting `./content/posts` and `./content/slides` for call for presentations

##### Generate Slide in `./content/slides`
- fetch slide content of last year from `./content/slides/*/_index.md` as reference for structure, style, and voice.
- `skills/generate-slide-md.md`: Skill for generating `content/slides/*/_index.md`; must read `wiki/slide-pages-pattern.md` before drafting outline.
- `skills/chechia-content.md`: Skills for generating text and sentence content with chechia's unique style and voice.

##### Generate Transcript in `./content/transcripts`
- read markdown slide by slide. Slides are split by `---`.
- generate transcript for each slide in `./content/slides/*/_index.md` that the presenter would say during the presentation
- Overall format should be a article or blog post. Each page's transcript should be a complete paragraph that cover all content on that page as if the presenter is explaining it to the audience. 
- transcript should include greetings, introductions, transitions, and conclusions as if the presenter is delivering the presentation in person.

## review-agent Instructions

##### Review Overview

1. read `content/slides/*/_index.md`
1. review content for accuracy, clarity, and consistency with chechia's style and voice.

##### Review Slide Content in `./content/slides`

1. read markdown slide by slide. Slides are split by `---`.
1. output result slide by slide, in format `Slide N: [OK/Needs Work] - Reason (if Needs Work)`.
1. first Empty Slide (no text) is meta-data
