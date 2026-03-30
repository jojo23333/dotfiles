---
name: slidev
description: This skill should be used when the user asks to create, revise, debug, style, animate, export, or explain a Slidev deck, `slides.md`, or Slidev presentation workflow.
version: 1.0.0
---

# Slidev

Use this skill to create or revise valid Slidev Markdown decks. Keep the output practical, runnable, and consistent with Slidev syntax.

## Default target

Unless the user specifies another entry file, assume the deck lives in `slides.md`.

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

- Use deck headmatter at the top only when deck-wide configuration is needed.
- Separate slides with `---` on its own line.
- Use per-slide frontmatter only when a slide needs layout, transition, or other slide-local settings.
- Keep speaker notes in HTML comments at the end of the slide they belong to.
- Prefer built-in Slidev layouts and components before inventing ad hoc HTML.
- For technical talks, favor code clarity and progressive reveal over dense text walls.
- When adding advanced features like `v-click`, `magic-move`, Mermaid, Monaco, or slot-based layouts, follow documented Slidev syntax exactly.

## Output expectations

When writing or revising a deck:

1. Make the file syntactically valid Slidev Markdown.
2. Keep frontmatter keys coherent and minimal.
3. Preserve code fences, Vue components, and directives exactly where needed.
4. Mention any required local commands such as install, dev, or export steps.

## Reference map

Load `references/slidev-authoring.md` for:

- deck structure and frontmatter
- layouts and slots
- click animations and transitions
- code blocks and magic-move
- Mermaid, PlantUML, and LaTeX
- presenter notes and export setup
