#!/usr/bin/env python3
"""
Sync Tracks Agent Command: Sync
Delegates to skt CLI and ensures beacon symlink.
"""

import sys
import subprocess
import os
from pathlib import Path

def main():
    root = Path.cwd()
    
    # 1. Delegate to skt CLI
    print("🛰️ Synchronizing beacon via skt...")
    result = subprocess.run(["skt", "orchestrator:sync"], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Beacon Sync Failed:\n{result.stderr}")
        sys.exit(1)
    
    # 2. Ensure symlink (visibility helper)
    beacon_target = root / ".skt" / "tracks" / "ACTIVE_PLAN.md"
    beacon_link = root / "ACTIVE_PLAN.md"
    
    if beacon_target.exists():
        if not beacon_link.exists():
            try:
                os.symlink(beacon_target, beacon_link)
                print(f"🔗 Created symlink: ACTIVE_PLAN.md -> {beacon_target}")
            except Exception as e:
                print(f"⚠️  Failed to create symlink: {e}")
        print("✅ Beacon synchronized successfully.")
    else:
        print("⚠️  Sync completed but beacon target not found. No tracks might be active.")

if __name__ == "__main__":
    main()
