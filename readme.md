# Jojo Workbench

Personal installable skills, bootstrap scripts, and a small pile of editor and terminal configs.

## Layout

- `skills/` portable Agent Skills that can be installed with `npx skills add <owner>/<repo>`
- `installers/` bootstrap scripts for local skills, external skills, and runtime dependencies
- `other-configs/` non-skill configs that I still keep around

## Included skills

- `deep-research`: do broad external research and filter it down to source-backed findings.
- `email-draft-send`: draft emails into reusable `.mail.txt` files, validate them, then open Apple Mail drafts one at a time for manual review and sending.
- `read-arxiv-paper`: read arXiv or AlphaXiv papers for summary, critique, comparison, and implementation takeaways.
- `read-github-code`: inspect GitHub repos by surveying README/docs/manifests and DeepWiki-style summaries first, then reading the actual source files that answer the question.
- `slides-pptgenjs`: create or edit editable PowerPoint decks with PptxGenJS plus render and validation helpers.
- `slidev`: keep a Slidev deck workflow around for Markdown-based presentations, but this one is not currently active for me.
- `smux`: local fork of the split-pane agent communication skill; this is the one for letting the left coding pane talk to the right coding pane through `tmux-bridge`.
- `system-viva`: fight cognitive offloading by turning recent AI-generated code changes into a short quiz, immediate teach-back review, and learning debrief.

## Install

Install everything globally for your user:

```bash
./installers/install-all.sh
```

Install only this repo's portable skills:

```bash
./installers/install-repo-skills.sh
```

Install the external skills and runtimes referenced by this repo:

```bash
./installers/install-external-skills.sh
```

All installer scripts accept `--project` if you want project-local installs instead of global ones. They also accept repeated `--agent <name>` flags for agent-specific installs.

## Upstreams

### Included here as local forks or custom variants

- `smux`: based on [ShawnPana/smux](https://github.com/ShawnPana/smux)

### Referenced here but not vendored into this repo

- `agent-browser`: [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser)
- `dogfood`: [agent-browser skills docs](https://agent-browser.dev/skills)
- `gstack`: [garrytan/gstack](https://github.com/garrytan/gstack)

## Other configs

- `other-configs/terminal/terminator/config`
- `other-configs/vim/.vimrc`
- `other-configs/vim/python.vimrc`
- `other-configs/tmux/.tmux.conf`

## Random useful tools

- `gdown`: [wkentaro/gdown](https://github.com/wkentaro/gdown)
- `curlget`: [Chrome extension](https://chrome.google.com/webstore/detail/curlwget/jmocjfidanebdlinpbcdkcmgdifblncg)
