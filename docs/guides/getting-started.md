# Getting Started Guide

Follow these steps to set up your macOS development environment using these dotfiles.

## 🛡️ Prerequisites
- macOS system
- [Homebrew](https://brew.sh/) installed
- [Fish Shell](https://fishshell.com/) (`brew install fish`)

## 🚀 Installation Steps

### 1. Clone the repository
```fish
git clone git@github.com-stelixx:Stelixx-Studio/dotfiles-public.git ~/dotfiles-public
```

### 2. Basic Setup
Run the installation script to set up base configurations:
```fish
cd ~/dotfiles-public
fish .scripts/install.fish
```

### 3. Restore Packages
Use Homebrew to install all tools listed in the `Brewfile`:
```fish
brew bundle
```

## 🔄 Keeping Updated
Whenever you make changes to your local configs, run the sync script to update the repository:
```fish
fish .scripts/sync.fish
git status
git add -A
git commit -m "feat: update my configs"
git push
```