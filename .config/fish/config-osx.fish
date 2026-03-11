if type -q eza
  if set -q CODEX_SHELL
    alias ll "eza -l -g --icons=never"
  else
    alias ll "eza -l -g --icons"
  end
  alias lla "ll -a"
end

# Inkdrop
set -gx INKDROP_HOME ~/.inkdrop

# Fzf
set -g FZF_PREVIEW_FILE_CMD "bat --style=numbers --color=always --line-range :500"
set -g FZF_LEGACY_KEYBINDINGS 0
