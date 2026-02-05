# Installation Script for Yoong's Dotfiles

set -e

echo "🚀 Installing Yoong's Dotfiles..."

# Check if Fish is installed
if not command -v fish >/dev/null
    echo "❌ Fish shell not found. Please install Fish first:"
    echo "   brew install fish"
    exit 1
end

# Backup existing config
if test -d ~/.config/fish
    set backup_dir ~/.config/fish.backup-(date +%Y%m%d-%H%M%S)
    echo "📦 Backing up existing Fish config to $backup_dir"
    mv ~/.config/fish $backup_dir
end

# Create symlink
echo "🔗 Creating symlink..."
ln -s ~/dotfiles-public/.config/fish ~/.config/fish

# Install Fisher if not already installed
if not type -q fisher
    echo "📥 Installing Fisher plugin manager..."
    curl -sL https://raw.githubusercontent.com/jorgebucaran/fisher/main/functions/fisher.fish | source
    fisher install jorgebucaran/fisher
end

# Install Fisher plugins
echo "📦 Installing Fisher plugins..."
fisher update

# Git config
if test -f ~/dotfiles-public/.gitconfig
    echo "🔗 Symlinking .gitconfig..."
    test -f ~/.gitconfig && mv ~/.gitconfig ~/.gitconfig.backup
    ln -s ~/dotfiles-public/.gitconfig ~/.gitconfig
end

echo ""
echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Restart your terminal or run: exec fish"
echo "2. Configure Tide prompt: tide configure"
echo "3. Install recommended tools: brew install eza fzf ghq bat"
echo ""
echo "📊 Check startup time: time fish -c exit"
echo "🎯 Verify no PATH duplicates: echo \$PATH | tr ' ' '\\n' | sort | uniq -d"
