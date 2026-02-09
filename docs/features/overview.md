# Features Overview

The `dotfiles-public` repository provides a comprehensive and optimized development environment for macOS.

## 🚀 Core Features

- **⚡ High Performance Fish Shell**: Modular configuration optimized for < 150ms startup time.
- **📦 Comprehensive Tool Coverage**: Synchronized configurations for:
  - **Ghostty**: Modern terminal emulator.
  - **Lazygit**: Terminal UI for git.
  - **Mise**: Polyglot tool manager (Node, Python, Ruby, etc.).
  - **Tmux**: Terminal multiplexer with custom status lines.
  - **Neovim**: Essential Lua-based IDE-like experience.
- **🍺 Homebrew Management**: Automatic `Brewfile` generation to track and restore all system packages.
- **🛡️ Secure-by-Design**: Built-in exclusion of local secrets via `.gitignore` and `*.local.fish` patterns.
- **🔄 One-Command Sync**: Easy-to-use `.scripts/sync.fish` for keeping the repo updated with system changes.