# Sync Script - Update dotfiles from system

set -e

echo "📦 Syncing dotfiles from system..."

# Fish shell configs
echo "🐟 Syncing Fish configs..."
mkdir -p .config/fish/conf.d .config/fish/functions
cp -v ~/.config/fish/config.fish .config/fish/ 2>/dev/null || true
cp -v ~/.config/fish/config-osx.fish .config/fish/ 2>/dev/null || true
cp -v ~/.config/fish/fish_plugins .config/fish/ 2>/dev/null || true
# Sync only .fish files in conf.d, excluding local/secret ones if any
cp -rv ~/.config/fish/conf.d/*.fish .config/fish/conf.d/ 2>/dev/null || true
# Sync functions
cp -rv ~/.config/fish/functions/*.fish .config/fish/functions/ 2>/dev/null || true

# Ghostty
if test -d ~/.config/ghostty
    echo "👻 Syncing Ghostty config..."
    mkdir -p .config/ghostty
    cp -rv ~/.config/ghostty/* .config/ghostty/
end

# Lazygit
if test -d ~/.config/lazygit
    echo "git Syncing Lazygit config..."
    mkdir -p .config/lazygit
    cp -rv ~/.config/lazygit/config.yml .config/lazygit/ 2>/dev/null || true
end

# Mise
if test -d ~/.config/mise
    echo "⚙️ Syncing Mise config..."
    mkdir -p .config/mise
    cp -rv ~/.config/mise/config.toml .config/mise/ 2>/dev/null || true
end

# Tmux
if test -d ~/.config/tmux
    echo "🪟 Syncing Tmux config..."
    mkdir -p .config/tmux
    cp -rv ~/.config/tmux/*.conf .config/tmux/ 2>/dev/null || true
end

# Neovim (Essential files)
if test -d ~/.config/nvim
    echo "💤 Syncing Neovim essential config..."
    mkdir -p .config/nvim/lua
    cp -v ~/.config/nvim/init.lua .config/nvim/ 2>/dev/null || true
    cp -v ~/.config/nvim/lazy-lock.json .config/nvim/ 2>/dev/null || true
    cp -v ~/.config/nvim/*.json .config/nvim/ 2>/dev/null || true
    cp -rv ~/.config/nvim/lua/* .config/nvim/lua/ 2>/dev/null || true
end

# Homebrew
echo "🍺 Syncing Homebrew bundle..."
brew bundle dump --force --file=Brewfile

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
echo "  git commit -m 'feat: update expanded dotfiles coverage'"
echo "  git push"
