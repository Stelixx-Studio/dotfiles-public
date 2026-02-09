#!/usr/bin/env python3
"""
ClaudeKit Workflow Query Engine

Queries workflow database and returns structured information about workflows,
their phases, and applicable best practices.
"""

import csv
import sys
import json
import io
from pathlib import Path
from typing import Dict, List, Optional

# DX Metrics Integration
sys.path.append(str(Path(__file__).parent.parent.parent / "shared" / "workflows" / "scripts"))
try:
    from dx_metrics import track_dx, log_event
except ImportError:
    def track_dx(*args, **kwargs): return lambda f: f
    def log_event(*args, **kwargs): pass

# Force UTF-8 output to prevent mojibake (e.g. â instead of ✅)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add current script directory to path for validation module
sys.path.insert(0, str(Path(__file__).parent))
from validation import SecurityValidator

# Base paths for data files
SHARED_DIR = Path(__file__).parent.parent.parent
DATA_DIRS = [SHARED_DIR / "claudekit" / "data"]

# Add skt-core/claudekit-core data directory (handles both prod and dev structures)
SKT_CORE_PROD = SHARED_DIR / "skt-core" / "data"
SKT_CORE_DEV = SHARED_DIR.parent / "infrastructure" / "skt-core" / "data"

if not SKT_CORE_PROD.exists():
    SKT_CORE_PROD = SHARED_DIR / "claudekit-core" / "data"
if not SKT_CORE_DEV.exists():
    SKT_CORE_DEV = SHARED_DIR.parent / "infrastructure" / "claudekit-core" / "data"

