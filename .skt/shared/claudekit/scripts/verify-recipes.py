#!/usr/bin/env python3
"""
Verify Recipes - Automated Test Suite
======================================
Tests all SKT Workflow Recipes for correctness.

Test Categories:
1. Workflow Registration
2. Recipe 1 Flow (Build Feature)
3. Recipe 2 Flow (Fix Bug)
4. Recipe 3 Flow (Quick Implementation)
5. CLI Flags
"""

import unittest
import os
import sys
import tempfile
import shutil
import subprocess
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent
QUERY_WORKFLOW = SCRIPT_DIR / "query-workflow.py"


class TestWorkflowRegistration(unittest.TestCase):
    """Test that all required workflows are registered."""

    def run_query(self, workflow_name):
        """Helper to query a workflow."""
        result = subprocess.run(
            ["python3", str(QUERY_WORKFLOW), workflow_name, "--format", "markdown"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT
        )
        return result

    def test_debug_workflow_exists(self):
        """Test that debug workflow is registered."""
        result = self.run_query("debug")
        self.assertEqual(result.returncode, 0, f"debug workflow failed: {result.stderr}")
        self.assertIn("debug", result.stdout.lower())

    def test_ultrathink_workflow_exists(self):
        """Test that ultrathink workflow is registered."""
        result = self.run_query("ultrathink")
        self.assertEqual(result.returncode, 0, f"ultrathink workflow failed: {result.stderr}")
        self.assertIn("ultrathink", result.stdout.lower())

    def test_clear_workflow_exists(self):
        """Test that clear workflow is registered."""
        result = self.run_query("clear")
        self.assertEqual(result.returncode, 0, f"clear workflow failed: {result.stderr}")
        self.assertIn("clear", result.stdout.lower())

    def test_plan_workflow_exists(self):
        """Test that plan workflow is registered."""
        result = self.run_query("plan")
        self.assertEqual(result.returncode, 0, f"plan workflow failed: {result.stderr}")

    def test_cook_workflow_exists(self):
        """Test that cook workflow is registered."""
        result = self.run_query("cook")
        self.assertEqual(result.returncode, 0, f"cook workflow failed: {result.stderr}")

    def test_fix_workflow_exists(self):
        """Test that fix workflow is registered."""
        result = self.run_query("fix")
        self.assertEqual(result.returncode, 0, f"fix workflow failed: {result.stderr}")


class TestDebugScript(unittest.TestCase):
    """Test the debug-context.py script."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.cwd_backup = os.getcwd()
        os.chdir(self.test_dir)
        self.debug_script = SCRIPT_DIR / "debug-context.py"

    def tearDown(self):
        os.chdir(self.cwd_backup)
        shutil.rmtree(self.test_dir)

    def test_debug_with_error_message(self):
        """Test debug script with a sample error."""
        result = subprocess.run(
            ["python3", str(self.debug_script), "TypeError: Cannot read property 'map' of undefined"],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertTrue(Path("debug-report.md").exists())
        
        content = Path("debug-report.md").read_text()
        self.assertIn("TypeError", content)
        self.assertIn("Root Cause", content)

    def test_debug_generates_hypotheses(self):
        """Test that debug script generates hypotheses."""
        subprocess.run(
            ["python3", str(self.debug_script), "ReferenceError: x is not defined"],
            capture_output=True,
            text=True
        )
        
        content = Path("debug-report.md").read_text()
        self.assertIn("Hypotheses", content)
        self.assertIn("not defined", content.lower())


class TestSecureContext(unittest.TestCase):
    """Test the secure-context.py (clear) script."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.cwd_backup = os.getcwd()
        os.chdir(self.test_dir)
        self.clear_script = SCRIPT_DIR / "secure-context.py"

    def tearDown(self):
        os.chdir(self.cwd_backup)
        shutil.rmtree(self.test_dir)

    def test_clear_requires_plan(self):
        """Test that clear fails without implementation_plan.md."""
        result = subprocess.run(
            ["python3", str(self.clear_script)],
            capture_output=True,
            text=True
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not found", result.stdout)

    def test_clear_copies_plan(self):
        """Test that clear copies plan to ACTIVE_PLAN.md."""
        # Create test plan
        Path("implementation_plan.md").write_text("# Test Plan\nContent here")
        
        result = subprocess.run(
            ["python3", str(self.clear_script)],
            capture_output=True,
            text=True
        )
        
        self.assertEqual(result.returncode, 0)
        self.assertTrue(Path("ACTIVE_PLAN.md").exists())
        self.assertIn("Test Plan", Path("ACTIVE_PLAN.md").read_text())


class TestRecipeDocumentation(unittest.TestCase):
    """Test that recipe documentation files exist and have content."""

    def test_readme_exists(self):
        """Test that recipes README exists."""
        readme = PROJECT_ROOT / "docs" / "recipes" / "README.md"
        self.assertTrue(readme.exists(), "docs/recipes/README.md not found")
        content = readme.read_text()
        self.assertIn("Workflow Recipes", content)

    def test_build_feature_exists(self):
        """Test that build-feature.md exists."""
        doc = PROJECT_ROOT / "docs" / "recipes" / "build-feature.md"
        self.assertTrue(doc.exists(), "build-feature.md not found")
        content = doc.read_text()
        self.assertIn("ultrathink", content)
        self.assertIn("plan", content)
        self.assertIn("clear", content)
        self.assertIn("cook", content)

    def test_fix_bug_exists(self):
        """Test that fix-bug.md exists."""
        doc = PROJECT_ROOT / "docs" / "recipes" / "fix-bug.md"
        self.assertTrue(doc.exists(), "fix-bug.md not found")
        content = doc.read_text()
        self.assertIn("debug", content)
        self.assertIn("fix", content)

    def test_quick_implementation_exists(self):
        """Test that quick-implementation.md exists."""
        doc = PROJECT_ROOT / "docs" / "recipes" / "quick-implementation.md"
        self.assertTrue(doc.exists(), "quick-implementation.md not found")
        content = doc.read_text()
        self.assertIn("cook", content)
        self.assertIn("--quick", content)


def run_tests():
    """Run all tests and return results."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestWorkflowRegistration))
    suite.addTests(loader.loadTestsFromTestCase(TestDebugScript))
    suite.addTests(loader.loadTestsFromTestCase(TestSecureContext))
    suite.addTests(loader.loadTestsFromTestCase(TestRecipeDocumentation))

    # Run
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
