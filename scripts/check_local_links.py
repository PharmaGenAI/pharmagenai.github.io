#!/usr/bin/env python3
"""Validate local documentation links in source Markdown and built HTML artifacts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "tel:", "javascript:", "data:")
LINK_PATTERN = re.compile(r'href="([^"]+)"|\[[^\]]+\]\(([^)]+)\)')


def link_targets(text: str) -> set[str]:
    targets: set[str] = set()
    for html_target, markdown_target in LINK_PATTERN.findall(text):
        target = (html_target or markdown_target).strip()
        if target:
            targets.add(target)
    return targets


def normalize_source_target(base: Path, target: str) -> Path | None:
    if not target or target.startswith(EXTERNAL_PREFIXES) or target.startswith("#"):
        return None
    path_text = target.split("#", 1)[0]
    candidate = (base / path_text).resolve()
    if path_text.endswith("/"):
        directory_index = (candidate / "index.md").resolve()
        if directory_index.exists():
            return directory_index
        # Raw HTML links use MkDocs' clean output URLs. A source page such as
        # capabilities/hcp-intelligence.md is rendered at
        # capabilities/hcp-intelligence/, so accept that source equivalent.
        return candidate.with_suffix(".md")
    return candidate


def check_source_links() -> list[str]:
    errors: list[str] = []
    for page in sorted(DOCS.rglob("*.md")):
        text = page.read_text(encoding="utf-8")
        for target in link_targets(text):
            candidate = normalize_source_target(page.parent, target)
            if candidate is None:
                continue
            if not candidate.exists():
                errors.append(
                    f"{page.relative_to(ROOT)}: broken local source link {target!r}"
                )
    return errors


class SiteParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.targets: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        identifier = data.get("id")
        if identifier:
            self.ids.add(identifier)
        for key in ("href", "src"):
            target = data.get(key)
            if target:
                self.targets.append(target)


def normalize_site_target(base_file: Path, site_dir: Path, target: str) -> tuple[Path, str | None] | None:
    if not target or target.startswith(EXTERNAL_PREFIXES):
        return None
    path_text, _, fragment = target.partition("#")
    if target.startswith("#"):
        return base_file, fragment
    if path_text.startswith("/"):
        candidate = site_dir / path_text.lstrip("/")
    else:
        candidate = (base_file.parent / path_text).resolve()
    if not path_text or path_text.endswith("/"):
        candidate = (candidate / "index.html").resolve()
    elif candidate.suffix == "":
        candidate = (candidate / "index.html").resolve()
    return candidate, fragment or None


def check_built_site(site_dir: Path) -> list[str]:
    errors: list[str] = []
    html_ids: dict[Path, set[str]] = {}
    html_targets: dict[Path, list[str]] = {}
    for page in sorted(site_dir.rglob("*.html")):
        parser = SiteParser()
        parser.feed(page.read_text(encoding="utf-8"))
        html_ids[page.resolve()] = parser.ids
        html_targets[page.resolve()] = parser.targets

    for page, targets in html_targets.items():
        for target in targets:
            resolved = normalize_site_target(page, site_dir.resolve(), target)
            if resolved is None:
                continue
            candidate, fragment = resolved
            if not candidate.exists():
                errors.append(
                    f"{page.relative_to(ROOT)}: broken built-site link {target!r}"
                )
                continue
            if fragment and candidate.suffix == ".html":
                if fragment not in html_ids.get(candidate.resolve(), set()):
                    errors.append(
                        f"{page.relative_to(ROOT)}: missing built-site anchor {target!r}"
                    )

    release_snapshot = site_dir / "assets/data/release.json"
    if not release_snapshot.is_file():
        errors.append("site/assets/data/release.json is missing from the built site")
    else:
        try:
            json.loads(release_snapshot.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"site/assets/data/release.json is invalid JSON: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site-dir", type=Path, help="Built MkDocs output directory")
    args = parser.parse_args()

    errors = check_source_links()
    if args.site_dir:
        errors.extend(check_built_site((ROOT / args.site_dir).resolve()))

    if errors:
        print(
            f"Local-link and artifact validation failed with {len(errors)} error(s):",
            file=sys.stderr,
        )
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Local-link and artifact validation passed for Markdown sources and built site artifacts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
