# Keep zsh for automation/AI runtimes. Only jump to fish for normal human terminal sessions.
typeset -i _is_human_terminal=1

if [[ ! -o interactive ]] || [[ ! -t 0 ]] || [[ ! -t 1 ]]; then
  _is_human_terminal=0
fi

if [[ -n "${CI:-}" ]] || [[ -n "${CODEX_SHELL:-}" ]] || [[ -n "${CODEX_CI:-}" ]]; then
  _is_human_terminal=0
fi

_parent_cmd="$(ps -o comm= -p "$PPID" 2>/dev/null)"
case "$_parent_cmd" in
  *codex*|*antigravity*|*opencode*|*aider*|*claude*|*agent*)
    _is_human_terminal=0
    ;;
esac

if (( _is_human_terminal )); then
  if [[ -x /opt/homebrew/bin/fish ]]; then
    exec /opt/homebrew/bin/fish -l
  elif [[ -x /usr/local/bin/fish ]]; then
    exec /usr/local/bin/fish -l
  fi
fi

unset _is_human_terminal _parent_cmd

# Existing env
export PATH="$PATH:$HOME/.rvm/bin"
export NODE_OPTIONS="--max-old-space-size=8192"
