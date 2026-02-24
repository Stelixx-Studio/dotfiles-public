# ==============================================================================
# PATH Management - Modern fish_add_path pattern
# Priority: Homebrew → User bins → Language tools → System defaults
# ==============================================================================

# Homebrew (CRITICAL - must be first for fish/brew commands)
fish_add_path --prepend --move /opt/homebrew/bin
fish_add_path --prepend --move /opt/homebrew/sbin

# User binaries (highest priority after Homebrew)
fish_add_path --prepend --move ~/.local/bin
fish_add_path --prepend --move ~/bin

# PNPM (Node.js package manager)
set -gx PNPM_HOME ~/Library/pnpm
fish_add_path --prepend --move $PNPM_HOME

# Go language
set -gx GOPATH ~/go
fish_add_path --append $GOPATH/bin

# Ruby version managers (conditional)
if command -v rbenv >/dev/null
    # rbenv shims will be added by lazy init
else if test -d ~/.rvm/bin
    fish_add_path ~/.rvm/bin
end

# Flutter & Dart
if test -d ~/fvm/default/bin
    fish_add_path --prepend ~/fvm/default/bin
end
if test -d ~/.pub-cache/bin
    fish_add_path --append ~/.pub-cache/bin
end

# Development tools (VS Code alternatives)
fish_add_path --append ~/.codeium/windsurf/bin
fish_add_path --append ~/.antigravity/antigravity/bin
fish_add_path --append ~/.opencode/bin

# Android SDK (manual install from Google, not Homebrew)
if test -d ~/Library/Android/sdk
    set -gx ANDROID_HOME ~/Library/Android/sdk
    fish_add_path --append $ANDROID_HOME/cmdline-tools/latest/bin
    fish_add_path --append $ANDROID_HOME/platform-tools
end

# Project-local bins (ONLY in interactive shells to avoid overhead in automation)
if status is-interactive
    if test -d node_modules/.bin
        fish_add_path --append --move node_modules/.bin
    end
    if test -d bin
        fish_add_path --append --move ./bin
    end
end

# Note: fish_add_path automatically deduplicates and handles prepending/appending correctly.
# No manual loop needed.
