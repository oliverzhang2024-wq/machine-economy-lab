#!/usr/bin/env python3
"""Summarize local Codex experiment runs without uploading private traces."""
from __future__ import annotations
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "runs"

def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}

def error_events(path):
    if not path.exists():
        return []
    matches = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if event.get("type") in ("error", "turn.failed"):
            value = event.get("message") or event.get("error") or event.get("type")
            if isinstance(value, dict):
                value = value.get("message") or str(value)
            matches.append(str(value))
    return matches[-2:]

def scrub(value):
    # Review summaries before copying; this is not a comprehensive secret scanner.
    value = re.sub(r"(sk-[A-Za-z0-9_-]{8,}|github_pat_[A-Za-z0-9_]{8,}|gh[pousr]_[A-Za-z0-9_]{8,})", "[REDACTED]", str(value))
    return value[:700]

def main():
    if not RUNS.exists():
        print("No local runs/ folder was found. Check the correct Codespace.")
        return
    dirs = sorted(p for p in RUNS.iterdir() if p.is_dir())
    if not dirs:
        print("No experiment runs in runs/.")
        return
    for p in dirs:
        meta = read_json(p / "metadata.json")
        result = read_json(p / "result.json")
        status = result.get("run_status") or meta.get("status") or "unknown"
        tokens = result.get("input_tokens")
        test_passed = result.get("tests_passed")
        solution = p / "workspace" / "solution.py"
        original_stub = solution.exists() and "raise NotImplementedError" in solution.read_text(encoding="utf-8", errors="replace")
        if status.startswith("agent_failed_exit_") or status == "agent_timeout":
            category = "EXECUTION ERROR (not a coding result)"
        elif test_passed is True:
            category = "PASSED"
        elif test_passed is False:
            category = "GRADER FAILURE (investigate solution)"
        else:
            category = "NO GRADE"
        print(f"\n=== {p.name} | {meta.get('task_id',result.get('task_id','?'))} ===")
        print(f"category={category}; run_status={status}; input_tokens={tokens}; solution_has_stub={original_stub}")
        print(f"elapsed_seconds={result.get('wall_seconds') or meta.get('wall_seconds')}; model={result.get('model_name') or meta.get('model_name')}")
        stderr = p / "codex_stderr.txt"
        if stderr.exists():
            messages = [line.strip() for line in stderr.read_text(encoding="utf-8",errors="replace").splitlines() if line.strip()]
            if messages:
                print("stderr_tail: " + scrub(" | ".join(messages[-3:])))
        for ev in error_events(p / "codex_events.jsonl"):
            print("codex_error_event: " + scrub(ev))
        if category == "GRADER FAILURE (investigate solution)":
            grade = p / "grader_output.txt"
            if grade.exists():
                lines = [line.strip() for line in grade.read_text(encoding="utf-8",errors="replace").splitlines() if line.strip()]
                print("grader_tail: " + scrub(" | ".join(lines[-5:])))
    print("\nReview this diagnostic summary for sensitive content before sharing. Do not share auth.json or raw Codex traces.")

if __name__ == "__main__":
    main()
