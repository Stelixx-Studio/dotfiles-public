#!/usr/bin/env python3
"""
Verify Clear Workflow
=====================
Automated test suite for secure-context.py.
Tests:
1. Standard Context Security
2. Symlink/Orchestrator Awareness
3. Error Handling (Missing Plan)
"""

import unittest
import os
import shutil
import tempfile
import subprocess
from pathlib import Path

# Path to the script under test
SCRIPT_PATH = Path(__file__).parent / "secure-context.py"

class TestSecureContext(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for each test
        self.test_dir = tempfile.mkdtemp()
        self.cwd_backup = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        # Restore CWD and cleanup
        os.chdir(self.cwd_backup)
        shutil.rmtree(self.test_dir)

    def run_script(self):
        # Helper to run the script in the current temp dir
        return subprocess.run(
            ["python3", str(SCRIPT_PATH)],
            capture_output=True,
            text=True
        )

    def test_missing_plan_fails(self):
        """Test that missing implementation_plan.md causes failure"""
        result = self.run_script()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not found", result.stdout)

    def test_standard_secure(self):
        """Test standard securing of context to a local file"""
        # Data Setup
        Path("implementation_plan.md").write_text("# My Plan", encoding='utf-8')
        
        # Action
        result = self.run_script()
        
        # Assertions
        self.assertEqual(result.returncode, 0)
        self.assertTrue(Path("ACTIVE_PLAN.md").exists())
        self.assertEqual(Path("ACTIVE_PLAN.md").read_text(encoding='utf-8'), "# My Plan")
        self.assertIn("ACTIVE_PLAN.md", result.stdout)
        self.assertIn("STOP & RESET", result.stdout)

    def test_orchestrator_symlink(self):
        """Test that script writes to the symlink target, not breaking the link"""
        # Data Setup
        tracks_dir = Path(".skt/tracks")
        tracks_dir.mkdir(parents=True)
        target_file = tracks_dir / "ACTIVE_PLAN.md"
        target_file.write_text("# Old Plan", encoding='utf-8')
        
        os.symlink(target_file, "ACTIVE_PLAN.md")
        Path("implementation_plan.md").write_text("# New Plan", encoding='utf-8')
        
        # Action
        result = self.run_script()
        
        # Assertions
        self.assertEqual(result.returncode, 0)
        
        # 1. Link should still be a link
        self.assertTrue(Path("ACTIVE_PLAN.md").is_symlink())
        
        # 2. Target should be updated
        self.assertEqual(target_file.read_text(encoding='utf-8'), "# New Plan")
        
        # 3. Output should mention symlink/track logic
        self.assertIn("Track Synced", result.stdout)

if __name__ == "__main__":
    unittest.main()
