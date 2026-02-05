# Quick Start Guide

Get up and running with these dotfiles in 5 minutes.

## Prerequisites

- macOS (tested on macOS Ventura+)
- Homebrew installed
- Git configured

## 1. Install Fish Shell

```fish
brew install fish
```

## 2. Clone This Repository

```fish
git clone git@github.com-stelixx:Stelixx-Studio/dotfiles-public.git ~/dotfiles-public
cd ~/dotfiles-public
```

## 3. Backup Existing Configs

```fish
# Backup your current Fish config
mv ~/.config/fish ~/.config/fish.backup-$(date +%Y%m%d)

# Backup your current Git config (optional)
cp ~/.gitconfig ~/.gitconfig.backup
```

## 4. Run Installation Script

```fish
./.scripts/install.fish
```

This will:
- Create symlinks to configs
- Install Fisher plugin manager
- Install all Fisher plugins from `fish_plugins`
- Set up Git config

## 5. Restart Terminal

```fish
exec fish
```

## 6. Configure Tide Prompt

```fish
tide configure
```

Choose your preferred style:
- **Lean** - Minimal, fast (Recommended)
- **Classic** - Two-line with decorations
- **Rainbow** - Colorful

## 7. Install Recommended Tools (Optional)

```fish
# Essential CLI tools
brew install eza bat fzf ripgrep fd ghq delta

# Git UI
brew install lazygit

# System monitoring
brew install htop btop
```

## 8. Verify Installation

```fish
# Check startup time (should be <200ms)
time fish -c exit

# Check for PATH duplicates (should be empty)
echo $PATH | tr ' ' '\n' | sort | uniq -d

# Verify commands
command -v git node pnpm ruby java
```

## Expected Results

After installation, you should see:
- ⚡ Fast shell startup (~100ms)
- 🎨 Tide prompt with git status
- 🔧 All aliases working (`ll`, `g`, `vim`)
- 📦 Clean PATH with no duplicates

## Troubleshooting

### Fisher not found

```fish
curl -sL https://raw.githubusercontent.com/jorgebucaran/fisher/main/functions/fisher.fish | source
fisher install jorgebucaran/fisher
```

### Slow startup

```fish
# Profile startup
fish --profile-startup=/tmp/fish-profile.log
cat /tmp/fish-profile.log
```

### Tide not showing

```fish
fisher install IlanCosman/tide@v6
tide configure
```

### PATH issues

```fish
set -e fish_user_paths
exec fish
```

## Next Steps

1. **Customize**: Edit configs in `~/.config/fish/conf.d/`
2. **Add tools**: See [docs/TOOLS.md](TOOLS.md) for recommendations
3. **Screenshot**: Take a screenshot for your setup
4. **Sync**: Use `.scripts/sync.fish` to backup changes

## Rollback

If anything goes wrong:

```fish
# Remove dotfiles
rm ~/.config/fish

# Restore backup
mv ~/.config/fish.backup-* ~/.config/fish

# Restart
exec fish
```

## Support

- 📖 [Full Documentation](../README.md)
- 🛠️ [Tools Guide](TOOLS.md)
- 🐛 [Report Issues](https://github.com/Stelixx-Studio/dotfiles-public/issues)
