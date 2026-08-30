#!/usr/bin/env python3
"""Validate the business-site foundation without network access."""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

CANONICAL_REPOSITORY = "PharmaGenAI/open-pharma-plugins"
PUBLIC_SITE_REPOSITORY = "PharmaGenAI/pharmagenai.github.io"
PUBLIC_SITE_REPOSITORY_URL = f"https://github.com/{PUBLIC_SITE_REPOSITORY}"
RELEASE_CAPABILITY_ORDER = (
    "HCP Intelligence",
    "Field Training",
    "Campaign Studio",
    "Next-Best-Engagement",
    "Territory Alignment",
    "Competitive Intelligence",
)

CAPABILITY_SLUGS = {
    "hcp-intelligence": "HCP Intelligence",
    "competitive-intelligence": "Competitive Intelligence",
    "territory-alignment": "Territory Alignment",
    "next-best-engagement": "Next-Best-Engagement",
    "field-training": "Field Training",
    "campaign-studio": "Campaign Studio",
}

CAPABILITY_SECTIONS = (
    "## The problem",
    "## Objective",
    "## How it helps",
    "## How the plugin works",
    "## A three-step workflow",
    "## Sample input",
    "## Interpreted sample output",
    "## Business value indicators",
    "## Boundaries and human review",
    "## Get started",
)

MANIFEST_KEYS = (
    "capability_slug",
    "capability_version",
    "distribution_version",
    "source_commit",
    "fictional_data",
    "status",
    "input_path",
    "output_path",
    "notes",
)

MANIFEST_STATUS_BY_SLUG = {
    "hcp-intelligence": "validated-representative",
    "competitive-intelligence": "validated-representative",
    "territory-alignment": "validated-representative",
    "next-best-engagement": "generated-from-pinned-fixture",
    "field-training": "validated-representative",
    "campaign-studio": "validated-representative",
}
LINK_PATTERN = re.compile(r'href="([^"]+)"|\[[^\]]+\]\(([^)]+)\)')
NBE_SAMPLE_EXPECTED_METRICS = {
    "total_universe": 80,
    "total_eligible": 76,
    "total_planned": 76,
    "no_action_count": 4,
}

CONFIG_CAPABILITY_NAMES = {
    "hcp_intelligence": "HCP Intelligence",
    "field_training": "Field Training",
    "campaign_studio": "Campaign Studio",
    "next_best_engagement": "Next-Best-Engagement",
    "territory_alignment": "Territory Alignment",
    "competitive_intelligence": "Competitive Intelligence",
}

HOMEPAGE_VERSION_LABELS = {
    "HCP Intelligence": "HCP",
    "Competitive Intelligence": "CI",
    "Territory Alignment": "TA",
    "Next-Best-Engagement": "NBE",
    "Field Training": "FT",
    "Campaign Studio": "CS",
}

PROHIBITED_ASSURANCE_PATTERNS = {
    "output claimed compliant": r"\boutputs?\s+(?:is|are)\s+(?:fully\s+)?compliant\b",
    "system claimed compliant": r"\b(?:system|platform|workflow|tool|capability|product)\s+(?:is|are)\s+(?:fully\s+)?compliant\b",
    "output claimed approved": r"\b(?:this\s+)?(?:output|artifact|plan|report)s?\s+(?:is|are|has\s+been|have\s+been)\s+approved\b",
    "compliant output label": r"\b(?:fully\s+)?compliant\s+outputs?\b",
    "approved output label": r"\bapproved\s+outputs?\b",
    "regulatory approval claim": r"\b(?:regulatory|mlr|fda)\s+approved\b",
    "automatic approval claim": r"\bautomatically\s+approved\b",
    "compliance guarantee": r"\bguarantee(?:d|s)?\s+(?:regulatory\s+)?compliance\b",
    "autonomous operation claim": r"\b(?:fully\s+)?autonomous\s+(?:operation|workflow|execution|decision(?:-making)?|system)\b",
    "autonomous approval claim": r"\bautonomous\s+approval\b",
    "human review waived": r"\bno\s+(?:qualified\s+)?human\s+review\s+(?:is\s+)?required\b",
}

REQUIRED_FILES = (
    "mkdocs.yml",
    "requirements.txt",
    "requirements.lock",
    "overrides/main.html",
    "docs/index.md",
    "docs/get-started.md",
    "docs/outcomes/index.md",
    "docs/examples/index.md",
    "docs/trust-governance.md",
    "docs/technical-reference.md",
    "docs/operations/release-sync.md",
    "docs/assets/stylesheets/extra.css",
    "docs/assets/javascripts/extra.js",
    "docs/assets/images/favicon.svg",
    "docs/favicon.ico",
    "docs/assets/data/release.json",
)

