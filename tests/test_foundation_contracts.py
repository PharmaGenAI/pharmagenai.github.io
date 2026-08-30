from __future__ import annotations

import copy
import json
import re
import unittest
from pathlib import Path

import yaml

from scripts.check_content import (
    CAPABILITY_SLUGS,
    MANIFEST_KEYS,
    capability_version_errors,
    find_prohibited_assurances,
    link_targets,
    nbe_public_sample_errors,
    navigation_lifecycle_errors,
    private_canonical_access_errors,
    release_metadata_errors,
    sample_manifest_errors,
    technical_reference_errors,
)
from scripts.check_local_links import normalize_source_target


ROOT = Path(__file__).resolve().parents[1]


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


class FoundationContractsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
        cls.css = (ROOT / "docs/assets/stylesheets/extra.css").read_text(encoding="utf-8")
        cls.javascript = (ROOT / "docs/assets/javascripts/extra.js").read_text(encoding="utf-8")
        cls.homepage = (ROOT / "docs/index.md").read_text(encoding="utf-8")
        cls.release = json.loads(
            (ROOT / "docs/assets/data/release.json").read_text(encoding="utf-8")
        )

    def test_instant_navigation_uses_supported_document_lifecycle(self) -> None:
        features = self.config["theme"].get("features", [])
        self.assertIn("navigation.instant", features)
        self.assertNotIn("DOMContentSwitch", self.javascript)
        self.assertIn("document$.subscribe", self.javascript)
        self.assertIsNone(
            re.search(
                r"\.opp-js\s+\.opp-hero__(?:copy|aside)[^{}]*\{[^}]*opacity:\s*0",
                self.css,
                re.DOTALL,
            ),
            "primary hero content must not depend on JavaScript to become visible",
        )

    def test_clean_output_urls_resolve_to_their_markdown_sources(self) -> None:
        docs = ROOT / "docs"
        self.assertEqual(
            normalize_source_target(docs, "get-started/"),
            docs / "get-started.md",
        )
        self.assertEqual(
            normalize_source_target(docs, "outcomes/"),
            docs / "outcomes/index.md",
        )

    def test_focus_indicator_has_three_to_one_non_text_contrast(self) -> None:
        match = re.search(r"--opp-focus:\s*(#[0-9a-fA-F]{6})", self.css)
        self.assertIsNotNone(match, "a dedicated focus color must be declared")
        focus = match.group(1)
        for background in ("#ffffff", "#f4f8fb"):
            with self.subTest(background=background):
                self.assertGreaterEqual(contrast_ratio(focus, background), 3.0)
        self.assertIn("box-shadow: 0 0 0 5px var(--opp-focus)", self.css)

    def test_homepage_keeps_beta_and_release_details_out_of_global_chrome(self) -> None:
        override = (ROOT / "overrides/main.html").read_text(encoding="utf-8")
        self.assertNotIn("{% block announce %}", override)
        self.assertNotIn("public beta", self.config["copyright"].lower())
        self.assertNotIn("release-line", self.homepage)
        self.assertNotIn("Pinned source", self.homepage)

    def test_homepage_installation_is_a_separate_wrapping_section(self) -> None:
        hero_end = self.homepage.index("</section>")
        install_start = self.homepage.index('<section class="quick-install"')
        self.assertGreater(install_start, hero_end)
        self.assertIn("white-space: pre-wrap;", self.css)
        self.assertIn("overflow-wrap: anywhere;", self.css)
        self.assertIn("word-break: break-word;", self.css)

    def test_homepage_uses_an_aligned_capability_table(self) -> None:
        self.assertIn('<table class="capability-table">', self.homepage)
        self.assertIn('<th scope="col">Business question</th>', self.homepage)
        self.assertIn('<th scope="col">Expected output</th>', self.homepage)
        self.assertNotIn("evidence-ribbon", self.homepage)

    def test_preferred_install_is_the_native_agent_harness(self) -> None:
        get_started = (ROOT / "docs/get-started.md").read_text(encoding="utf-8")
        for marker in (
            "Preferred · Claude or Codex",
            "https://github.com/PharmaGenAI/open-pharma-plugins",
            "less install.sh",
            "bash install.sh",
        ):
            self.assertIn(marker, get_started)
        self.assertIn("MCP-server-only installation", get_started)

    def test_every_capability_visualizes_input_tools_and_expected_output(self) -> None:
        for slug in CAPABILITY_SLUGS:
            page = (ROOT / "docs/capabilities" / f"{slug}.md").read_text(encoding="utf-8")
            with self.subTest(slug=slug):
                self.assertEqual(page.count('class="plugin-flow"'), 1)
                self.assertIn(">Input<", page)
                self.assertIn(">Tools<", page)
                self.assertIn(">Expected output<", page)
                self.assertIn('class="plugin-flow__tools"', page)

    def test_homepage_includes_a_responsive_architecture_diagram(self) -> None:
        diagram = ROOT / "docs/assets/images/architecture.svg"
        self.assertTrue(diagram.is_file())
        self.assertIn(
            '<img src="assets/images/architecture.svg" alt="Architecture diagram',
            self.homepage,
        )
        self.assertIn('href="assets/images/architecture.svg"', self.homepage)
        self.assertIn(".architecture-diagram img", self.css)
        self.assertIn("width: 100%;", self.css)
        self.assertIn("height: auto;", self.css)

    def test_regression_check_rejects_previous_navigation_pattern(self) -> None:
        previous_javascript = 'document.addEventListener("DOMContentSwitch", revealHero);'
        previous_css = """
        .opp-js .opp-hero__copy,
        .opp-js .opp-hero__aside { opacity: 0; }
        """
        errors = navigation_lifecycle_errors(
            self.config, previous_css, previous_javascript
        )
        self.assertIn(
            "extra.js uses unsupported DOMContentSwitch with navigation.instant", errors
        )
        self.assertIn(
            "hero content is hidden until JavaScript mutates page state", errors
        )

    def test_direct_compliance_approval_and_autonomy_claims_are_rejected(self) -> None:
        prohibited = (
            "Outputs are compliant.",
            "This output is approved.",
            "The platform offers autonomous operation.",
            "The system is fully compliant.",
            "The workflow supports autonomous approval.",
            "These are compliant outputs.",
            "These are approved outputs.",
            "The report is MLR approved.",
            "No human review is required.",
        )
        for statement in prohibited:
            with self.subTest(statement=statement):
                self.assertTrue(find_prohibited_assurances(statement))

    def test_boundary_language_is_not_misclassified_as_an_assurance(self) -> None:
        allowed = (
            "Outputs are not compliant and this output is not approved.",
            "This is a review aid, not an autonomous operation.",
            "Campaign materials are drafts for qualified MLR review, not evidence of approval.",
            "Use approved documents as inputs.",
        )
        for statement in allowed:
            with self.subTest(statement=statement):
                self.assertEqual(find_prohibited_assurances(statement), [])

    def test_config_and_visible_versions_match_release_snapshot(self) -> None:
        self.assertEqual(
            capability_version_errors(self.config, self.homepage, self.release), []
        )

        stale_config = copy.deepcopy(self.config)
        stale_config["extra"]["capability_versions"]["hcp_intelligence"] = "9.9.9"
        self.assertIn(
            "mkdocs.yml capability_versions differ from release.json",
            capability_version_errors(stale_config, self.homepage, self.release),
        )

        current_hcp = self.release["capabilities"]["HCP Intelligence"]
        stale_homepage = self.homepage.replace(f"HCP {current_hcp}", "HCP 9.9.9")
        self.assertIn(
            "homepage visible version tags differ from release.json",
            capability_version_errors(self.config, stale_homepage, self.release),
        )

    def test_repository_link_override_points_to_public_website_source(self) -> None:
        partial = (ROOT / "overrides/partials/source.html").read_text(encoding="utf-8")
        self.assertIn(
            'href="https://github.com/PharmaGenAI/pharmagenai.github.io"', partial
        )
        self.assertIn("Website source", partial)
        self.assertNotIn('data-md-component="source"', partial)

    def test_favicon_ico_is_a_real_windows_icon_fallback(self) -> None:
        favicon = ROOT / "docs/favicon.ico"
        self.assertTrue(favicon.is_file())
        if not favicon.is_file():
            return
        self.assertEqual(favicon.read_bytes()[:4], b"\x00\x00\x01\x00")

    def test_preview_dossier_headings_wrap_long_release_tokens(self) -> None:
        match = re.search(
            r"\.preview-dossier h2,\s*\.preview-dossier h3\s*\{([^}]*)\}",
            self.css,
            re.DOTALL,
        )
        self.assertIsNotNone(match)
        block = match.group(1)
        self.assertIn("overflow-wrap: anywhere;", block)
        self.assertIn("word-break: break-word;", block)

    def test_every_capability_has_a_valid_sample_manifest(self) -> None:
        for slug, capability in CAPABILITY_SLUGS.items():
            with self.subTest(capability=capability):
                manifest_path = ROOT / "docs/examples" / slug / "manifest.yml"
                manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
                self.assertEqual(tuple(manifest), MANIFEST_KEYS)
                self.assertEqual(
                    sample_manifest_errors(
                        manifest, manifest_path, slug, capability, self.release
                    ),
                    [],
                )

    def test_manifest_validation_rejects_malformed_provenance_and_missing_disclosure(self) -> None:
        slug = "hcp-intelligence"
        capability = CAPABILITY_SLUGS[slug]
        manifest_path = ROOT / "docs/examples" / slug / "manifest.yml"
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        manifest["capability_version"] = "not-semver"
        manifest["notes"] = "Representative sample."
        errors = sample_manifest_errors(
            manifest, manifest_path, slug, capability, self.release
        )
        self.assertTrue(any("capability_version must be semver" in error for error in errors))
        self.assertTrue(any("not current runtime-generated" in error for error in errors))

    def test_manifest_artifact_provenance_may_predate_site_release(self) -> None:
        slug = "hcp-intelligence"
        capability = CAPABILITY_SLUGS[slug]
        manifest_path = ROOT / "docs/examples" / slug / "manifest.yml"
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        future_release = copy.deepcopy(self.release)
        future_release["source_commit"] = "1234567890abcdef1234567890abcdef12345678"
        future_release["distribution_version"] = "2.3.0"
        future_release["capabilities"][capability] = "1.0.3"
        self.assertEqual(
            sample_manifest_errors(
                manifest, manifest_path, slug, capability, future_release
            ),
            [],
        )

    def test_nbe_manifest_requires_generated_fixture_status_and_disclosure(self) -> None:
        slug = "next-best-engagement"
        capability = CAPABILITY_SLUGS[slug]
        manifest_path = ROOT / "docs/examples" / slug / "manifest.yml"
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        manifest["status"] = "validated-representative"
        manifest["notes"] = "Representative sample."
        errors = sample_manifest_errors(
            manifest, manifest_path, slug, capability, self.release
        )
        self.assertTrue(any("status" in error for error in errors))
        self.assertTrue(any("runtime-generated fixture provenance" in error for error in errors))

    def test_nbe_manifest_rejects_note_that_disagrees_with_artifact_version(self) -> None:
        slug = "next-best-engagement"
        capability = CAPABILITY_SLUGS[slug]
        manifest_path = ROOT / "docs/examples" / slug / "manifest.yml"
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        manifest["capability_version"] = "1.0.3"
        manifest["notes"] = (
            "This sample uses the exact pinned built-in fictional demo fixture. "
            "The published output.json was last runtime-generated from it on 2026-08-30 "
            "with Next-Best-Engagement 1.0.2. This release-synchronization update did not "
            "regenerate the sample artifact."
        )
        errors = sample_manifest_errors(
            manifest, manifest_path, slug, capability, self.release
        )
        self.assertTrue(any("runtime-generated note must match capability_version" in error for error in errors))

    def test_capability_pages_link_to_their_local_example_files(self) -> None:
        for slug in CAPABILITY_SLUGS:
            with self.subTest(slug=slug):
                page_text = (ROOT / "docs/capabilities" / f"{slug}.md").read_text(
                    encoding="utf-8"
                )
                manifest_path = ROOT / "docs/examples" / slug / "manifest.yml"
                manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
                targets = link_targets(page_text)
                self.assertIn(
                    f"../examples/{slug}/{manifest['input_path']}",
                    targets,
                )
                self.assertIn(
                    f"../examples/{slug}/{manifest['output_path']}",
                    targets,
                )
                self.assertIn(f"../examples/{slug}/manifest.yml", targets)

    def test_examples_index_links_every_guide_download_and_manifest(self) -> None:
        page_text = (ROOT / "docs/examples/index.md").read_text(encoding="utf-8")
        targets = link_targets(page_text)
        for slug in CAPABILITY_SLUGS:
            with self.subTest(slug=slug):
                manifest = yaml.safe_load(
                    (ROOT / "docs/examples" / slug / "manifest.yml").read_text(
                        encoding="utf-8"
                    )
                )
                self.assertIn(f"../capabilities/{slug}.md", targets)
                self.assertIn(f"{slug}/{manifest['input_path']}", targets)
                self.assertIn(f"{slug}/{manifest['output_path']}", targets)
                self.assertIn(f"{slug}/manifest.yml", targets)

    def test_nbe_public_sample_matches_fixture_metrics_and_page_claims(self) -> None:
        page_text = (ROOT / "docs/capabilities/next-best-engagement.md").read_text(
            encoding="utf-8"
        )
        errors = nbe_public_sample_errors(
            page_text,
            ROOT / "docs/examples/next-best-engagement/input.csv",
            ROOT / "docs/examples/next-best-engagement/output.json",
        )
        self.assertEqual(errors, [])

    def test_nbe_public_sample_detects_page_metric_drift(self) -> None:
        page_text = (
            ROOT / "docs/capabilities/next-best-engagement.md"
        ).read_text(encoding="utf-8").replace("76 planned\nactions", "75 planned\nactions")
        errors = nbe_public_sample_errors(
            page_text,
            ROOT / "docs/examples/next-best-engagement/input.csv",
            ROOT / "docs/examples/next-best-engagement/output.json",
        )
        self.assertTrue(any("76 planned actions" in error for error in errors))

    def test_nbe_public_sample_requires_exact_priority_visit_example(self) -> None:
        page_text = (ROOT / "docs/capabilities/next-best-engagement.md").read_text(
            encoding="utf-8"
        ).replace("`HCP-E-003` is a priority-1 `in_person_visit`", "one high-priority visit")
        errors = nbe_public_sample_errors(
            page_text,
            ROOT / "docs/examples/next-best-engagement/input.csv",
            ROOT / "docs/examples/next-best-engagement/output.json",
        )
        self.assertTrue(any("priority-1 visit example" in error for error in errors))

    def test_nbe_public_sample_requires_exact_no_consent_example(self) -> None:
        page_text = (ROOT / "docs/capabilities/next-best-engagement.md").read_text(
            encoding="utf-8"
        ).replace(
            "`HCP-E-015` is `unassigned`\nwith reason `no_consent`",
            "one unassigned record with reason no_consent",
        )
        errors = nbe_public_sample_errors(
            page_text,
            ROOT / "docs/examples/next-best-engagement/input.csv",
            ROOT / "docs/examples/next-best-engagement/output.json",
        )
        self.assertTrue(any("no_consent example" in error for error in errors))

    def test_release_snapshot_contract_is_dynamic_but_strict(self) -> None:
        self.assertEqual(release_metadata_errors(self.release), [])

        stale_release = copy.deepcopy(self.release)
        stale_release["source_commit"] = "not-a-sha"
        errors = release_metadata_errors(stale_release)
        self.assertIn(
            "release.json source_commit must be a 7-40 character lowercase git SHA",
            errors,
        )

    def test_private_canonical_links_require_exact_access_label(self) -> None:
        text = (
            "[Guide](https://github.com/PharmaGenAI/open-pharma-plugins/blob/"
            "6bfc6ce43491d66b4ef45b1d3934a58648e1afc6/docs/en/installation.md)"
        )
        errors = private_canonical_access_errors("docs/get-started.md", text)
        self.assertIn(
            "docs/get-started.md: private canonical links require the exact access label",
            errors,
        )

    def test_private_canonical_root_link_requires_exact_access_label(self) -> None:
        text = "[Repository](https://github.com/PharmaGenAI/open-pharma-plugins)"
        errors = private_canonical_access_errors("docs/get-started.md", text)
        self.assertIn(
            "docs/get-started.md: private canonical links require the exact access label",
            errors,
        )

    def test_technical_reference_private_rows_must_include_access_label(self) -> None:
        text = (
            "## Authorized repository access required\n"
            "| Need | Link | Access |\n"
            "| --- | --- | --- |\n"
            "| Install | [docs](https://github.com/PharmaGenAI/open-pharma-plugins/blob/"
            "6bfc6ce43491d66b4ef45b1d3934a58648e1afc6/docs/en/installation.md) | missing |\n"
        )
        errors = private_canonical_access_errors("docs/technical-reference.md", text)
        self.assertIn(
            "docs/technical-reference.md: each private canonical table row must include the exact access label",
            errors,
        )

    def test_technical_reference_private_tables_require_markdown_table_blocks(self) -> None:
        text = (
            "## Authorized repository access required\n"
            "Private canonical links live below.\n"
            "| Need | Link | Access |\n"
            "| --- | --- | --- |\n"
            "| Install | [docs](https://github.com/PharmaGenAI/open-pharma-plugins/blob/"
            "6bfc6ce43491d66b4ef45b1d3934a58648e1afc6/docs/en/installation.md) | "
            "Authorized repository access required |\n"
            "## Authorized repository access required\n"
            "Cookbooks live below.\n"
            "| Capability | Pinned cookbook | Access |\n"
            "| --- | --- | --- |\n"
            "| HCP Intelligence | [cookbooks](https://github.com/PharmaGenAI/open-pharma-plugins/blob/"
            "6bfc6ce43491d66b4ef45b1d3934a58648e1afc6/cookbooks/hcp-intelligence/usage.md) | "
            "Authorized repository access required |\n"
        )
        errors = technical_reference_errors(text, self.release)
        self.assertIn(
            "docs/technical-reference.md: private canonical access tables must stay in Markdown table blocks",
            errors,
        )


if __name__ == "__main__":
    unittest.main()
