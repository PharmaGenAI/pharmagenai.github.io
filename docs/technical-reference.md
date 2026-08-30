---
title: Technical reference
description: Version-pinned links to the canonical Open Pharma Plugins installation, configuration, security, and release documentation.
---

# Technical reference

This site keeps business guidance local, but technical truth stays in the canonical
`PharmaGenAI/open-pharma-plugins` repository. Use the pinned links below when you need installation details,
configuration fields, release policy, or capability-specific cookbook behavior for the exact site edition.

## Pinned release this site describes

<div class="preview-dossier" markdown="1">
  <div class="preview-label">Release truth</div>
  <div markdown="1">
### Distribution 2.2.1 from source commit 6bfc6ce43491d66b4ef45b1d3934a58648e1afc6

The machine-readable [release snapshot](assets/data/release.json) records the exact duplicated release data this
site displays. The visible short SHA `6bfc6ce` is derived from that full pinned source commit for display only.
The release-sync workflow validates the upstream tag, full source commit, and hardcoded `plugin-versions.json`
before opening a review PR for any future update.
  </div>
</div>

## Public paths available today

| Need | Public path |
| --- | --- |
| Install a released MCP server without repository access | Public PyPI project for [open-pharma-plugins 2.2.1](https://pypi.org/project/open-pharma-plugins/2.2.1/) |
| Review business guidance and fictional examples | This site's [Get started](get-started.md), [Examples](examples/index.md), and capability pages |
| Inspect the pinned release truth this site duplicates | Machine-readable [release snapshot](assets/data/release.json) |

## Authorized repository access required

These links are version-pinned into the private canonical repository. Use them only after GitHub access to
`PharmaGenAI/open-pharma-plugins` has been granted.


| Need | Pinned canonical document | Access |
| --- | --- | --- |
| Repository overview | [README](https://github.com/PharmaGenAI/open-pharma-plugins/blob/6bfc6ce43491d66b4ef45b1d3934a58648e1afc6/README.md) | Authorized repository access required |
| Installation surfaces and exact commands | [docs/en/installation.md](https://github.com/PharmaGenAI/open-pharma-plugins/blob/6bfc6ce43491d66b4ef45b1d3934a58648e1afc6/docs/en/installation.md) | Authorized repository access required |
| Configuration variables and defaults | [docs/en/configuration.md](https://github.com/PharmaGenAI/open-pharma-plugins/blob/6bfc6ce43491d66b4ef45b1d3934a58648e1afc6/docs/en/configuration.md) | Authorized repository access required |
| Data security and compliance boundaries | [docs/en/data_security.md](https://github.com/PharmaGenAI/open-pharma-plugins/blob/6bfc6ce43491d66b4ef45b1d3934a58648e1afc6/docs/en/data_security.md) | Authorized repository access required |
| Local development | [docs/en/local_development.md](https://github.com/PharmaGenAI/open-pharma-plugins/blob/6bfc6ce43491d66b4ef45b1d3934a58648e1afc6/docs/en/local_development.md) | Authorized repository access required |
| Testing and offline verification | [docs/en/testing.md](https://github.com/PharmaGenAI/open-pharma-plugins/blob/6bfc6ce43491d66b4ef45b1d3934a58648e1afc6/docs/en/testing.md) | Authorized repository access required |
| Release process and invariants | [docs/en/releasing.md](https://github.com/PharmaGenAI/open-pharma-plugins/blob/6bfc6ce43491d66b4ef45b1d3934a58648e1afc6/docs/en/releasing.md) | Authorized repository access required |
| Guided installer source | [install.sh](https://github.com/PharmaGenAI/open-pharma-plugins/blob/6bfc6ce43491d66b4ef45b1d3934a58648e1afc6/install.sh) | Authorized repository access required |
| Capability release index | [plugin-versions.json](https://github.com/PharmaGenAI/open-pharma-plugins/blob/6bfc6ce43491d66b4ef45b1d3934a58648e1afc6/plugin-versions.json) | Authorized repository access required |

## Authorized repository access required

The capability cookbooks below are also version-pinned into the private canonical repository.


| Capability | Pinned cookbook | Access |
| --- | --- | --- |
| HCP Intelligence | [cookbooks/hcp-intelligence/usage.md](https://github.com/PharmaGenAI/open-pharma-plugins/blob/6bfc6ce43491d66b4ef45b1d3934a58648e1afc6/cookbooks/hcp-intelligence/usage.md) | Authorized repository access required |
| Competitive Intelligence | [cookbooks/competitive-intelligence/usage.md](https://github.com/PharmaGenAI/open-pharma-plugins/blob/6bfc6ce43491d66b4ef45b1d3934a58648e1afc6/cookbooks/competitive-intelligence/usage.md) | Authorized repository access required |
| Territory Alignment | [cookbooks/territory-alignment/usage.md](https://github.com/PharmaGenAI/open-pharma-plugins/blob/6bfc6ce43491d66b4ef45b1d3934a58648e1afc6/cookbooks/territory-alignment/usage.md) | Authorized repository access required |
| Next-Best-Engagement | [cookbooks/next-best-engagement/usage.md](https://github.com/PharmaGenAI/open-pharma-plugins/blob/6bfc6ce43491d66b4ef45b1d3934a58648e1afc6/cookbooks/next-best-engagement/usage.md) | Authorized repository access required |
| Field Training | [cookbooks/field-training/usage.md](https://github.com/PharmaGenAI/open-pharma-plugins/blob/6bfc6ce43491d66b4ef45b1d3934a58648e1afc6/cookbooks/field-training/usage.md) | Authorized repository access required |
| Campaign Studio | [cookbooks/campaign-studio/usage.md](https://github.com/PharmaGenAI/open-pharma-plugins/blob/6bfc6ce43491d66b4ef45b1d3934a58648e1afc6/cookbooks/campaign-studio/usage.md) | Authorized repository access required |

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
