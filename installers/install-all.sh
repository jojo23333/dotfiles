#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Bootstrap this repo's skills and supporting runtimes in one shot.

Usage:
  ./installers/install-all.sh [--global|--project] [--agent AGENT]
                             [--skip-system-packages] [--skip-python-packages]
                             [--skip-smux-runtime] [--skip-external-skills]

Defaults:
  --global    Install skills globally for your user
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

detect_pkg_manager() {
  if command -v brew >/dev/null 2>&1; then
    echo "brew"
  elif command -v apt-get >/dev/null 2>&1; then
    echo "apt"
  elif command -v dnf >/dev/null 2>&1; then
    echo "dnf"
  elif command -v pacman >/dev/null 2>&1; then
    echo "pacman"
  elif command -v apk >/dev/null 2>&1; then
    echo "apk"
  else
    echo "unknown"
  fi
}

brew_formula_installed() {
  brew list --formula "$1" >/dev/null 2>&1
}

brew_cask_installed() {
  brew list --cask "$1" >/dev/null 2>&1
}

apt_updated="0"

apt_update_once() {
  if [[ "$apt_updated" == "0" ]]; then
    sudo apt-get update -qq
    apt_updated="1"
  fi
}

install_pkg() {
  local manager="$1"
  local package_name="$2"
  local check_cmd="${3:-}"
  local optional="${4:-0}"

  if [[ -n "$check_cmd" ]] && command -v "$check_cmd" >/dev/null 2>&1; then
    return
  fi

  case "$manager" in
    brew)
      if ! brew_formula_installed "$package_name"; then
        brew install "$package_name"
      fi
      ;;
    apt)
      apt_update_once
      sudo apt-get install -y -qq "$package_name"
      ;;
    dnf)
      sudo dnf install -y -q "$package_name"
      ;;
    pacman)
      sudo pacman -S --noconfirm "$package_name"
      ;;
    apk)
      sudo apk add "$package_name"
      ;;
    *)
      if [[ "$optional" == "1" ]]; then
        warn "no supported package manager found; skipping $package_name"
        return
      fi
      die "no supported package manager found; install $package_name manually"
      ;;
  esac
}

install_pkg_maybe() {
  local manager="$1"
  local package_name="$2"
  local check_cmd="${3:-}"
  if ! install_pkg "$manager" "$package_name" "$check_cmd" 1; then
    warn "failed to install optional package: $package_name"
  fi
}

install_brew_cask_maybe() {
  local cask_name="$1"
  if ! brew_cask_installed "$cask_name"; then
    if ! brew install --cask "$cask_name"; then
      warn "failed to install optional cask: $cask_name"
    fi
  fi
}

pip_install_user() {
  local python_bin="$1"
  shift
  if ! "$python_bin" -m pip install --user --upgrade "$@"; then
    "$python_bin" -m pip install --user --break-system-packages --upgrade "$@"
  fi
}

