# Recommended Tools & Setup

This document lists recommended tools that work well with this dotfiles setup.

## Essential Tools

### Terminal Emulators

- **[WezTerm](https://wezfurlong.org/wezterm/)** - GPU-accelerated, cross-platform (Recommended)
- **[iTerm2](https://iterm2.com/)** - macOS native, feature-rich
- **[Kitty](https://sw.kovidgoyal.net/kitty/)** - Fast, GPU-based
- **[Alacritty](https://alacritty.org/)** - Minimal, GPU-accelerated

### Fonts

- **[Nerd Fonts](https://www.nerdfonts.com/)** - Patched fonts with icons
  - Recommended: FiraCode Nerd Font, JetBrains Mono Nerd Font
  - Install: `brew install --cask font-fira-code-nerd-font`

### Shell Tools

```fish
# Core utilities
brew install eza       # Modern ls replacement
brew install bat       # cat with syntax highlighting
brew install fzf       # Fuzzy finder
brew install ripgrep   # Fast grep alternative
brew install fd        # Fast find alternative
brew install ghq       # Git repository organizer
brew install delta     # Better git diff

# Directory navigation
brew install z         # Jump to frequent directories
brew install zoxide    # Smarter cd

# Git tools
brew install lazygit   # Terminal UI for git
brew install gh        # GitHub CLI
brew install tig       # Text-mode interface for git
```

## Development Tools

### Version Managers

```fish
# Node.js
brew install nvm       # Node version manager
# OR use nvm.fish plugin (included in fish_plugins)

# Ruby
brew install rbenv     # Ruby version manager
brew install ruby-build

# Python
brew install pyenv     # Python version manager

# Java
brew install openjdk@17
brew install openjdk@21
```

### Editors

```fish
brew install neovim    # Modern Vim
brew install --cask visual-studio-code
brew install --cask cursor
brew install --cask zed
```

## Productivity Tools

### File Management

```fish
brew install ranger    # Terminal file manager
brew install lf        # Faster ranger alternative
brew install nnn       # Minimal file manager
```

### System Monitoring

```fish
brew install htop      # Process viewer
brew install btop      # Modern htop
brew install glances   # Cross-platform monitoring
brew install bottom    # Graphical process monitor
```

### Network Tools

```fish
brew install wget      # File downloader
brew install curl      # Transfer tool
brew install httpie    # HTTP client
brew install dog       # DNS lookup
```

## Customization

### Fish Plugins (via Fisher)

Included in `fish_plugins`:
- `jorgebucaran/fisher` - Plugin manager
- `jorgebucaran/nvm.fish` - Node version manager
- `ilancosman/tide@v6` - Prompt theme
- `jethrokuan/z` - Directory jumping
- `decors/fish-ghq` - ghq integration
- `patrickf1/fzf.fish` - fzf integration

Additional recommended:
```fish
fisher install edc/bass              # Bash script support
fisher install meaningful-ooo/sponge # Clean command history
fisher install gazorby/fish-abbreviation-tips
```

### Tide Prompt Styles

```fish
# Reconfigure Tide anytime
tide configure

# Styles available:
# - Classic: Two-line with decorations
# - Rainbow: Colorful two-line
# - Lean: Minimal one-line (Fast)
```

## macOS-Specific

### Package Managers

```fish
# Homebrew (required)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Additional tools
brew install mas       # Mac App Store CLI
brew install cask      # GUI app installer
```

### macOS Utilities

```fish
brew install --cask rectangle      # Window manager
brew install --cask raycast        # Spotlight replacement
brew install --cask stats          # System monitor
brew install --cask cleanmymac     # System cleaner
```

## Docker & Containers

```fish
brew install --cask orbstack       # Fast Docker alternative (Recommended)
# OR
brew install --cask docker         # Docker Desktop
```

## Performance Tips

1. **Startup Time**: Keep under 200ms
   - Use lazy loading for heavy tools
   - Minimize plugin count
   - Avoid heavy computations in config

2. **PATH Management**:
   - Use `fish_add_path --move` to prevent duplicates
   - Keep PATH entries under 50
   - Remove unused paths

3. **Plugin Management**:
   - Only install plugins you actively use
   - Check plugin startup impact: `time fish -c exit`

## Troubleshooting

### Slow Startup

```fish
# Profile startup
fish --profile-startup=/tmp/fish-profile.log
cat /tmp/fish-profile.log

# Check plugin load times
time fish -c "fisher list"
```

### PATH Issues

```fish
# Reset PATH
set -e fish_user_paths
exec fish

# Debug PATH
echo $PATH | tr ' ' '\n' | nl
```

### Plugin Errors

```fish
# Reinstall all plugins
fisher update

# Remove all plugins
fisher list | fisher remove

# Reinstall from fish_plugins
fisher update
```

## References

- [Fish Shell Documentation](https://fishshell.com/docs/current/)
- [Fisher Plugin Manager](https://github.com/jorgebucaran/fisher)
- [Tide Prompt](https://github.com/IlanCosman/tide)
- [Awesome Fish](https://github.com/jorgebucaran/awsm.fish)
