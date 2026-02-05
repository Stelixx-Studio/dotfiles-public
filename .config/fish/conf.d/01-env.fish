# ==============================================================================
# Environment Variables
# Non-PATH environment configuration
# ==============================================================================

# Editor
set -gx EDITOR nvim

# Terminal
set -gx TERM xterm-256color

# Java - Dynamic Homebrew detection (prefer Java 17)
if test -d /opt/homebrew/opt/openjdk@17
    set -gx JAVA_HOME /opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home
    set -gx CPPFLAGS "-I/opt/homebrew/opt/openjdk@17/include"
    fish_add_path --prepend $JAVA_HOME/bin
else if test -d /opt/homebrew/opt/openjdk@21
    # Fallback to Java 21 if 17 not found
    set -gx JAVA_HOME /opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home
    set -gx CPPFLAGS "-I/opt/homebrew/opt/openjdk@21/include"
    fish_add_path --prepend $JAVA_HOME/bin
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
