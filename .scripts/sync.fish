# Sync Script - Update dotfiles from system

set -e

echo "📦 Syncing dotfiles from system..."

# Fish shell configs
echo "🐟 Syncing Fish configs..."
cp -v ~/.config/fish/config.fish .config/fish/
cp -v ~/.config/fish/config-osx.fish .config/fish/
cp -v ~/.config/fish/fish_plugins .config/fish/
cp -rv ~/.config/fish/conf.d/*.fish .config/fish/conf.d/
cp -rv ~/.config/fish/functions/rbenv.fish .config/fish/functions/ 2>/dev/null || true

# Git config
echo "🔧 Syncing Git config..."
cp -v ~/.gitconfig .gitconfig 2>/dev/null || echo "⚠️ No .gitconfig found"

# Show changes
echo ""
echo "📊 Changes:"
git status --short

echo ""
echo "✅ Sync complete!"
echo ""
echo "Next steps:"
echo "  git add -A"
echo "  git commit -m 'docs: update dotfiles'"
echo "  git push"
