#!/usr/bin/env python3
"""
Context Loader - SKT CLI
========================
Provides "Context Awareness" to Agents by scanning the project state.
Output is formatted as a Markdown block for direct injection into Agent prompts.

Usage:
    python3 context_loader.py [path]
"""

import os
import json
import sys
import argparse
from pathlib import Path
from typing import Dict, Any, List
import io

# Force UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def get_project_root(path: str) -> Path:
    return Path(path).resolve()

def analyze_package_json(root: Path) -> Dict[str, Any]:
    pkg_file = root / "package.json"
    if not pkg_file.exists():
        # Try to find package.json in sub-apps for Monorepo context
        apps_dir = root / "apps"
        if apps_dir.exists():
            for app in apps_dir.iterdir():
                if (app / "package.json").exists():
                    # Analyze the first app found for stack context
                    pkg_file = app / "package.json"
                    break
        
    if not pkg_file.exists():
        return {"stack": ["Unknown (No package.json)"]}
    
    try:
        with open(pkg_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        deps = data.get("dependencies", {})
        dev_deps = data.get("devDependencies", {})
        all_deps = {**deps, **dev_deps}
        
        stack = []
        # Frameworks
        if "next" in all_deps: stack.append("Next.js")
        elif "react" in all_deps: stack.append("React")
        elif "vue" in all_deps: stack.append("Vue")
        elif "svelte" in all_deps: stack.append("Svelte")
        elif "express" in all_deps: stack.append("Express")
        elif "@nestjs/core" in all_deps: stack.append("NestJS")
        
        # Languages/Tools
        if "typescript" in all_deps: stack.append("TypeScript")
        if "tailwindcss" in all_deps: stack.append("Tailwind CSS")
        if "prisma" in all_deps: stack.append("Prisma")
        if "drizzle-orm" in all_deps: stack.append("Drizzle")
        
        # Fallback for generic Node/TS apps
        if not stack:
            if "typescript" in all_deps: stack.append("Node.js (TypeScript)")
            elif "commander" in all_deps: stack.append("Node.js (CLI)")
            else: stack.append("Node.js")
            
        return {
            "name": data.get("name", "unnamed"),
            "stack": stack
        }
    except Exception:
        return {"stack": ["Error parsing package.json"]}

def get_git_status() -> str:
    # Simple check if git is initialized and status
    if not os.path.exists(".git"):
        return "Not a git repository"
    
    try:
        import subprocess
        result = subprocess.run(["git", "status", "--short"], capture_output=True, text=True)
        if not result.stdout.strip():
            return "Clean working directory"
        return "Uncommitted changes present"
    except Exception:
        return "Git status unavailable"

def get_active_rules(root: Path) -> List[str]:
    # Check .agent/instructions.md or similar for rule headers
    rules_file = root / ".agent/instructions.md"
    if not rules_file.exists():
        return []
    
    try:
        import re
        content = rules_file.read_text(encoding='utf-8')
        # Extract H2 headers as categories
        categories = re.findall(r'^## (.*)$', content, re.MULTILINE)
        return [c.strip() for c in categories if c.strip()]
    except Exception:
        return []

def generate_context_block(root: Path):
    info = analyze_package_json(root)
    git_stat = get_git_status()
    rules = get_active_rules(root)
    
    print("\n> [!CONTEXT] Project Context Loaded")
    print("> **Stack**: " + ", ".join(info.get('stack', [])))
    print(f"> **Git**: {git_stat}")
    print(f"> **Root**: {root}")
    if rules:
        print(f"> **Active Rules**: {', '.join(rules)}")
    print("\n")

def main():
    parser = argparse.ArgumentParser(description="Context Loader")
    parser.add_argument("path", nargs="?", default=".", help="Project path")
    args = parser.parse_args()
    
    root = get_project_root(args.path)
    generate_context_block(root)
    
    # Inject Project Rules if available
    # Search for .agent/instructions/custom/project-rules.md
    rules_path = root / ".agent/instructions/custom/project-rules.md"
    if not rules_path.exists():
        # Try to find it by walking up if root is relative
        cwd = Path.cwd()
        for parent in [cwd] + list(cwd.parents)[:3]:
            candidate = parent / ".agent/instructions/custom/project-rules.md"
            if candidate.exists():
                rules_path = candidate
                break

    if rules_path.exists():
        try:
            content = rules_path.read_text(encoding='utf-8').strip()
            print(f"\n> [!IMPORTANT] Project Rules (from {rules_path.name})")
            print("> The following rules MUST be followed:\n")
            print(content)
            print("\n")
        except Exception as e:
            # Silently fail or warn, but don't crash context loading
            pass

    # Inject Conductor Beacon (ACTIVE_PLAN.md) if available
    beacon_path = root / "ACTIVE_PLAN.md"
    if not beacon_path.exists():
        cwd = Path.cwd()
        for parent in [cwd] + list(cwd.parents)[:3]:
            candidate = parent / "ACTIVE_PLAN.md"
            if candidate.exists():
                beacon_path = candidate
                break

    if beacon_path.exists():
        try:
            content = beacon_path.read_text(encoding='utf-8').strip()
            print(f"\n> [!IMPORTANT] 🔥 Active Development (from Conductor)")
            print("> Current task context and multi-agent state:\n")
            print(content)
            print("\n")
        except Exception:
            pass

    # Inject Scout Results & Rule-Gap Analysis (New for Scout Evolution)
    scout_json = root / ".skt" / "meta" / "last-scout.json"
    if scout_json.exists():
        try:
            with open(scout_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            paths = data.get("paths", [])
            print(f"\n> [!NOTE] 🛸 Scout Intelligence (Found {len(paths)} files)")
            
            # Rule-Gap Analysis: Check if any new feature/schema files lack an associated .md rule
            feature_files = [p for p in paths if 'features/' in p and (p.endswith('.ts') or p.endswith('.tsx'))]
            rules_content = ""
            rules_path = root / ".agent/instructions.md"
            if rules_path.exists():
                rules_content = rules_path.read_text(encoding='utf-8').lower()
            
            missing_rules = []
            for f in feature_files:
                feature_name = f.split('/')[1]
                if f"## {feature_name}" not in rules_content and feature_name not in rules_content:
                    missing_rules.append(feature_name)
            
            if missing_rules:
                unique_missing = sorted(list(set(missing_rules)))
                print("> [!WARNING] Rule Gap Detected!")
                print("> The following features have code but NO governing rules in `.agent/instructions.md`:")
                for m in unique_missing:
                    print(f"> - `{m}`")
                print("> **Action**: Run `/skt:skill-create` or update `.agent/instructions.md`.")
                
        except Exception:
            pass

if __name__ == "__main__":
    main()
