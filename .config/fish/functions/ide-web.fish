function ide-web --description "Launch IDE for next-starter web project"
    set -l project_path ~/ghq/github.com-stelixx/Stelixx-Studio/next-starter
    
    if not test -d $project_path
        echo "❌ Project not found: $project_path"
        return 1
    end
    
    cd $project_path
    
    if set -q TMUX
        echo "❌ Already in tmux session!"
        return 1
    end
    
    set -l session_name web
    
    # Create session with nvim
    tmux new-session -d -s $session_name
    tmux send-keys -t $session_name "nvim" C-m
    
    # Right sidebar - test watcher
    tmux split-window -h -t $session_name -l 25%
    tmux send-keys -t $session_name "pnpm test:watch" C-m
    
    # Bottom left - dev server
    tmux select-pane -t $session_name -L
    tmux split-window -v -t $session_name -l 30%
    tmux send-keys -t $session_name "pnpm dev" C-m
    
    # Bottom right - git status
    tmux split-window -h -t $session_name
    tmux send-keys -t $session_name "git status" C-m
    
    # Select main editor
    tmux select-pane -t $session_name -U
    tmux attach -t $session_name
end
