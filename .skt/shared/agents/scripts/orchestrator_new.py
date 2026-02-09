#!/usr/bin/env python3
"""
Orchestrate Agent Command: New
Delegates to skt CLI and provides detected anchors.
"""

import sys
import subprocess
import re
import json
from pathlib import Path

def detect_anchors(description):
    """Heuristic for detecting anchors from description"""
    # Look for paths or specific directories
    path_regex = r'([a-zA-Z0-9_\-\./]+\.(?:ts|tsx|js|jsx|json|md|csv))'
    dir_regex = r'(?:apps|features|packages|libs|docs)/[a-zA-Z0-9_\-\./]+'
    
    paths = re.findall(path_regex, description)
    dirs = re.findall(dir_regex, description)
    
    unique_anchors = list(set(paths + dirs))
    unique_anchors = [a for a in unique_anchors if '/' in a and not a.startswith('./')]
    
    return unique_anchors if unique_anchors else ["."]

def main():
    if len(sys.argv) < 2:
        print("Usage: orchestrator:new <description>")
        sys.exit(1)
        
    description = sys.argv[1]
    anchors = detect_anchors(description)
    
    print(f"🎯 Creating track via skt...")
    skt_cmd = ["skt", "orchestrator:new", description]
    if anchors:
        skt_cmd.extend(["--anchors", ",".join(anchors)])
        
    result = subprocess.run(skt_cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Orchestration Failed:\n{result.stderr}")
        sys.exit(1)
        
    # Standard output parsing for track ID
    id_match = re.search(r'Track created: (\S+)', result.stdout)
    track_id = id_match.group(1) if id_match else "unknown"
    
    print(f"🎯 Track Created: {track_id}")
    print(f"📍 Detected Anchors: {', '.join(anchors)}")
    print(f"🚀 Status: Track activated and beacon updated.")

if __name__ == "__main__":
    main()
