#!/usr/bin/env python3
"""
DX Metrics - Universal Developer Experience Metrics System

This module provides the core infrastructure for collecting, tagging, and storing
DX metrics across all SKT workflows using a "Google Tag" style event system.

Usage:
    from dx_metrics import log_event, track_dx

    # Direct logging
    log_event("workflow_query", {"workflow": "cook"}, tags=["pillar:transparency"])

    # Decorator usage
    @track_dx(event_name="workflow_execution", pillar="efficiency")
    def my_function():
        ...
"""

import json
import os
import time
import subprocess
from datetime import datetime, timezone
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional
from abc import ABC, abstractmethod

# ============================================================================
# Configuration
# ============================================================================

METRICS_DIR = ".skt/metrics"
EVENTS_FILE = "events.jsonl"
SCHEMA_VERSION = "1.0"

# ============================================================================
# Exporters (Adapter Pattern)
# ============================================================================

class DXExporter(ABC):
    """Abstract base class for DX event exporters."""

    @abstractmethod
    def export(self, event: Dict[str, Any]) -> bool:
        """Export an event. Returns True on success."""
        pass


class LocalFileExporter(DXExporter):
    """Exports events to local JSONL file."""

    def __init__(self, root_dir: Optional[Path] = None):
        self.root_dir = root_dir or self._find_project_root()
        self.metrics_dir = self.root_dir / METRICS_DIR
        self.events_file = self.metrics_dir / EVENTS_FILE

    def _find_project_root(self) -> Path:
        """Find project root by looking for .skt or .git directory."""
        cwd = Path.cwd()
        for parent in [cwd] + list(cwd.parents)[:5]:
            if (parent / ".skt").exists() or (parent / ".git").exists():
                return parent
        return cwd

    def _ensure_dir(self) -> None:
        """Ensure metrics directory exists."""
        self.metrics_dir.mkdir(parents=True, exist_ok=True)

    def export(self, event: Dict[str, Any]) -> bool:
        """Append event to JSONL file."""
        try:
            self._ensure_dir()
            with open(self.events_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(event, ensure_ascii=False) + "\n")
            return True
        except Exception as e:
            print(f"[dx_metrics] Export error: {e}")
            return False


