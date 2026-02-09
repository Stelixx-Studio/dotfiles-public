#!/bin/bash
# Update frontmatter for templates and custom prompts

PROMPTS_DIR=".github/prompts"

update_frontmatter() {
  local file=$1
  local name=$2
  local description=$3
  
  if [ -f "$file" ]; then
    content=$(awk '/^---$/{c++; if(c==2){p=1; next}} p' "$file")
    
    {
      echo "---"
      echo "name: $name"
      echo "description: '$description'"
      echo "agent: 'agent'"
      echo "---"
      echo "$content"
    } > "${file}.tmp"
    
    mv "${file}.tmp" "$file"
    echo "  ✓ Updated: $(basename $file)"
  else
    echo "  ✗ Not found: $file"
  fi
}

echo "Updating frontmatter for templates and custom prompts..."
echo "========================================================"

# Templates
update_frontmatter "$PROMPTS_DIR/templates/auto-check.prompt.md" \
  "auto-check" \
  "Automated quality check template with 27 verification points covering development rules, common pitfalls, and quality commands"

update_frontmatter "$PROMPTS_DIR/templates/check-before-create.prompt.md" \
  "check-before-create" \
  "Pre-creation checklist to verify file organization, naming conventions, and prevent duplicate code"

update_frontmatter "$PROMPTS_DIR/templates/feature-check.prompt.md" \
  "feature-check" \
  "Feature implementation checklist covering architecture, types, testing, i18n, accessibility, and deployment"

update_frontmatter "$PROMPTS_DIR/templates/infrastructure-check.prompt.md" \
  "infrastructure-check" \
  "Infrastructure deployment checklist for Docker, Kubernetes, CI/CD, monitoring, and security"

# Custom
update_frontmatter "$PROMPTS_DIR/custom/ck.prompt.md" \
  "ck" \
  "ClaudeKit command manager for syncing, creating, and managing workflow commands"

update_frontmatter "$PROMPTS_DIR/custom/instructions.prompt.md" \
  "instructions" \
  "Project instructions manager to show rules and verify compliance with development standards"

echo ""
echo "========================================================"
echo "✓ Frontmatter update complete!"
