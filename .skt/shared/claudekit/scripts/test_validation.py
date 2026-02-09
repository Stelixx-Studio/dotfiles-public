#!/usr/bin/env python3
import unittest
from validation import SecurityValidator

class TestSecurityValidator(unittest.TestCase):
    def test_validate_skill_name_valid(self):
        valid_names = ["plan", "cook", "git-commit", "skill:create", "my_workflow_123"]
        for name in valid_names:
            self.assertEqual(SecurityValidator.validate_skill_name(name), name)

    def test_validate_skill_name_invalid_chars(self):
        invalid_names = ["plan; rm", "cook $(id)", "git&push", "workflow<script>"]
        for name in invalid_names:
            with self.assertRaises(ValueError):
                SecurityValidator.validate_skill_name(name)

    def test_validate_skill_name_traversal(self):
        traversal_names = ["../../etc/passwd", "sub/../../secret", "C:\\Windows\\System32"]
        for name in traversal_names:
            with self.assertRaises(ValueError):
                SecurityValidator.validate_skill_name(name)

    def test_validate_skill_name_empty(self):
        with self.assertRaises(ValueError):
            SecurityValidator.validate_skill_name("")

    def test_validate_skill_name_too_long(self):
        long_name = "a" * 101
        with self.assertRaises(ValueError):
            SecurityValidator.validate_skill_name(long_name)

if __name__ == "__main__":
    unittest.main()