class SupabaseExporter(DXExporter):
    """Export events to Supabase via REST API."""

    def __init__(self, url: str, anon_key: str):
        self.url = url.rstrip("/")
        self.anon_key = anon_key
        self.endpoint = f"{self.url}/rest/v1/skt_events"
        self.headers = {
            "apikey": self.anon_key,
            "Authorization": f"Bearer {self.anon_key}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }

    def export(self, event: Dict[str, Any]) -> bool:
        """Export event to Supabase."""
        try:
            import urllib.request
            import urllib.error

            data = json.dumps(event).encode("utf-8")
            req = urllib.request.Request(
                self.endpoint,
                data=data,
                headers=self.headers,
                method="POST"
            )
            
            with urllib.request.urlopen(req, timeout=5) as response:
                return response.status in (200, 201, 204)
                
        except Exception as e:
            # Silently fail for metrics to avoid disrupting workflow
            # But print for debug if needed
            if os.environ.get("SKT_DEBUG"):
                print(f"[dx_metrics] Supabase export error: {e}")
            return False


class MultiExporter(DXExporter):
    """Chain multiple exporters."""

    def __init__(self, exporters: List[DXExporter]):
        self.exporters = exporters

    def export(self, event: Dict[str, Any]) -> bool:
        results = [e.export(event) for e in self.exporters]
        return any(results)


# ============================================================================
# Global Context
# ============================================================================

def _get_git_commit() -> Optional[str]:
    """Get current git commit hash."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return None


def _get_track_id() -> Optional[str]:
    """Get active track ID from ACTIVE_PLAN.md or .skt/tracks/."""
    try:
        cwd = Path.cwd()
        # Check for active plan beacon
        beacon = cwd / "ACTIVE_PLAN.md"
        if beacon.exists():
            content = beacon.read_text()
            for line in content.split("\n"):
                if "tracks/" in line:
                    # Extract track name from path
                    start = line.find("tracks/") + 7
                    end = line.find("/", start) if "/" in line[start:] else len(line)
                    return line[start:end].strip("`/")
    except Exception:
        pass
    return None


def _get_global_context() -> Dict[str, Any]:
    """Build global context for all events."""
    return {
        "schema_version": SCHEMA_VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "git_commit": _get_git_commit(),
        "track_id": _get_track_id(),
        "shell": os.environ.get("SHELL", "unknown"),
        "cwd": str(Path.cwd())
    }


# ============================================================================
# Event Logging
# ============================================================================

# Default exporter
_default_exporter: Optional[DXExporter] = None


def get_exporter() -> DXExporter:
    """Get or create the default exporter."""
    global _default_exporter
    if _default_exporter is None:
        local_exporter = LocalFileExporter()
        
        # Check for Supabase config
        sb_url = os.environ.get("NEXT_PUBLIC_SUPABASE_URL")
        sb_key = os.environ.get("NEXT_PUBLIC_SUPABASE_ANON_KEY")
        
        if sb_url and sb_key:
            remote_exporter = SupabaseExporter(sb_url, sb_key)
            # Use both: ensure local backup + remote
            _default_exporter = MultiExporter([local_exporter, remote_exporter])
        else:
            _default_exporter = local_exporter
            
    return _default_exporter


def normalize_tags(tags: List[str]) -> List[str]:
    """Normalize and deduplicate tags."""
    normalized = []
    seen = set()
    for tag in tags:
        tag = tag.lower().strip()
        if tag and tag not in seen:
            normalized.append(tag)
            seen.add(tag)
    return normalized


def log_event(
    event_name: str,
    data: Optional[Dict[str, Any]] = None,
    tags: Optional[List[str]] = None
) -> bool:
    """
    Log a DX event.

    Args:
        event_name: Name of the event (e.g., "workflow_query", "agent_call")
        data: Event-specific data
        tags: List of tags (e.g., ["pillar:reliability", "severity:warning"])

    Returns:
        True if event was logged successfully
    """
    event = {
        **_get_global_context(),
        "event": event_name,
        "tags": normalize_tags(tags or []),
        "data": data or {}
    }

    return get_exporter().export(event)


# ============================================================================
# Decorator
# ============================================================================

def track_dx(
    event_name: str = "function_call",
    pillar: Optional[str] = None,
    domain: Optional[str] = None,
    extra_tags: Optional[List[str]] = None
) -> Callable:
    """
    Decorator to track function execution with DX metrics.

    Args:
        event_name: Name of the event to log
        pillar: DX pillar (reliability, efficiency, cost, evolution, transparency)
        domain: Domain tag (dx, arch, infra, logic, ui-ux)
        extra_tags: Additional tags

    Example:
        @track_dx(event_name="workflow_query", pillar="transparency")
        def query_workflow(name: str):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            tags = list(extra_tags or [])

            if pillar:
                tags.append(f"pillar:{pillar}")
            if domain:
                tags.append(f"domain:{domain}")

            tags.append(f"function:{func.__name__}")

            try:
                result = func(*args, **kwargs)
                duration = time.perf_counter() - start_time

                # Auto-tag slow functions
                if duration > 5.0:
                    tags.append("severity:bottleneck")
                elif duration > 2.0:
                    tags.append("severity:warning")

                log_event(event_name, {
                    "function": func.__name__,
                    "duration_ms": round(duration * 1000, 2),
                    "status": "success"
                }, tags=tags)

                return result

            except Exception as e:
                duration = time.perf_counter() - start_time
                tags.append("severity:critical")
                tags.append("status:failure")

                log_event(event_name, {
                    "function": func.__name__,
                    "duration_ms": round(duration * 1000, 2),
                    "status": "failure",
                    "error": str(e),
                    "error_type": type(e).__name__
                }, tags=tags)

                raise

        return wrapper
    return decorator


# ============================================================================
# CLI Interface
# ============================================================================

def _test_metrics():
    """Run basic self-test."""
    print("🧪 DX Metrics Self-Test")
    print("-" * 40)

    # Test 1: Direct logging
    print("1. Testing log_event()...")
    success = log_event("test_event", {"test_key": "test_value"}, tags=["test", "pillar:reliability"])
    print(f"   Result: {'✅ OK' if success else '❌ FAILED'}")

    # Test 2: Decorator
    print("2. Testing @track_dx decorator...")

    @track_dx(event_name="test_decorated", pillar="efficiency")
    def sample_function():
        time.sleep(0.1)
        return "done"

    result = sample_function()
    print(f"   Result: {'✅ OK' if result == 'done' else '❌ FAILED'}")

    # Test 3: Check file
    print("3. Checking events file...")
    exporter = get_exporter()
    if isinstance(exporter, LocalFileExporter):
        if exporter.events_file.exists():
            lines = exporter.events_file.read_text().strip().split("\n")
            print(f"   Events logged: {len(lines)}")
            print(f"   File: {exporter.events_file}")
            print("   ✅ OK")
        else:
            print("   ❌ File not created")

    print("-" * 40)
    print("✅ Self-test complete!")


def main():
    """CLI entry point."""
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            _test_metrics()
        elif sys.argv[1] == "--help":
            print(__doc__)
        else:
            print(f"Unknown option: {sys.argv[1]}")
            print("Usage: python3 dx_metrics.py [--test|--help]")
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
