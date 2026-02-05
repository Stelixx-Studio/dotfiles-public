function rbenv --description 'Lazy-load rbenv on first use'
    # Remove this wrapper function
    functions -e rbenv
    
    # Initialize rbenv for real
    if command -v rbenv >/dev/null
        status is-interactive; and command rbenv init - --no-rehash fish | source
    end
    
    # Execute the original command
    command rbenv $argv
end
