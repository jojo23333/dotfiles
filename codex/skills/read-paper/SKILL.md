---
name: paper-reading
description: Use this skill whenever the user shares an arxiv/alphaxiv URL or paper ID, or asks to read, summarize, explain, or analyze a research paper. Triggers on any mention of arxiv, alphaxiv, paper IDs like "2401.12345", or requests to review academic papers. Supports both quick survey mode (alphaxiv) and deep-read mode (TeX source).
---

# Paper Reading

Two modes: **survey** (fast, alphaxiv overview) and **deep-read** (full TeX source). Default to survey unless the user asks for in-depth analysis or the alphaxiv overview is insufficient.

## Step 1: Extract Paper ID

| Input | Paper ID |
|---|---|
| `arxiv.org/abs/2401.12345` | `2401.12345` |
| `arxiv.org/pdf/2401.12345` | `2401.12345` |
| `alphaxiv.org/overview/2401.12345` | `2401.12345` |
| `2401.12345v2` | `2401.12345v2` |

## Mode A: Survey (default)

Fetch the alphaxiv machine-readable report:

```bash
curl -s "https://alphaxiv.org/overview/{PAPER_ID}.md"
```

If you need more detail than the overview provides:

```bash
curl -s "https://alphaxiv.org/abs/{PAPER_ID}.md"
```

If both return 404, fall through to Mode B.

## Mode B: Deep Read

Use when the user wants in-depth understanding, or alphaxiv endpoints are unavailable.

1. **Download TeX source** (not the PDF):
   ```bash
   mkdir -p ~/.cache/arxiv/{PAPER_ID}
   curl -sL "https://arxiv.org/src/{PAPER_ID}" -o ~/.cache/arxiv/{PAPER_ID}/source.tar.gz
   ```
   Skip download if the file already exists.

2. **Unpack**: Extract into `~/.cache/arxiv/{PAPER_ID}/`

3. **Locate entrypoint**: Find `main.tex` or the primary `.tex` file.

4. **Read thoroughly**: Read the entrypoint and recurse through all `\input`/`\include` files.

## Step 3: Output Summary

Save a markdown summary to:

```
autoresearch/knowledge_base/related_works/summary_{tag}.md
```

- Generate a descriptive `tag` (e.g. `conditional_memory`, `sparse_attention`).
- Check the tag doesn't collide with existing files.
- If working within a project context, connect the paper's ideas to the current codebase — read relevant source files and note how the paper's techniques might apply.

## Error Handling

- **alphaxiv 404**: Report not yet generated — fall through to Mode B.
- **arxiv src 404**: Source unavailable — direct user to `https://arxiv.org/pdf/{PAPER_ID}` as last resort.