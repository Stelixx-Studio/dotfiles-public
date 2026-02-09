#!/usr/bin/env python3
"""
Policy Injector - SKT CLI
=========================
Scans documentation for **Rule** definitions and injects them into a dedicated section
of the agent instructions. This bridges the gap between "Docs" (Past) and "Instructions" (Present).
"""

import os
import re
from pathlib import Path

def extract_rules_from_file(file_path: Path) -> list:
    rules = []
    try:
        content = file_path.read_text(encoding='utf-8')
        # Regex to find **Rule**: ... blocks
        # We assume the standard format defined in documentation-management.md
        matches = re.finditer(r'(?:\n|^)\s*\*\*Rule\*\*:\s*(.+?)(?:\n|$)', content)
        
        for match in matches:
            rule_text = match.group(1).strip()
            # Try to find a header before this rule for context
            pre_text = content[:match.start()]
            header_match = re.search(r'(?:^|\n)#{2,5}\s+(.+?)\s*$', pre_text)
            header = header_match.group(1).strip() if header_match else "General Rule"
            
            rules.append(f"- **{header}**: {rule_text} ([Source]({file_path.name}))")
            
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}")
        
    return rules

def inject_policies(root: Path):
    docs_dir = root / "docs"
    if not docs_dir.exists():
        print("No docs directory found.")
        return

    all_rules = []
    
    # Priority folders for extraction
    dirs_to_scan = [
        docs_dir / "architecture",
        docs_dir / "features"
    ]
    
    print("\n> [!POLICY] Scanning documentation for rules...")
    
    for d in dirs_to_scan:
        if d.exists():
            for f in d.glob("*.md"):
                file_rules = extract_rules_from_file(f)
                if file_rules:
                    all_rules.extend(file_rules)
                    print(f"  - Extracted {len(file_rules)} rules from {f.name}")

    if not all_rules:
        print("  - No structured rules found.")
        return

    # In a real implementation, this would append to .agent/instructions.md
    # For now, we generate a block that can be copied/used by the builder
    
    print("\n> [!INJECT] Generated Policy Block for Instructions:")
    print("-" * 40)
    print("## 🛡️ Project Policies (Auto-Extracted)")
    print("> These are critical architectural rules extracted from `docs/`.")
    print("")
    for rule in all_rules:
        print(rule)
    print("-" * 40)
    print("")

def main():
    root = Path(".").resolve()
    inject_policies(root)

if __name__ == "__main__":
    main()
