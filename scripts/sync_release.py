#!/usr/bin/env python3
"""Validate an upstream release event and sync duplicated site release metadata."""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_REPOSITORY = "PharmaGenAI/open-pharma-plugins"
RELEASE_INDEX_PATH = "plugin-versions.json"
PAYLOAD_KEYS = (
    "repository",
    "capability",
    "tag",
    "commit",
    "distribution_version",
    "plugin_version",
)
SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")
COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")
TAG_PATTERN = re.compile(r"^open-pharma-plugins-[a-z0-9]+(?:-[a-z0-9]+)*-v\d+\.\d+\.\d+$")
RUN_ID_PATTERN = re.compile(r"^[0-9]+$")
CAPABILITY_DISPLAY = {
    "hcp-intelligence": "HCP Intelligence",
    "field-training": "Field Training",
    "campaign-studio": "Campaign Studio",
    "next-best-engagement": "Next-Best-Engagement",
    "territory-alignment": "Territory Alignment",
    "competitive-intelligence": "Competitive Intelligence",
}
HOMEPAGE_LABELS = {
    "HCP Intelligence": "HCP",
    "Competitive Intelligence": "CI",
    "Territory Alignment": "TA",
    "Next-Best-Engagement": "NBE",
    "Field Training": "FT",
    "Campaign Studio": "CS",
}
def api_get_json(url: str) -> dict:
    token = os.environ.get("GITHUB_API_TOKEN") or os.environ.get("GH_TOKEN")
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "open-pharma-pages-release-sync",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(
        url,
        headers=headers,
    )
    with urllib.request.urlopen(request) as response:
        return json.load(response)


def resolve_tag_to_commit(repository: str, tag: str) -> str:
    encoded_tag = urllib.parse.quote(tag, safe="")
    ref = api_get_json(f"https://api.github.com/repos/{repository}/git/ref/tags/{encoded_tag}")
    target = ref["object"]
    if target["type"] == "tag":
        target = api_get_json(f"https://api.github.com/repos/{repository}/git/tags/{target['sha']}")[
            "object"
        ]
    if target["type"] != "commit":
        raise ValueError(f"tag {tag!r} does not resolve to a commit")
    return target["sha"]


def fetch_release_index(repository: str, commit: str, path: str) -> dict:
    if path != RELEASE_INDEX_PATH:
        raise ValueError(f"release index path must be exactly {RELEASE_INDEX_PATH}")
    encoded_path = "/".join(urllib.parse.quote(part, safe="") for part in path.split("/"))
    payload = api_get_json(
        f"https://api.github.com/repos/{repository}/contents/{encoded_path}?ref={commit}"
    )
    content = base64.b64decode(payload["content"]).decode("utf-8")
    return json.loads(content)


def validate_payload_fields(payload: dict) -> list[str]:
    """Validate the payload before any field reaches a URL, shell, or GitHub output."""
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["payload must be a JSON object"]
    if set(payload) != set(PAYLOAD_KEYS):
        errors.append(f"payload keys must be exactly {list(PAYLOAD_KEYS)}")
        return errors

    non_strings = [key for key in PAYLOAD_KEYS if not isinstance(payload.get(key), str)]
    if non_strings:
        return [f"payload fields must be strings: {non_strings}"]

    if payload["repository"] != CANONICAL_REPOSITORY:
        errors.append("payload repository must be PharmaGenAI/open-pharma-plugins")
    if payload["capability"] not in CAPABILITY_DISPLAY:
        errors.append("payload capability must be a known safe slug")
    if not SEMVER_PATTERN.fullmatch(payload["distribution_version"]):
        errors.append("payload distribution_version must be semver")
    if not SEMVER_PATTERN.fullmatch(payload["plugin_version"]):
        errors.append("payload plugin_version must be semver")
    if not COMMIT_PATTERN.fullmatch(payload["commit"]):
        errors.append("payload commit must be a 40-character lowercase git SHA")
    if not TAG_PATTERN.fullmatch(payload["tag"]):
        errors.append("payload tag has an invalid format")

    return errors


def validate_payload(payload: dict, resolved_commit: str, release_index: dict) -> list[str]:
    errors = validate_payload_fields(payload)
    if errors:
        return errors

    expected_tag = f"open-pharma-plugins-{payload['capability']}-v{payload['plugin_version']}"
    if payload["tag"] != expected_tag:
        errors.append(f"payload tag must be {expected_tag!r}")
    if payload["commit"] != resolved_commit:
        errors.append("payload commit does not match the upstream tag commit")
    if release_index.get("distribution_version") != payload["distribution_version"]:
        errors.append("payload distribution_version does not match plugin-versions.json")
    if release_index.get("plugins", {}).get(payload["capability"]) != payload["plugin_version"]:
        errors.append("payload plugin_version does not match plugin-versions.json")
    if release_index.get("tag_format") != "open-pharma-plugins-{cap}-v{version}":
        errors.append("plugin-versions.json tag_format is unexpected")
    return errors


