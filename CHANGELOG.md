# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.2.0] - 2026-02-24

### Added
- **Granular Symlinking**: Improved Fish configuration installation to use granular symlinks for individual config files/folders instead of symlinking the entire `~/.config/fish` directory.
- **Isolation**: Machine-specific state files (like `fish_variables`) now remain local and are no longer tracked in the repository.

### Changed
- Updated `install.fish` with smarter symlink logic.
- Updated documentation (`README.md`, `QUICKSTART.md`) to reflect the new installation pattern.
- Updated `Brewfile` and environment configurations.

### Removed
- Cleaned up redundant `github.com` and `fish_variables` files from the repository.

## [1.1.0] - 2026-02-09

### Added
- Expanded configuration coverage:
  - Ghostty terminal config
  - Lazygit config
  - Mise runtime manager config
  - Tmux multiplexer config (modular)
  - Neovim essential Lua config
  - Homebrew `Brewfile` (auto-dumped)
- Improved `sync.fish` script with support for new tools
- Security: Added ignore patterns for `local.fish` and private secrets

## [1.0.0] - 2026-02-06

### Added
- Initial dotfiles setup with modernized Fish shell configuration
- Modular config structure (00-path.fish, 01-env.fish, 02-aliases.fish, 03-tools.fish)
- Lazy loading for rbenv and RVM
- Dynamic Java detection via Homebrew
- Automatic PATH deduplication system
- Fisher plugins integration (tide, z, fzf, ghq)
- Installation script for new machines
- Sync script for updating dotfiles from system
- Comprehensive README with documentation
- MIT License

### Performance
- Startup time: 103ms (improved from 320ms - 68% faster)
- PATH entries: 40 (reduced from 51)
- Config size: 31 lines main file (reduced from 99 lines)
- Zero PATH duplicates (improved from 11 duplicates)

### Features
- Fish shell 4.4.0 with Tide v6 prompt
- Smart environment detection (Java, Node, Ruby, Go)
- Project-local bin support
- macOS optimizations
- Git configuration included

[1.0.0]: https://github.com/Stelixx-Studio/dotfiles-public/releases/tag/v1.0.0
