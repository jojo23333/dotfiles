# Skills

This directory keeps the same skill set in two native layouts:

- `claude/` -> install into `.claude/skills/`
- `codex/` -> install into `.agents/skills/`

Current shared skill set:

- `deep-research`
- `read-arxiv-paper`
- `read-github-code`
- `slides-slidev`
- `slides-pptgenjs`
- `system-viva`

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

## Useful off-the-shelf skills

These are external tools or skill packs I use, but do not vendor in this repo.

### agent-browser

- Repo: [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser)
- Install runtime:

```bash
npm install -g agent-browser
agent-browser install
```

- Install skill:

```bash
npx skills add vercel-labs/agent-browser --skill agent-browser
```

- Notes: browser automation for agents: pages, forms, screenshots, sessions, and auth.

### dogfood

- Docs: [agent-browser skills](https://agent-browser.dev/skills)
- Install skill:

```bash
npx skills add vercel-labs/agent-browser --skill dogfood
```

- Notes: structured exploratory QA with repro steps, screenshots, and videos. Uses the `agent-browser` runtime above.

### gstack

- Repo: [garrytan/gstack](https://github.com/garrytan/gstack)
- Install into a Codex repo:

```bash
git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git .agents/skills/gstack
cd .agents/skills/gstack && ./setup --host codex
```

- Notes: a large role-based skill pack for planning, review, QA, shipping, and retros.

### smux

- Repo: [ShawnPana/smux](https://github.com/ShawnPana/smux)
- Install runtime:

```bash
curl -fsSL https://shawnpana.com/smux/install.sh | bash
```

- Install skill:

```bash
npx skills add ShawnPana/smux
```

- Notes: tmux setup plus `tmux-bridge` for cross-pane terminal automation and agent-to-agent communication.
