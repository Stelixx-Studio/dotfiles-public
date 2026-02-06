function gc --description "Smart conventional commit"
    set -l type $argv[1]
    set -l msg $argv[2..-1]
    
    if test (count $argv) -lt 2
        echo "Usage: gc <type> <message>"
        echo "Types: feat, fix, docs, style, refactor, test, chore"
        return 1
    end
    
    switch $type
        case feat fix docs style refactor test chore perf ci build revert
            git commit -m "$type: $msg"
        case '*'
            # If type is unknown, treat entire input as message
            git commit -m "$type $msg"
    end
end
