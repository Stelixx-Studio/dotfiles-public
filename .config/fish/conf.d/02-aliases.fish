# ==============================================================================
# Command Aliases
# Short commands and replacements
# ==============================================================================

# Filesystem
alias ls "ls -p -G"
alias la "ls -A"
alias ll "ls -l"
alias lla "ll -A"

# Git shorthand
alias g git

# Neovim
if command -v nvim >/dev/null
    alias vim nvim
end

# Terminal launcher (WezTerm)
if test -d /Applications/WezTerm.app
    alias terminal '/Applications/WezTerm.app/Contents/MacOS/wezterm start'
end

# macOS Firewall shortcut
if test (uname) = Darwin
    alias socketfilterfw /usr/libexec/ApplicationFirewall/socketfilterfw
end
