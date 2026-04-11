#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Install all portable skills from this repository with the open `skills` CLI.

Usage:
  ./installers/install-repo-skills.sh [--global|--project] [--agent AGENT] [--copy]

Defaults:
  --global    Install to user-level agent skill directories
EOF
}

log() {
  printf '%s\n' "$*"
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || die "missing required command: $1"
}

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCOPE="global"
COPY_MODE="0"
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
    --copy)
      COPY_MODE="1"
      shift
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

require_cmd npx

cmd=(npx --yes skills@latest add "$REPO_ROOT" --all -y)
if [[ "$SCOPE" == "global" ]]; then
  cmd+=("--global")
fi
if [[ "$COPY_MODE" == "1" ]]; then
  cmd+=("--copy")
fi
cmd+=("${AGENT_ARGS[@]}")

log "Installing repo skills from $REPO_ROOT"
"${cmd[@]}"

