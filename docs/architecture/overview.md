# Architecture Overview

## 📁 Directory Structure

The project follows a standard Unix-like directory structure for configuration management:

- `.config/`: Contains tool-specific configurations (e.g., `fish/`, `ghostty/`, `lazygit/`).
- `.scripts/`: Automation scripts for installation and synchronization.
- `.skt/`: Private CLI state and AI shared resources.
- `docs/`: Technical documentation and guides.
- `Brewfile`: Source of truth for Homebrew packages.

## 🔄 Synchronization Workflow

The architecture uses a "Copy-to-Repo" synchronization pattern:

1. **System Source**: Configurations reside in their standard macOS locations (e.g., `~/.config/fish`).
2. **Local Sync**: The `.scripts/sync.fish` script copies allowed files from the system to the repository.
3. **Commit & Push**: User reviews the changes and pushes them to GitHub.

## 🛡️ Security Model

Sensitive data (tokens, private paths) is handled via:
- **Exclusion**: `local.fish` and `*.local.fish` are ignored by Git.
- **Local Overrides**: Tools are configured to load these local files if they exist, keeping secrets out of public storage.