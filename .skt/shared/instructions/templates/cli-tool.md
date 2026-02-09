## CLI Tool Development

### Build Integrity
**Rule**: NEVER assume CLI code works without rebuilding.
- **Trigger**: Any modification to `cli/src` (or source folder)
- **Action**: Run build script (e.g., `npm run build`).
- **Reason**: Binaries run from `dist/` or `lib/`, not directly from `src/` (unless using ts-node/tsx, but production builds matter).

### Local Verification
**Rule**: Verify the binary, not just the code.
- **Action**: Run `./bin/cli.js --version` (or equivalent) to verify changes.
- **Check**: Ensure `which <cmd>` points to your local version if testing globally.

### Release Process
**Rule**: Use Changesets for versioning.
- **Trigger**: Feature completion.
- **Action**: `npx changeset add`
- **Content**: Clearly describe user-facing changes.
- **Reason**: Automates version bumping and changelog generation.
