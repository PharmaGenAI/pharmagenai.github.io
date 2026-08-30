#!/usr/bin/env python3
"""Validate the site's GitHub Actions workflows."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github/workflows"
PINNED_ACTIONS = {
    "actions/checkout": "3d3c42e5aac5ba805825da76410c181273ba90b1",
    "actions/setup-python": "5fda3b95a4ea91299a34e894583c3862153e4b97",
    "actions/configure-pages": "45bfe0192ca1faeb007ade9deae92b16b8254a0d",
    "actions/upload-pages-artifact": "fc324d3547104276b827a68afc52ff2a11cc49c9",
    "actions/deploy-pages": "cd2ce8fcbc39b97be8ca5fce6e763baed58fa128",
}
REQUIRED_WORKFLOWS = ("ci.yml", "pages.yml", "release-sync.yml")
PINNED_USE_PATTERN = re.compile(r"^[^@]+@[0-9a-f]{40}$")


def load_workflows() -> dict[str, dict]:
    data: dict[str, dict] = {}
    for path in sorted(WORKFLOWS.glob("*.yml")):
        parsed = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(parsed, dict) and True in parsed and "on" not in parsed:
            parsed["on"] = parsed.pop(True)
        data[path.name] = parsed
    return data


def workflow_uses(workflow: dict) -> list[str]:
    uses: list[str] = []
    for job in workflow.get("jobs", {}).values():
        for step in job.get("steps", []):
            use = step.get("uses")
            if use:
                uses.append(use)
    return uses


def job_runs(workflow: dict) -> str:
    commands: list[str] = []
    for job in workflow.get("jobs", {}).values():
        for step in job.get("steps", []):
            run = step.get("run")
            if run:
                commands.append(run)
    return "\n".join(commands)


def direct_run_expression_errors(name: str, workflow: dict) -> list[str]:
    """Reject GitHub expression interpolation inside shell programs."""
    errors: list[str] = []
    for job_name, job in workflow.get("jobs", {}).items():
        for index, step in enumerate(job.get("steps", []), start=1):
            run = step.get("run")
            if isinstance(run, str) and "${{" in run:
                errors.append(
                    f"{name}: job {job_name} step {index} contains a direct GitHub expression in shell run"
                )
    return errors


def event_keys(workflow: dict) -> set[str]:
    trigger = workflow.get("on", {})
    if isinstance(trigger, str):
        return {trigger}
    if isinstance(trigger, list):
        return set(trigger)
    return set(trigger)


def workflow_contract_errors(workflows: dict[str, dict]) -> list[str]:
    errors: list[str] = []

    if sorted(workflows) != sorted(REQUIRED_WORKFLOWS):
        errors.append(f"workflow set must be exactly {list(REQUIRED_WORKFLOWS)}")
        return errors

    for name, workflow in workflows.items():
        if not isinstance(workflow, dict):
            errors.append(f"{name}: workflow must parse as a mapping")
            continue
        for use in workflow_uses(workflow):
            if use.startswith("./"):
                continue
            if not PINNED_USE_PATTERN.fullmatch(use):
                errors.append(f"{name}: action must be pinned to a 40-character SHA: {use}")
                continue
            action, sha = use.split("@", 1)
            expected = PINNED_ACTIONS.get(action)
            if expected and sha != expected:
                errors.append(f"{name}: {action} must be pinned to {expected}")
        errors.extend(direct_run_expression_errors(name, workflow))

    ci = workflows.get("ci.yml", {})
    if event_keys(ci) != {"pull_request", "push"}:
        errors.append("ci.yml must trigger on push and pull_request")
    if ci.get("permissions") != {"contents": "read"}:
        errors.append("ci.yml must use top-level contents: read permissions")
    ci_commands = job_runs(ci)
    for needle in (
        "python -m unittest discover -s tests",
        "python scripts/check_content.py",
        "mkdocs build --strict",
        "python scripts/check_local_links.py --site-dir site",
        "python scripts/check_workflows.py",
    ):
        if needle not in ci_commands:
            errors.append(f"ci.yml must run {needle!r}")

    pages = workflows.get("pages.yml", {})
    page_events = pages.get("on", {})
    if "push" not in event_keys(pages) or "workflow_dispatch" not in event_keys(pages):
        errors.append("pages.yml must trigger on push and workflow_dispatch")
    push = page_events.get("push", {}) if isinstance(page_events, dict) else {}
    if push.get("branches") != ["main"]:
        errors.append("pages.yml push trigger must target main only")
    if pages.get("permissions") != {
        "contents": "read",
        "pages": "write",
        "id-token": "write",
    }:
        errors.append("pages.yml must use contents:read, pages:write, and id-token:write")
    if pages.get("concurrency", {}).get("group") != "pages":
        errors.append("pages.yml must declare pages concurrency")
    deploy_job = pages.get("jobs", {}).get("deploy", {})
    if deploy_job.get("environment", {}).get("name") != "github-pages":
        errors.append("pages.yml deploy job must use the github-pages environment")
    if "actions/configure-pages@" not in "\n".join(workflow_uses(pages)):
        errors.append("pages.yml must use actions/configure-pages")

    release_sync = workflows.get("release-sync.yml", {})
    if "repository_dispatch" not in event_keys(release_sync) or "workflow_dispatch" not in event_keys(release_sync):
        errors.append("release-sync.yml must trigger on repository_dispatch and workflow_dispatch")
    repository_dispatch = release_sync.get("on", {}).get("repository_dispatch", {})
    if repository_dispatch.get("types") != ["open-pharma-plugins-release"]:
        errors.append("release-sync.yml repository_dispatch type must be open-pharma-plugins-release")
    if release_sync.get("permissions") != {"contents": "write", "pull-requests": "write"}:
        errors.append("release-sync.yml must use contents:write and pull-requests:write only")
    sync_commands = job_runs(release_sync)
    for needle in (
        "python scripts/sync_release.py",
        "python scripts/check_content.py",
        "python scripts/check_workflows.py",
        "python scripts/check_local_links.py --site-dir site",
        "gh pr create",
    ):
        if needle not in sync_commands:
            errors.append(f"release-sync.yml must run {needle!r}")
    dispatch_text = job_runs(release_sync)
    if (
        "release_index_path" in str(release_sync)
        or "inputs.release_index_path" in str(release_sync)
        or "--release-index-path" in dispatch_text
    ):
        errors.append("release-sync.yml must not expose a release_index_path override")
    if "create-pull-request" in sync_commands:
        errors.append("release-sync.yml must not use a third-party PR action")

    return errors


def main() -> int:
    workflows = load_workflows()
    errors = workflow_contract_errors(workflows)
    if errors:
        print(f"Workflow validation failed with {len(errors)} error(s):", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Workflow validation passed for CI, Pages deploy, and release sync.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
