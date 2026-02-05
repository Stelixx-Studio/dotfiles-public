# ==============================================================================
# External Tool Initialization
# Heavy/slow-loading tools loaded last
# ==============================================================================

# RVM and rbenv use lazy loading (see functions/rbenv.fish)
# They will be initialized on first use to speed up shell startup

# OrbStack - Docker/Linux alternative
if test -f ~/.orbstack/shell/init2.fish
    source ~/.orbstack/shell/init2.fish 2>/dev/null
end

# Flutter project-specific functions (auto-load only in Flutter projects)
if test -f pubspec.yaml
    if test -f ~/.config/fish/functions/flutter-familylink.fish
        source ~/.config/fish/functions/flutter-familylink.fish
    end
end

# Auto-load project-specific config (if exists)
set -l local_config ~/.config/fish/config-local.fish
if test -f $local_config
    source $local_config
end
