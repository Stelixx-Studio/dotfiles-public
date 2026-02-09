#!/usr/bin/env python3
"""
Tracks Agent Command
Shows active tracks dashboard in markdown format.
"""

import sys
import json
from pathlib import Path

def main():
    root = Path.cwd()
    active_path = root / ".skt" / "tracks" / "active.json"
    
    if not active_path.exists():
        print("No active tracks found.")
        return
        
    try:
        with open(active_path, 'r') as f:
            active_data = json.load(f)
            
        if not active_data.get('activeTracks'):
            print("No active tracks found.")
            return
            
        print("# 🛰️ Active Tracks Dashboard\n")
        print("| Order | Track ID | Description | Anchors | Conflicts |")
        print("|-------|----------|-------------|---------|-----------|")
        
        for track in active_data['activeTracks']:
            track_id = track['id']
            # Load metadata for description
            meta_path = root / ".skt" / "tracks" / track_id / "metadata.json"
            description = "N/A"
            if meta_path.exists():
                with open(meta_path, 'r') as mf:
                    meta = json.load(mf)
                    description = meta.get('description', 'N/A')
            
            anchors = ", ".join(track.get('anchors', []))
            if len(anchors) > 30:
                anchors = anchors[:27] + "..."
            
            # Check for conflict file
            impact_path = root / ".skt" / "tracks" / track_id / "impact.md"
            conflicts = "✅ Clear"
            if impact_path.exists():
                conflicts = "⚠️ [Impact](file://" + str(impact_path) + ")"
                
            print(f"| {track.get('priority', '-')} | {track_id} | {description} | {anchors} | {conflicts} |")
            
    except Exception as e:
        print(f"Error loading dashboard: {e}")

if __name__ == "__main__":
    main()
