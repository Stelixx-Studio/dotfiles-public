#!/bin/bash
# Load project context for ClaudeKit workflows

echo "Loading project context..."

# Load instructions
cat .agent/instructions.md

# Show feature structure
echo -e "\n## Feature Structure"
find apps/web/features -type d -maxdepth 2 | head -15
