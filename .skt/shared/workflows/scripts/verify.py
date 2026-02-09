#!/usr/bin/env python3
"""
Smart Verification Engine
=========================
Active quality gate that automatically detects and runs project checks.
Replaces passive checklists with actual execution.

Supported Checks:
- TypeScript (tsc --noEmit)
- Lint (npm/pnpm lint)
- Tests (npm/pnpm test)
- Python (flake8/black/pytest) - Future proofing
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from typing import List, Dict, Any

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(msg):
    print(f"\n{Colors.HEADER}{Colors.BOLD}=== {msg} ==={Colors.RESET}")

def print_step(msg):
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.RESET}")

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.RESET}")

def print_fail(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.RESET}")

def print_warn(msg):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.RESET}")

def run_cmd(cmd: List[str], cwd: Path, ignore_fail=False) -> bool:
    cmd_str = " ".join(cmd)
    print_step(f"Running: {cmd_str}")
    try:
        result = subprocess.run(
            cmd, 
            cwd=cwd,
            check=False,
            capture_output=False  # Let output stream to console
        )
        if result.returncode == 0:
            return True
        else:
            if not ignore_fail:
                print_fail(f"Command failed: {cmd_str}")
            return False
    except FileNotFoundError:
        print_fail(f"Command not found: {cmd[0]}")
        return False

def detect_manager(root: Path) -> str:
    if (root / "pnpm-lock.yaml").exists(): return "pnpm"
    if (root / "yarn.lock").exists(): return "yarn"
    return "npm"

def check_node_project(root: Path) -> bool:
    pkg_json = root / "package.json"
    if not pkg_json.exists():
        return True # Not a node project, skip

    print_header("Node.js/TypeScript Verification")
    manager = detect_manager(root)
    
    try:
        with open(pkg_json, 'r') as f:
            data = json.load(f)
            scripts = data.get("scripts", {})
    except Exception as e:
        print_fail(f"Failed to read package.json: {e}")
        return False

    success = True

    # 1. TypeScript Check
    tsconfig = root / "tsconfig.json"
    if tsconfig.exists():
        # Prefer 'typecheck' script if exists, else direct tsc
        if "typecheck" in scripts:
            if not run_cmd([manager, "run", "typecheck"], root): success = False
        else:
            # Check if tsc is available via pnpm/npx
            tsc_cmd = [manager, "tsc", "--noEmit"] if manager == "pnpm" else ["npx", "tsc", "--noEmit"]
            if not run_cmd(tsc_cmd, root): success = False
    
    # 2. Lint Check
    if "lint" in scripts:
        if not run_cmd([manager, "run", "lint"], root): success = False
    elif "lint:fix" in scripts:
         if not run_cmd([manager, "run", "lint:fix"], root): success = False

    # 3. Test Check (Critical Path)
    # Only run if expected to be robust. AI often skips writing tests, so we warn if missing but fail if failing.
    if "test" in scripts:
        # Avoid running watch mode
        test_cmd = [manager, "run", "test"]
        # Add CI=true to prevent watch mode in some frameworks (CRA, Vitest)
        env = os.environ.copy()
        env["CI"] = "true"
        
        print_step(f"Running: {manager} run test")
        try:
            res = subprocess.run(test_cmd, cwd=root, env=env, check=False)
            if res.returncode != 0:
                success = False
                print_fail("Tests failed")
        except:
             success = False
    else:
        print_warn("No test script found in package.json")

    return success

def main():
    root = Path.cwd()
    overall_success = True
    
    # Node/TS Checks
    if not check_node_project(root):
        overall_success = False

    # Python Checks (Placeholder for future)
    if (root / "requirements.txt").exists() or (root / "pyproject.toml").exists():
        # print_header("Python Verification")
        pass

    if overall_success:
        print_header("Verification Summary")
        print_success("All checks passed! The codebase is healthy.")
        sys.exit(0)
    else:
        print_header("Verification Summary")
        print_fail("Verification failed. Please fix the errors above.")
        
        # 🆘 AI Recovery Protocol 🆘
        print(f"\n{Colors.YELLOW}🆘 RECOVERY_PROTOCOL_INITIATED{Colors.RESET}")
        print(f"{Colors.YELLOW}Trigger: Verification Failure Detected{Colors.RESET}")
        print(f"{Colors.YELLOW}Mandate: You are strictly forbidden from ending the task in this state.{Colors.RESET}")
        print(f"{Colors.YELLOW}Instructions for Agent:{Colors.RESET}")
        print("1. Analyze the logs above to identify the failing files and error messages.")
        print("2. Formulate a repair plan for the specific violations.")
        print("3. Implement the fixes immediately.")
        print("4. Re-run this verification command until PASS.")
        print(f"{Colors.YELLOW}🆘 RECOVERY_PROTOCOL_END{Colors.RESET}\n")
        
        sys.exit(1)

if __name__ == "__main__":
    main()
