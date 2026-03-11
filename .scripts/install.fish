# Installation Script for Yoong's Dotfiles

set repo_root (cd (dirname (status --current-filename))/..; pwd)
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

# Create fish config directory
echo "📁 Creating Fish config directory..."
mkdir -p ~/.config/fish

# Granular symlinks for Fish
echo "🔗 Creating granular symlinks for Fish..."
set -l fish_items config.fish config-osx.fish fish_plugins conf.d functions completions themes
for item in $fish_items
    if test -e "$repo_root/.config/fish/$item"
        ln -sfn "$repo_root/.config/fish/$item" ~/.config/fish/$item
        echo "   ✅ Linked $item"
    end
end

# Zsh config for AI-agent-safe fish handoff
if test -f ~/.zshrc
    set zsh_backup ~/.zshrc.backup-(date +%Y%m%d-%H%M%S)
    echo "📦 Backing up existing .zshrc to $zsh_backup"
    mv ~/.zshrc $zsh_backup
end
echo "🔗 Symlinking .zshrc..."
ln -sfn "$repo_root/.zshrc" ~/.zshrc

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
if test -f "$repo_root/.gitconfig"
    echo "🔗 Symlinking .gitconfig..."
    test -f ~/.gitconfig -a ! -L ~/.gitconfig && mv ~/.gitconfig ~/.gitconfig.backup
    ln -sfn "$repo_root/.gitconfig" ~/.gitconfig
end

echo ""
echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Restart your terminal or run: exec fish"
echo "2. Configure Tide prompt: tide configure"
echo "3. Install recommended tools: brew install eza fzf ghq bat"
echo "4. Ensure login shell is zsh: chsh -s /bin/zsh"
echo ""
echo "📊 Check startup time: time fish -c exit"
echo "🎯 Verify no PATH duplicates: echo \$PATH | tr ' ' '\\n' | sort | uniq -d"
