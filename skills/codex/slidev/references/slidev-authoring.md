# Slidev Authoring Reference

Use this reference when editing `slides.md` or any Slidev entry file.

## Deck structure

- The default entry file is `slides.md`.
- The first frontmatter block is deck headmatter.
- Separate slides with `---` on a line by itself.
- Per-slide frontmatter also uses `---` blocks, but belongs to that slide.

Example:

````md
---
theme: default
title: Demo Deck
---

# Intro

Welcome.

---
layout: two-cols
---

# Code

::left::

```ts
console.log('hi')
```

::right::

Explanation text.
````

## Notes

- Presenter notes are HTML comments at the end of a slide.
- Notes support Markdown and can include click markers.

Example:

```md
# Demo

Visible content

<!--
[click] Mention the setup first.
[click:3] Jump to the final takeaway on the third click.
-->
```

## Clicks and animation

- Use `v-click` or `v-clicks` for incremental reveal.
- Use transitions sparingly and only when they improve comprehension.
- Use `magic-move` for stepwise code evolution.

Example:

```md
- <span v-click>First point</span>
- <span v-click>Second point</span>
```

Example magic move:

````md
`````md magic-move
```ts
const count = 1
```
```ts
const count = 2
```
`````
````

## Code features

- Regular fenced code blocks work as expected.
- Line highlighting uses fence metadata.
- Monaco editor support is available with `{monaco}`.
- Code groups, imported snippets, and Twoslash require exact syntax.

Examples:

````md
```ts {2,4-5}
function add(a: number, b: number) {
  return a + b
}
```
````

````md
```ts {monaco}
const msg: string = 'hello'
```
````

## Diagrams and math

- Mermaid: fenced `mermaid` blocks
- PlantUML: fenced `plantuml` blocks
- Math: inline `$...$` and block `$$...$$`

## Layout guidance

- Prefer built-in layouts such as `cover`, `center`, `quote`, `fact`, `two-cols`, and image layouts when they fit.
- Use slot syntax like `::left::` and `::right::` only for layouts that support slots.
- Keep slides visually sparse. One idea per slide is usually better than dense prose.

## Export and local workflow

Common commands:

```bash
pnpm create slidev
pnpm install
pnpm slidev
pnpm slidev export
```

If PDF export is part of the task, mention any browser or Playwright dependency the project may need.

## Quality bar

- Keep output valid Slidev Markdown, not plain Markdown slides.
- Avoid malformed frontmatter and unbalanced fences.
- Prefer concise slides with strong hierarchy.
- Preserve existing theme, layout, and custom components unless the user asked to change them.
