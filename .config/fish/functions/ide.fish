function ide --description "Launch tmux IDE layout"
    if set -q TMUX
        echo "❌ Already in tmux session!"
        return 1
    end
    
    set -l session_name dev
    
    # Create new session with nvim in main pane
    tmux new-session -d -s $session_name
    tmux send-keys -t $session_name "nvim" C-m
    
    # Right sidebar (25% width) - for tests/logs
    tmux split-window -h -t $session_name -l 25%
    
    # Bottom terminals (30% height of main pane)
    tmux select-pane -t $session_name -L
    tmux split-window -v -t $session_name -l 30%
    
    # Split bottom into two terminals
    tmux split-window -h -t $session_name
    
    # Select main editor pane
    tmux select-pane -t $session_name -U
    
    # Attach to session
    tmux attach -t $session_name
end
