---
title: Trust and governance
description: Human-review boundaries, data handling expectations, evidence requirements, and public-beta limits for Open Pharma Plugins.
---

# Trust and governance boundaries

Open Pharma Plugins is local-first software, but local-first does not remove governance work. Teams remain
responsible for deciding whether the data, provider configuration, rendered output, and intended use are
permitted in their organization and jurisdiction.

## Human review is part of the workflow

No capability removes accountable business, medical, legal, privacy, or regulatory judgement.

| Workflow area | What the software can structure | What a qualified person still decides |
| --- | --- | --- |
| Public-source intelligence | Retrieval, summarisation, evidence grouping, and source display | Identity match, source sufficiency, and whether a conclusion is decision-ready |
| Territory and engagement planning | Constraint application, trade-off visibility, and candidate actions | Whether data rights, consent, coverage rules, staffing, and field practicality support execution |
| Training and campaign drafting | Source or claim grounding, packaging, validation gates, and render output | Medical accuracy, fair balance, jurisdictional fit, legal review, approval status, and distribution readiness |

## Data boundaries

Mutable data defaults under `~/.open-pharma-plugins` with restrictive local file permissions where supported,
but those permissions are not enterprise access control, encryption, backup, or retention management.

- Keep provider keys in `~/.open-pharma-plugins/config` or the process environment.
- Run servers with least-privilege filesystem access.
- Do not place credentials, confidential strategy, private source content, or unnecessary personal data in search queries.
- Move capability data directories to approved managed storage when local defaults are not sufficient.

## Evidence and traceability

The useful output is usually not the text alone. It is the combination of output, source references, input
scope, limitations, and who still needs to review it.

<div class="outcome-list">
  <section class="outcome-row">
    <span class="outcome-id">SOURCE</span>
    <h3>Evidence should stay visible</h3>
    <p>Use outputs that keep source references, retrieval timing, or claim support attached to the decision artifact.</p>
    <span class="version-tag">TRACE</span>
  </section>
  <section class="outcome-row">
    <span class="outcome-id">SCOPE</span>
    <h3>Coverage limits should stay explicit</h3>
    <p>Competitive Intelligence source status, HCP identity ambiguity, and scenario exclusions are part of the result.</p>
    <span class="version-tag">BOUND</span>
  </section>
  <section class="outcome-row">
    <span class="outcome-id">REVIEW</span>
    <h3>Approval state is external</h3>
    <p>Generated drafts and recommendations do not become approved because they passed a schema or validation gate.</p>
    <span class="version-tag">HUMAN</span>
  </section>
</div>

## Public-beta limits

Public beta means the site and plugin help teams inspect workflows safely, but they do not claim that every
release has regenerated every sample artifact or that every operational edge case has been validated.

- Validate source coverage, identities, assumptions, and rendered assets before operational use.
- Treat the public examples as fictional training material, not as production templates.
- Confirm release-specific technical behavior in the canonical repository, not from summary copy on this site.

## Capability-specific boundaries

| Capability | Material boundary to review |
| --- | --- |
| HCP Intelligence | Public-source evidence can still include personal data; confirm identity, minimisation, and whether optional synthesis is permitted |
| Competitive Intelligence | Source status can be complete, partial, failed, or not configured; lack of evidence is not proof that an event did not occur |
| Territory Alignment | The default consolidated report stays offline; explicitly selecting the public basemap can send map extent or coordinates to CARTO/OpenStreetMap providers |
| Next-Best-Engagement | Plans depend on governed consent, recency, capacity, and assignment inputs; recommendations do not authorize outreach |
| Field Training | Generated claims and model answers must stay tied to the supplied approved source set; output is still a draft for qualified MLR review |
| Campaign Studio | Input, channel, and rendered-file gates plus package hashes support review, but they do not approve content or authorize sending, publishing, or distribution |

<aside class="evidence-note evidence-note--boundary" aria-labelledby="governance-boundary">
  <h2 id="governance-boundary">Review boundaries differ by capability, but they never disappear</h2>
  <p>Use the narrowest workflow, the minimum permitted data, and the clearest evidence trail. If the data rights, approval state, or reviewer ownership are uncertain, stop at the fictional or sandbox stage until those boundaries are resolved.</p>
</aside>

[Open the version-pinned technical references →](technical-reference.md){ .opp-button .opp-button--primary }
[Review the release-sync operating contract →](operations/release-sync.md){ .opp-button }
