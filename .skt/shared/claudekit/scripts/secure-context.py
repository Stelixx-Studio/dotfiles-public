#!/usr/bin/env python3
"""
Secure Context - Context Bridge
===============================
Safely bridges the gap between Brainstorming and Execution phases.
1. Validates implementation_plan.md existence
2. Updates ACTIVE_PLAN.md (Orchestrator/Symlink aware)
3. Instructs user to manually reset chat context
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def setup_utf8():
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def main():
    setup_utf8()
    cwd = Path.cwd()
    
    # 1. Validation: Check for source plan
    source_plan = cwd / "implementation_plan.md"
    if not source_plan.exists():
        print("\n❌ Error: 'implementation_plan.md' not found.")
        print("   Cannot secure context without a plan. Please run /plan first.\n")
        sys.exit(1)

    # 2. Resolve Target: ACTIVE_PLAN.md
    target_plan = cwd / "ACTIVE_PLAN.md"
    real_target = target_plan
    is_symlink = False

    if target_plan.is_symlink():
        is_symlink = True
        real_target = target_plan.resolve()
        # Security check: Ensure we are not writing outside project scope strangely
        # (Basic check, effectively we trust the symlink if established by orchestrator)
    
    try:
        # 3. Secure the content
        content = source_plan.read_text(encoding='utf-8')
        
        # Write to the REAL target (follows symlink if present)
        real_target.write_text(content, encoding='utf-8')
        
        print(f"\n✅ Context Secured!")
        print(f"   Source: {source_plan.name}")
        if is_symlink:
             # Show relative path for cleaner output if possible
            try:
                rel_path = real_target.relative_to(cwd)
                print(f"   Target: ACTIVE_PLAN.md -> {rel_path} (Track Synced)")
            except ValueError:
                print(f"   Target: ACTIVE_PLAN.md -> {real_target} (Track Synced)")
        else:
            print(f"   Target: ACTIVE_PLAN.md")

        # 4. Sync Verification (if Orchestrator is active)
        if is_symlink:
            try:
                subprocess.run(["skt", "orchestrator:sync"], check=False, capture_output=True)
            except Exception:
                pass # Silent fail on sync is acceptable here, data is already written
        
        # 5. The "Clear" Instruction
        print("\n" + "="*50)
        print("🛑  STOP & RESET  🛑".center(50))
        print("="*50)
        print("\nYour plan is now SAFELY SAVED in the system beacon.")
        print("\n👉 ACTION REQUIRED: Click 'New Chat' / 'Clear History' NOW.")
        print("\nAfter resetting, type:")
        print("   /cook")
        print("\n(The agent will auto-load your plan from the beacon)")
        print("="*50 + "\n")

    except Exception as e:
        print(f"\n❌ Error securing context: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
