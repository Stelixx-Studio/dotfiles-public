# Yoong's dotfiles

> ⚠️ **Warning**: Don't blindly use my settings unless you know what that entails. Use at your own risk!

## Contents

- Fish shell config (modernized with modular structure)
- Git config
- Development tools setup

## Shell setup (macOS)

### Fish Shell

- [Fish shell](https://fishshell.com/) - v4.4.0
- [Fisher](https://github.com/jorgebucaran/fisher) - Plugin manager
- [Tide](https://github.com/IlanCosman/tide) - Shell theme (v6)
- [Nerd fonts](https://github.com/ryanoasis/nerd-fonts) - Patched fonts
- [z for fish](https://github.com/jethrokuan/z) - Directory jumping
- [Eza](https://github.com/eza-community/eza) - `ls` replacement
- [ghq](https://github.com/x-motemen/ghq) - Local Git repository organizer
- [fzf](https://github.com/PatrickF1/fzf.fish) - Interactive filtering

### Features

- ⚡ **Fast startup**: 103ms (optimized from 320ms)
- 🎯 **Zero PATH duplicates**: Automatic deduplication
- 🔧 **Lazy loading**: rbenv and RVM load on-demand
- ☕ **Dynamic Java detection**: Auto-detects via Homebrew
- 📦 **Modular structure**: Organized config files

## File Structure

```
.config/fish/
├── config.fish           # Main orchestrator (minimal)
├── config-osx.fish       # macOS-specific settings
├── fish_plugins          # Fisher plugins list
├── conf.d/
│   ├── 00-path.fish     # PATH management (fish_add_path)
│   ├── 01-env.fish      # Environment variables
│   ├── 02-aliases.fish  # Command aliases
│   └── 03-tools.fish    # External tools initialization
└── functions/
    └── rbenv.fish       # Lazy loading for rbenv
```

## Installation

### 1. Clone this repository

```fish
git clone git@github.com-stelixx:Stelixx-Studio/dotfiles-public.git ~/dotfiles-public
```

### 2. Install Fish shell

```fish
brew install fish
```

### 3. Install Fisher (plugin manager)

```fish
curl -sL https://raw.githubusercontent.com/jorgebucaran/fisher/main/functions/fisher.fish | source && fisher install jorgebucaran/fisher
```

### 4. Symlink configs

```fish
# Backup existing configs
mv ~/.config/fish ~/.config/fish.backup

# Create symlink
ln -s ~/dotfiles-public/.config/fish ~/.config/fish

# Install Fisher plugins
fisher update
```

### 5. Install Tide prompt

```fish
fisher install IlanCosman/tide@v6
tide configure
```

### 6. Set Fish as default shell

```fish
echo /opt/homebrew/bin/fish | sudo tee -a /etc/shells
chsh -s /opt/homebrew/bin/fish
```

## Additional Tools

### Required

```fish
brew install git node pnpm go
```

### Optional (for full functionality)

```fish
brew install eza fzf ghq bat ripgrep fd
brew install rbenv # Ruby version manager
brew install openjdk@17 # Java
```

### Fisher Plugins

Plugins are listed in `.config/fish/fish_plugins`:

```
jorgebucaran/fisher
jorgebucaran/nvm.fish
ilancosman/tide@v6
jethrokuan/z
decors/fish-ghq
patrickf1/fzf.fish
```

Install all with:

```fish
fisher update
```

## Customization

### PATH Management

Edit `.config/fish/conf.d/00-path.fish` to add custom paths.

**Best practices**:
- Use `fish_add_path` (not `set -gx PATH`)
- Use `--prepend` for high-priority paths
- Use `--append` for low-priority paths
- Use `--move` flag to prevent duplicates

### Environment Variables

Edit `.config/fish/conf.d/01-env.fish` for custom environment variables.

### Aliases

Edit `.config/fish/conf.d/02-aliases.fish` for custom command aliases.

### External Tools

Edit `.config/fish/conf.d/03-tools.fish` to configure tool initialization.

## Performance

- **Startup time**: ~100ms (achieved through lazy loading)
- **PATH entries**: 40 (deduplicated)
- **Config size**: 31 lines in main config.fish (vs 99 lines before)

## Git Configuration

See `.gitconfig` for Git settings including:
- User info
- Aliases
- Diff/merge tools
- Colors and formatting

## Maintenance

### Update Fisher plugins

```fish
fisher update
```

### Update Fish shell

```fish
brew upgrade fish
```

### Check startup time

```fish
time fish -c exit
```

### Verify PATH

```fish
echo $PATH | tr ' ' '\n' | sort | uniq -d  # Should be empty
```

## Troubleshooting

### Rollback to backup

If something breaks:

```fish
rm ~/.config/fish
mv ~/.config/fish.backup ~/.config/fish
exec fish
```

### Reset PATH cache

```fish
set -e fish_user_paths
exec fish
```

### Debug config loading

```fish
fish --debug-output=/tmp/fish-debug.log
cat /tmp/fish-debug.log
```

## About

Personal dotfiles for macOS development environment.

**Last updated**: February 6, 2026

## License

MIT
