#!/usr/bin/env python3
"""
Debug Context - Root Cause Analyzer
====================================
Analyzes bugs and errors to identify root causes.
Used by the /debug workflow.

Phases:
1. Analyze Code - Read relevant files
2. Read Logs - Parse error messages
3. Reproduce - Identify reproduction steps
4. Identify Root Cause - Generate hypotheses
5. Report - Output debug-report.md
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime

def setup_utf8():
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def parse_error_message(error_text: str) -> dict:
    """Extract structured info from error message."""
    result = {
        "type": "Unknown",
        "message": error_text,
        "file": None,
        "line": None,
        "stack_trace": []
    }
    
    # Common error patterns
    patterns = [
        # JavaScript/TypeScript
        r"(?P<type>\w+Error):\s*(?P<message>.+?)(?:\n|$)",
        # Python
        r"(?P<type>\w+Error):\s*(?P<message>.+)",
        # Generic file:line pattern
        r"(?P<file>[\w/.-]+):(?P<line>\d+)",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, error_text)
        if match:
            groups = match.groupdict()
            for key, value in groups.items():
                if value:
                    result[key] = value
    
    # Extract stack trace lines
    stack_lines = re.findall(r"at\s+(.+?)\s+\((.+?):(\d+):\d+\)", error_text)
    result["stack_trace"] = [{"fn": fn, "file": f, "line": l} for fn, f, l in stack_lines]
    
    return result

def generate_hypotheses(error_info: dict) -> list:
    """Generate root cause hypotheses based on error type."""
    hypotheses = []
    error_type = error_info.get("type", "").lower()
    
    if "typeerror" in error_type:
        hypotheses.extend([
            "Variable is undefined or null when accessed",
            "Method called on wrong type (e.g., .map() on non-array)",
            "Missing null check before property access",
            "Async data not loaded before render"
        ])
    elif "referenceerror" in error_type:
        hypotheses.extend([
            "Variable not defined in current scope",
            "Import statement missing or incorrect",
            "Typo in variable name"
        ])
    elif "syntaxerror" in error_type:
        hypotheses.extend([
            "Missing bracket, parenthesis, or semicolon",
            "Invalid JSON format",
            "Unexpected token in expression"
        ])
    elif "networkerror" in error_type or "fetch" in error_info.get("message", "").lower():
        hypotheses.extend([
            "API endpoint not reachable",
            "CORS policy blocking request",
            "Invalid URL or missing environment variable"
        ])
    else:
        hypotheses.extend([
            "Logic error in control flow",
            "State mutation issue",
            "Race condition or timing issue"
        ])
    
    return hypotheses

def main():
    setup_utf8()
    cwd = Path.cwd()
    
    # Get error description from args or stdin
    error_description = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    
    if not error_description:
        print("\n🔍 Debug Context Analyzer")
        print("=" * 50)
        print("\nUsage: debug-context.py <error description>")
        print("\nExample:")
        print("  debug-context.py 'TypeError: Cannot read property map of undefined'")
        print("\nOr pipe error logs:")
        print("  cat error.log | debug-context.py")
        print("=" * 50)
        
        # Check if there's piped input
        if not sys.stdin.isatty():
            error_description = sys.stdin.read()
        else:
            sys.exit(1)
    
    print(f"\n🔍 Analyzing: {error_description[:100]}...")
    
    # Parse error
    error_info = parse_error_message(error_description)
    
    # Generate hypotheses
    hypotheses = generate_hypotheses(error_info)
    
    # Generate report
    report_content = f"""# Debug Report

**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## 1. Error Summary

| Field | Value |
|-------|-------|
| **Type** | `{error_info['type']}` |
| **Message** | {error_info['message'][:200]} |
| **File** | {error_info['file'] or 'Unknown'} |
| **Line** | {error_info['line'] or 'Unknown'} |

---

## 2. Stack Trace Analysis

"""
    
    if error_info["stack_trace"]:
        report_content += "| Function | File | Line |\n|----------|------|------|\n"
        for item in error_info["stack_trace"][:5]:
            report_content += f"| `{item['fn']}` | {item['file']} | {item['line']} |\n"
    else:
        report_content += "> No stack trace available.\n"
    
    report_content += f"""
---

## 3. Root Cause Hypotheses

"""
    for i, hypothesis in enumerate(hypotheses, 1):
        report_content += f"{i}. **{hypothesis}**\n"
    
    report_content += """
---

## 4. Recommended Next Steps

1. **Verify Hypothesis #1**: Check the identified file/line for null/undefined values
2. **Add Logging**: Insert console.log/print statements to trace variable states
3. **Check Recent Changes**: Review git diff for related modifications
4. **Run `/fix`**: Once root cause is confirmed, use `/fix` to apply the solution

---

> [!TIP]
> After debugging, run `/fix` to apply the fix and `/cook` to verify with tests.
"""
    
    # Save report
    report_path = cwd / "debug-report.md"
    report_path.write_text(report_content, encoding='utf-8')
    
    print(f"\n✅ Debug Report Generated: {report_path.name}")
    print("\n📋 Summary:")
    print(f"   Error Type: {error_info['type']}")
    print(f"   Top Hypothesis: {hypotheses[0] if hypotheses else 'Unknown'}")
    print(f"\n👉 Next: Review debug-report.md, then run /fix")

if __name__ == "__main__":
    main()
