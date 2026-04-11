#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Export or apply the iTerm2 config tracked in this repo.

Usage:
  ./other-configs/terminal/iterm2/iterm2-sync.sh export
  ./other-configs/terminal/iterm2/iterm2-sync.sh apply
  ./other-configs/terminal/iterm2/iterm2-sync.sh status

Commands:
  export   Export the current com.googlecode.iterm2 defaults domain into this repo.
  apply    Import the tracked plist and point iTerm2 at this folder as its custom settings folder.
  status   Show the current iTerm2 custom-folder settings and tracked plist path.
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

require_macos() {
  [[ "$(uname -s)" == "Darwin" ]] || die "iTerm2 preferences are only supported on macOS"
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$SCRIPT_DIR"
PLIST_PATH="$CONFIG_DIR/com.googlecode.iterm2.plist"
DOMAIN="com.googlecode.iterm2"

current_custom_folder() {
  defaults read "$DOMAIN" PrefsCustomFolder 2>/dev/null || true
}

current_load_flag() {
  defaults read "$DOMAIN" LoadPrefsFromCustomFolder 2>/dev/null || true
}

print_status() {
  local custom_folder load_flag
  custom_folder="$(current_custom_folder)"
  load_flag="$(current_load_flag)"

  log "Tracked plist: $PLIST_PATH"
  if [[ -f "$PLIST_PATH" ]]; then
    log "Tracked plist exists: yes"
  else
    log "Tracked plist exists: no"
  fi

  log "iTerm2 load custom folder: ${load_flag:-unset}"
  log "iTerm2 custom folder: ${custom_folder:-unset}"

  if [[ -n "$custom_folder" && "$custom_folder" == "$CONFIG_DIR" ]]; then
    log "Repo folder is currently active in iTerm2."
  fi
}

export_prefs() {
  require_macos
  require_cmd defaults

  if pgrep -x iTerm2 >/dev/null 2>&1; then
    warn "iTerm2 is running. Export works, but quitting iTerm2 first is safer if you have unsaved settings changes."
  fi

  defaults export "$DOMAIN" "$PLIST_PATH"
  log "Exported iTerm2 preferences to:"
  log "  $PLIST_PATH"
}

apply_prefs() {
  require_macos
  require_cmd defaults
  require_cmd plutil

  [[ -f "$PLIST_PATH" ]] || die "tracked plist not found: $PLIST_PATH"
  plutil -lint "$PLIST_PATH" >/dev/null

  defaults import "$DOMAIN" "$PLIST_PATH"
  defaults write "$DOMAIN" PrefsCustomFolder -string "$CONFIG_DIR"
  defaults write "$DOMAIN" LoadPrefsFromCustomFolder -bool true

  log "Imported iTerm2 preferences from:"
  log "  $PLIST_PATH"
  log "Configured iTerm2 to load settings from:"
  log "  $CONFIG_DIR"
  log
  log "Next step:"
  log "  Quit and reopen iTerm2."
  log
  log "Optional:"
  log "  In iTerm2 > Settings > General > Settings, enable"
  log "  'Save changes to folder when iTerm2 quits' if you want GUI edits"
  log "  to write back into this repo automatically."
}

main() {
  local command="${1:-}"
  case "$command" in
    export)
      export_prefs
      ;;
    apply)
      apply_prefs
      ;;
    status)
      print_status
      ;;
    -h|--help|help|"")
      usage
      ;;
    *)
      die "unknown command: $command"
      ;;
  esac
}

main "$@"
