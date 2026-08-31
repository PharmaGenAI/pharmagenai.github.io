---
title: Campaign Studio
description: Create claim-linked campaign drafts, validation evidence, rendered assets, and a package for qualified MLR review.
---

<section class="capability-header" aria-labelledby="capability-title">
  <div>
    <p class="dossier-kicker">Capability 06 · Prepare materials</p>
    <h1 id="capability-title">Campaign Studio</h1>
    <p class="capability-header__summary">Connect exact approved-claims and brand-kit inputs to claim-linked copy, rendered-file validation, and a content-addressed draft review package.</p>
  </div>
  <aside class="capability-header__proof" aria-label="Release evidence">
    <strong>Capability 1.1.0</strong><br>
    Distribution 2.4.1 · source bf1518d<br>
    Fictional sample · public beta
  </aside>
</section>

## The problem

Campaign review slows when claims, safety context, channel copy, brand components, validation evidence, and rendered
files live in separate places. A technically valid copy object can still produce a clipped or stale final asset, and
an informal handoff can lose the exact inputs and file hashes that reviewers need.

## Objective

Create a structured campaign brief, fail-closed input record, claim-linked message and channel drafts, policy and
rendered-file evidence, and a deterministic package that qualified medical, legal, and regulatory reviewers can assess.

## How it helps

- Preflights the exact approved-claims JSON and brand-kit paths; missing, malformed, excluded, or inconsistent inputs stop the workflow instead of falling back to demo data.
- Reports the current workflow status and next required step, then enforces applicable claim IDs and exact approved text or allowed variants for each channel.
- Validates the actual rendered files, seals their hashes, and exports a manifest plus content-addressed ZIP for review.

## How the plugin works

<section class="plugin-flow" aria-label="Campaign Studio input, tools, and expected output">
  <div class="plugin-flow__stage plugin-flow__stage--input">
    <span class="plugin-flow__label">Input</span>
    <h3>Exact governed inputs</h3>
    <p>A campaign brief, approved-claims JSON path, brand-kit directory, jurisdiction, audience, CTA, and requested channels.</p>
  </div>
  <span class="plugin-flow__arrow" aria-hidden="true">→</span>
  <div class="plugin-flow__stage plugin-flow__stage--tools">
    <span class="plugin-flow__label">Tools</span>
    <h3>Draft, validate, render, and package</h3>
    <ul class="plugin-flow__tools" aria-label="Campaign Studio tools">
      <li><code>create_campaign_brief</code></li><li><code>retrieve_approved_claims</code></li><li><code>retrieve_brand_components</code></li>
      <li><code>get_campaign_status</code></li><li><code>preflight_campaign_inputs</code></li>
      <li><code>generate_audience_journey</code></li><li><code>generate_message_architecture</code></li><li><code>generate_channel_copy</code></li>
      <li><code>validate_claims_and_fair_balance</code></li><li><code>render_email</code></li><li><code>render_banner</code></li>
      <li><code>render_poster</code></li><li><code>validate_rendered_assets</code></li><li><code>package_mlr_submission</code></li>
      <li><code>render_mlr_review</code></li><li><code>export_mlr_package</code></li>
    </ul>
  </div>
  <span class="plugin-flow__arrow" aria-hidden="true">→</span>
  <div class="plugin-flow__stage plugin-flow__stage--output">
    <span class="plugin-flow__label">Expected output</span>
    <h3>Traceable draft MLR handoff</h3>
    <p>Validated copy and rendered assets, canonical Markdown and interactive HTML review, manifest, hashes, and a content-addressed ZIP.</p>
  </div>
</section>

## A three-step workflow

<div class="capability-workflow">
  <section class="workflow-step"><span>01 / PREFLIGHT</span><h3>Bind the exact inputs</h3><p>Set the governed brief and validate the approved-claims JSON and brand-kit directory before drafting.</p></section>
  <section class="workflow-step"><span>02 / BUILD</span><h3>Draft with traceability</h3><p>Create the journey, message architecture, and English email, banner, or poster copy with claim IDs and fair balance.</p></section>
  <section class="workflow-step"><span>03 / REVIEW</span><h3>Validate, render, export</h3><p>Check every channel and rendered file, render the canonical review, and export the sealed draft package.</p></section>
</div>

## Sample input

The fictional JSON combines a compact US/FDA campaign brief with one simulated efficacy claim and one simulated
safety statement. It is explicitly demonstration content and must never be adapted as real product messaging.

<div class="sample-actions" markdown="1">
  [Download fictional input](../examples/campaign-studio/input.json){ .opp-button .opp-button--primary }
  [Inspect sample manifest](../examples/campaign-studio/manifest.yml){ .opp-button }
</div>

## Interpreted sample output

<div class="sample-interpretation" markdown="1">

The representative email excerpt links each non-CTA block to a fictional claim ID and includes both efficacy and safety
content. Its software policy check passes, while the claim status remains `needs_review` and the package remains a draft
for qualified MLR review. A passing validator is not evidence that the content or rendered asset is approved.

</div>

[Download representative output JSON](../examples/campaign-studio/output.json){ .opp-button }

## Business value indicators

<div class="value-indicators" markdown="1">

| Indicator | What a business reviewer learns |
| --- | --- |
| Copy blocks with claim IDs | Whether promotional statements retain an approved-claim reference |
| Claim and policy check results | Which wording, fair-balance, or required-element issues remain |
| Input paths, fingerprints, and workflow status | Whether the run uses the intended sources and which step is required next |
| Rendered-file checks and hashes | Whether email, banner, or poster output is complete, current, visible, and unchanged |
| Package manifest and digest | Whether reviewers received the exact content-addressed handoff that the workflow exported |

</div>

## Boundaries and human review

The package is a review aid, not regulatory approval. Version 1.1 produces English email, banner, and poster drafts;
it does not extract approved claims from PDF or other formats. A qualified medical, legal, and regulatory reviewer
must assess claims, fair balance, jurisdictional elements, source currency, and final visual fidelity before use.
Revalidate after any brief, claim, brand, policy, template, copy, or rendered-output change. The tools do not send
email, traffic ads, publish assets, or record an authoritative external decision.

## Get started

Inspect the fictional claim-to-copy mapping, then use the canonical pinned guide for exact input preflight, status-led
resume, renderer validation, and the content-addressed review export.

[Open the pinned Campaign Studio guide →](https://github.com/PharmaGenAI/open-pharma-plugins/blob/bf1518dee6a56f8410feb3058672bfbb479d0bc8/cookbooks/campaign-studio/usage.md){ .opp-button .opp-button--primary }
