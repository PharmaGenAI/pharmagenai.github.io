---
title: Campaign Studio
description: Create claim-linked campaign drafts, validation evidence, rendered assets, and a package for qualified MLR review.
---

<section class="capability-header" aria-labelledby="capability-title">
  <div>
    <p class="dossier-kicker">Capability 06 · Prepare materials</p>
    <h1 id="capability-title">Campaign Studio</h1>
    <p class="capability-header__summary">Connect a campaign brief, approved claims, brand components, channel copy, validation evidence, and rendered artifacts in one draft review package.</p>
  </div>
  <aside class="capability-header__proof" aria-label="Release evidence">
    <strong>Capability 1.0.1</strong><br>
    Distribution 2.2.1 · source 6bfc6ce<br>
    Fictional sample · public beta
  </aside>
</section>

## The problem

Campaign review slows when claims, safety context, channel copy, brand components, validation evidence, and rendered
files live in separate places. A technically valid copy object can still produce a clipped or stale final asset.

## Objective

Create a structured campaign brief, claim-linked message and channel drafts, policy-check evidence, rendered assets,
and a human-readable package that qualified medical, legal, and regulatory reviewers can assess.

## How it helps

- Loads approved claims from JSON and brand components from a supplied kit; PDF claim extraction is not supported.
- Requires claim IDs for promotional copy blocks except exact legal text and the brief's exact call to action.
- Invalidates prior validation when the brief, claims, or copy changes, then packages current artifacts for review.

## How the plugin works

<section class="plugin-flow" aria-label="Campaign Studio input, tools, and expected output">
  <div class="plugin-flow__stage plugin-flow__stage--input">
    <span class="plugin-flow__label">Input</span>
    <h3>Governed campaign components</h3>
    <p>A campaign brief, approved-claims JSON, brand kit, jurisdiction, audience, CTA, and requested channels.</p>
  </div>
  <span class="plugin-flow__arrow" aria-hidden="true">→</span>
  <div class="plugin-flow__stage plugin-flow__stage--tools">
    <span class="plugin-flow__label">Tools</span>
    <h3>Draft, validate, render, and package</h3>
    <ul class="plugin-flow__tools" aria-label="Campaign Studio tools">
      <li><code>create_campaign_brief</code></li><li><code>retrieve_approved_claims</code></li><li><code>retrieve_brand_components</code></li>
      <li><code>generate_audience_journey</code></li><li><code>generate_message_architecture</code></li><li><code>generate_channel_copy</code></li>
      <li><code>validate_claims_and_fair_balance</code></li><li><code>render_email</code></li><li><code>render_banner</code></li>
      <li><code>render_poster</code></li><li><code>package_mlr_submission</code></li>
    </ul>
  </div>
  <span class="plugin-flow__arrow" aria-hidden="true">→</span>
  <div class="plugin-flow__stage plugin-flow__stage--output">
    <span class="plugin-flow__label">Expected output</span>
    <h3>Draft MLR review package</h3>
    <p>Validated copy, rendered email HTML, SVG banner or PDF poster, and a human-readable review summary.</p>
  </div>
</section>

## A three-step workflow

<div class="capability-workflow">
  <section class="workflow-step"><span>01 / FRAME</span><h3>Define the governed brief</h3><p>Set jurisdiction, indication, audience, objective, channels, CTA, approved claims, safety, and brand inputs.</p></section>
  <section class="workflow-step"><span>02 / BUILD</span><h3>Draft with traceability</h3><p>Create the audience journey, message architecture, and channel copy with claim IDs and fair balance.</p></section>
  <section class="workflow-step"><span>03 / REVIEW</span><h3>Validate, render, package</h3><p>Run claim and policy checks, inspect rendered fidelity, and assemble the current draft review package.</p></section>
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
| Current input fingerprint | Whether validation still binds to the present brief, claims, and copy |
| Review-package completeness | Whether expected source, copy, validation, and rendered files are present |
| Rendered-asset QA exceptions | Whether email, banner, or poster output is clipped, hidden, stale, or distorted |

</div>

## Boundaries and human review

The package is a review aid, not regulatory approval. A qualified medical, legal, and regulatory reviewer must assess
claims, fair balance, jurisdictional elements, source currency, and final visual fidelity before use. Revalidate after
any input or copy change and inspect the actual email HTML, SVG banner, or PDF poster. Public-beta validation supports
review; it does not replace approval or authorize distribution.

## Get started

Inspect the fictional claim-to-copy mapping, then use the canonical pinned guide for the supported JSON claim source,
brand-kit inputs, renderer sequence, and review-package behavior.

[Open the pinned Campaign Studio guide →](https://github.com/PharmaGenAI/open-pharma-plugins/blob/6bfc6ce43491d66b4ef45b1d3934a58648e1afc6/cookbooks/campaign-studio/usage.md){ .opp-button .opp-button--primary }
Authorized repository access required.
