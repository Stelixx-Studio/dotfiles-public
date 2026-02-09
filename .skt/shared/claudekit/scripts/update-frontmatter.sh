#!/bin/bash
# Update Copilot frontmatter - FIXED VERSION
# Properly preserves content while updating frontmatter

PROMPTS_DIR=".github/prompts/claudekit"

echo "Updating Copilot frontmatter..."
echo "================================"

update_frontmatter() {
  local workflow=$1
  local description=$2
  local file="$PROMPTS_DIR/${workflow}.prompt.md"
  
  if [ -f "$file" ]; then
    # Extract content after second ---
    content=$(awk '/^---$/{c++; if(c==2){p=1; next}} p' "$file")
    
    # Write new frontmatter + content
    {
      echo "---"
      echo "name: $workflow"
      echo "description: '$description'"
      echo "agent: 'agent'"
      echo "---"
      echo "$content"
    } > "${file}.tmp"
    
    mv "${file}.tmp" "$file"
    echo "  ✓ Updated: $workflow.prompt.md"
  else
    echo "  ✗ Not found: $workflow.prompt.md"
  fi
}

# Update all workflows
update_frontmatter "cook" "Implement feature with parallel research, context loading, and automated testing"
update_frontmatter "code" "Execute existing implementation plan with quality checks"
update_frontmatter "review" "Code review against project standards and best practices"
update_frontmatter "test" "Run test suite and report results without auto-fix"
update_frontmatter "brainstorm" "Explore multiple solution approaches with trade-off analysis"

update_frontmatter "design" "Design UI/UX with fast mockup, high-quality, or 3D component options"
update_frontmatter "design-fast" "Quick design mockups with image generation"
update_frontmatter "design-good" "UI/UX design with research and accessibility focus"
update_frontmatter "design-3d" "3D component design with Three.js and React Three Fiber"

update_frontmatter "fix" "General bug fix with analysis and verification"
update_frontmatter "fix-fast" "Quick bug fix with minimal research"
update_frontmatter "fix-hard" "Complex bug fix with deep analysis and debugging"
update_frontmatter "fix-ci" "Fix CI/CD pipeline issues"
update_frontmatter "fix-logs" "Fix bugs from error logs analysis"
update_frontmatter "fix-test" "Fix failing tests until all pass"

update_frontmatter "git-commit" "Create conventional commit message"
update_frontmatter "git-commit-push" "Commit and push changes with conventional message"
update_frontmatter "git-pr" "Create pull request with description"
update_frontmatter "git-cherry-pick" "Cherry-pick commits with conflict resolution"

update_frontmatter "docs-init" "Initialize documentation structure"
update_frontmatter "docs-summarize" "Summarize documentation"
update_frontmatter "docs-update" "Update documentation"

update_frontmatter "content-good" "Marketing copywriting with research"
update_frontmatter "content-cro" "Conversion-focused content optimization"

update_frontmatter "bootstrap" "Bootstrap new project with parallel research"
update_frontmatter "bootstrap-auto" "Autonomous bootstrap without user interaction"

update_frontmatter "skill" "Create or optimize workflow/skill documentation"
update_frontmatter "skill-create" "Create new skill workflow"
update_frontmatter "skill-optimize" "Optimize existing skill workflow"

update_frontmatter "ask" "Ask questions with context-aware answers"

echo ""
echo "================================"
echo "✓ Frontmatter update complete!"
