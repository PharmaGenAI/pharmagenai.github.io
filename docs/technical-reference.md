---
title: Technical reference
description: Version-pinned links to the canonical Open Pharma Plugins installation, configuration, security, and release documentation.
---

# Technical reference

This site keeps business guidance local. Technical truth stays in the canonical repository. Use the pinned links
below for installation, configuration, release policy, and capability behavior for this site edition.

[Open the Open Pharma Plugins repository →](https://github.com/PharmaGenAI/open-pharma-plugins){ .opp-button .opp-button--primary }

## Pinned release this site describes

<div class="preview-dossier" markdown="1">
  <div class="preview-label">Release truth</div>
  <div markdown="1">
### Distribution 2.4.1 from source commit bf1518dee6a56f8410feb3058672bfbb479d0bc8

The machine-readable [release snapshot](assets/data/release.json) records the exact release data shown here. The
visible short SHA `bf1518d` is derived from the full pinned source commit for display only.

The release-sync workflow validates the upstream tag, full commit, and hardcoded `plugin-versions.json` before
opening a review PR for a future update.
  </div>
</div>

## Installation and repository paths

| Need | Canonical path |
| --- | --- |
| Browse the source, installer, and documentation | [Open Pharma Plugins repository](https://github.com/PharmaGenAI/open-pharma-plugins) |
| Install in Claude Code, Codex, or GitHub Copilot CLI | Clone the repository, inspect the pinned [install.sh](https://github.com/PharmaGenAI/open-pharma-plugins/blob/bf1518dee6a56f8410feb3058672bfbb479d0bc8/install.sh), then run `bash install.sh` |
| Install the published Python distribution | Public PyPI project for [open-pharma-plugins 2.4.1](https://pypi.org/project/open-pharma-plugins/2.4.1/) |
| Review business guidance and fictional examples | This site's [Get started](get-started.md), [Examples](examples/index.md), and capability pages |
| Inspect the pinned release truth this site duplicates | Machine-readable [release snapshot](assets/data/release.json) |

## Pinned repository documents

| Need | Pinned canonical document |
| --- | --- |
| Repository overview | [README](https://github.com/PharmaGenAI/open-pharma-plugins/blob/bf1518dee6a56f8410feb3058672bfbb479d0bc8/README.md) |
| Installation surfaces and exact commands | [docs/en/installation.md](https://github.com/PharmaGenAI/open-pharma-plugins/blob/bf1518dee6a56f8410feb3058672bfbb479d0bc8/docs/en/installation.md) |
| Configuration variables and defaults | [docs/en/configuration.md](https://github.com/PharmaGenAI/open-pharma-plugins/blob/bf1518dee6a56f8410feb3058672bfbb479d0bc8/docs/en/configuration.md) |
| Data security and compliance boundaries | [docs/en/data_security.md](https://github.com/PharmaGenAI/open-pharma-plugins/blob/bf1518dee6a56f8410feb3058672bfbb479d0bc8/docs/en/data_security.md) |
| Local development | [docs/en/local_development.md](https://github.com/PharmaGenAI/open-pharma-plugins/blob/bf1518dee6a56f8410feb3058672bfbb479d0bc8/docs/en/local_development.md) |
| Testing and offline verification | [docs/en/testing.md](https://github.com/PharmaGenAI/open-pharma-plugins/blob/bf1518dee6a56f8410feb3058672bfbb479d0bc8/docs/en/testing.md) |
| Release process and invariants | [docs/en/releasing.md](https://github.com/PharmaGenAI/open-pharma-plugins/blob/bf1518dee6a56f8410feb3058672bfbb479d0bc8/docs/en/releasing.md) |
| Guided installer source | [install.sh](https://github.com/PharmaGenAI/open-pharma-plugins/blob/bf1518dee6a56f8410feb3058672bfbb479d0bc8/install.sh) |
| Capability release index | [plugin-versions.json](https://github.com/PharmaGenAI/open-pharma-plugins/blob/bf1518dee6a56f8410feb3058672bfbb479d0bc8/plugin-versions.json) |

## Pinned capability cookbooks

| Capability | Pinned cookbook |
| --- | --- |
| HCP Intelligence | [cookbooks/hcp-intelligence/usage.md](https://github.com/PharmaGenAI/open-pharma-plugins/blob/bf1518dee6a56f8410feb3058672bfbb479d0bc8/cookbooks/hcp-intelligence/usage.md) |
| Competitive Intelligence | [cookbooks/competitive-intelligence/usage.md](https://github.com/PharmaGenAI/open-pharma-plugins/blob/bf1518dee6a56f8410feb3058672bfbb479d0bc8/cookbooks/competitive-intelligence/usage.md) |
| Territory Alignment | [cookbooks/territory-alignment/usage.md](https://github.com/PharmaGenAI/open-pharma-plugins/blob/bf1518dee6a56f8410feb3058672bfbb479d0bc8/cookbooks/territory-alignment/usage.md) |
| Next-Best-Engagement | [cookbooks/next-best-engagement/usage.md](https://github.com/PharmaGenAI/open-pharma-plugins/blob/bf1518dee6a56f8410feb3058672bfbb479d0bc8/cookbooks/next-best-engagement/usage.md) |
| Field Training | [cookbooks/field-training/usage.md](https://github.com/PharmaGenAI/open-pharma-plugins/blob/bf1518dee6a56f8410feb3058672bfbb479d0bc8/cookbooks/field-training/usage.md) |
| Campaign Studio | [cookbooks/campaign-studio/usage.md](https://github.com/PharmaGenAI/open-pharma-plugins/blob/bf1518dee6a56f8410feb3058672bfbb479d0bc8/cookbooks/campaign-studio/usage.md) |

## Website-specific automation

The following material belongs to this Pages repository rather than the canonical plugin repository:

- [Release sync operating contract](operations/release-sync.md)
- [GitHub Actions workflows directory](https://github.com/PharmaGenAI/pharmagenai.github.io/tree/main/.github/workflows)

<aside class="evidence-note" aria-labelledby="reference-boundary">
  <h2 id="reference-boundary">Use the repository for exact behavior changes</h2>
  <p>The site summarizes business usage and review boundaries. When a command, environment variable, capability version, or release step matters operationally, follow the pinned GitHub document for that exact source revision.</p>
</aside>

[Start with installation choices →](get-started.md){ .opp-button .opp-button--primary }
[Read the trust boundaries first →](trust-governance.md){ .opp-button }
