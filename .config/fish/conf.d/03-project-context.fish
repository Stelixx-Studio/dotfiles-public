# Auto-load project environment variables when entering directory
function __load_project_env --on-variable PWD
    # Load direnv if available
    if test -f .envrc
        if type -q direnv
            direnv allow 2>/dev/null
        end
    end
    
    # Update window title with project name
    set -l project_name (basename $PWD)
    echo -ne "\033]0;$project_name\007"
end
