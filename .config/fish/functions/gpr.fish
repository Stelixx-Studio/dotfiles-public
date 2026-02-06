function gpr --description "Create pull request to release branch"
    set -l branch (git branch --show-current)
    set -l target $argv[1]
    
    if test -z "$target"
        set target "release/web/staging"
    end
    
    if not type -q gh
        echo "Error: gh CLI not installed. Install with: brew install gh"
        return 1
    end
    
    echo "Creating PR: $branch → $target"
    gh pr create --base $target --head $branch --fill
end