def build_release_snapshot(repository: str, commit: str, release_index: dict) -> dict:
    return {
        "canonical_repository": repository,
        "source_commit": commit,
        "distribution_version": release_index["distribution_version"],
        "capabilities": {
            CAPABILITY_DISPLAY[slug]: release_index["plugins"][slug]
            for slug in CAPABILITY_DISPLAY
        },
    }


def replace_required(text: str, pattern: str, replacement: str, description: str) -> str:
    updated, count = re.subn(pattern, replacement, text, flags=re.MULTILINE)
    if count == 0:
        raise ValueError(f"could not update {description}")
    return updated


def sync_site_release(root: Path, release: dict) -> list[str]:
    changed: list[str] = []
    source_commit = release["source_commit"]
    short_commit = source_commit[:7]
    distribution = release["distribution_version"]

    release_json_path = root / "docs/assets/data/release.json"
    release_json_text = json.dumps(release, indent=2) + "\n"
    if release_json_path.read_text(encoding="utf-8") != release_json_text:
        release_json_path.write_text(release_json_text, encoding="utf-8")
        changed.append(release_json_path.relative_to(root).as_posix())

    mkdocs_path = root / "mkdocs.yml"
    mkdocs_text = mkdocs_path.read_text(encoding="utf-8")
    mkdocs_text = replace_required(
        mkdocs_text,
        r'distribution: "[^"]+"',
        f'distribution: "{distribution}"',
        "mkdocs distribution version",
    )
    mkdocs_text = replace_required(
        mkdocs_text,
        r'source_commit: "[0-9a-f]{7,40}"',
        f'source_commit: "{source_commit}"',
        "mkdocs source commit",
    )
    for key, capability in (
        ("hcp_intelligence", "HCP Intelligence"),
        ("field_training", "Field Training"),
        ("campaign_studio", "Campaign Studio"),
        ("next_best_engagement", "Next-Best-Engagement"),
        ("territory_alignment", "Territory Alignment"),
        ("competitive_intelligence", "Competitive Intelligence"),
    ):
        mkdocs_text = replace_required(
            mkdocs_text,
            rf'{key}: "[^"]+"',
            f'{key}: "{release["capabilities"][capability]}"',
            f"mkdocs capability version for {capability}",
        )
    mkdocs_text = re.sub(
        rf"https://github.com/{re.escape(release['canonical_repository'])}/tree/[0-9a-f]{{7,40}}",
        f"https://github.com/{release['canonical_repository']}/tree/{source_commit}",
        mkdocs_text,
    )
    mkdocs_text = re.sub(
        r"https://pypi\.org/project/open-pharma-plugins/\d+\.\d+\.\d+/",
        f"https://pypi.org/project/open-pharma-plugins/{distribution}/",
        mkdocs_text,
    )
    if mkdocs_path.read_text(encoding="utf-8") != mkdocs_text:
        mkdocs_path.write_text(mkdocs_text, encoding="utf-8")
        changed.append(mkdocs_path.relative_to(root).as_posix())

    index_path = root / "docs/index.md"
    index_text = index_path.read_text(encoding="utf-8")
    index_text = replace_required(
        index_text,
        r"<strong>Public beta</strong> · Distribution [0-9]+\.[0-9]+\.[0-9]+ · "
        r"Pinned source <code>[0-9a-f]{7,40}</code>",
        f"<strong>Public beta</strong> · Distribution {distribution} · "
        f"Pinned source <code>{short_commit}</code>",
        "homepage release line",
    )
    index_text = replace_required(
        index_text,
        r'open-pharma-plugins\[hcp-intelligence\]==[0-9]+\.[0-9]+\.[0-9]+',
        f'open-pharma-plugins[hcp-intelligence]=={distribution}',
        "homepage quick-install distribution version",
    )
    for capability, label in HOMEPAGE_LABELS.items():
        version = release["capabilities"][capability]
        index_text = replace_required(
            index_text,
            rf"<span class=\"version-tag\">{re.escape(label)} [^<]+</span>",
            f'<span class="version-tag">{label} {version}</span>',
            f"homepage version tag for {capability}",
        )
    index_text = re.sub(
        rf"https://github.com/{re.escape(release['canonical_repository'])}/tree/[0-9a-f]{{7,40}}",
        f"https://github.com/{release['canonical_repository']}/tree/{source_commit}",
        index_text,
    )
    index_text = replace_required(
        index_text,
        r"records the full pinned source commit `[0-9a-f]{7,40}`; the visible short SHA `[0-9a-f]{7,40}`",
        f"records the full pinned source commit `{source_commit}`; the visible short SHA `{short_commit}`",
        "homepage source commit explanation",
    )
    if index_path.read_text(encoding="utf-8") != index_text:
        index_path.write_text(index_text, encoding="utf-8")
        changed.append(index_path.relative_to(root).as_posix())

    for slug, capability in CAPABILITY_DISPLAY.items():
        page_path = root / "docs/capabilities" / f"{slug}.md"
        page_text = page_path.read_text(encoding="utf-8")
        version = release["capabilities"][capability]
        page_text = replace_required(
            page_text,
            r"<strong>Capability [^<]+</strong>",
            f"<strong>Capability {version}</strong>",
            f"{slug} capability version",
        )
        page_text = replace_required(
            page_text,
            r"Distribution [^·]+ · source [0-9a-f]{7,40}",
            f"Distribution {distribution} · source {short_commit}",
            f"{slug} capability header release fields",
        )
        page_text = re.sub(
            rf"https://github.com/{re.escape(release['canonical_repository'])}/blob/[0-9a-f]{{7,40}}/",
            f"https://github.com/{release['canonical_repository']}/blob/{source_commit}/",
            page_text,
        )
        if page_path.read_text(encoding="utf-8") != page_text:
            page_path.write_text(page_text, encoding="utf-8")
            changed.append(page_path.relative_to(root).as_posix())

    for relative in (
        "docs/technical-reference.md",
        "docs/get-started.md",
        "docs/trust-governance.md",
        "docs/operations/release-sync.md",
    ):
        path = root / relative
        text = path.read_text(encoding="utf-8")
        text = re.sub(
            rf"https://github.com/{re.escape(release['canonical_repository'])}/(blob|tree)/[0-9a-f]{{7,40}}/",
            lambda match: f"https://github.com/{release['canonical_repository']}/{match.group(1)}/{source_commit}/",
            text,
        )
        text = re.sub(
            r"https://pypi\.org/project/open-pharma-plugins/\d+\.\d+\.\d+/",
            f"https://pypi.org/project/open-pharma-plugins/{distribution}/",
            text,
        )
        text = re.sub(
            r'open-pharma-plugins\[hcp-intelligence\]==\d+\.\d+\.\d+',
            f'open-pharma-plugins[hcp-intelligence]=={distribution}',
            text,
        )
        text = replace_required(
            text,
            r"Distribution [0-9]+\.[0-9]+\.[0-9]+ from source commit [0-9a-f]{7,40}",
            f"Distribution {distribution} from source commit {source_commit}",
            f"{relative} release panel",
        ) if relative == "docs/technical-reference.md" else text
        text = replace_required(
            text,
            r"visible short SHA `[0-9a-f]{7,40}` is derived",
            f"visible short SHA `{short_commit}` is derived",
            "technical reference short source commit",
        ) if relative == "docs/technical-reference.md" else text
        if path.read_text(encoding="utf-8") != text:
            path.write_text(text, encoding="utf-8")
            changed.append(relative)

    return changed


