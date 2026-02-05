# ==============================================================================
# PATH Management - Modern fish_add_path pattern
# Priority: User bins → Language tools → System defaults
# ==============================================================================

# User binaries (highest priority)
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

# Android SDK
if test -d ~/Library/Android/sdk
    set -gx ANDROID_HOME ~/Library/Android/sdk
    fish_add_path --append $ANDROID_HOME/platform-tools
end

# Project-local bins (LAST - lowest priority to avoid conflicts)
# Only add if in a project directory with these folders
if test -d node_modules/.bin
    fish_add_path --append node_modules/.bin
end
if test -d bin
    fish_add_path --append ./bin
end

# Deduplicate PATH by removing duplicates (keeps first occurrence)
# This handles system PATH duplicates that Fish doesn't control
set -l unique_paths
for p in $PATH
    if not contains $p $unique_paths
        set -a unique_paths $p
    end
end
set -gx PATH $unique_paths
