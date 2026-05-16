#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path

FRONTMATTER_DELIM = "---"
SLIDE_SEPARATOR_RE = re.compile(r"(?m)^\s*---\s*$")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*$", re.MULTILINE)
BULLET_RE = re.compile(r"^\s*(?:[-*+]\s+|\d+\.\s+)", re.MULTILINE)
LINK_RE = re.compile(r"(?<!\!)\[[^\]]+\]\(([^)]+)\)")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
SHORTCODE_RE = re.compile(r"\{\{[%<].*?[>%]\}\}")
CODE_FENCE_RE = re.compile(r"```")

PURPOSE_RULES = [
    (
        "cover/title",
        ["coscup", "devops", "workshop", "title", "@", "活動", "演講", "投影片"],
    ),
    ("agenda/outline", ["大綱", "outline", "今天要聊", "goals", "agenda", "目標"]),
    ("concept/explanation", ["什麼是", "why", "為何", "architecture", "原理", "概念", "mcp", "llm"]),
    ("demo/hands-on", ["demo", "live", "source code", "step", "workshop", "command", "實作", "範例"]),
    ("evidence/metrics", ["cost", "latency", "benchmark", "evaluation", "dataset", "數據", "結果", "指標"]),
    ("conclusion/cta", ["結論", "takeaway", "q&a", "thanks", "下一步", "summary", "總結"]),
]

SYNTAX_BY_PURPOSE = {
    "Deck metadata (front matter at file top)": [
        "YAML front matter: `--- ... ---` with `title`, `description`, `date`, `tags`, `categories`.",
        "Reveal output switch: `outputs: [\"Reveal\"]`.",
        "Deck-level reveal settings: `reveal_hugo` (theme, margin, transition, highlight theme).",
    ],
    "Slide structure and flow": [
        "Horizontal slide separator: line containing only `---`.",
        "Headings `#`..`######` as slide title hierarchy.",
        "Bullet and numbered lists for speaking flow and key points.",
        "Blockquote `>` for emphasized takeaway or quote.",
    ],
    "Progressive/stacked sections": [
        "Section wrapper shortcode: `{{% section %}} ... {{% /section %}}` for grouped related slides.",
        "Use section blocks for intro, concept clusters, and demo sequence grouping.",
    ],
    "Reusable and embedded content": [
        "Hugo shortcode include: `{{< slide content=\"slides.about-me\" >}}` for reusable slide snippets.",
        "General shortcode forms: `{{< ... >}}` and `{{% ... %}}`.",
    ],
    "Technical diagrams and code": [
        "Mermaid shortcode: `{{< mermaid >}} ... {{< /mermaid >}}` for architecture/process diagrams.",
        "Fenced code block: triple backticks for commands/code examples.",
        "Markdown links and images for references and visual evidence.",
    ],
    "Speaker and parser notes": [
        "Keep shortcode pairs balanced (`section`, `mermaid`) to satisfy CI parser checks.",
        "Keep `outputs: [\"Reveal\"]` on each `content/slides/**/_index.md` deck.",
    ],
}

SYNTAX_SOURCES = [
    "https://reveal-hugo.dzello.com",
    "https://github.com/joshed-io/reveal-hugo",
    "https://revealjs.com/markdown/",
    "https://gohugo.io/content-management/",
    "https://gohugo.io/content-management/shortcodes/",
    "Repository conventions: skills/presentation.md and .github/workflows/test-slides.yml",
]


def parse_frontmatter_and_body(raw: str) -> tuple[str, str]:
    lines = raw.splitlines()
    if not lines or lines[0].strip() != FRONTMATTER_DELIM:
        return "", raw

    end_index = None
    for i in range(1, len(lines)):
        if lines[i].strip() == FRONTMATTER_DELIM:
            end_index = i
            break

    if end_index is None:
        return "", raw

    frontmatter = "\n".join(lines[1:end_index])
    body = "\n".join(lines[end_index + 1 :])
    return frontmatter, body


