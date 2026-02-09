# CLI & Script Overview

This project provides several scripts to manage the dotfiles life-cycle.

## 🔄 sync.fish
- **Path**: `.scripts/sync.fish`
- **Purpose**: Synchronizes configuration changes from your macOS home directory into this repository.
- **Usage**: `fish .scripts/sync.fish`
- **Scope**: Fish, Ghostty, Lazygit, Mise, Tmux, Neovim, Git, and Homebrew.

## 📦 install.fish
- **Path**: `.scripts/install.fish`
- **Purpose**: Bootstrap a new machine by installing essentials and setting up symlinks (Base version).
- **Usage**: `fish .scripts/install.fish`