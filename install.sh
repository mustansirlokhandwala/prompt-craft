#!/usr/bin/env bash
# Install or uninstall prompt-craft for Claude Code and Antigravity (macOS and Linux).
#
#   curl -fsSL https://raw.githubusercontent.com/mustansirlokhandwala/prompt-craft/main/install.sh | bash
#   ./install.sh [--claude] [--antigravity] [--uninstall]
#
# With no tool flags it sets up every tool it finds. Skills are symlinked, so
# re-running the installer (or `git pull` in the source folder) updates them.
set -euo pipefail

REPO_URL="https://github.com/mustansirlokhandwala/prompt-craft.git"
START="<!-- prompt-craft:start -->"
END="<!-- prompt-craft:end -->"

want_claude=0 want_ag=0 uninstall=0
for arg in "$@"; do
  case "$arg" in
    --claude) want_claude=1 ;;
    --antigravity) want_ag=1 ;;
    --uninstall) uninstall=1 ;;
    -h|--help) sed -n '2,8p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown option: $arg (try --help)" >&2; exit 2 ;;
  esac
done
explicit=$((want_claude + want_ag))

# Source folder: this clone if the script lives in one, otherwise a managed clone.
here="$(cd "$(dirname "${BASH_SOURCE[0]:-.}")" 2>/dev/null && pwd || echo .)"
if [ -d "$here/skills" ] && [ -f "$here/rules/always-on.md" ]; then
  SRC="$here"
else
  SRC="${PROMPT_CRAFT_HOME:-$HOME/.prompt-craft}"
  if [ "$uninstall" -eq 0 ]; then
    command -v git >/dev/null || { echo "error: git is required" >&2; exit 1; }
    if [ -d "$SRC/.git" ]; then git -C "$SRC" pull -q --ff-only
    else git clone -q --depth 1 "$REPO_URL" "$SRC"; fi
  fi
fi

# Remove our marked block from a file, leaving everything else untouched.
strip_block() {
  [ -f "$1" ] || return 0
  awk -v s="$START" -v e="$END" '$0==s{skip=1;next} $0==e{skip=0;next} !skip' "$1" > "$1.tmp" && mv "$1.tmp" "$1"
}

# Replace our block in a file with new content; backs the file up once.
write_block() {
  local file="$1" body="$2"
  mkdir -p "$(dirname "$file")"
  [ -f "$file" ] && [ ! -f "$file.prompt-craft.bak" ] && cp "$file" "$file.prompt-craft.bak"
  strip_block "$file"
  { [ -s "$file" ] && echo; echo "$START"; printf '%s\n' "$body"; echo "$END"; } >> "$file"
}

link_skills() {
  local dir="$1" name target
  mkdir -p "$dir"
  for s in "$SRC"/skills/*/; do
    name="$(basename "$s")"; target="$dir/$name"
    if [ -e "$target" ] && [ ! -L "$target" ]; then
      echo "  skip $name: $target already exists and isn't ours" >&2; continue
    fi
    ln -sfn "${s%/}" "$target"
  done
}

unlink_skills() {
  local dir="$1" link
  [ -d "$dir" ] || return 0
  for link in "$dir"/*; do
    [ -L "$link" ] || continue
    case "$(readlink "$link")" in "$SRC"/skills/*) rm "$link" ;; esac
  done
}

ag_skills_dir() {
  if [ -n "${ANTIGRAVITY_SKILLS_DIR:-}" ]; then echo "$ANTIGRAVITY_SKILLS_DIR"
  elif [ -d "$HOME/.gemini/antigravity" ] && [ ! -d "$HOME/.gemini/config" ]; then echo "$HOME/.gemini/antigravity/skills"
  else echo "$HOME/.gemini/config/skills"; fi
}

did=0
if [ "$want_claude" -eq 1 ] || { [ "$explicit" -eq 0 ] && [ -d "$HOME/.claude" ]; }; then
  did=1
  if [ "$uninstall" -eq 1 ]; then
    unlink_skills "$HOME/.claude/skills"; strip_block "$HOME/.claude/CLAUDE.md"
    echo "Claude Code: removed"
  else
    link_skills "$HOME/.claude/skills"
    write_block "$HOME/.claude/CLAUDE.md" "@$SRC/rules/always-on.md"
    echo "Claude Code: skills in ~/.claude/skills, rules loaded from ~/.claude/CLAUDE.md"
  fi
fi

if [ "$want_ag" -eq 1 ] || { [ "$explicit" -eq 0 ] && [ -d "$HOME/.gemini" ]; }; then
  did=1; agdir="$(ag_skills_dir)"
  if [ "$uninstall" -eq 1 ]; then
    unlink_skills "$agdir"; strip_block "$HOME/.gemini/GEMINI.md"
    echo "Antigravity: removed"
  else
    link_skills "$agdir"
    # Antigravity has no import syntax we can rely on, so the rules are copied in.
    write_block "$HOME/.gemini/GEMINI.md" "$(cat "$SRC/rules/always-on.md")"
    echo "Antigravity: skills in ${agdir/#$HOME/~}, rules in ~/.gemini/GEMINI.md"
  fi
fi

if [ "$did" -eq 0 ]; then
  echo "No Claude Code (~/.claude) or Antigravity (~/.gemini) found. Use --claude or --antigravity to set one up anyway." >&2
  exit 1
fi
if [ "$uninstall" -eq 1 ] && [ "$SRC" = "${PROMPT_CRAFT_HOME:-$HOME/.prompt-craft}" ] && [ -d "$SRC" ]; then
  echo "The downloaded copy is still in $SRC. Delete it with: rm -rf \"$SRC\""
fi
echo "Done. Start a new session to load the changes."
