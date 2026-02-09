#!/bin/bash
# Active Quality Gate
# Redirects to the smart verification engine to enforce TSC/Lint/Test

# Resolve the absolute path to verify.py relative to this script
# structure: features/workflows/claudekit/scripts/auto-check.sh -> ../../shared/scripts/verify.py
SCRIPT_DIR="$(dirname "$0")"
VERIFY_SCRIPT="$SCRIPT_DIR/../../shared/scripts/verify.py"

if [ -f "$VERIFY_SCRIPT" ]; then
  python3 "$VERIFY_SCRIPT"
else
  # Fallback if path resolution fails (e.g. symlinks)
  echo "⚠️  Count not find verify.py at relative path. Trying features/workflows override..."
  python3 features/shared/scripts/verify.py
fi