REQUIRED_TOKENS = {
    "Clinical Ink": "#102a43",
    "Porcelain": "#f4f8fb",
    "Signal Teal": "#0b7a75",
    "Evidence Blue": "#2b5fb3",
    "Audit Amber": "#d58b24",
    "Evidence Red": "#b33a3a",
}

SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")
COMMIT_PATTERN = re.compile(r"^[0-9a-f]{7,40}$")
PRIVATE_CANONICAL_URL_PATTERN = re.compile(
    rf"https://github\.com/{re.escape(CANONICAL_REPOSITORY)}(?:/[^\s)\"'<>]*)?"
)
PRIVATE_RAW_INSTALL_PATTERN = re.compile(
    r"https://raw\.githubusercontent\.com/PharmaGenAI/open-pharma-plugins/"
)
CURRENT_NBE_NOTE_PATTERN = re.compile(
    r"exact pinned built-in fictional demo fixture.*runtime-generated from it on "
    r"(?P<date>\d{4}-\d{2}-\d{2}) with the pinned next-best-engagement "
    r"(?P<version>\d+\.\d+\.\d+) implementation\.",
    re.IGNORECASE | re.DOTALL,
)
STALE_NBE_NOTE_PATTERN = re.compile(
    r"exact pinned built-in fictional demo fixture.*last runtime-generated from it on "
    r"(?P<date>\d{4}-\d{2}-\d{2}) with next-best-engagement (?P<version>\d+\.\d+\.\d+).*"
    r"did not regenerate the sample artifact",
    re.IGNORECASE | re.DOTALL,
)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def frontmatter(path: Path, errors: list[str]) -> str:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        fail(errors, f"{path.relative_to(ROOT)}: missing YAML front matter")
        return text
    header = text.split("\n---\n", 1)[0]
    for key in ("title:", "description:"):
        if key not in header:
            fail(errors, f"{path.relative_to(ROOT)}: missing {key[:-1]} metadata")
    return text


def private_canonical_access_errors(relative: str, text: str) -> list[str]:
    errors: list[str] = []
    private_links = PRIVATE_CANONICAL_URL_PATTERN.findall(text)
    label = "Authorized repository access required"
    if not private_links:
        return errors
    label_count = text.count(label)
    if relative == "docs/technical-reference.md":
        if label_count < 2:
            errors.append(
                "docs/technical-reference.md: private canonical link groups must be labeled 'Authorized repository access required'"
            )
        lines = text.splitlines()
        for line in lines:
            if PRIVATE_CANONICAL_URL_PATTERN.search(line) and label not in line:
                errors.append(
                    "docs/technical-reference.md: each private canonical table row must include the exact access label"
                )
                break
    elif label_count < 1:
        errors.append(f"{relative}: private canonical links require the exact access label")
    return errors


