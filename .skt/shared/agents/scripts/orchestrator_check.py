#!/usr/bin/env python3
"""
Conflicts Agent Command: Check
Delegates to skt CLI and summarizes conflicts.
"""

import sys
import subprocess
import re
from pathlib import Path

def main():
    root = Path.cwd()
    
    print("🔍 Running conflict assessment via skt...")
    # skt orchestrator:sync automatically runs detectConflicts and generates impact assessments
    result = subprocess.run(["skt", "orchestrator:sync"], capture_output=True, text=True)
    
    if result.returncode != 0:
         print(f"❌ Conflict Assessment Failed:\n{result.stderr}")
         sys.exit(1)
         
    # Parse output or ACTIVE_PLAN.md for summary
    beacon_path = root / "ACTIVE_PLAN.md"
    if beacon_path.exists():
        with open(beacon_path, 'r') as f:
            content = f.read()
            
        conflicts = re.findall(r'⚠️ (High|Medium|Low) with (\d+) track\(s\)', content)
        
        print(f"🔍 Conflict Assessment Complete.")
        if conflicts:
            print(f"⚠️  Detected {len(conflicts)} tracks with conflicts.")
            print("📊 Impact assessments updated in .skt/tracks/<id>/impact.md")
        else:
            print("✅ No conflicts found across active tracks.")
    else:
        print("⚠️  Assessment complete, but ACTIVE_PLAN.md not found.")

if __name__ == "__main__":
    main()
