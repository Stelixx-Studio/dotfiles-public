function gsync --description "Sync current branch with main and update dependencies"
    echo "🔄 Fetching from origin..."
    git fetch origin
    
    echo "🔀 Rebasing onto origin/main..."
    if git rebase origin/main
        echo "✅ Rebase successful"
        
        # Update dependencies if package manager files exist
        if test -f package.json
            echo "📦 Updating npm dependencies..."
            if type -q pnpm
                pnpm install
            else if type -q yarn
                yarn install
            else
                npm install
            end
        end
        
        if test -f Gemfile
            echo "💎 Updating Ruby gems..."
            bundle install
        end
        
        echo "✅ Sync complete!"
    else
        echo "❌ Rebase failed. Fix conflicts and run: git rebase --continue"
        return 1
    end
end
