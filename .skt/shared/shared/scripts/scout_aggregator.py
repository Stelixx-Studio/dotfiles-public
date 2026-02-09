#!/usr/bin/env python3
"""
Scout Aggregator - SKT CLI (Source)
==========================
Analyzes, deduplicates, and categorizes results from agent_executor.py.
Generates structured reports for subsequent planning phases.
"""

import sys
import json
import re
from pathlib import Path
from typing import List, Dict, Set

def parse_input() -> List[str]:
    """Extract file paths from STDIN using aggressive regex"""
    content = sys.stdin.read()
    
    # Save raw input for deep debugging if needed
    root = Path.cwd()
    meta_dir = root / ".skt" / "meta"
    meta_dir.mkdir(parents=True, exist_ok=True)
    with open(meta_dir / "last-scout-raw.txt", 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n[DEBUG] Aggregator received content length: {len(content)}")
    
    # Aggressive patterns
    # 1. Any string looking like a path at the start of a line or after a bullet
    p1 = re.findall(r'^[ \t]*[\-\*]?[ \t]*([a-zA-Z0-9_\-\./\\]+\.[a-z0-9]+)', content, re.MULTILINE)
    # 2. Any string in backticks
    p2 = re.findall(r'`([a-zA-Z0-9_\-\./\\]+\.[a-z0-9]+)`', content)
    # 3. Any string followed by a newline that looks like a path
    p3 = re.findall(r'(\S+\.[a-z0-9]+)\s*$', content, re.MULTILINE)
    
    all_paths = list(set(p1 + p2 + p3))
    print(f"[DEBUG] Extracted {len(all_paths)} unique paths.")
    return all_paths

def categorize_path(path: str) -> str:
    """Categorize file path into logical groups"""
    p = path.lower()
    if p.startswith('.agent') or 'instruction' in p:
        return 'Standard Rules'
    if p.startswith('features/') and '/scripts/' in p:
        return 'Core Logic'
    if p.startswith('features/') or p.startswith('apps/'):
        return 'Features'
    if any(p.endswith(ext) for ext in ['.json', '.csv', '.yaml', '.yml']):
        return 'Config/Data'
    return 'Assets/Misc'

def generate_report(paths: List[str]):
    """Generate Markdown and JSON reports"""
    categorized: Dict[str, List[str]] = {
        'Standard Rules': [],
        'Core Logic': [],
        'Features': [],
        'Config/Data': [],
        'Assets/Misc': []
    }

    for p in sorted(paths):
        # Basic filter for noise
        if 'node_modules' in p or '.git/' in p or 'dist/' in p:
            continue
        
        cat = categorize_path(p)
        categorized[cat].append(p)

    # 1. Save JSON for persistence
    root = Path.cwd()
    meta_dir = root / ".skt" / "meta"
    meta_dir.mkdir(parents=True, exist_ok=True)
    
    with open(meta_dir / "last-scout.json", 'w', encoding='utf-8') as f:
        json.dump({"paths": paths, "categorized": categorized}, f, indent=2)

    # 2. Generate Markdown Report
    report = []
    report.append("## 🛰️ Scout Discovery Report\n")
    report.append("| Category | File Path | Status |")
    report.append("| :--- | :--- | :--- |")
    
    found_any = False
    for cat, files in categorized.items():
        for f in files[:10]: # Limit report size for prompt cleanliness
            report.append(f"| {cat} | `{f}` | ✅ Found |")
            found_any = True
            
    if not found_any:
        report.append("| - | No relevant files discovered | - |")
        
    report.append("\n> [!TIP]\n> Detailed results saved to `.skt/meta/last-scout.json`.")

    with open(meta_dir / "scout-report.md", 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
        
    print("\n".join(report))

def main():
    paths = parse_input()
    generate_report(paths)

if __name__ == "__main__":
    main()
