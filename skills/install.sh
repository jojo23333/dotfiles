#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Install Claude and/or Codex skills into a target project.

Usage:
  ./skills/install.sh [--target DIR] [--vendor claude|codex|all] [--overwrite]
  ./skills/install.sh --repo owner/repo [--ref REF] [--target DIR] [--vendor claude|codex|all] [--overwrite]

Examples:
  ./skills/install.sh
  ./skills/install.sh --vendor claude
  ./skills/install.sh --target /path/to/project
  bash <(curl -fsSL https://raw.githubusercontent.com/jojo23333/dotfiles/master/skills/install.sh) --repo jojo23333/dotfiles
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

copy_skill_tree() {
  local src_root="$1"
  local dest_root="$2"

  [ -d "$src_root" ] || return 0
  mkdir -p "$dest_root"

  local skill
  for skill in "$src_root"/*; do
    [ -d "$skill" ] || continue
    local name
    name="$(basename "$skill")"
    local dest="$dest_root/$name"
    if [ -e "$dest" ]; then
      if [ "$OVERWRITE" = "1" ]; then
        rm -rf "$dest"
      else
        die "destination already exists: $dest (use --overwrite to replace)"
      fi
    fi
    cp -R "$skill" "$dest"
    log "installed $name -> $dest"
  done
}

TARGET_DIR="$(pwd)"
VENDOR="all"
OVERWRITE="0"
REPO=""
REF="master"
SCRIPT_DIR=""
SOURCE_ROOT=""
TMP_DIR=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --target)
      [ "$#" -ge 2 ] || die "--target requires a value"
      TARGET_DIR="$2"
      shift 2
      ;;
    --vendor)
      [ "$#" -ge 2 ] || die "--vendor requires a value"
      VENDOR="$2"
      shift 2
      ;;
    --overwrite)
      OVERWRITE="1"
      shift
      ;;
    --repo)
      [ "$#" -ge 2 ] || die "--repo requires a value"
      REPO="$2"
      shift 2
      ;;
    --ref)
      [ "$#" -ge 2 ] || die "--ref requires a value"
      REF="$2"
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

case "$VENDOR" in
  claude|codex|all) ;;
  *)
    die "--vendor must be claude, codex, or all"
    ;;
esac

mkdir -p "$TARGET_DIR"
TARGET_DIR="$(cd "$TARGET_DIR" && pwd)"

cleanup() {
  if [ -n "${TMP_DIR:-}" ] && [ -d "$TMP_DIR" ]; then
    rm -rf "$TMP_DIR"
  fi
}
trap cleanup EXIT

if [ -n "$REPO" ]; then
  require_cmd curl
  require_cmd tar
  TMP_DIR="$(mktemp -d)"
  log "downloading $REPO@$REF"
  curl -fsSL "https://codeload.github.com/${REPO}/tar.gz/${REF}" | LC_ALL=C tar -xzf - -C "$TMP_DIR"
  SOURCE_ROOT="$(find "$TMP_DIR" -mindepth 1 -maxdepth 1 -type d | head -n 1)"
  [ -n "$SOURCE_ROOT" ] || die "failed to unpack repository archive"
else
  if [ -n "${BASH_SOURCE[0]:-}" ]; then
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  else
    die "cannot resolve local script directory; use --repo when streaming the script"
  fi
  SOURCE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
fi

CLAUDE_SRC="$SOURCE_ROOT/skills/claude"
CODEX_SRC="$SOURCE_ROOT/skills/codex"
CLAUDE_DEST="$TARGET_DIR/.claude/skills"
CODEX_DEST="$TARGET_DIR/.agents/skills"

[ -d "$CLAUDE_SRC" ] || die "missing source directory: $CLAUDE_SRC"
[ -d "$CODEX_SRC" ] || die "missing source directory: $CODEX_SRC"

case "$VENDOR" in
  claude)
    copy_skill_tree "$CLAUDE_SRC" "$CLAUDE_DEST"
    ;;
  codex)
    copy_skill_tree "$CODEX_SRC" "$CODEX_DEST"
    ;;
  all)
    copy_skill_tree "$CLAUDE_SRC" "$CLAUDE_DEST"
    copy_skill_tree "$CODEX_SRC" "$CODEX_DEST"
    ;;
esac

log "done"
