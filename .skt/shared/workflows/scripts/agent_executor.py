#!/usr/bin/env python3
"""
Agent Executor - SKT CLI
========================
Parallel CLI tool orchestrator for Agent-type workflows.
Spawns multiple AI CLI tools in parallel and aggregates results.

Usage:
    python3 agent_executor.py <query> [--tools gemini,opencode] [--test]
"""

import os
import sys
import json
import argparse
import subprocess
import concurrent.futures
from pathlib import Path
from typing import Dict, List, Optional, Any


def load_config() -> Dict[str, Any]:
    """Load agent config from .sktrc.json"""
    cwd = Path.cwd()
    # Priority list of config files
    config_files = [".skt/config.json", ".skt/config", ".sktrc.json"]
    
    for parent in [cwd] + list(cwd.parents)[:5]:
        for config_file in config_files:
            config_path = parent / config_file
            if config_path.exists():
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                        # If it has an 'agents' key, use that. 
                        # If not, use the whole config IF it has a 'tools' key.
                        # Return the full config if it has 'tools' or 'agents'
                        if 'agents' in config or 'tools' in config:
                            return config
                        # If it's the main .sktrc.json with no agents key, it's not our config.
                        continue
                except Exception:
                    pass
    
    # Return defaults if no config found
    return {
        "tools": {
            "gemini": {"command": "gemini", "model": "gemini-2.5-flash", "available": True},
            "opencode": {"command": "opencode", "available": True},
            "copilot": {"command": "gh copilot", "available": True},
            "find": {"command": "find", "available": True}
        },
        "parallelism": 3,
        "timeout": 300

    }


def check_tool_available(tool_config: Dict) -> bool:
    """Check if a CLI tool is available on the system"""
    command_str = tool_config.get('command', '')
    if not command_str:
        return False
    
    parts = command_str.split()
    if not parts:
        return False
        
    command = parts[0]
    
    try:
        result = subprocess.run(
            ['which', command],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except Exception:
        return False


def run_tool(tool_name: str, tool_config: Dict, query: str, timeout: int, hidden: bool = False) -> Dict:
    """Execute a single CLI tool and return results"""
    command = tool_config.get('command', tool_name)
    model = tool_config.get('model', '')
    
    # Build command based on tool type
    if tool_name == 'gemini':
        cmd = f'{command} -y -p "{query}"'
        if model:
            cmd += f' --model {model}'
    elif tool_name == 'opencode':
        cmd = f'{command} run "{query}"'
        if hidden:
            cmd += ' --hidden'
    elif tool_name == 'copilot':
        # Use -p for non-interactive mode as required by gh copilot CLI
        cmd = f'{command} -p "explain {query}"'
    elif tool_name == 'find':
        # High-performance local search fallback
        search_term = query.replace('"', '').replace("'", "")
        cmd = f'find . -maxdepth 4 -name "*{search_term}*"'
        if hidden:
            # find shows hidden by default, but we can filter or expand
            pass
    else:
        cmd = f'{command} "{query}"'
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            stdin=subprocess.DEVNULL
        )
        return {
            "tool": tool_name,
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None
        }
    except subprocess.TimeoutExpired:
        return {
            "tool": tool_name,
            "success": False,
            "output": None,
            "error": f"Timeout after {timeout}s"
        }
    except Exception as e:
        return {
            "tool": tool_name,
            "success": False,
            "output": None,
            "error": str(e)
        }


def execute_parallel(query: str, tools: List[str], config: Dict) -> List[Dict]:
    """Execute multiple tools in parallel"""
    parallelism = config.get('parallelism', 3)
    timeout = config.get('timeout', 180)
    tool_configs = config.get('tools', {})
    
    results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=parallelism) as executor:
        futures = {}
        
        for tool_name in tools:
            tool_cfg = tool_configs.get(tool_name, {})
            if tool_cfg.get('available', False) or check_tool_available(tool_cfg):
                future = executor.submit(run_tool, tool_name, tool_cfg, query, timeout, config.get('hidden', False))
                futures[future] = tool_name
        
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                results.append({
                    "tool": futures[future],
                    "success": False,
                    "output": None,
                    "error": str(e)
                })
    
    return results


def aggregate_results(results: List[Dict]) -> str:
    """Aggregate and format results from multiple tools"""
    output = []
    
    successful = [r for r in results if r.get('success')]
    failed = [r for r in results if not r.get('success')]
    
    if successful:
        output.append("## Results\n")
        for r in successful:
            output.append(f"### {r['tool']}\n")
            output.append(r.get('output', '') + "\n")
    
    if failed:
        output.append("\n## Errors\n")
        for r in failed:
            output.append(f"- **{r['tool']}**: {r.get('error', 'Unknown error')}\n")
    
    if not successful and not failed:
        output.append("No tools were executed. Check agent config in .sktrc.json\n")
    
    return "\n".join(output)


def run_test() -> None:
    """Test mode: verify config and tool availability"""
    config = load_config()
    print("Agent Executor Test\n" + "=" * 40)
    print(f"\nConfig loaded: {json.dumps(config, indent=2)}\n")
    
    print("Tool Availability:")
    for tool_name, tool_cfg in config.get('tools', {}).items():
        available = check_tool_available(tool_cfg)
        status = "✅ Available" if available else "❌ Not found"
        print(f"  - {tool_name}: {status}")
    
    print(f"\nParallelism: {config.get('parallelism', 3)}")
    print(f"Timeout: {config.get('timeout', 180)}s")


def main():
    parser = argparse.ArgumentParser(description="Agent Executor - Parallel CLI orchestrator")
    parser.add_argument("query", nargs="?", help="Search query")
    parser.add_argument("--tools", help="Comma-separated list of tools to use")
    parser.add_argument("--test", action="store_true", help="Test mode: check config and tools")
    parser.add_argument("--hidden", action="store_true", help="Include hidden files in search")
    
    args = parser.parse_args()
    
    if args.test:
        run_test()
        return
    
    if not args.query:
        parser.print_help()
        sys.exit(1)
    
    config = load_config()
    
    # Determine which tools to use
    if args.tools:
        tools = [t.strip() for t in args.tools.split(',')]
    else:
        tools = list(config.get('tools', {}).keys())
        # Scout Optimization: Use local find for faster metadata results
        if "find" not in tools:
            tools.append("find")
    
    # Auto-hidden detection
    hidden_keywords = ["hidden", "config", "instruction", ".env", ".agent", ".skt"]
    if args.hidden or any(k in (args.query or "").lower() for k in hidden_keywords):
        config['hidden'] = True
        print("> [!NOTE] Deep Scout: Hidden file visibility enabled.")
    
    print(f"> [!INFO] Executing agent with tools: {', '.join(tools)}")
    
    results = execute_parallel(args.query, tools, config)
    output = aggregate_results(results)
    
    print(output)


if __name__ == "__main__":
    main()
