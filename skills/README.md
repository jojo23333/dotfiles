# Skills

This repo now keeps a single portable copy of each skill under `skills/<skill-name>/`.

Each skill may include:

- `SKILL.md` for trigger metadata and workflow instructions
- `agents/` for UI metadata such as `openai.yaml`
- `scripts/` for deterministic helpers
- `references/` for on-demand docs
- `assets/` for templates or runtime files

## Included skills

- `deep-research`: external research and evidence synthesis for ambiguous or high-impact questions.
- `email-draft-send`: draft emails into text files, validate them, then open Apple Mail drafts one by one for manual review and sending.
- `read-arxiv-paper`: read arXiv or AlphaXiv papers with a focus on method, evidence, limitations, and implementation relevance.
- `read-github-code`: inspect GitHub repositories by starting with README/docs/manifests and DeepWiki-style orientation, then reading the source that answers the actual question.
- `slides-pptgenjs`: create or edit editable `.pptx` decks with bundled rendering and validation helpers.
- `slidev`: keep a Slidev workflow around for Markdown presentation decks. Present in the repo, but not currently an active workflow for me.
- `smux`: local fork of the tmux split-pane communication skill for letting two coding agents talk to each other across panes.
- `system-viva`: convert recent AI-assisted code changes into a quiz and debrief to reinforce the human’s understanding.

## External upstreams

Local fork or custom variant included in this repo:

- `smux`: based on [ShawnPana/smux](https://github.com/ShawnPana/smux)

Referenced in docs and installers, but not vendored here:

- `agent-browser`: [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser)
- `dogfood`: [agent-browser skills docs](https://agent-browser.dev/skills)
- `gstack`: [garrytan/gstack](https://github.com/garrytan/gstack)

## Install

Install all local skills:

```bash
./installers/install-repo-skills.sh
```

Install local skills plus external runtimes and referenced external skills:

```bash
./installers/install-all.sh
```
