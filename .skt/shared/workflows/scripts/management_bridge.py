#!/usr/bin/env python3
"""
Management Bridge - SKT CLI
===========================
Helper script to analyze synergies between documentation (docs/) and implementation plans (plans/).
Used by skt:docs-* and skt:plans-* workflows.
"""

import os
import argparse
from pathlib import Path
from typing import List, Dict

def get_active_plans(plans_dir: Path) -> List[Path]:
    active_plans = []
    if not plans_dir.exists():
        return []
    
    for root, dirs, files in os.walk(plans_dir):
        if "archive" in root:
            continue
        for file in files:
            if file.endswith(".md") and file != "README.md":
                active_plans.append(Path(root) / file)
    return active_plans

def get_docs(docs_dir: Path) -> List[Path]:
    docs = []
    if not docs_dir.exists():
        return []
        
    for root, dirs, files in os.walk(docs_dir):
        if "archive" in root:
            continue
        for file in files:
            if file.endswith(".md") and file != "README.md":
                docs.append(Path(root) / file)
    return docs

def analyze_coverage(root: Path):
    plans_dir = root / "plans"
    docs_dir = root / "docs"
    
    active_plans = get_active_plans(plans_dir)
    docs = get_docs(docs_dir)
    
    print("\n> [!MANAGEMENT] Docs/Plans Synergy Report")
    print(f"> **Active Plans**: {len(active_plans)}")
    print(f"> **Active Docs**: {len(docs)}")
    
    # Simple cross-referencing logic based on filenames
    plan_stems = [p.stem.split('-', 1)[-1] if '-' in p.stem else p.stem for p in active_plans]
    doc_stems = [d.stem for d in docs]
    
    covered = 0
    for ps in plan_stems:
        if any(ps in ds for ds in doc_stems):
            covered += 1
            
    coverage_score = (covered / len(active_plans) * 100) if active_plans else 100
    print(f"> **Documentation Coverage**: {coverage_score:.1f}%")
    
    if coverage_score < 100:
        print("> [!TIP] Some active plans lack corresponding documentation. Consider running `skt:docs-update` after implementation.")

def main():
    parser = argparse.ArgumentParser(description="Management Bridge")
    parser.add_argument("path", nargs="?", default=".", help="Project path")
    args = parser.parse_args()
    
    root = Path(args.path).resolve()
    analyze_coverage(root)

if __name__ == "__main__":
    main()
