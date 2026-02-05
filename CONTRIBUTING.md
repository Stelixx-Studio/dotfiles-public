# Contributing to Yoong's Dotfiles

Thank you for your interest in contributing!

## How to Contribute

### Reporting Issues

1. Check existing issues first
2. Use the [issue template](ISSUE_TEMPLATE.md)
3. Provide clear reproduction steps
4. Include your environment details

### Suggesting Enhancements

1. Open an issue with the `enhancement` label
2. Describe the enhancement clearly
3. Explain why it would be useful

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly on your system
5. Commit with conventional commits (`feat:`, `fix:`, `docs:`, etc.)
6. Push to your fork
7. Open a Pull Request

### Commit Convention

We use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `perf:` - Performance improvements
- `test:` - Test additions or changes
- `chore:` - Build process or auxiliary tool changes

### Testing

Before submitting:

```fish
# Test startup time
time fish -c exit

# Check for PATH duplicates
echo $PATH | tr ' ' '\n' | sort | uniq -d

# Verify commands work
command -v git node pnpm ruby java
```

## Code Style

- Use 4 spaces for Fish scripts (not tabs)
- Add comments for complex logic
- Keep configs modular and organized
- Test on clean Fish installation

## Questions?

Open an issue with the `question` label.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