def split_slides(body: str) -> list[str]:
    parts = [part.strip() for part in SLIDE_SEPARATOR_RE.split(body)]
    return [part for part in parts if part]


def normalize_md_text(text: str) -> str:
    text = re.sub(r"```[\s\S]*?```", " ", text)
    text = re.sub(r"\{\{[%<][\s\S]*?[>%]\}\}", " ", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"^\s{0,3}#{1,6}\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*(?:[-*+]\s+|\d+\.\s+)", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*>\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def split_sentences(text: str) -> list[str]:
    normalized = normalize_md_text(text)
    if not normalized:
        return []

    # Simple regex splitter for mixed Traditional Chinese and English slide text.
    chunks = re.split(r"(?<=[。！？!?\.])\s+|\s*[\n\r]+\s*", normalized)
    out = []
    for chunk in chunks:
        sentence = chunk.strip(" -•\t\r\n")
        if len(sentence) >= 2:
            out.append(sentence)
    return out


def classify_purpose(text: str) -> str:
    t = text.lower()
    for purpose, keywords in PURPOSE_RULES:
        if any(keyword in t for keyword in keywords):
            return purpose
    return "general content"


def first_heading_or_line(slide: str) -> str:
    m = HEADING_RE.search(slide)
    if m:
        return m.group(1).strip()

    for line in slide.splitlines():
        line = line.strip()
        if line:
            return line[:120]
    return "(empty)"


def slide_stats(slide: str) -> dict[str, int]:
    return {
        "headings": len(HEADING_RE.findall(slide)),
        "bullets": len(BULLET_RE.findall(slide)),
        "links": len(LINK_RE.findall(slide)),
        "images": len(IMAGE_RE.findall(slide)),
        "shortcodes": len(SHORTCODE_RE.findall(slide)),
        "code_fences": len(CODE_FENCE_RE.findall(slide)) // 2,
    }


def safe_name(path: Path) -> str:
    rel = str(path)
    return re.sub(r"[^a-zA-Z0-9._-]+", "__", rel)


def write_deck_outputs(source_file: Path, out_root: Path) -> dict[str, str]:
    raw = source_file.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter_and_body(raw)
    slides = split_slides(body)

    deck_dir = out_root / "decks" / safe_name(source_file)
    deck_dir.mkdir(parents=True, exist_ok=True)

    slides_md_path = deck_dir / "slides.md"
    outline_md_path = deck_dir / "outline.md"
    sentences_md_path = deck_dir / "sentences-by-purpose.md"

    slide_sections = []
    outline_lines = [f"# Outline: {source_file}", "", f"- total slides: {len(slides)}", ""]

    sentence_groups: dict[str, list[tuple[int, str]]] = defaultdict(list)

    if frontmatter.strip():
        outline_lines.append("## Front matter")
        outline_lines.append("```")
        outline_lines.append(frontmatter)
        outline_lines.append("```")
        outline_lines.append("")

    for idx, slide in enumerate(slides, start=1):
        title = first_heading_or_line(slide)
        stats = slide_stats(slide)
        purpose = classify_purpose(slide)

        outline_lines.append(f"## Slide {idx}: {title}")
        outline_lines.append(f"- purpose: {purpose}")
        outline_lines.append(
            f"- elements: headings={stats['headings']}, bullets={stats['bullets']}, links={stats['links']}, images={stats['images']}, shortcodes={stats['shortcodes']}, code_blocks={stats['code_fences']}"
        )
        outline_lines.append("")

        slide_sections.extend(
            [
                f"## Slide {idx}: {title}",
                "",
                "### Basic elements",
                f"- purpose: {purpose}",
                f"- headings: {stats['headings']}",
                f"- bullets: {stats['bullets']}",
                f"- links: {stats['links']}",
                f"- images: {stats['images']}",
                f"- shortcodes: {stats['shortcodes']}",
                f"- code blocks: {stats['code_fences']}",
                "",
                "### Slide content",
                slide,
                "",
                "---",
                "",
            ]
        )

        for sentence in split_sentences(slide):
            sentence_groups[classify_purpose(sentence)].append((idx, sentence))

    slides_md = [f"# Slides: {source_file}", "", f"- total slides: {len(slides)}", ""] + slide_sections
    slides_md_path.write_text("\n".join(slides_md).rstrip() + "\n", encoding="utf-8")
    outline_md_path.write_text("\n".join(outline_lines).rstrip() + "\n", encoding="utf-8")

    sentence_lines = [f"# Sentences by purpose: {source_file}", "", f"- total slides: {len(slides)}", ""]
    for purpose in sorted(sentence_groups.keys()):
        sentence_lines.append(f"## {purpose}")
        sentence_lines.append("")
        seen = set()
        for slide_index, sentence in sentence_groups[purpose]:
            key = sentence.strip()
            if key in seen:
                continue
            seen.add(key)
            sentence_lines.append(f"- [slide {slide_index}] {sentence}")
        sentence_lines.append("")

    if len(sentence_lines) <= 4:
        sentence_lines.extend(["## general content", "", "- (no sentences detected)", ""])

    sentences_md_path.write_text("\n".join(sentence_lines).rstrip() + "\n", encoding="utf-8")

    return {
        "source": str(source_file),
        "deck_dir": str(deck_dir),
        "slides": str(slides_md_path),
        "outline": str(outline_md_path),
        "sentences": str(sentences_md_path),
    }


def write_syntax_reference(out_root: Path) -> Path:
    path = out_root / "syntax-by-purpose.md"
    lines = ["# Available syntax grouped by purpose", ""]

    for purpose, syntaxes in SYNTAX_BY_PURPOSE.items():
        lines.append(f"## {purpose}")
        lines.append("")
        for item in syntaxes:
            lines.append(f"- {item}")
        lines.append("")

    lines.append("## Sources")
    lines.append("")
    for source in SYNTAX_SOURCES:
        lines.append(f"- {source}")
    lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_manifest(out_root: Path, records: list[dict[str, str]], syntax_path: Path) -> Path:
    path = out_root / "manifest.md"
    lines = [
        "# Slides ingest manifest",
        "",
        f"- total markdown files ingested: {len(records)}",
        f"- syntax reference: {syntax_path}",
        "",
        "## Ingest order (one-by-one)",
        "",
    ]

    for i, record in enumerate(records, start=1):
        lines.extend(
            [
                f"### {i}. {record['source']}",
                f"- output deck dir: {record['deck_dir']}",
                f"- slides: {record['slides']}",
                f"- outline: {record['outline']}",
                f"- sentences: {record['sentences']}",
                "",
            ]
        )

    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def discover_markdown_files(input_dir: Path) -> list[Path]:
    return sorted(input_dir.glob("**/_index.md"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest and analyze slides markdown files.")
    parser.add_argument("--input", required=True, type=Path, help="Slides root directory (e.g., content/slides)")
    parser.add_argument("--output", required=True, type=Path, help="Export directory for analysis outputs")
    args = parser.parse_args()

    input_dir = args.input.resolve()
    out_root = args.output.resolve()

    if not input_dir.exists() or not input_dir.is_dir():
        raise SystemExit(f"Input directory not found: {input_dir}")

    out_root.mkdir(parents=True, exist_ok=True)

    markdown_files = discover_markdown_files(input_dir)
    records = []

    for source_file in markdown_files:
        records.append(write_deck_outputs(source_file, out_root))

    syntax_path = write_syntax_reference(out_root)
    manifest_path = write_manifest(out_root, records, syntax_path)

    print(f"Ingested {len(records)} markdown files.")
    print(f"Export root: {out_root}")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
