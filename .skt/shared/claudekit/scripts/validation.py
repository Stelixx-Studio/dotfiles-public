#!/usr/bin/env python3
"""
Legacy validation wrapper for SKT.
Points to the new centralized security_scanner.
"""

from pathlib import Path
import sys

# Try to find the new centralized scanner
# In production, it will be at .skt/shared/skt-core/scripts/common/
# In development, it might be relative to the current script
shared_common = Path(__file__).parent.parent.parent.parent / '.skt' / 'shared' / 'skt-core' / 'scripts' / 'common'

if not shared_common.exists():
    # Fallback to feature-relative path for development
    shared_common = Path(__file__).parent.parent.parent.parent / 'infrastructure' / 'skt-core' / 'scripts' / 'common'

sys.path.insert(0, str(shared_common))

try:
    from security_scanner import SecurityValidator, safe_skill_name, safe_csv_content, SecurityError
except ImportError:
    # Minimal fallback if not found
    import re
    class SecurityValidator:
        @classmethod
        def validate_skill_name(cls, name): return name
        @classmethod
        def sanitize_csv_content(cls, content): return content
    def safe_skill_name(name): return name
    def safe_csv_content(content): return content
    class SecurityError(Exception): pass
