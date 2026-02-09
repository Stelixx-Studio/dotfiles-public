# Documentation Management Standards

This document defines documentation standards, update triggers, and quality checks for the SKT CLI project.

---

## Documentation Standards

### Code Comments

- **JSDoc for all public functions**: Use JSDoc comments for all exported functions and classes
- **Inline comments for complex logic**: Add comments explaining non-obvious code blocks
- **No commented-out code**: Remove commented code before committing

**Example**:
```typescript
/**
 * Syncs workspace resources from features/ to .agent/ and .claudekit/
 * @param targets - Optional list of feature names to sync
 * @param options - Sync command options (dryRun, force, verbose)
 * @returns Promise<void>
 */
export async function syncCommand(
  targets?: string[],
  options: SyncCommandOptions = {}
): Promise<void> {
  // Implementation...
}
```

### API Documentation

- **OpenAPI/Swagger specs for REST APIs**: Document all REST endpoints
- **GraphQL schema documentation**: Annotate GraphQL types and queries
- **Examples for all endpoints**: Provide request/response examples

### Architecture Documentation

- **System architecture diagrams (C4 model)**: Use C4 model for system context and component diagrams
- **Database ERD diagrams**: Document database schema relationships
- **Deployment architecture**: Show infrastructure and deployment topology

### User Guides

- **Getting started guide**: Step-by-step onboarding for new users
- **Feature tutorials**: How-to guides for each major feature
- **Troubleshooting guide**: Common issues and solutions

---

## Update Triggers

### Automatic Triggers

When these changes occur, documentation MUST be updated:

| Change Type | Affected Docs | Required Action |
|-------------|---------------|-----------------|
| **New features** | `docs/features/`, `README.md` | Document feature usage and API |
| **API changes** | `docs/api/`, API reference | Update endpoint documentation |
| **Breaking changes** | `CHANGELOG.md`, migration guide | Document migration path |
| **Config updates** | Configuration docs | Update config examples |
| **CLI commands** | Command reference | Update command help and examples |

### Manual Triggers

These may require documentation updates (review on case-by-case basis):

- Architecture refactoring
- Security updates
- Performance improvements
- Dependency updates

---

## Cross-referencing with Plans

When updating documentation, always check for related active plans in `plans/`.

1. **Active Implementation**: If a feature is currently being implemented, refer to the corresponding `plans/features/` file for technical details.
2. **Post-Implementation**: Ensure all "Technical Decisions" recorded in archived plans are reflected in `docs/architecture/`.
3. **Traceability**: Link to plan files in the documentation if they contain vital reasoning details.

---

---

## Policy Injection

To allow the AI system to automatically extract rules from documentation into `instructions.md`, use the following strict format for critical architectural constraints:

```markdown
### [Rule Name]

**Rule**: [The specific constraint or requirement]
**Context**: [When this rule applies]
```

**Example**:
```markdown
### Server Components First
**Rule**: Default to Server Components, use Client Components only when needed.
**Context**: Next.js App Router development.
```

---

## File Locations

```
docs/
├── architecture/       # System design and diagrams
│   ├── project-overview.md
│   └── diagrams/
├── features/          # Feature-specific documentation
│   ├── claudekit/
│   ├── ui-ux-pro-max/
│   └── instructions/
├── api/               # API reference
│   └── rest-api.md
├── guides/            # User guides and tutorials
│   ├── getting-started.md
│   ├── workflows-guide.md
│   └── troubleshooting.md
└── README.md          # Documentation index

README.md              # Project overview
CHANGELOG.md           # Version history
CONTRIBUTING.md        # Contributing guide
```

---

## Documentation Quality Checklist

### Before Committing

- [ ] All new functions have JSDoc comments
- [ ] Breaking changes documented in CHANGELOG.md
- [ ] API changes reflected in docs/api/
- [ ] Examples updated with new features
- [ ] Links validated (no 404s)
- [ ] Code snippets tested and working
- [ ] Spelling and grammar checked

### Before Release

- [ ] README.md up to date
- [ ] CHANGELOG.md complete
- [ ] Migration guide (if breaking changes)
- [ ] All docs built without errors
- [ ] Search functionality working

---

## Maintenance Procedures

### When to Update Docs

1. **With every feature PR**: Update relevant docs in the same PR
2. **Before each release**: Review and update all public-facing docs
3. **After architecture changes**: Update architecture diagrams and overview
4. **When user feedback indicates confusion**: Improve clarity in guides

### Who Reviews Doc Changes

- **Code author**: First pass review for accuracy
- **Tech lead**: Architecture and technical accuracy
- **Product/UX**: User-facing clarity and completeness

### Documentation Testing

- **Link checking**: Use `markdown-link-check` for broken links
- **Code examples**: Run examples through linter and tests
- **Build verification**: Ensure docs site builds without errors

---

## Best Practices

1. **Update docs in the same commit as code**: Keep code and docs in sync
2. **Use relative links**: Ensure links work in local and deployed environments
3. **Include code examples**: Show real usage, not just API signatures
4. **Keep it concise**: Prefer clear, short explanations over verbose text
5. **Use diagrams**: Visual representations aid understanding
6. **Version breaking changes**: Clearly mark deprecated features and migration paths

---

## Tools

- **Markdown linter**: `markdownlint` for consistent formatting
- **Link checker**: `markdown-link-check` for broken links
- **Diagram tools**: Mermaid.js for inline diagrams, Excalidraw for architecture diagrams
- **Spell checker**: VS Code spell checker extension
