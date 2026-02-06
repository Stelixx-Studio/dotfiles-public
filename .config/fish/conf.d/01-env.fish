# ==============================================================================
# Environment Variables
# Non-PATH environment configuration
# ==============================================================================

# Editor
set -gx EDITOR nvim

# Terminal
set -gx TERM xterm-256color

# Java - Use Homebrew symlink (shorter path, auto-updates)
if test -d /opt/homebrew/opt/openjdk@17
    set -gx JAVA_HOME /opt/homebrew/opt/openjdk@17
    set -gx CPPFLAGS "-I/opt/homebrew/opt/openjdk@17/include"
    fish_add_path --prepend /opt/homebrew/opt/openjdk@17/bin
else if test -d /opt/homebrew/opt/openjdk@21
    set -gx JAVA_HOME /opt/homebrew/opt/openjdk@21
    set -gx CPPFLAGS "-I/opt/homebrew/opt/openjdk@21/include"
    fish_add_path --prepend /opt/homebrew/opt/openjdk@21/bin
end

# Inkdrop (macOS only)
if test (uname) = Darwin
    set -gx INKDROP_HOME ~/.inkdrop
end

# Node.js memory optimization (for large projects)
set -gx NODE_OPTIONS "--max-old-space-size=8192"

# Disable Fish greeting
set -g fish_greeting ""

# FZF preview configuration
set -g FZF_PREVIEW_FILE_CMD "bat --style=numbers --color=always --line-range :500"
set -g FZF_LEGACY_KEYBINDINGS 0
