---
title: Fictional examples
description: A guide to the representative, fictional input and output examples for all six Open Pharma Plugins capabilities.
---

# Examples designed for inspection

The examples in this site are **fictional and representative**. They contain no real HCP, employee, customer,
or patient data. Their purpose is to show the shape of an input, the decisions in a workflow, the form of an
output, and the review boundary—not to promise a particular result.

## What every example will include

<div class="outcome-list">
  <section class="outcome-row">
    <span class="outcome-id">A / INPUT</span>
    <h3>A small, readable starting artifact</h3>
    <p>Only the fields needed to understand the workflow, with fictional identities and values clearly marked.</p>
    <span class="version-tag">FICTIONAL</span>
  </section>
  <section class="outcome-row">
    <span class="outcome-id">B / OUTPUT</span>
    <h3>A representative output excerpt</h3>
    <p>Enough structure to inspect traceability, assumptions, limitations, and the decision the artifact supports.</p>
    <span class="version-tag">REPRESENTATIVE</span>
  </section>
  <section class="outcome-row">
    <span class="outcome-id">C / PROOF</span>
    <h3>A machine-readable manifest</h3>
    <p>The immutable artifact-generation source commit, distribution and capability versions, fictional-data declaration, and validation status.</p>
    <span class="version-tag">PINNED</span>
  </section>
  <section class="outcome-row">
    <span class="outcome-id">D / REVIEW</span>
    <h3>An explicit human checkpoint</h3>
    <p>What a qualified reviewer should verify before the pattern is adapted to operational data or materials.</p>
    <span class="version-tag">REQUIRED</span>
  </section>
</div>

## The six example sets

<div class="preview-dossier" markdown="1">
  <div class="preview-label">Public evidence</div>
  <div markdown="1">
### HCP Intelligence

A fictional account request paired with a compact, cited profile excerpt. The review focuses on identity
disambiguation, source coverage, confidence, and data minimisation.

[Open guide](../capabilities/hcp-intelligence.md){ .opp-button } [Input CSV](hcp-intelligence/input.csv){ .opp-button } [Output JSON](hcp-intelligence/output.json){ .opp-button } [Manifest](hcp-intelligence/manifest.yml){ .opp-button }
  </div>
</div>

<div class="preview-dossier" markdown="1">
  <div class="preview-label">Market evidence</div>
  <div markdown="1">
### Competitive Intelligence

A fictional competitor watch question paired with evidence-run, briefing, and timeline excerpts. The review
distinguishes complete, partial, failed, and not-configured source coverage.

[Open guide](../capabilities/competitive-intelligence.md){ .opp-button } [Input YAML](competitive-intelligence/input.yml){ .opp-button } [Output JSON](competitive-intelligence/output.json){ .opp-button } [Manifest](competitive-intelligence/manifest.yml){ .opp-button }
  </div>
</div>

<div class="preview-dossier" markdown="1">
  <div class="preview-label">Coverage choice</div>
  <div markdown="1">
### Territory Alignment

A small fictional territory scenario paired with assignment and comparison excerpts. The review checks workload,
continuity, movements, unassigned records, and manager judgement.

[Open guide](../capabilities/territory-alignment.md){ .opp-button } [Input YAML](territory-alignment/input.yml){ .opp-button } [Output JSON](territory-alignment/output.json){ .opp-button } [Manifest](territory-alignment/manifest.yml){ .opp-button }
  </div>
</div>

<div class="preview-dossier" markdown="1">
  <div class="preview-label">Engagement choice</div>
  <div markdown="1">
### Next-Best-Engagement

A fictional, consent-aware HCP universe paired with a plan excerpt. The review checks eligibility, channel
permissions, capacity, gaps, assigned ownership, and unassigned reasons.

[Open guide](../capabilities/next-best-engagement.md){ .opp-button } [Input CSV](next-best-engagement/input.csv){ .opp-button } [Output JSON](next-best-engagement/output.json){ .opp-button } [Manifest](next-best-engagement/manifest.yml){ .opp-button }
  </div>
</div>

<div class="preview-dossier" markdown="1">
  <div class="preview-label">Approved sources</div>
  <div markdown="1">
### Field Training

A fictional approved-document excerpt paired with learning and role-play material. The review checks exact source
references, claims, fair balance, source-set isolation, and qualified MLR review status.

[Open guide](../capabilities/field-training.md){ .opp-button } [Input YAML](field-training/input.yml){ .opp-button } [Output JSON](field-training/output.json){ .opp-button } [Manifest](field-training/manifest.yml){ .opp-button }
  </div>
</div>

<div class="preview-dossier" markdown="1">
  <div class="preview-label">Approved claims</div>
  <div markdown="1">
### Campaign Studio

A fictional campaign brief and claims set paired with channel and review-package excerpts. The review checks claim
traceability, fair balance, jurisdictional elements, validation freshness, and rendered-asset fidelity.

[Open guide](../capabilities/campaign-studio.md){ .opp-button } [Input JSON](campaign-studio/input.json){ .opp-button } [Output JSON](campaign-studio/output.json){ .opp-button } [Manifest](campaign-studio/manifest.yml){ .opp-button }
  </div>
</div>

!!! note "Every set is pinned and inspectable"
    Each guide links one pinned fictional input, one output artifact, and one YAML manifest. The manifest records
    immutable artifact-generation provenance: capability version, distribution 2.2.1, source commit
    `6bfc6ce43491d66b4ef45b1d3934a58648e1afc6`, validation status, and whether the output is a representative
    illustrative artifact or a runtime-generated result from a pinned fictional fixture. A newer site release does
    not rewrite these fields or imply that the sample was regenerated.

<aside class="evidence-note evidence-note--boundary" aria-labelledby="example-boundary">
  <h2 id="example-boundary">A sample is not a production template</h2>
  <p>Do not substitute fictional claims, identities, consent, assignments, policy settings, or review outcomes into operational work. Validate every adapted input and output with the accountable business, data, privacy, medical, legal, and regulatory reviewers.</p>
</aside>

[Choose a business outcome →](../outcomes/index.md){ .opp-button }