def release_metadata_errors(release: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(release, dict):
        return ["release.json must be a JSON object"]

    expected_keys = ("canonical_repository", "source_commit", "distribution_version", "capabilities")
    if tuple(release) != expected_keys:
        errors.append(f"release.json keys must be exactly {list(expected_keys)}")
        return errors

    if release.get("canonical_repository") != CANONICAL_REPOSITORY:
        errors.append("release.json canonical_repository is incorrect")
    if not isinstance(release.get("source_commit"), str) or not COMMIT_PATTERN.fullmatch(
        release["source_commit"]
    ):
        errors.append("release.json source_commit must be a 7-40 character lowercase git SHA")
    if not isinstance(release.get("distribution_version"), str) or not SEMVER_PATTERN.fullmatch(
        release["distribution_version"]
    ):
        errors.append("release.json distribution_version must be semver")

    capabilities = release.get("capabilities")
    if not isinstance(capabilities, dict):
        errors.append("release.json capabilities must be a JSON object")
        return errors
    if tuple(capabilities) != RELEASE_CAPABILITY_ORDER:
        errors.append(
            f"release.json capability names must be exactly {list(RELEASE_CAPABILITY_ORDER)}"
        )
        return errors
    for capability, version in capabilities.items():
        if not isinstance(version, str) or not SEMVER_PATTERN.fullmatch(version):
            errors.append(f"release.json capability version for {capability!r} must be semver")
    return errors


def find_prohibited_assurances(text: str) -> list[str]:
    """Return unsafe direct-assurance categories found in site copy."""
    normalized = " ".join(text.lower().split())
    found: list[str] = []
    for name, pattern in PROHIBITED_ASSURANCE_PATTERNS.items():
        for match in re.finditer(pattern, normalized):
            context = normalized[max(0, match.start() - 40) : match.start()]
            if re.search(r"\b(?:not|never|without)\b[^.!?;]{0,30}$", context):
                continue
            found.append(name)
            break
    return found


def relative_luminance(color: str) -> float:
    channels = [int(color[index : index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [
        channel / 12.92
        if channel <= 0.04045
        else ((channel + 0.055) / 1.055) ** 2.4
        for channel in channels
    ]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast_ratio(first: str, second: str) -> float:
    lighter, darker = sorted(
        (relative_luminance(first), relative_luminance(second)), reverse=True
    )
    return (lighter + 0.05) / (darker + 0.05)


def navigation_lifecycle_errors(config: dict, css: str, javascript: str) -> list[str]:
    """Check Material instant-navigation behavior against hero enhancement code."""
    features = config.get("theme", {}).get("features", [])
    if "navigation.instant" not in features:
        return []

    errors: list[str] = []
    if "DOMContentSwitch" in javascript:
        errors.append("extra.js uses unsupported DOMContentSwitch with navigation.instant")
    if "is-ready" in javascript and "document$.subscribe" not in javascript:
        errors.append("extra.js does not subscribe hero enhancement to Material document$")
    if re.search(
        r"\.opp-js\s+\.opp-hero__(?:copy|aside)[^{}]*\{[^}]*opacity:\s*0",
        css,
        re.DOTALL,
    ):
        errors.append("hero content is hidden until JavaScript mutates page state")
    return errors


def capability_version_errors(config: dict, homepage: str, release: dict) -> list[str]:
    """Compare both duplicated version displays with the release snapshot."""
    errors: list[str] = []
    release_versions = release.get("capabilities", {})
    expected_config = {
        key: release_versions.get(capability)
        for key, capability in CONFIG_CAPABILITY_NAMES.items()
    }
    actual_config = config.get("extra", {}).get("capability_versions")
    if actual_config != expected_config:
        errors.append("mkdocs.yml capability_versions differ from release.json")

    tags = re.findall(r'<span class="version-tag">([^<]+)</span>', homepage)
    actual_visible: dict[str, str] = {}
    for tag in tags:
        parts = tag.strip().split(maxsplit=1)
        if len(parts) == 2:
            label, version = parts
            actual_visible[label] = version
    expected_visible = {
        HOMEPAGE_VERSION_LABELS[capability]: version
        for capability, version in release_versions.items()
        if capability in HOMEPAGE_VERSION_LABELS
    }
    if len(tags) != len(expected_visible) or actual_visible != expected_visible:
        errors.append("homepage visible version tags differ from release.json")
    return errors


def expected_public_pypi_url(release: dict) -> str:
    """Return the version-pinned public PyPI project URL from release metadata."""
    return f"https://pypi.org/project/open-pharma-plugins/{release['distribution_version']}/"


def technical_reference_errors(technical: str, release: dict) -> list[str]:
    """Validate technical-reference links and copy against the pinned release snapshot."""
    errors: list[str] = []
    technical_links = link_targets(technical)
    for target in (
        f"https://github.com/{CANONICAL_REPOSITORY}/blob/{release['source_commit']}/README.md",
        f"https://github.com/{CANONICAL_REPOSITORY}/blob/{release['source_commit']}/docs/en/installation.md",
        f"https://github.com/{CANONICAL_REPOSITORY}/blob/{release['source_commit']}/docs/en/configuration.md",
        f"https://github.com/{CANONICAL_REPOSITORY}/blob/{release['source_commit']}/docs/en/data_security.md",
        f"https://github.com/{CANONICAL_REPOSITORY}/blob/{release['source_commit']}/docs/en/releasing.md",
        f"https://github.com/{CANONICAL_REPOSITORY}/blob/{release['source_commit']}/plugin-versions.json",
        expected_public_pypi_url(release),
        "operations/release-sync.md",
    ):
        if target not in technical_links:
            errors.append(
                f"docs/technical-reference.md: missing technical link target {target!r}"
            )

    technical_lower = technical.lower()
    for required in (
        "authorized repository access required",
        "public paths available today",
        expected_public_pypi_url(release).removeprefix("https://"),
        f"visible short sha `{release['source_commit'][:7]}` is derived",
    ):
        if required not in technical_lower:
            errors.append(
                f"docs/technical-reference.md: missing honest access/fallback text {required!r}"
            )

    for forbidden in (
        "no repo access required",
        "publicly available github guide",
        "anonymous github access",
    ):
        if forbidden in technical_lower:
            errors.append(
                f"docs/technical-reference.md: forbidden anonymous-access wording {forbidden!r}"
            )

    for required_block in (
        "\n\n| Need | Pinned canonical document | Access |\n| --- | --- | --- |",
        "\n\n| Capability | Pinned cookbook | Access |\n| --- | --- | --- |",
    ):
        if required_block not in technical:
            errors.append(
                "docs/technical-reference.md: private canonical access tables must stay in Markdown table blocks"
            )
    return errors


def sample_manifest_errors(
    manifest: dict,
    manifest_path: Path,
    slug: str,
    capability: str,
    release: dict,
) -> list[str]:
    """Validate one sample manifest and its local input/output contract."""
    errors: list[str] = []
    if not isinstance(manifest, dict):
        return [f"{manifest_path.relative_to(ROOT)}: manifest must be a YAML mapping"]
    if tuple(manifest) != MANIFEST_KEYS:
        errors.append(
            f"{manifest_path.relative_to(ROOT)}: keys must be exactly {list(MANIFEST_KEYS)}"
        )
        return errors

    expected_values = {
        "capability_slug": slug,
        "fictional_data": True,
        "status": MANIFEST_STATUS_BY_SLUG[slug],
    }
    for field, expected in expected_values.items():
        if manifest.get(field) != expected:
            errors.append(
                f"{manifest_path.relative_to(ROOT)}: {field} must be {expected!r}"
            )

    for field in ("capability_version", "distribution_version"):
        value = manifest.get(field)
        if not isinstance(value, str) or not SEMVER_PATTERN.fullmatch(value):
            errors.append(f"{manifest_path.relative_to(ROOT)}: {field} must be semver")
    source_commit = manifest.get("source_commit")
    if not isinstance(source_commit, str) or not COMMIT_PATTERN.fullmatch(source_commit):
        errors.append(
            f"{manifest_path.relative_to(ROOT)}: source_commit must be a 7-40 character lowercase git SHA"
        )

    for path_field in ("input_path", "output_path"):
        value = manifest.get(path_field)
        if (
            not isinstance(value, str)
            or not value
            or Path(value).is_absolute()
            or Path(value).parent != Path(".")
        ):
            errors.append(
                f"{manifest_path.relative_to(ROOT)}: {path_field} must name one local sample file"
            )
            continue
        sample_path = manifest_path.parent / value
        if not sample_path.is_file():
            errors.append(
                f"{manifest_path.relative_to(ROOT)}: {path_field} does not exist: {value}"
            )
            continue
        sample_text = sample_path.read_text(encoding="utf-8")
        if not sample_text.strip():
            errors.append(f"{sample_path.relative_to(ROOT)}: sample file is empty")
        if slug != "next-best-engagement" and "fictional" not in sample_text.lower():
            errors.append(
                f"{sample_path.relative_to(ROOT)}: sample must declare fictional data"
            )
        if sample_path.suffix == ".json":
            try:
                json.loads(sample_text)
            except json.JSONDecodeError as exc:
                errors.append(f"{sample_path.relative_to(ROOT)}: invalid JSON: {exc}")
        elif sample_path.suffix in {".yml", ".yaml"}:
            try:
                if yaml.safe_load(sample_text) is None:
                    errors.append(f"{sample_path.relative_to(ROOT)}: YAML sample is empty")
            except yaml.YAMLError as exc:
                errors.append(f"{sample_path.relative_to(ROOT)}: invalid YAML: {exc}")
        elif sample_path.suffix == ".csv":
            rows = list(csv.reader(sample_text.splitlines()))
            if len(rows) < 2 or not rows[0] or any(not column for column in rows[0]):
                errors.append(
                    f"{sample_path.relative_to(ROOT)}: CSV sample needs a complete header and at least one row"
                )
            elif len(rows[0]) != len(set(rows[0])):
                errors.append(f"{sample_path.relative_to(ROOT)}: CSV header contains duplicates")
            elif any(len(row) != len(rows[0]) for row in rows[1:]):
                errors.append(f"{sample_path.relative_to(ROOT)}: CSV rows do not match the header width")
        for assurance in find_prohibited_assurances(sample_text):
            errors.append(
                f"{sample_path.relative_to(ROOT)}: sample contains prohibited assurance: {assurance}"
            )

    notes = manifest.get("notes")
    if not isinstance(notes, str):
        errors.append(f"{manifest_path.relative_to(ROOT)}: notes must be a string")
    elif slug == "next-best-engagement":
        current_match = CURRENT_NBE_NOTE_PATTERN.search(notes)
        stale_match = STALE_NBE_NOTE_PATTERN.search(notes)
        if current_match:
            if current_match.group("version") != manifest.get("capability_version"):
                errors.append(
                    f"{manifest_path.relative_to(ROOT)}: current runtime-generated note must match capability_version"
                )
        elif stale_match:
            if stale_match.group("version") != manifest.get("capability_version"):
                errors.append(
                    f"{manifest_path.relative_to(ROOT)}: runtime-generated note must match capability_version"
                )
        else:
            errors.append(
                f"{manifest_path.relative_to(ROOT)}: notes must disclose either the current runtime-generated fixture provenance or that release synchronization did not regenerate the sample artifact"
            )
    elif "not current runtime-generated" not in notes.lower():
        errors.append(
            f"{manifest_path.relative_to(ROOT)}: notes must disclose that the sample is not current runtime-generated"
        )
    return errors


def link_targets(text: str) -> set[str]:
    """Extract HTML href and Markdown link targets from a source page."""
    targets: set[str] = set()
    for html_target, markdown_target in LINK_PATTERN.findall(text):
        target = (html_target or markdown_target).strip()
        if target:
            targets.add(target)
    return targets


def nbe_public_sample_errors(page_text: str, input_path: Path, output_path: Path) -> list[str]:
    """Validate that the public NBE sample is the pinned 80-HCP fixture and matching generated plan."""
    errors: list[str] = []

    with input_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    input_row_count = len(rows)
    if input_row_count != NBE_SAMPLE_EXPECTED_METRICS["total_universe"]:
        errors.append(
            f"{input_path.relative_to(ROOT)}: expected {NBE_SAMPLE_EXPECTED_METRICS['total_universe']} fixture rows, found {input_row_count}"
        )

    try:
        output = json.loads(output_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{output_path.relative_to(ROOT)}: invalid JSON: {exc}"]
    if not isinstance(output, dict):
        return [f"{output_path.relative_to(ROOT)}: generated plan must be a JSON object"]

    required_keys = {
        "universe_fingerprint",
        "universe_generation",
        "period_start",
        "period_end",
        "generated_at",
        "engagements",
        "unassigned",
        "metrics",
    }
    if set(output) != required_keys:
        errors.append(
            f"{output_path.relative_to(ROOT)}: top-level keys must be exactly {sorted(required_keys)}"
        )
        return errors

    metrics = output.get("metrics")
    if not isinstance(metrics, dict):
        return [f"{output_path.relative_to(ROOT)}: metrics must be a JSON object"]

    for field, expected in NBE_SAMPLE_EXPECTED_METRICS.items():
        actual = metrics.get(field)
        if actual != expected:
            errors.append(
                f"{output_path.relative_to(ROOT)}: metrics.{field} must be {expected}, found {actual}"
            )

    engagements = output.get("engagements")
    unassigned = output.get("unassigned")
    if not isinstance(engagements, list) or not isinstance(unassigned, list):
        return [f"{output_path.relative_to(ROOT)}: engagements and unassigned must be arrays"]
    if len(engagements) != metrics.get("total_planned"):
        errors.append(
            f"{output_path.relative_to(ROOT)}: engagement count must match metrics.total_planned"
        )
    if len(unassigned) != metrics.get("no_action_count"):
        errors.append(
            f"{output_path.relative_to(ROOT)}: unassigned count must match metrics.no_action_count"
        )
    if metrics.get("total_universe") != input_row_count:
        errors.append(
            f"{output_path.relative_to(ROOT)}: metrics.total_universe must match input row count"
        )
    if metrics.get("total_planned", 0) + metrics.get("no_action_count", 0) != input_row_count:
        errors.append(
            f"{output_path.relative_to(ROOT)}: total_planned + no_action_count must equal the input row count"
        )
    if metrics.get("total_eligible") != metrics.get("total_planned"):
        errors.append(
            f"{output_path.relative_to(ROOT)}: this pinned fixture must keep total_eligible equal to total_planned"
        )

    priority_visit = next(
        (item for item in engagements if item.get("hcp_id") == "HCP-E-003"), None
    )
    if not isinstance(priority_visit, dict) or (
        priority_visit.get("priority") != 1
        or priority_visit.get("action_type") != "in_person_visit"
    ):
        errors.append(
            f"{output_path.relative_to(ROOT)}: HCP-E-003 must remain the pinned priority-1 in_person_visit example"
        )
    no_consent = next(
        (item for item in unassigned if item.get("hcp_id") == "HCP-E-015"), None
    )
    if not isinstance(no_consent, dict) or no_consent.get("reason") != "no_consent":
        errors.append(
            f"{output_path.relative_to(ROOT)}: HCP-E-015 must remain the pinned no_consent example"
        )

    required_page_phrases = (
        f"{input_row_count} HCP rows",
        f"{metrics.get('total_eligible')} eligible HCPs",
        f"{metrics.get('total_planned')} planned actions",
        f"{len(unassigned)} unassigned HCPs",
        "`HCP-E-003` is a priority-1 `in_person_visit`",
        "`HCP-E-015` is `unassigned` with reason `no_consent`",
    )
    page_text_lower = " ".join(page_text.lower().split())
    for phrase in required_page_phrases:
        normalized_phrase = " ".join(phrase.lower().split())
        if normalized_phrase not in page_text_lower:
            example = (
                "priority-1 visit example"
                if "in_person_visit" in phrase
                else "no_consent example"
                if "no_consent" in phrase
                else f"artifact-backed phrase {phrase!r}"
            )
            errors.append(
                f"docs/capabilities/next-best-engagement.md: missing visible {example}"
            )
    return errors


def main() -> int:
    errors: list[str] = []

    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            fail(errors, f"missing required file: {relative}")

    # Continue only when the files needed by subsequent checks exist.
    if errors:
        return report(errors)

    config_text = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    config = yaml.safe_load(config_text)
    release = json.loads((DOCS / "assets/data/release.json").read_text(encoding="utf-8"))
    css = (DOCS / "assets/stylesheets/extra.css").read_text(encoding="utf-8").lower()
    javascript = (DOCS / "assets/javascripts/extra.js").read_text(encoding="utf-8")
    expected_nav = [
        {"Home": "index.md"},
        {"Get started": "get-started.md"},
        {"Business outcomes": "outcomes/index.md"},
        {
            "Capabilities": [
                {capability: f"capabilities/{slug}.md"}
                for slug, capability in CAPABILITY_SLUGS.items()
            ]
        },
        {"Examples": "examples/index.md"},
        {"Trust & governance": "trust-governance.md"},
        {"Technical reference": "technical-reference.md"},
        {"Operations": [{"Release sync": "operations/release-sync.md"}]},
    ]
    if config.get("nav") != expected_nav:
        fail(errors, f"checkpoint nav must be exactly {expected_nav}, found {config.get('nav')}")
    nav_paths: list[str] = []
    for item in config.get("nav", []):
        value = next(iter(item.values()))
        if isinstance(value, list):
            nav_paths.extend(next(iter(child.values())) for child in value)
        else:
            nav_paths.append(value)
    for nav_path in nav_paths:
        if not (DOCS / nav_path).is_file():
            fail(errors, f"navigation target does not exist: docs/{nav_path}")

    if config.get("strict") is not True:
        fail(errors, "mkdocs.yml must enable strict mode")
    if config.get("site_url") != "https://pharmagenai.github.io/":
        fail(errors, "mkdocs.yml must declare the public site URL")
    if config.get("repo_name") != "Website source":
        fail(errors, "mkdocs.yml repo_name must honestly label the public website source")
    if config.get("repo_url") != PUBLIC_SITE_REPOSITORY_URL:
        fail(errors, "mkdocs.yml repo_url must point to the public website source repository")
    if config.get("extra", {}).get("social") != [
        {
            "icon": "fontawesome/brands/github",
            "link": PUBLIC_SITE_REPOSITORY_URL,
            "name": "Website source on GitHub",
        }
    ]:
        fail(errors, "mkdocs.yml social link must identify the public website source repository")
    utility_links = config.get("extra", {}).get("utility_links", [])
    pypi_links = [
        item.get("href")
        for item in utility_links
        if isinstance(item, dict) and item.get("label") == "Public PyPI project"
    ]
    if pypi_links != [expected_public_pypi_url(release)]:
        fail(errors, "mkdocs.yml footer PyPI URL must match release.json")
    if config.get("theme", {}).get("name") != "material":
        fail(errors, "mkdocs.yml must use Material for MkDocs")
    if config.get("theme", {}).get("custom_dir") != "overrides":
        fail(errors, "mkdocs.yml must load the custom template directory")
    expected_config_release = {
        "distribution": release["distribution_version"],
        "source_commit": release["source_commit"],
        "repository": release["canonical_repository"],
    }
    if config.get("extra", {}).get("release") != expected_config_release:
        fail(errors, "mkdocs.yml release metadata differs from the pinned release truth")

    pages = {
        path.relative_to(ROOT).as_posix(): frontmatter(path, errors)
        for path in (
            DOCS / "index.md",
            DOCS / "get-started.md",
            DOCS / "outcomes/index.md",
            DOCS / "examples/index.md",
            DOCS / "trust-governance.md",
            DOCS / "technical-reference.md",
            DOCS / "operations/release-sync.md",
        )
    }

    capability_pages: dict[str, str] = {}
    sample_manifests: dict[str, dict] = {}
    example_dirs = sorted(path.name for path in (DOCS / "examples").iterdir() if path.is_dir())
    if example_dirs != sorted(CAPABILITY_SLUGS):
        fail(
            errors,
            f"docs/examples must contain exactly these sample directories: {sorted(CAPABILITY_SLUGS)}",
        )
    for slug, capability in CAPABILITY_SLUGS.items():
        page_path = DOCS / "capabilities" / f"{slug}.md"
        if not page_path.is_file():
            fail(errors, f"missing capability page: {page_path.relative_to(ROOT)}")
            continue
        page_text = frontmatter(page_path, errors)
        capability_pages[slug] = page_text
        if capability not in page_text:
            fail(errors, f"{page_path.relative_to(ROOT)}: missing capability name {capability!r}")
        if release["capabilities"][capability] not in page_text:
            fail(errors, f"{page_path.relative_to(ROOT)}: missing pinned capability version")
        for section in CAPABILITY_SECTIONS:
            if section not in page_text:
                fail(errors, f"{page_path.relative_to(ROOT)}: missing required section {section!r}")
        if page_text.count('class="workflow-step"') != 3:
            fail(errors, f"{page_path.relative_to(ROOT)}: expected exactly three workflow steps")
        if page_text.count('class="plugin-flow"') != 1:
            fail(errors, f"{page_path.relative_to(ROOT)}: expected exactly one plugin input-tools-output visual")
        for stage in ("Input", "Tools", "Expected output"):
            if f">{stage}<" not in page_text:
                fail(errors, f"{page_path.relative_to(ROOT)}: missing plugin-flow stage {stage!r}")
        if 'class="plugin-flow__tools"' not in page_text:
            fail(errors, f"{page_path.relative_to(ROOT)}: missing visual tool list")
        for marker in ("Fictional", "representative", "qualified", "public beta"):
            if marker.lower() not in page_text.lower():
                fail(errors, f"{page_path.relative_to(ROOT)}: missing boundary marker {marker!r}")

        manifest_path = DOCS / "examples" / slug / "manifest.yml"
        if not manifest_path.is_file():
            fail(errors, f"missing sample manifest: {manifest_path.relative_to(ROOT)}")
            continue
        try:
            manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            fail(errors, f"{manifest_path.relative_to(ROOT)}: invalid YAML: {exc}")
            continue
        for error in sample_manifest_errors(
            manifest, manifest_path, slug, capability, release
        ):
            fail(errors, error)
        if isinstance(manifest, dict):
            sample_manifests[slug] = manifest
            sample_dir = manifest_path.parent
            files = sorted(path.name for path in sample_dir.iterdir() if path.is_file())
            expected_files = sorted(
                [manifest.get("input_path", ""), manifest.get("output_path", ""), "manifest.yml"]
            )
            if files != expected_files:
                fail(
                    errors,
                    f"{sample_dir.relative_to(ROOT)}: files must be exactly {expected_files}, found {files}",
                )

            for link_target in (
                f"../examples/{slug}/{manifest.get('input_path', '')}",
                f"../examples/{slug}/{manifest.get('output_path', '')}",
                f"../examples/{slug}/manifest.yml",
            ):
                if link_target not in link_targets(page_text):
                    fail(
                        errors,
                        f"{page_path.relative_to(ROOT)}: missing sample link target {link_target!r}",
                    )
            if slug == "next-best-engagement":
                for error in nbe_public_sample_errors(
                    page_text,
                    sample_dir / manifest["input_path"],
                    sample_dir / manifest["output_path"],
                ):
                    fail(errors, error)

    examples_index_links = link_targets(pages["docs/examples/index.md"])
    for slug, manifest in sample_manifests.items():
        for link_target in (
            f"../capabilities/{slug}.md",
            f"{slug}/{manifest.get('input_path', '')}",
            f"{slug}/{manifest.get('output_path', '')}",
            f"{slug}/manifest.yml",
        ):
            if link_target not in examples_index_links:
                fail(
                    errors,
                    f"docs/examples/index.md: missing example index link target {link_target!r}",
                )

    portfolio_pages = {
        key: pages[key]
        for key in (
            "docs/index.md",
            "docs/get-started.md",
            "docs/outcomes/index.md",
            "docs/examples/index.md",
            "docs/trust-governance.md",
            "docs/technical-reference.md",
        )
    }
    for capability in CAPABILITY_SLUGS.values():
        for relative, text in portfolio_pages.items():
            if capability not in text:
                fail(errors, f"{relative}: missing capability name {capability!r}")

    pages.update(
        {
            f"docs/capabilities/{slug}.md": text
            for slug, text in capability_pages.items()
        }
    )
    combined = "\n".join(pages.values())

    homepage = pages["docs/index.md"]
    for marker in ("data-hero", "capability-table", "01", "02", "03", "04", "05", "06"):
        if marker not in homepage:
            fail(errors, f"docs/index.md: missing lifecycle marker {marker!r}")
    for error in capability_version_errors(config, homepage, release):
        fail(errors, error)

    examples = pages["docs/examples/index.md"].lower()
    for declaration in ("fictional and representative", "no real hcp", "patient data"):
        if declaration not in examples:
            fail(errors, f"docs/examples/index.md: missing example safety declaration {declaration!r}")

    get_started = pages["docs/get-started.md"]
    expected_pip_command = f'python -m pip install "open-pharma-plugins[hcp-intelligence]=={release["distribution_version"]}"'
    for required in (
        expected_pip_command,
        "public pypi distribution",
        "authorized repository checkout required",
        "bash install.sh",
        "bash install.sh local",
        "~/.open-pharma-plugins/config",
        "fictional",
        "platform owner",
        "business user",
        "--check-system",
    ):
        if required.lower() not in get_started.lower():
            fail(errors, f"docs/get-started.md: missing required guidance {required!r}")
    for forbidden in (
        "raw.githubusercontent.com/pharmagenai/open-pharma-plugins",
        "curl -fsSLO https://raw.githubusercontent.com/PharmaGenAI/open-pharma-plugins/main/install.sh".lower(),
        "anonymous",
    ):
        if forbidden in get_started.lower():
            fail(errors, f"docs/get-started.md: forbidden anonymous/private install claim {forbidden!r}")

    trust = pages["docs/trust-governance.md"].lower()
    for required in (
        "human review",
        "public beta",
        "least-privilege filesystem access",
        "open-pharma-plugins/config",
        "competitive intelligence",
        "territory alignment",
        "next-best-engagement",
        "field training",
        "campaign studio",
    ):
        if required not in trust:
            fail(errors, f"docs/trust-governance.md: missing trust boundary {required!r}")

    technical = pages["docs/technical-reference.md"]
    for error in technical_reference_errors(technical, release):
        fail(errors, error)

    release_sync = pages["docs/operations/release-sync.md"].lower()
    for required in (
        "repository_dispatch",
        "open-pharma-plugins-release",
        "plugin-versions.json",
        "contents: write",
        "pull request",
        "dispatch-only token",
        "separate canonical-read-only",
        "sample manifests, inputs, and outputs remain byte-for-byte unchanged",
        "open_pharma_pages_sync_token",
        "github_token",
    ):
        if required not in release_sync:
            fail(errors, f"docs/operations/release-sync.md: missing release-sync contract text {required!r}")
    if "release_index_path" in release_sync:
        fail(errors, "docs/operations/release-sync.md: must not expose release_index_path")

    for relative in ("docs/outcomes/index.md", "docs/examples/index.md"):
        text = pages[relative]
        if text.count('class="preview-dossier" markdown="1"') != 6:
            fail(errors, f"{relative}: expected six Markdown-enabled preview dossiers")
        if '<div class="preview-dossier">' in text:
            fail(errors, f"{relative}: preview dossier would emit nested Markdown literally")

    lower_combined = combined.lower()
    for statement in ("public beta", "qualified", "review"):
        if statement not in lower_combined:
            fail(errors, f"site copy must state the {statement!r} boundary")
    for assurance in find_prohibited_assurances(combined):
        fail(errors, f"site copy contains prohibited assurance: {assurance}")
    if PRIVATE_RAW_INSTALL_PATTERN.search(combined):
        fail(errors, "site copy must not claim anonymous raw installer access for the private canonical repository")

    for relative, text in pages.items():
        for error in private_canonical_access_errors(relative, text):
            fail(errors, error)
    for slug, text in capability_pages.items():
        for error in private_canonical_access_errors(f"docs/capabilities/{slug}.md", text):
            fail(errors, error)

    for error in release_metadata_errors(release):
        fail(errors, error)

    for name, token in REQUIRED_TOKENS.items():
        if token not in css:
            fail(errors, f"visual system is missing {name} token {token}")
    for requirement in (":focus-visible", "prefers-reduced-motion", "@media screen and (max-width"):
        if requirement not in css:
            fail(errors, f"visual system is missing accessibility/responsive rule {requirement!r}")
    focus_match = re.search(r"--opp-focus:\s*(#[0-9a-f]{6})", css)
    if not focus_match:
        fail(errors, "visual system is missing the dedicated focus color")
    else:
        focus = focus_match.group(1)
        for background in ("#ffffff", REQUIRED_TOKENS["Porcelain"]):
            ratio = contrast_ratio(focus, background)
            if ratio < 3:
                fail(errors, f"focus color contrast against {background} is {ratio:.2f}:1, below 3:1")
    if "box-shadow: 0 0 0 5px var(--opp-focus)" not in css:
        fail(errors, "focus-visible styling must use the validated focus color as an outer ring")

    for error in navigation_lifecycle_errors(config, css, javascript):
        fail(errors, error)

    template = (ROOT / "overrides/main.html").read_text(encoding="utf-8")
    for metadata in ("og:title", "og:description", "application/ld+json", "theme-color"):
        if metadata not in template:
            fail(errors, f"site template is missing metadata {metadata!r}")

    source_partial = (ROOT / "overrides/partials/source.html").read_text(encoding="utf-8")
    if PUBLIC_SITE_REPOSITORY_URL not in source_partial or "Website source" not in source_partial:
        fail(errors, "source override must identify the public website source repository")
    if f"https://github.com/{CANONICAL_REPOSITORY}" in source_partial:
        fail(errors, "source override must not expose the private canonical repository as a global link")

    favicon_header = (DOCS / "favicon.ico").read_bytes()[:4]
    if favicon_header != b"\x00\x00\x01\x00":
        fail(errors, "docs/favicon.ico must be a valid ICO fallback")

    return report(errors)


def report(errors: list[str]) -> int:
    if errors:
        print(f"Content validation failed with {len(errors)} error(s):", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(
        "Content validation passed: foundation, navigation, get-started/trust/reference pages, "
        "six capability dossiers, sample manifests/files, release truth, safety copy, and visual tokens verified."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