install_system_packages() {
  local manager
  manager="$(detect_pkg_manager)"
  log "Installing system packages with: $manager"

  case "$manager" in
    brew)
      install_pkg "$manager" git git
      install_pkg "$manager" curl curl
      install_pkg "$manager" python python3
      install_pkg "$manager" node node
      install_pkg "$manager" tmux tmux
      install_pkg "$manager" poppler pdftoppm
      install_pkg "$manager" fontconfig fc-list
      install_pkg "$manager" ghostscript gs
      install_pkg "$manager" imagemagick magick
      install_pkg_maybe "$manager" inkscape inkscape
      install_pkg_maybe "$manager" libheif heif-convert
      install_brew_cask_maybe libreoffice
      install_brew_cask_maybe mactex-no-gui
      ;;
    apt)
      install_pkg "$manager" git git
      install_pkg "$manager" curl curl
      install_pkg "$manager" python3 python3
      install_pkg "$manager" python3-pip pip3
      install_pkg "$manager" nodejs node
      install_pkg "$manager" npm npm
      install_pkg "$manager" tmux tmux
      install_pkg "$manager" libreoffice soffice
      install_pkg "$manager" poppler-utils pdftoppm
      install_pkg "$manager" fontconfig fc-list
      install_pkg "$manager" ghostscript gs
      install_pkg "$manager" imagemagick convert
      install_pkg_maybe "$manager" inkscape inkscape
      install_pkg_maybe "$manager" libheif-examples heif-convert
      install_pkg_maybe "$manager" xclip xclip
      install_pkg_maybe "$manager" latexmk latexmk
      install_pkg_maybe "$manager" biber biber
      install_pkg_maybe "$manager" texlive-latex-base pdflatex
      install_pkg_maybe "$manager" texlive-latex-recommended ""
      install_pkg_maybe "$manager" texlive-latex-extra ""
      install_pkg_maybe "$manager" texlive-fonts-recommended ""
      install_pkg_maybe "$manager" texlive-pictures ""
      ;;
    dnf)
      install_pkg "$manager" git git
      install_pkg "$manager" curl curl
      install_pkg "$manager" python3 python3
      install_pkg "$manager" python3-pip pip3
      install_pkg "$manager" nodejs node
      install_pkg "$manager" npm npm
      install_pkg "$manager" tmux tmux
      install_pkg_maybe "$manager" libreoffice soffice
      install_pkg_maybe "$manager" poppler-utils pdftoppm
      install_pkg_maybe "$manager" fontconfig fc-list
      install_pkg_maybe "$manager" ghostscript gs
      install_pkg_maybe "$manager" ImageMagick convert
      install_pkg_maybe "$manager" inkscape inkscape
      install_pkg_maybe "$manager" libheif heif-convert
      install_pkg_maybe "$manager" xclip xclip
      install_pkg_maybe "$manager" latexmk latexmk
      install_pkg_maybe "$manager" biber biber
      install_pkg_maybe "$manager" texlive-scheme-medium pdflatex
      install_pkg_maybe "$manager" texlive-collection-latexextra ""
      ;;
    pacman)
      install_pkg "$manager" git git
      install_pkg "$manager" curl curl
      install_pkg "$manager" python python3
      install_pkg "$manager" python-pip pip3
      install_pkg "$manager" nodejs node
      install_pkg "$manager" npm npm
      install_pkg "$manager" tmux tmux
      install_pkg_maybe "$manager" libreoffice-fresh soffice
      install_pkg_maybe "$manager" poppler pdftoppm
      install_pkg_maybe "$manager" fontconfig fc-list
      install_pkg_maybe "$manager" ghostscript gs
      install_pkg_maybe "$manager" imagemagick convert
      install_pkg_maybe "$manager" inkscape inkscape
      install_pkg_maybe "$manager" libheif heif-convert
      install_pkg_maybe "$manager" xclip xclip
      install_pkg_maybe "$manager" latexmk latexmk
      install_pkg_maybe "$manager" biber biber
      install_pkg_maybe "$manager" texlive-core pdflatex
      install_pkg_maybe "$manager" texlive-latexextra ""
      ;;
    apk)
      install_pkg "$manager" git git
      install_pkg "$manager" curl curl
      install_pkg "$manager" python3 python3
      install_pkg "$manager" py3-pip pip3
      install_pkg "$manager" nodejs node
      install_pkg "$manager" npm npm
      install_pkg "$manager" tmux tmux
      install_pkg_maybe "$manager" libreoffice soffice
      install_pkg_maybe "$manager" poppler-utils pdftoppm
      install_pkg_maybe "$manager" fontconfig fc-list
      install_pkg_maybe "$manager" ghostscript gs
      install_pkg_maybe "$manager" imagemagick convert
      install_pkg_maybe "$manager" inkscape inkscape
      install_pkg_maybe "$manager" libheif heif-convert
      install_pkg_maybe "$manager" xclip xclip
      install_pkg_maybe "$manager" texlive-full pdflatex
      ;;
    *)
      warn "no supported package manager found; skipping system package installation"
      ;;
  esac
}

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCOPE="global"
AGENT_ARGS=()
SKIP_SYSTEM_PACKAGES="0"
SKIP_PYTHON_PACKAGES="0"
SKIP_SMUX_RUNTIME="0"
SKIP_EXTERNAL_SKILLS="0"

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
    --skip-system-packages)
      SKIP_SYSTEM_PACKAGES="1"
      shift
      ;;
    --skip-python-packages)
      SKIP_PYTHON_PACKAGES="1"
      shift
      ;;
    --skip-smux-runtime)
      SKIP_SMUX_RUNTIME="1"
      shift
      ;;
    --skip-external-skills)
      SKIP_EXTERNAL_SKILLS="1"
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

if [[ "$SKIP_SYSTEM_PACKAGES" != "1" ]]; then
  install_system_packages
fi

require_cmd python3
require_cmd npm
require_cmd npx

if [[ "$SKIP_PYTHON_PACKAGES" != "1" ]]; then
  log "Installing Python helpers for slide rendering"
  pip_install_user python3 pip
  pip_install_user python3 Pillow pdf2image python-pptx numpy
fi

log "Installing shared Node tooling"
npm install -g pnpm

if [[ "$SKIP_SMUX_RUNTIME" != "1" ]]; then
  log "Installing local smux runtime"
  bash "$REPO_ROOT/skills/smux/runtime/install.sh" install
fi

repo_args=()
if [[ "$SCOPE" == "project" ]]; then
  repo_args+=("--project")
else
  repo_args+=("--global")
fi
repo_args+=("${AGENT_ARGS[@]}")

log "Installing repo skills"
bash "$REPO_ROOT/installers/install-repo-skills.sh" "${repo_args[@]}"

if [[ "$SKIP_EXTERNAL_SKILLS" != "1" ]]; then
  log "Installing external skills"
  bash "$REPO_ROOT/installers/install-external-skills.sh" "${repo_args[@]}"
fi

log "Bootstrap complete"
