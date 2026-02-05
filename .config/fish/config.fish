# ==============================================================================
# Fish Shell Configuration
# Main orchestrator - loads modular configs
# ==============================================================================

# Disable greeting
set fish_greeting ""

# Basic terminal setup
set -gx TERM xterm-256color

# Theme settings (for compatibility with older Fish themes)
set -g theme_color_scheme terminal-dark
set -g fish_prompt_pwd_dir_length 1
set -g theme_display_user yes
set -g theme_hide_hostname no
set -g theme_hostname always

# OS-specific configuration
switch (uname)
    case Darwin
        test -f ~/.config/fish/config-osx.fish; and source ~/.config/fish/config-osx.fish
    case Linux
        test -f ~/.config/fish/config-linux.fish; and source ~/.config/fish/config-linux.fish
    case '*'
        test -f ~/.config/fish/config-windows.fish; and source ~/.config/fish/config-windows.fish
end

# Note: conf.d/*.fish files are auto-loaded by Fish in alphabetical order
# Load order: 00-path.fish → 01-env.fish → 02-aliases.fish → 03-tools.fish

