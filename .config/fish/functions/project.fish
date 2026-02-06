function project --description "Switch to project and setup environment"
    set -l proj $argv[1]
    
    if test (count $argv) -eq 0
        echo "Usage: project <name>"
        echo ""
        echo "Available projects:"
        echo "  next, web       - Next.js web app"
        echo "  dotfiles, dots  - Dotfiles repository"
        echo "  blog, wp        - WordPress blog"
        return 1
    end
    
    switch $proj
        case next next-starter web
            cd ~/ghq/github.com-stelixx/Stelixx-Studio/next-starter
            set -gx NODE_ENV development
            echo "📂 Switched to: next-starter"
            echo "🌍 NODE_ENV=$NODE_ENV"
            
        case dotfiles dots
            cd ~/dotfiles-public
            echo "📂 Switched to: dotfiles-public"
            
        case blog wp wordpress
            cd ~/ghq/github.com-stelixx/Stelixx-Studio/next-starter/apps/wp-blog
            echo "📂 Switched to: wp-blog"
            
        case '*'
            echo "❌ Unknown project: $proj"
            echo "Run 'project' to see available options"
            return 1
    end
    
    # Update terminal title
    set -l project_name (basename $PWD)
    echo -ne "\033]0;$project_name\007"
    
    # Show current directory
    ls -la
end

# Autocomplete
complete -c project -f -a "next web dotfiles dots blog wp"
