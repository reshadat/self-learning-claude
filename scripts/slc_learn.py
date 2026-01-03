#!/usr/bin/env python3
"""
SLC: Self-Learning Claude

A framework for building self-improving LLM systems through evolving context playbooks.
This script is called automatically by Claude Code at key workflow points.

Usage:
    # At task start - loads patterns into stdout
    python3 slc_learn.py load [--endpoint "POST /api/example"]

    # After success - records what worked
    python3 slc_learn.py success --helpful P-abc123,S-def456 --lesson "New insight" --category strategy

    # After failure - records what went wrong
    python3 slc_learn.py failure --harmful P-xyz789 --lesson "What failed" --endpoint "POST /api/x"

    # Initialize with seed patterns (run once)
    python3 slc_learn.py seed

    # Show stats
    python3 slc_learn.py stats
"""

import argparse
import json
import hashlib
import sys
from pathlib import Path
from datetime import datetime

# Playbook storage - local to current project directory
# Creates .playbook/slc-playbook.json in whatever directory Claude is working from
PLAYBOOKS_DIR = Path.cwd() / ".playbook"
PLAYBOOK_PATH = PLAYBOOKS_DIR / "slc-playbook.json"


def load_playbook():
    if PLAYBOOK_PATH.exists():
        return json.loads(PLAYBOOK_PATH.read_text())
    return {"metadata": {"created": datetime.now().isoformat()}, "bullets": []}


def save_playbook(data):
    PLAYBOOKS_DIR.mkdir(parents=True, exist_ok=True)
    PLAYBOOK_PATH.write_text(json.dumps(data, indent=2))


def make_id(category, content):
    prefix = category[0].upper()
    hash_val = hashlib.md5(content.encode()).hexdigest()[:6]
    return f"{prefix}-{hash_val}"


def cmd_load(args):
    """Load and display relevant patterns for current task."""
    # Auto-seed if playbook doesn't exist
    if not PLAYBOOK_PATH.exists():
        print("[*] First run - initializing playbook with seed patterns...\n")
        cmd_seed(argparse.Namespace(force=False))

    data = load_playbook()
    bullets = data.get("bullets", [])

    if not bullets:
        return

    # Sort by score
    bullets = sorted(bullets, key=lambda b: b.get("helpful_count", 0) - b.get("harmful_count", 0), reverse=True)

    # Filter for endpoint if specified
    if args.endpoint:
        endpoint_lower = args.endpoint.lower()
        relevant = [b for b in bullets if
                    (b.get("source_endpoint") and endpoint_lower in b.get("source_endpoint", "").lower()) or
                    b.get("helpful_count", 0) - b.get("harmful_count", 0) >= 2 or
                    b.get("category") in ("domain", "code")]
        bullets = relevant if relevant else bullets

    # Group and display
    by_cat = {}
    for b in bullets[:25]:  # Limit total
        by_cat.setdefault(b["category"], []).append(b)

    print("## Learned Patterns\n")
    for cat in ["pitfall", "strategy", "domain", "endpoint", "code"]:
        if cat not in by_cat:
            continue
        print(f"### {cat.title()}")
        for b in by_cat[cat][:5]:
            h, m = b.get("helpful_count", 0), b.get("harmful_count", 0)
            print(f"- **[{b['id']}]** (+{h}/-{m}) {b['content']}")
        print()


def cmd_success(args):
    """Record successful task completion."""
    data = load_playbook()

    # Mark helpful
    if args.helpful:
        for bid in args.helpful.split(","):
            bid = bid.strip()
            for b in data["bullets"]:
                if b["id"] == bid:
                    b["helpful_count"] = b.get("helpful_count", 0) + 1
                    b["last_used"] = datetime.now().isoformat()

    # Add new lesson
    if args.lesson:
        new_id = make_id(args.category, args.lesson)
        # Check duplicate
        if not any(args.lesson.lower() in b["content"].lower() for b in data["bullets"]):
            data["bullets"].append({
                "id": new_id,
                "content": args.lesson,
                "category": args.category,
                "helpful_count": 1,  # Start with 1 since it just worked
                "harmful_count": 0,
                "source_endpoint": args.endpoint,
                "created": datetime.now().isoformat()
            })
            print(f"[+] Learned: [{new_id}] {args.lesson[:60]}...")

    data["metadata"]["last_success"] = datetime.now().isoformat()
    data["metadata"]["total_successes"] = data["metadata"].get("total_successes", 0) + 1
    save_playbook(data)


