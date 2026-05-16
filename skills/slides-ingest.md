# Slides Ingest Skill

Ingest `content/slides/**/_index.md` one-by-one and export analysis to:

- `tmp/slides-ingest-export/`

## Run

```bash
python3 tools/slides_ingest.py \
  --input content/slides \
  --output tmp/slides-ingest-export
```

## Exported Artifacts

For each slide markdown file, export:

- `slides.md`: all slides split by `---`, with basic element analysis.
- `outline.md`: one-file slide-by-slide outline (overall structure).
- `sentences-by-purpose.md`: all sentences grouped by slide purpose.

Global export:

- `syntax-by-purpose.md`: markdown/Hugo/reveal-hugo syntax grouped by purpose.
- `manifest.md`: list of ingested files and output locations.

## Notes

- Sentence segmentation is regex-based and optimized for mixed Traditional Chinese + English slide text.