def build_branch_metadata(
    capability: str, tag: str, plugin_version: str, run_id: str
) -> tuple[str, str]:
    """Build shell-safe branch metadata only from validated release fields."""
    if capability not in CAPABILITY_DISPLAY:
        raise ValueError("capability must be a known safe slug")
    if not SEMVER_PATTERN.fullmatch(plugin_version):
        raise ValueError("plugin version must be semver")
    if tag != f"open-pharma-plugins-{capability}-v{plugin_version}":
        raise ValueError("tag must match capability and plugin version")
    if not RUN_ID_PATTERN.fullmatch(run_id):
        raise ValueError("run id must contain decimal digits only")
    safe_version = plugin_version.replace(".", "-")
    return (
        f"automation/release-sync-{capability}-{safe_version}-{run_id}",
        f"chore: sync site release for {tag}",
    )


def write_github_output(changed: list[str], payload: dict) -> None:
    output_path = os.environ.get("GITHUB_OUTPUT")
    if not output_path:
        return
    errors = validate_payload_fields(payload)
    if errors:
        raise ValueError("refusing to write GitHub outputs for an invalid payload")
    branch, title = build_branch_metadata(
        payload["capability"],
        payload["tag"],
        payload["plugin_version"],
        os.environ.get("GITHUB_RUN_ID", ""),
    )
    with open(output_path, "a", encoding="utf-8") as handle:
        handle.write(f"changed={'true' if changed else 'false'}\n")
        handle.write(f"branch={branch}\n")
        handle.write(f"title={title}\n")


def load_payload(args: argparse.Namespace) -> dict:
    if args.event_path:
        event = json.loads(Path(args.event_path).read_text(encoding="utf-8"))
        return event["client_payload"]
    return {
        "repository": CANONICAL_REPOSITORY,
        "capability": args.capability,
        "tag": args.tag,
        "commit": args.commit,
        "distribution_version": args.distribution_version,
        "plugin_version": args.plugin_version,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--event-path")
    parser.add_argument("--capability")
    parser.add_argument("--tag")
    parser.add_argument("--commit")
    parser.add_argument("--distribution-version")
    parser.add_argument("--plugin-version")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = load_payload(args)
    errors = validate_payload_fields(payload)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    resolved_commit = resolve_tag_to_commit(payload["repository"], payload["tag"])
    release_index = fetch_release_index(payload["repository"], payload["commit"], RELEASE_INDEX_PATH)
    errors = validate_payload(payload, resolved_commit, release_index)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    release = build_release_snapshot(payload["repository"], payload["commit"], release_index)
    changed = sync_site_release(ROOT, release)
    write_github_output(changed, payload)
    print(
        json.dumps(
            {
                "changed": bool(changed),
                "source_commit": release["source_commit"],
                "distribution_version": release["distribution_version"],
                "changed_files": changed,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
