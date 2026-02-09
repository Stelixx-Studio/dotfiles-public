#!/bin/bash
# Batch convert ClaudeKit workflows
# Usage: ./convert-workflows.sh

set -e

WORKFLOWS_DIR=".agent/workflows/claudekit"
PROMPTS_DIR=".github/prompts/claudekit"

echo "Converting ClaudeKit workflows..."
echo "================================="

# List of all workflows
WORKFLOWS=(
  "cook" "code" "review" "test" "brainstorm"
  "design" "design-fast" "design-good" "design-3d"
  "fix" "fix-fast" "fix-hard" "fix-ci" "fix-logs" "fix-test"
  "git-commit" "git-commit-push" "git-pr" "git-cherry-pick"
  "docs-init" "docs-summarize" "docs-update"
  "content-good" "content-cro"
  "bootstrap" "bootstrap-auto"
  "skill" "skill-create" "skill-optimize"
  "ask"
)

# Update script paths in Antigravity workflows
echo "Step 1: Updating script paths in Antigravity workflows..."
for workflow in "${WORKFLOWS[@]}"; do
  file="$WORKFLOWS_DIR/${workflow}.md"
  if [ -f "$file" ]; then
    # Update parallel-research.sh path
    sed -i '' 's|.agent/workflows/scripts/parallel-research.sh|.shared/claudekit/scripts/parallel-research.sh|g' "$file"
    
    # Update auto-check path
    sed -i '' 's|cat .agent/workflows/auto-check-template.md|.shared/claudekit/scripts/auto-check.sh|g' "$file"
    
    echo "  ✓ Updated: $workflow.md"
  else
    echo "  ✗ Not found: $workflow.md"
  fi
done

# Copy to Copilot prompts
echo ""
echo "Step 2: Copying to Copilot prompts..."
for workflow in "${WORKFLOWS[@]}"; do
  src="$WORKFLOWS_DIR/${workflow}.md"
  dest="$PROMPTS_DIR/${workflow}.prompt.md"
  
  if [ -f "$src" ]; then
    cp "$src" "$dest"
    echo "  ✓ Copied: $workflow.prompt.md"
  fi
done

echo ""
echo "================================="
echo "✓ Conversion complete!"
echo "  - Updated: ${#WORKFLOWS[@]} Antigravity workflows"
echo "  - Created: ${#WORKFLOWS[@]} Copilot prompts"
echo ""
echo "Next steps:"
echo "1. Manually update Copilot frontmatter (YAML)"
echo "2. Test workflows in both platforms"
