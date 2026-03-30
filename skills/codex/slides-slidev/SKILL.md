---
name: slidev
description: Use when the user asks to create, revise, debug, style, animate, export, or explain a Slidev deck, slides.md, or Slidev presentation workflow.
---

# Slidev

Use this skill to create or revise valid Slidev Markdown decks. Keep the output runnable and faithful to Slidev syntax.

## Default target

Unless the user specifies otherwise, assume the deck entry file is `slides.md`.

## Core workflow

1. Clarify the deck goal, audience, and tone.
2. Decide whether the task is:
   - a new deck
   - an edit to an existing deck
   - a syntax or layout fix
   - an export or tooling setup task
3. Read `references/slidev-authoring.md` when the task touches syntax, layouts, clicks, code, diagrams, notes, or export behavior.
4. Produce valid Slidev Markdown, not generic Markdown slides.
5. Preserve existing deck structure unless the user asked for a rewrite.

## Authoring rules

- Use deck headmatter only when deck-wide configuration is needed.
- Separate slides with `---` on its own line.
- Use per-slide frontmatter only when a slide needs slide-local config.
- Keep speaker notes in HTML comments at the end of the relevant slide.
- Prefer built-in Slidev layouts and components over ad hoc HTML.
- For technical talks, prefer progressive reveal and clear code over dense prose.
- When adding advanced features like `v-click`, `magic-move`, Mermaid, Monaco, or layout slots, follow exact Slidev syntax.

## Output expectations

When writing or revising a deck:

1. make the file syntactically valid Slidev Markdown
2. keep frontmatter minimal and coherent
3. preserve code fences, Vue components, and directives where needed
4. mention required local commands such as install, dev, or export steps

## Reference map

Load `references/slidev-authoring.md` for:

- deck structure and frontmatter
- layouts and slots
- click animations and transitions
- code blocks and magic-move
- Mermaid, PlantUML, and LaTeX
- presenter notes and export setup