def load_workflows() -> Dict[str, Dict]:
    """Load all workflows from all available DATA_DIRS and Feature Directories"""
    workflows = {}
    
    # 1. Load from central data dirs
    for data_dir in DATA_DIRS:
        csv_path = data_dir / "workflows.csv"
        if not csv_path.exists():
            continue
            
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    row['_data_dir'] = data_dir
                    workflows[row['name']] = row
        except Exception as e:
            print(f"Error loading workflows from {csv_path}: {e}", file=sys.stderr)
            
    # 2. Dynamic Scan: features/*/data/workflows.csv
    features_dir = SHARED_DIR.parent.parent / "features"
    if features_dir.exists():
        for workflow_csv in features_dir.glob("*/data/workflows.csv"):
            try:
                feature_dir = workflow_csv.parent.parent
                feature_name = feature_dir.name
                
                # Check for project.json namespace override
                project_json = feature_dir / "project.json"
                if project_json.exists():
                    try:
                        with open(project_json, 'r', encoding='utf-8') as pj:
                            pdata = json.load(pj)
                            if "skt" in pdata and "namespace" in pdata["skt"]:
                                feature_name = pdata["skt"]["namespace"]
                    except: pass
                with open(workflow_csv, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        # Prefix key to avoid collisions, but keep name clean
                        # If row['name'] is 'deploy', and feature is 'cloudflare', key might be 'deploy' if unique
                        # BUT to support 'cloudflare:deploy', we usually add aliases.
                        # For now, just load them in.
                        row['_data_dir'] = workflow_csv.parent
                        
                        # Store by raw name (e.g., 'deploy')
                        workflows[row['name']] = row
                        
                        # Also store by fully qualified name (e.g., 'cloudflare:deploy')
                        # This allows `skt cloudflare:deploy` to work even if `deploy` is ambiguous
                        fqdn = f"{feature_name}:{row['name']}"
                        workflows[fqdn] = row
                        
            except Exception as e:
                # Silently fail for individual invalid files to avoid crashing entire engine
                pass
            
    return workflows

def load_phases(workflow_id: str, data_dir: Path) -> List[Dict]:
    """Load phases for a specific workflow from its specific data_dir"""
    phases = []
    csv_path = data_dir / "phases.csv"
    
    try:
        if not csv_path.exists():
            return []
            
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['workflow_id'] == workflow_id:
                    phases.append(row)
        return sorted(phases, key=lambda x: int(x['phase_order']))
    except Exception as e:
        print(f"Error loading phases from {csv_path}: {e}", file=sys.stderr)
        return []

def load_best_practices(workflow_name: str) -> List[Dict]:
    """Load applicable best practices for a workflow from all data sources"""
    practices = []
    
    for data_dir in DATA_DIRS:
        csv_path = data_dir / "best-practices.csv"
        if not csv_path.exists():
            continue
            
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Check if workflow name is in applies_to field
                    if workflow_name in row['applies_to'].split('|'):
                        practices.append(row)
        except Exception as e:
            print(f"Error loading best practices from {csv_path}: {e}", file=sys.stderr)
            
    # Sort by priority (high, medium, low)
    priority_order = {'high': 0, 'medium': 1, 'low': 2}
    return sorted(practices, key=lambda x: priority_order.get(x['priority'], 3))

@track_dx(event_name="workflow_query", pillar="transparency", domain="arch")
def query_workflow(workflow_name: str) -> Dict:
    """
    Query workflow database and return complete workflow information
    
    Args:
        workflow_name: Name of the workflow to query
        
    Returns:
        Dictionary containing workflow metadata, phases, and best practices
    """
    workflows = load_workflows()
    
    if workflow_name not in workflows:
        return {
            "error": f"Workflow '{workflow_name}' not found",
            "available_workflows": sorted(list(workflows.keys()))
        }
    
    workflow = workflows[workflow_name]
    phases = load_phases(workflow['id'], workflow['_data_dir'])
    practices = load_best_practices(workflow_name)
    
    return {
        "workflow": {
            "id": workflow['id'],
            "name": workflow['name'],
            "type": workflow.get('category', 'workflow'),  # 'agent' for parallel execution
            "category": workflow['category'],
            "description": workflow['description'],
            "complexity": workflow['complexity'],
            "auto_execution": workflow.get('auto_execution', '2'),
            "auto_load_instructions": workflow.get('auto_load_instructions', 'false'),
            "tools": workflow['tools'].split('|') if workflow['tools'] else [],
            "template": workflow['template'] if workflow['template'] else None,
            "capability_group": workflow.get('capability_group', 'common'),
            "mcp_servers": workflow.get('mcp_servers', '').split('|') if workflow.get('mcp_servers') else []
        },
        "phases": [
            {
                "order": int(phase['phase_order']),
                "name": phase['phase_name'],
                "description": phase['description'],
                "commands": phase['commands'].split(';') if phase['commands'] else [],
                "outputs": phase['outputs']
            }
            for phase in phases
        ],
        "best_practices": [
            {
                "category": practice['category'],
                "practice": practice['practice'],
                "description": practice['description'],
                "priority": practice['priority']
            }
            for practice in practices
        ],
        "metadata": {
            "total_phases": len(phases),
            "total_practices": len(practices),
            "has_research": 'parallel-research.sh' in workflow.get('tools', ''),
            "has_template": bool(workflow.get('template'))
        }
    }

def list_workflows() -> Dict:
    """List all available workflows grouped by category"""
    workflows = load_workflows()
    
    # Group by category
    by_category = {}
    for name, workflow in workflows.items():
        category = workflow['category']
        if category not in by_category:
            by_category[category] = []
        by_category[category].append({
            "name": name,
            "description": workflow['description'],
            "complexity": workflow['complexity'],
            "capability_group": workflow.get('capability_group', 'common')
        })
    
    return {
        "total_workflows": len(workflows),
        "categories": by_category
    }

def format_as_markdown(data: Dict, args: Optional[str] = None, execution_flags: Optional[Dict] = None) -> str:
    """Format workflow data as markdown instructions for Agent"""
    if "error" in data:
        return f"# Error\n\n{data['error']}\n\nAvailable workflows: {', '.join(data.get('available_workflows', []))}"

    workflow = data['workflow']
    phases = data['phases']
    practices = data['best_practices']

    md = []
    
    # Auto-load project instructions if enabled
    auto_load = workflow.get('auto_load_instructions', 'false')
    if auto_load == 'true':
        # Deep Load Strategy:
        # 1. Search for .agent root
        # 2. Load .agent/instructions/generated/core.md
        # 3. Load .agent/instructions/custom/project-rules.md
        
        from pathlib import Path
        cwd = Path.cwd()
        agent_root = None
        
        # Locate .agent directory (up to 3 levels)
        for parent in [cwd] + list(cwd.parents)[:3]:
            candidate = parent / '.agent'
            if candidate.exists():
                agent_root = candidate
                break
        
        if agent_root:
            instructions_found = False
            md_content = []
            
            # 1. Core Framework Rules
            core_rules = agent_root / 'instructions/generated/core.md'
            if core_rules.exists():
                try:
                    content = core_rules.read_text(encoding='utf-8').strip()
                    md_content.append(f"## 🛡️ Framework Rules (from {core_rules.name})\n\n{content}\n")
                    instructions_found = True
                except: pass
                
            # 2. Custom Project Rules
            custom_rules = agent_root / 'instructions/custom/project-rules.md'
            if custom_rules.exists():
                try:
                    content = custom_rules.read_text(encoding='utf-8').strip()
                    md_content.append(f"## ⚡ Project Rules (from {custom_rules.name})\n\n{content}\n")
                    instructions_found = True
                except: pass
            
            # 3. Fallback to legacy if no modern rules found
            if not instructions_found:
                legacy = agent_root / 'instructions.md'
                if legacy.exists():
                    try:
                         # Legacy behavior: just link it or try to read it
                         content = legacy.read_text(encoding='utf-8')
                         md_content.append(f"## Project Instructions\n\n{content}\n")
                    except: pass

            if md_content:
                md.append("# 📋 Project Context & Rules\n")
                md.append("\n---\n".join(md_content))
                md.append("\n---\n")

            # 4. Conductor Beacon (ACTIVE_PLAN.md)
            beacon = agent_root.parent / 'ACTIVE_PLAN.md'
            if beacon.exists():
                try:
                    content = beacon.read_text(encoding='utf-8').strip()
                    md.append("# 🔥 Active Development (Conductor)\n")
                    md.append(f"{content}\n")
                    md.append("\n---\n")
                except: pass

    # Inject arguments into description if present
    description = workflow['description']
    if args and "$1" in description:
        description = description.replace("$1", args)

    md.append(f"# Workflow: {workflow['name'].title()}")
    md.append(f"**Description**: {description}\n")

    if args:
        md.append(f"**Context**: {args}\n")
    
    # Display MCP servers if workflow has them
    mcp_servers = workflow.get('mcp_servers', [])
    if mcp_servers:
        md.append("## 🔌 MCP Servers\n")
        md.append("This workflow uses the following MCP servers for enhanced capabilities:\n")
        
        # Load MCP registry for descriptions
        mcp_registry = {}
        try:
            # SHARED_DIR is features/, so registry is at features/mcp/data/registry.json
            registry_path = SHARED_DIR / "mcp" / "data" / "registry.json"
            if registry_path.exists():
                with open(registry_path, 'r', encoding='utf-8') as rf:
                    registry_data = json.load(rf)
                    mcp_registry = registry_data.get('servers', {})
        except Exception as e:
            pass  # Silently fail if registry not found
        
        for server_id in mcp_servers:
            server_info = mcp_registry.get(server_id, {})
            server_name = server_info.get('name', server_id)
            server_desc = server_info.get('description', 'MCP server')
            
            md.append(f"- **{server_name}** (`{server_id}`): {server_desc}")
        
        md.append("")  # Empty line after MCP servers

    for phase in phases:
        md.append(f"## Phase {phase['order']}: {phase['name']}")
        if phase['description']:
            md.append(f"{phase['description']}\n")
        
        if phase['commands']:
            for cmd in phase['commands']:
                # Inject args into commands
                final_cmd = cmd
                if args:
                    final_cmd = final_cmd.replace("$1", args)
                md.append(f"!{final_cmd}")
        
        md.append("") # Empty line between phases

    if practices:
        md.append("## Best Practices")
        for practice in practices:
            md.append(f"- **{practice['practice']}**: {practice['description']}")

    # Add execution flags if any are enabled
    if execution_flags:
        active_flags = [k for k, v in execution_flags.items() if v]
        if active_flags:
            md.append("\n## ⚡ Execution Mode")
            md.append("")
            if execution_flags.get("fast"):
                md.append("> **FAST MODE**: Skip deep research. Prioritize speed over thoroughness.")
            if execution_flags.get("quick"):
                md.append("> **QUICK MODE**: Minimal phases. Implement directly without extensive planning.")
            if execution_flags.get("interactive"):
                md.append("> **INTERACTIVE MODE**: Pause and ask for confirmation after each phase.")
            if execution_flags.get("parallel"):
                md.append("> **PARALLEL MODE**: Run multiple agents/tasks in parallel where possible.")
            if execution_flags.get("no_test"):
                md.append("> **NO TEST**: Skip test execution. Use for documentation-only changes.")
            md.append("")

    return "\n".join(md)

def main():
    """Main entry point for CLI usage"""
    import argparse
    import shlex
    
    parser = argparse.ArgumentParser(description="ClaudeKit Workflow Query Engine")
    parser.add_argument("workflow", nargs="*", help="Name of the workflow (or 'workflow description')")
    parser.add_argument("--list", action="store_true", help="List available workflows")
    parser.add_argument("--format", choices=["json", "markdown"], default="json", help="Output format")
    parser.add_argument("--args", help="Arguments to inject into workflow (replaces $1)")
    
    # Execution control flags
    parser.add_argument("--fast", action="store_true", help="Skip deep research, prioritize speed")
    parser.add_argument("--quick", action="store_true", help="Quick mode for simple tasks, minimal phases")
    parser.add_argument("--interactive", action="store_true", help="Pause for confirmation after each phase")
    parser.add_argument("--parallel", action="store_true", help="Run multiple agents in parallel")
    parser.add_argument("--no-test", action="store_true", help="Skip test execution")
    
    args = parser.parse_args()
    
    if args.list:
        print(json.dumps(list_workflows(), indent=2))
        return

    if not args.workflow:
        parser.print_help()
        sys.exit(1)
    
    # Handle implicit args in workflow string (e.g. "plan my feature")
    # Join list into string first to handle split args
    full_workflow_input = " ".join(args.workflow)
    
    workflow_name = full_workflow_input
    workflow_args = args.args

    # Handle explicit prefixes removal early (both skt: and claudekit: for compatibility)
    if workflow_name.startswith("claudekit:"):
        workflow_name = workflow_name.replace("claudekit:", "", 1)
    elif workflow_name.startswith("skt:"):
        workflow_name = workflow_name.replace("skt:", "", 1)

    if " " in workflow_name and not workflow_args:
        try:
            parts = workflow_name.split(" ", 1)
            workflow_name = parts[0]
            workflow_args = parts[1] if len(parts) > 1 else ""
        except Exception:
            # Fallback if split fails
            pass

    # ✅ Security: Validate workflow name
    try:
        workflow_name = SecurityValidator.validate_skill_name(workflow_name)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Validate workflow exists
    if workflow_name not in load_workflows():
        # Maybe user meant to pass args via --args
         if args.args and args.workflow in load_workflows():
             workflow_name = args.workflow
         else:
             # Just proceed and let query_workflow return error json/msg
             pass

    result = query_workflow(workflow_name)
    
    if "error" in result:
        if args.format == "markdown":
            print(format_as_markdown(result, workflow_args), file=sys.stderr)
        else:
            print(json.dumps(result, indent=2), file=sys.stderr)
        sys.exit(1)


    # Collect execution flags
    execution_flags = {
        "fast": args.fast,
        "quick": args.quick,
        "interactive": args.interactive,
        "parallel": args.parallel,
        "no_test": getattr(args, 'no_test', False)
    }
    
    if args.format == "markdown":
        print(format_as_markdown(result, workflow_args, execution_flags))
    else:
        # Include flags in JSON output
        result["execution_flags"] = execution_flags
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
