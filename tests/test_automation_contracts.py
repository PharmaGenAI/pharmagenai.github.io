from __future__ import annotations

import copy
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import scripts.sync_release as sync_release
from scripts.check_workflows import load_workflows, workflow_contract_errors
from scripts.sync_release import (
    build_release_snapshot,
    sync_site_release,
    validate_payload,
)
from scripts.check_content import expected_public_pypi_url, technical_reference_errors


ROOT = Path(__file__).resolve().parents[1]


class AutomationContractsTest(unittest.TestCase):
    def make_temp_site_root(self) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        root = Path(temp_dir.name)
        shutil.copytree(ROOT / "docs", root / "docs")
        shutil.copytree(ROOT / "overrides", root / "overrides")
        for relative in ("mkdocs.yml", "requirements.txt", "requirements.lock"):
            shutil.copy2(ROOT / relative, root / relative)
        (root / "scripts").mkdir()
        shutil.copy2(ROOT / "scripts/check_content.py", root / "scripts/check_content.py")
        return root

    @staticmethod
    def sample_hashes(root: Path) -> dict[str, str]:
        return {
            path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted((root / "docs/examples").glob("*/*"))
            if path.is_file()
        }

    def test_workflows_match_local_contract(self) -> None:
        self.assertEqual(workflow_contract_errors(load_workflows()), [])

    def test_workflow_contract_rejects_floating_action_ref(self) -> None:
        workflows = load_workflows()
        workflows["ci.yml"]["jobs"]["docs"]["steps"][0]["uses"] = "actions/checkout@v5"
        errors = workflow_contract_errors(workflows)
        self.assertTrue(any("40-character SHA" in error for error in errors))

    def test_workflow_contract_rejects_missing_release_dispatch_type(self) -> None:
        workflows = load_workflows()
        workflows["release-sync.yml"]["on"]["repository_dispatch"]["types"] = ["wrong-type"]
        errors = workflow_contract_errors(workflows)
        self.assertIn(
            "release-sync.yml repository_dispatch type must be open-pharma-plugins-release",
            errors,
        )

    def test_workflow_contract_rejects_github_expressions_inside_shell(self) -> None:
        workflows = load_workflows()
        sync_steps = workflows["release-sync.yml"]["jobs"]["sync"]["steps"]
        sync_steps[-1]["run"] += '\necho "${{ steps.meta.outputs.branch }}"'
        errors = workflow_contract_errors(workflows)
        self.assertTrue(any("direct GitHub expression" in error for error in errors))

    def test_workflow_contract_rejects_repository_github_token_for_pr_creation(self) -> None:
        workflows = load_workflows()
        sync_steps = workflows["release-sync.yml"]["jobs"]["sync"]["steps"]
        sync_steps[-1]["env"]["GH_TOKEN"] = "${{ github.token }}"

        errors = workflow_contract_errors(workflows)

        self.assertIn("release-sync.yml must not use GITHUB_TOKEN for PR API calls", errors)
        self.assertIn("release-sync.yml must use OPEN_PHARMA_PAGES_PR_TOKEN for PR API calls", errors)

    def test_workflow_contract_rejects_gh_pr_graphql_helpers(self) -> None:
        workflows = load_workflows()
        sync_steps = workflows["release-sync.yml"]["jobs"]["sync"]["steps"]
        sync_steps[-1]["run"] += '\ngh pr create --base main --head "$BRANCH_NAME" --title "$PR_TITLE"'

        errors = workflow_contract_errors(workflows)

        self.assertIn("release-sync.yml must use direct REST calls rather than gh pr GraphQL helpers", errors)

    def test_workflow_contract_rejects_pr_token_guard_after_side_effects(self) -> None:
        workflows = load_workflows()
        sync_steps = workflows["release-sync.yml"]["jobs"]["sync"]["steps"]
        pr_step = sync_steps[-1]
        guard = 'if [ -z "$GH_TOKEN" ]'
        pr_step["run"] = pr_step["run"].replace(guard, "if false", 1) + f"\n{guard}; then\n  exit 1\nfi\n"

        errors = workflow_contract_errors(workflows)

        self.assertIn("release-sync.yml must fail clearly when OPEN_PHARMA_PAGES_PR_TOKEN is absent", errors)

    def test_release_payload_validation_checks_tag_commit_and_index(self) -> None:
        payload = {
            "repository": "PharmaGenAI/open-pharma-plugins",
            "capability": "next-best-engagement",
            "tag": "open-pharma-plugins-next-best-engagement-v1.0.2",
            "commit": "6bfc6ce43491d66b4ef45b1d3934a58648e1afc6",
            "distribution_version": "2.2.1",
            "plugin_version": "1.0.2",
        }
        release_index = {
            "distribution_version": "2.2.1",
            "tag_format": "open-pharma-plugins-{cap}-v{version}",
            "plugins": {"next-best-engagement": "1.0.2"},
        }
        self.assertEqual(
            validate_payload(payload, payload["commit"], release_index),
            [],
        )

        stale = copy.deepcopy(payload)
        stale["plugin_version"] = "9.9.9"
        errors = validate_payload(stale, payload["commit"], release_index)
        self.assertTrue(any("payload tag must be" in error for error in errors))

    def test_release_payload_accepts_keys_in_any_order(self) -> None:
        payload = {
            "plugin_version": "1.0.2",
            "commit": "6bfc6ce43491d66b4ef45b1d3934a58648e1afc6",
            "repository": "PharmaGenAI/open-pharma-plugins",
            "distribution_version": "2.2.1",
            "tag": "open-pharma-plugins-next-best-engagement-v1.0.2",
            "capability": "next-best-engagement",
        }
        release_index = {
            "distribution_version": "2.2.1",
            "tag_format": "open-pharma-plugins-{cap}-v{version}",
            "plugins": {"next-best-engagement": "1.0.2"},
        }
        self.assertEqual(validate_payload(payload, payload["commit"], release_index), [])

    def test_release_payload_rejects_missing_key(self) -> None:
        payload = {
            "repository": "PharmaGenAI/open-pharma-plugins",
            "capability": "next-best-engagement",
            "tag": "open-pharma-plugins-next-best-engagement-v1.0.2",
            "commit": "6bfc6ce43491d66b4ef45b1d3934a58648e1afc6",
            "distribution_version": "2.2.1",
        }
        errors = validate_payload(payload, payload["commit"], {})
        self.assertTrue(any("payload keys must be exactly" in error for error in errors))

    def test_release_payload_rejects_newlines_and_malformed_release_fields(self) -> None:
        base = {
            "repository": "PharmaGenAI/open-pharma-plugins",
            "capability": "next-best-engagement",
            "tag": "open-pharma-plugins-next-best-engagement-v1.0.2",
            "commit": "6bfc6ce43491d66b4ef45b1d3934a58648e1afc6",
            "distribution_version": "2.2.1",
            "plugin_version": "1.0.2",
        }
        release_index = {
            "distribution_version": "2.2.1",
            "tag_format": "open-pharma-plugins-{cap}-v{version}",
            "plugins": {"next-best-engagement": "1.0.2"},
        }
        invalid = {
            "capability": "next-best-engagement\nbranch=owned",
            "tag": "open-pharma-plugins-next-best-engagement-v1.0.2\ntitle=owned",
            "commit": "6bfc6ce\nsource_commit=owned",
            "distribution_version": "2.2.1\nchanged=true",
            "plugin_version": "1.0.2\nbranch=owned",
        }
        expected_errors = {
            "capability": "payload capability must be a known safe slug",
            "tag": "payload tag has an invalid format",
            "commit": "payload commit must be a 40-character lowercase git SHA",
            "distribution_version": "payload distribution_version must be semver",
            "plugin_version": "payload plugin_version must be semver",
        }
        for field, value in invalid.items():
            with self.subTest(field=field):
                payload = copy.deepcopy(base)
                payload[field] = value
                errors = validate_payload(payload, payload["commit"], release_index)
                self.assertIn(expected_errors[field], errors)

    def test_branch_metadata_rejects_output_injection(self) -> None:
        builder = getattr(sync_release, "build_branch_metadata", None)
        self.assertIsNotNone(builder)
        if builder is None:
            return
        with self.assertRaisesRegex(ValueError, "run id"):
            builder(
                "next-best-engagement",
                "open-pharma-plugins-next-best-engagement-v1.0.2",
                "1.0.2",
                "123\nbranch=owned",
            )

    def test_branch_metadata_uses_validated_release_fields(self) -> None:
        builder = getattr(sync_release, "build_branch_metadata", None)
        self.assertIsNotNone(builder)
        if builder is None:
            return
        self.assertEqual(
            builder(
                "next-best-engagement",
                "open-pharma-plugins-next-best-engagement-v1.0.2",
                "1.0.2",
                "987654",
            ),
            (
                "automation/release-sync-next-best-engagement-1-0-2-987654",
                "chore: sync site release for open-pharma-plugins-next-best-engagement-v1.0.2",
            ),
        )

    def test_release_payload_rejects_extra_release_index_override_key(self) -> None:
        payload = {
            "repository": "PharmaGenAI/open-pharma-plugins",
            "capability": "next-best-engagement",
            "tag": "open-pharma-plugins-next-best-engagement-v1.0.2",
            "commit": "6bfc6ce43491d66b4ef45b1d3934a58648e1afc6",
            "distribution_version": "2.2.1",
            "plugin_version": "1.0.2",
            "release_index_path": "nested/plugin-versions.json",
        }
        release_index = {
            "distribution_version": "2.2.1",
            "tag_format": "open-pharma-plugins-{cap}-v{version}",
            "plugins": {"next-best-engagement": "1.0.2"},
        }
        errors = validate_payload(payload, payload["commit"], release_index)
        self.assertTrue(any("payload keys must be exactly" in error for error in errors))

    def test_release_sync_updates_release_snapshot_and_preserves_no_change(self) -> None:
        release_index = json.loads(
            (ROOT / "docs/assets/data/release.json").read_text(encoding="utf-8")
        )
        snapshot = build_release_snapshot(
            release_index["canonical_repository"],
            release_index["source_commit"],
            {
                "distribution_version": release_index["distribution_version"],
                "plugins": {
                    "hcp-intelligence": release_index["capabilities"]["HCP Intelligence"],
                    "field-training": release_index["capabilities"]["Field Training"],
                    "campaign-studio": release_index["capabilities"]["Campaign Studio"],
                    "next-best-engagement": release_index["capabilities"]["Next-Best-Engagement"],
                    "territory-alignment": release_index["capabilities"]["Territory Alignment"],
                    "competitive-intelligence": release_index["capabilities"]["Competitive Intelligence"],
                },
            },
        )
        root = self.make_temp_site_root()
        changed = sync_site_release(root, snapshot)
        self.assertEqual(changed, [])

    def test_release_sync_updates_technical_reference_pypi_link_dynamically(self) -> None:
        current_release = json.loads(
            (ROOT / "docs/assets/data/release.json").read_text(encoding="utf-8")
        )
        future_release = copy.deepcopy(current_release)
        future_release["source_commit"] = "1234567890abcdef1234567890abcdef12345678"
        future_release["distribution_version"] = "2.3.0"
        future_release["capabilities"]["Next-Best-Engagement"] = "1.0.3"

        root = self.make_temp_site_root()
        changed = sync_site_release(root, future_release)
        self.assertIn("docs/technical-reference.md", changed)

        technical = (root / "docs/technical-reference.md").read_text(encoding="utf-8")
        self.assertEqual(technical_reference_errors(technical, future_release), [])
        self.assertIn(expected_public_pypi_url(future_release), technical)
        self.assertIn(
            f'open-pharma-plugins {future_release["distribution_version"]}',
            technical,
        )

        config = (root / "mkdocs.yml").read_text(encoding="utf-8")
        self.assertIn(expected_public_pypi_url(future_release), config)
        self.assertNotIn(expected_public_pypi_url(current_release), config)

        short_commit = future_release["source_commit"][:7]
        self.assertIn(f"visible short SHA `{short_commit}` is derived", technical)
        self.assertNotIn("visible short SHA `6bfc6ce` is derived", technical)

        stale_technical = technical.replace(
            expected_public_pypi_url(future_release),
            expected_public_pypi_url(current_release),
        )
        errors = technical_reference_errors(stale_technical, future_release)
        self.assertIn(
            "docs/technical-reference.md: missing technical link target "
            f"{expected_public_pypi_url(future_release)!r}",
            errors,
        )

    def test_future_release_preserves_all_sample_artifacts_byte_for_byte(self) -> None:
        future_release = json.loads(
            (ROOT / "docs/assets/data/release.json").read_text(encoding="utf-8")
        )
        future_release["source_commit"] = "1234567890abcdef1234567890abcdef12345678"
        future_release["distribution_version"] = "2.3.0"
        future_release["capabilities"]["Next-Best-Engagement"] = "1.0.3"

        root = self.make_temp_site_root()
        before = self.sample_hashes(root)
        sync_site_release(root, future_release)
        self.assertEqual(self.sample_hashes(root), before)

    def test_future_release_with_older_sample_provenance_passes_content_validation(self) -> None:
        future_release = json.loads(
            (ROOT / "docs/assets/data/release.json").read_text(encoding="utf-8")
        )
        future_release["source_commit"] = "1234567890abcdef1234567890abcdef12345678"
        future_release["distribution_version"] = "2.3.0"
        future_release["capabilities"]["Next-Best-Engagement"] = "1.0.3"

        root = self.make_temp_site_root()
        sync_site_release(root, future_release)
        homepage = (root / "docs/index.md").read_text(encoding="utf-8")
        self.assertNotIn("Public beta", homepage)
        self.assertNotIn("Pinned source", homepage)
        self.assertIn("bash install.sh", homepage)
        self.assertIn("Claude Code, Codex, or GitHub Copilot CLI", homepage)
        self.assertNotIn("Technical truth stays with the release", homepage)
        self.assertIn(
            'open-pharma-plugins[hcp-intelligence]==2.3.0',
            homepage,
        )
        result = subprocess.run(
            [sys.executable, "scripts/check_content.py"],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_workflow_contract_rejects_release_index_override(self) -> None:
        workflows = load_workflows()
        workflows["release-sync.yml"]["jobs"]["sync"]["steps"][3]["run"] += (
            "\npython scripts/sync_release.py --release-index-path nested/plugin-versions.json"
        )
        errors = workflow_contract_errors(workflows)
        self.assertIn(
            "release-sync.yml must not expose a release_index_path override",
            errors,
        )


if __name__ == "__main__":
    unittest.main()
