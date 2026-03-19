# Skills

This directory keeps the same skill set in two native layouts:

- `claude/` -> install into `.claude/skills/`
- `codex/` -> install into `.agents/skills/`

Current shared skill set:

- `deep-research`
- `read-arxiv-paper`
- `read-github-code`
- `slidev`

## Quick install

From a local clone, install both skill sets into the current project:

```bash
./skills/install.sh
```

Install only one vendor:

```bash
./skills/install.sh --vendor claude
./skills/install.sh --vendor codex
```

Install into another project:

```bash
./skills/install.sh --target /path/to/project
```

Install from GitHub without cloning first:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/jojo23333/dotfiles/master/skills/install.sh) --repo jojo23333/dotfiles
```
