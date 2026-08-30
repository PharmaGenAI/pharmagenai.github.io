---
title: Release sync
description: Repository-dispatch contract and review workflow for synchronizing pinned Open Pharma Plugins release metadata into this site.
---

# Release sync operating contract

This site duplicates a small amount of release-sensitive content from
`PharmaGenAI/open-pharma-plugins`: the pinned source commit, distribution version, capability versions, visible
release badges, and version-aware GitHub links. Synchronization is review-gated. The workflow opens a pull
request; it does not auto-merge, auto-deploy, or claim that example artifacts were regenerated.

## Accepted triggers

| Trigger | Intended use |
| --- | --- |
| `repository_dispatch` with type `open-pharma-plugins-release` | Canonical repository notifies this site after a tagged upstream capability release |
| `workflow_dispatch` | Maintainer reruns the validation and sync flow manually with explicit inputs |

## Dispatch payload

The upstream sender should post the following `client_payload` to the site repository:

```json
{
  "repository": "PharmaGenAI/open-pharma-plugins",
  "capability": "next-best-engagement",
  "tag": "open-pharma-plugins-next-best-engagement-v1.0.2",
  "commit": "6bfc6ce43491d66b4ef45b1d3934a58648e1afc6",
  "distribution_version": "2.2.1",
  "plugin_version": "1.0.2"
}
```

The workflow independently validates all of the following before it changes any tracked file:

- the repository is exactly `PharmaGenAI/open-pharma-plugins`
- the tag resolves to the exact supplied commit through the GitHub API
- the hardcoded `plugin-versions.json` at that commit exists and matches the payload's distribution and capability version
- the tag format matches `open-pharma-plugins-{capability}-v{version}`

## Required credentials

Use two distinct, least-privilege machine credentials. Never create one cross-repository token with both canonical-read
and site-write access.

1. The canonical repository stores a narrow dispatch-only token that can call the
   `PharmaGenAI/pharmagenai.github.io` repository-dispatch endpoint. Limit its repository selection to this site and
   grant only the endpoint permission needed for repository dispatch. Do not grant it canonical-repository read access.
2. The site repository stores a separate canonical-read-only `OPEN_PHARMA_PAGES_SYNC_TOKEN`. Limit its repository
   selection to `PharmaGenAI/open-pharma-plugins` with `Contents: read`; the release-sync workflow uses it only to
   resolve the upstream tag and read the pinned `plugin-versions.json` through the GitHub API.

The site workflow's repository-scoped `GITHUB_TOKEN` handles its own branch push and pull request with
`contents: write` and `pull-requests: write`. Neither cross-repository credential should be a local interactive `gh`
token or a broad classic PAT.

## What the workflow updates

- `docs/assets/data/release.json`
- duplicated release metadata in `mkdocs.yml`
- visible release badges and pinned GitHub links in site pages
- every visible version-pinned PyPI URL, including the utility footer link

## What the workflow must not imply

- Sample manifests, inputs, and outputs remain byte-for-byte unchanged. Their version and source fields are immutable
  artifact-generation provenance, even when the site release advances.
- It does not claim or imply that a representative or runtime-generated sample was regenerated for the new site release.
- It does not publish the site. A maintainer still reviews and merges the pull request before the Pages workflow can deploy the updated claims.

<aside class="evidence-note evidence-note--boundary" aria-labelledby="sync-boundary">
  <h2 id="sync-boundary">Release metadata and sample provenance are related but not identical</h2>
  <p>The site can move to a newer pinned release while a public sample still discloses that it was last generated earlier. That distinction is deliberate and should stay visible in review.</p>
</aside>

[Open the technical reference landing page →](../technical-reference.md){ .opp-button .opp-button--primary }
