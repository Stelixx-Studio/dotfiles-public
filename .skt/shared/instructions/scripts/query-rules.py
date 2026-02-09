#!/usr/bin/env python3
"""
Instructions Rules Query Engine

Queries project instructions and rules.
"""

import argparse
import sys
import io
from pathlib import Path

# Force UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def main():
    parser = argparse.ArgumentParser(description="Instructions Rules Query Engine")
    parser.add_argument("--workflow", help="Workflow context (e.g. cook, plan)")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    args = parser.parse_args()

    # Priority Load Strategy:
    # 1. generated/core.md (Framework rules)
    # 2. custom/project-rules.md (User overrides)
    
    rules_files = []
    
    # Locate .agent root
    cwd = Path.cwd()
    agent_root = None
    for parent in [cwd] + list(cwd.parents)[:3]:
        candidate = parent / '.agent'
        if candidate.exists():
            agent_root = candidate
            break
            
    if agent_root:
        # Define priority list
        potential_files = [
            agent_root / 'instructions/generated/core.md',
            agent_root / 'instructions/custom/project-rules.md'
        ]
        
        for p in potential_files:
            if p.exists():
                rules_files.append(p)
    
    # If no specific rules found, fall back to legacy instructions.md
    if not rules_files and agent_root:
        legacy = agent_root / 'instructions.md'
        if legacy.exists():
            rules_files.append(legacy)

    if rules_files:
        if args.format == "markdown":
            context = f" (Context: {args.workflow})" if args.workflow else ""
            print(f"# 📋 Project Rules & Context{context}\n")
            
            for p in rules_files:
                try:
                    content = p.read_text(encoding='utf-8').strip()
                    print(f"## Rate Source: {p.name}\n")
                    print(content)
                    print("\n---\n")
                except Exception as e:
                    print(f"Error reading {p.name}: {e}", file=sys.stderr)
        else:
            # JSON output
            import json
            data = []
            for p in rules_files:
                try:
                    data.append({
                        "source": p.name,
                        "content": p.read_text(encoding='utf-8')
                    })
                except:
                    pass
            print(json.dumps(data))
    else:
        print(f"Error: No rule files found in .agent/instructions/ (checked generated/core.md, custom/project-rules.md)", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