def cmd_failure(args):
    """Record failed task for learning."""
    data = load_playbook()

    # Mark harmful
    if args.harmful:
        for bid in args.harmful.split(","):
            bid = bid.strip()
            for b in data["bullets"]:
                if b["id"] == bid:
                    b["harmful_count"] = b.get("harmful_count", 0) + 1

    # Add pitfall lesson
    if args.lesson:
        content = f"AVOID: {args.lesson}" if not args.lesson.startswith("AVOID") else args.lesson
        new_id = make_id("pitfall", content)
        if not any(args.lesson.lower() in b["content"].lower() for b in data["bullets"]):
            data["bullets"].append({
                "id": new_id,
                "content": content,
                "category": "pitfall",
                "helpful_count": 0,
                "harmful_count": 0,
                "source_endpoint": args.endpoint,
                "created": datetime.now().isoformat()
            })
            print(f"[!] Pitfall recorded: [{new_id}] {content[:60]}...")

    data["metadata"]["last_failure"] = datetime.now().isoformat()
    data["metadata"]["total_failures"] = data["metadata"].get("total_failures", 0) + 1
    save_playbook(data)


def cmd_seed(args):
    """Initialize playbook with starter patterns."""
    if PLAYBOOK_PATH.exists() and not args.force:
        print(f"Playbook exists at {PLAYBOOK_PATH}. Use --force to overwrite.")
        return

    # Generic starter patterns - customize for your project
    patterns = [
        ("pitfall", "Don't use mutable default arguments in Python (e.g., def foo(items=[]))"),
        ("pitfall", "Always validate input at API boundaries before processing"),
        ("pitfall", "Check for null/undefined before accessing nested object properties"),
        ("strategy", "Write tests before fixing bugs to prevent regression"),
        ("strategy", "Use environment variables for configuration, not hardcoded values"),
        ("strategy", "Log errors with context (request ID, user ID, operation) for debugging"),
        ("code", "Use try/finally or context managers to ensure resource cleanup"),
        ("code", "Prefer explicit imports over wildcard imports for clarity"),
    ]

    bullets = []
    for cat, content in patterns:
        bullets.append({
            "id": make_id(cat, content),
            "content": content,
            "category": cat,
            "helpful_count": 0,
            "harmful_count": 0,
            "created": datetime.now().isoformat()
        })

    data = {
        "metadata": {"created": datetime.now().isoformat(), "seeded": True},
        "bullets": bullets
    }
    save_playbook(data)
    print(f"[+] Seeded {len(bullets)} patterns -> {PLAYBOOK_PATH}")


def cmd_stats(args):
    """Show playbook statistics."""
    data = load_playbook()
    bullets = data.get("bullets", [])

    if not bullets:
        print("No patterns learned yet.")
        return

    by_cat = {}
    for b in bullets:
        by_cat.setdefault(b["category"], []).append(b)

    total_helpful = sum(b.get("helpful_count", 0) for b in bullets)
    total_harmful = sum(b.get("harmful_count", 0) for b in bullets)

    print(f"[i] Playbook: {len(bullets)} patterns")
    print(f"   Categories: {', '.join(f'{k}({len(v)})' for k, v in by_cat.items())}")
    print(f"   Feedback: +{total_helpful}/-{total_harmful}")
    print(f"   Tasks: {data['metadata'].get('total_successes', 0)} success, {data['metadata'].get('total_failures', 0)} failures")

    # Top performers
    top = sorted(bullets, key=lambda b: b.get("helpful_count", 0) - b.get("harmful_count", 0), reverse=True)[:3]
    if top:
        print(f"\n[*] Top patterns:")
        for b in top:
            score = b.get("helpful_count", 0) - b.get("harmful_count", 0)
            print(f"   [{b['id']}] score={score}: {b['content'][:50]}...")


def main():
    parser = argparse.ArgumentParser(description="SLC: Self-Learning Claude")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # load
    p = sub.add_parser("load", help="Load patterns for current task")
    p.add_argument("--endpoint", "-e", help="Filter for specific endpoint")

    # success
    p = sub.add_parser("success", help="Record successful completion")
    p.add_argument("--helpful", help="Comma-separated helpful bullet IDs")
    p.add_argument("--lesson", help="New pattern learned")
    p.add_argument("--category", default="strategy", choices=["strategy", "pitfall", "domain", "endpoint", "code"])
    p.add_argument("--endpoint", "-e", help="Source endpoint")

    # failure
    p = sub.add_parser("failure", help="Record failure for learning")
    p.add_argument("--harmful", help="Comma-separated harmful bullet IDs")
    p.add_argument("--lesson", help="What went wrong")
    p.add_argument("--endpoint", "-e", help="Source endpoint")

    # seed
    p = sub.add_parser("seed", help="Initialize with starter patterns")
    p.add_argument("--force", action="store_true", help="Overwrite existing")

    # stats
    sub.add_parser("stats", help="Show playbook statistics")

    args = parser.parse_args()

    if args.cmd == "load":
        cmd_load(args)
    elif args.cmd == "success":
        cmd_success(args)
    elif args.cmd == "failure":
        cmd_failure(args)
    elif args.cmd == "seed":
        cmd_seed(args)
    elif args.cmd == "stats":
        cmd_stats(args)


if __name__ == "__main__":
    main()
