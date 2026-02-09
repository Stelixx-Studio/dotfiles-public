#!/usr/bin/env python3
"""
Orchestrate Agent: Resume Command
Delegates to skt CLI and performs physical audit of planned files.
"""

import sys
import json
import subprocess
import re
import os
from pathlib import Path

def extract_planned_files(content):
    """Extract file paths from markdown checkboxes in plan.md"""
    matches = re.findall(r'\[[ xX/]?\]\s+`?([a-zA-Z0-9_\-\./]+\.[a-z]+)`?', content)
    return list(set(matches))

def main():
    root = Path.cwd()
    target_id = sys.argv[1] if len(sys.argv) > 1 else None

    print("🛰️  Resuming session...")
    
    # 1. Sync latest beacon state via skt
    subprocess.run(["skt", "orchestrator:sync"], capture_output=True)

    # 2. Identify Active Track ID
    track_id = target_id
    if not track_id or track_id == 'None':
        # Try to infer from ACTIVE_PLAN.md
        beacon_path = root / "ACTIVE_PLAN.md"
        if beacon_path.exists():
            with open(beacon_path, 'r') as f:
                content = f.read()
                tid_match = re.search(r'\- \*\*ID\*\*: `([^`]+)`', content)
                if tid_match:
                    track_id = tid_match.group(1)
        
    if not track_id:
        print("❌ No active track found. Start one with: `skt orchestrator:new`")
        sys.exit(1)

    print(f"🛰️  **Resuming Track: {track_id}**")
    
    # 3. Reality Check (Physical Audit)
    track_dir = root / ".skt" / "tracks" / track_id
    plan_path = track_dir / "plan.md"
    
    if plan_path.exists():
        with open(plan_path, 'r') as f:
            plan_content = f.read()
        
        planned_files = extract_planned_files(plan_content)
        
        if planned_files:
            print("\n🔍 **Reality Check (Physical Audit):**")
            found = []
            missing = []
            for f_rel in planned_files:
                f_path = root / f_rel
                if f_path.exists():
                    found.append(f_rel)
                else:
                    missing.append(f_rel)
            
            if found:
                print(f"  - ✅ Existing items: {', '.join([f'`{f}`' for f in found[:5]])}{'...' if len(found) > 5 else ''}")
            if missing:
                print(f"  - ❓ Pending item: {', '.join([f'`{f}`' for f in missing[:5]])}{'...' if len(missing) > 5 else ''}")
                print(f"  - *Suggestion: Agent should start from these missing files.*")
        else:
            print("\nℹ️  No specific files found in `plan.md` for audit.")
    else:
        print(f"\n⚠️  `plan.md` not found in `{track_dir}`. Check your plan manually.")

    print(f"\n🧠 **AI Warm-up Briefing:**")
    print(f"  1. Read context from `ACTIVE_PLAN.md` at root.")
    print(f"  2. Follow the implementation plan in `.skt/tracks/{track_id}/plan.md`.")
    print(f"  3. Use `skt orchestrator:sync` after major changes.")

if __name__ == "__main__":
    main()
