#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Install external skills and runtimes referenced by this repo.

Usage:
  ./installers/install-external-skills.sh [--global|--project] [--agent AGENT]

Defaults:
  --global    Install skills globally and gstack under ~/.codex/skills
EOF
}

log() {
  printf '%s\n' "$*"
}

warn() {
  printf 'warning: %s\n' "$*" >&2
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || die "missing required command: $1"
}

SCOPE="global"
AGENT_ARGS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --global)
      SCOPE="global"
      shift
      ;;
    --project)
      SCOPE="project"
      shift
      ;;
    --agent|-a)
      [[ $# -ge 2 ]] || die "--agent requires a value"
      AGENT_ARGS+=("--agent" "$2")
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      die "unknown argument: $1"
      ;;
  esac
done

require_cmd git
require_cmd npx
require_cmd npm

log "Installing external runtimes"
npm install -g pnpm agent-browser
agent-browser install

log "Installing external skills from vercel-labs/agent-browser"
skills_cmd=(npx --yes skills@latest add vercel-labs/agent-browser --skill agent-browser --skill dogfood -y)
if [[ "$SCOPE" == "global" ]]; then
  skills_cmd+=("--global")
fi
skills_cmd+=("${AGENT_ARGS[@]}")
"${skills_cmd[@]}"

if [[ "$SCOPE" == "global" ]]; then
  gstack_dest="$HOME/.codex/skills/gstack"
else
  gstack_dest="$(pwd)/.agents/skills/gstack"
fi

if [[ -d "$gstack_dest/.git" ]]; then
  warn "gstack already exists at $gstack_dest; leaving it in place"
else
  log "Cloning gstack into $gstack_dest"
  mkdir -p "$(dirname "$gstack_dest")"
  git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git "$gstack_dest"
fi

if [[ -x "$gstack_dest/setup" ]]; then
  log "Running gstack setup for Codex"
  (
    cd "$gstack_dest"
    ./setup --host codex
  )
else
  warn "gstack setup script not found at $gstack_dest/setup"
fi

