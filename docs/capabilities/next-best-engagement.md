---
title: Next-Best-Engagement
description: Produce consent-aware HCP, channel, and assigned-representative engagement recommendations with constraints and no-action reasons visible.
---

<section class="capability-header" aria-labelledby="capability-title">
  <div>
    <p class="dossier-kicker">Capability 04 · Plan engagement</p>
    <h1 id="capability-title">Next-Best-Engagement</h1>
    <p class="capability-header__summary">Turn an assigned HCP universe into one constrained action—or an explicit no-action outcome—per HCP for field review.</p>
  </div>
  <aside class="capability-header__proof" aria-label="Release evidence">
    <strong>Capability 1.0.2</strong><br>
    Distribution 2.2.1 · source 6bfc6ce<br>
    Fictional sample · public beta
  </aside>
</section>

## The problem

Engagement plans must balance tier coverage, recent activity, channel diversity, explicit consent, assigned ownership,
minimum gaps, and visit capacity. A ranked list alone does not explain why an HCP is eligible or why no action is safer.

## Objective

Recommend at most one action for each HCP, preserve the HCP's assigned representative, and expose plan metrics,
capacity, channel mix, unassigned records, and no-action reasons for accountable review.

## How it helps

- Loads a governed CSV universe and retains extra CRM columns that do not conflict with planner-owned fields.
- Scores eligible records with explicit weights and coverage constraints, then selects a consent-compatible channel.
- Fingerprints the loaded universe and fails closed if a later reload makes an earlier plan stale before export.

## How the plugin works

<section class="plugin-flow" aria-label="Next-Best-Engagement input, tools, and expected output">
  <div class="plugin-flow__stage plugin-flow__stage--input">
    <span class="plugin-flow__label">Input</span>
    <h3>Assigned HCP universe</h3>
    <p>A CSV with HCP, territory, and representative IDs; consent, tier, activity, and capacity fields refine eligibility.</p>
  </div>
  <span class="plugin-flow__arrow" aria-hidden="true">→</span>
  <div class="plugin-flow__stage plugin-flow__stage--tools">
    <span class="plugin-flow__label">Tools</span>
    <h3>Load, recommend, and export</h3>
    <ul class="plugin-flow__tools" aria-label="Next-Best-Engagement tools">
      <li><code>load_universe</code></li><li><code>recommend_engagements</code></li><li><code>render_plan</code></li>
    </ul>
  </div>
  <span class="plugin-flow__arrow" aria-hidden="true">→</span>
  <div class="plugin-flow__stage plugin-flow__stage--output">
    <span class="plugin-flow__label">Expected output</span>
    <h3>Consent-aware engagement plan</h3>
    <p>Plan JSON or engagement and summary CSVs with actions, assigned owners, metrics, and no-action reasons.</p>
  </div>
</section>

## A three-step workflow

<div class="capability-workflow">
  <section class="workflow-step"><span>01 / LOAD</span><h3>Snapshot the universe</h3><p>Load governed HCP, territory, representative, consent, tier, activity, and capacity fields.</p></section>
  <section class="workflow-step"><span>02 / CONSTRAIN</span><h3>Generate a plan</h3><p>Apply minimum gaps, tier targets, weights, channel permissions, and visit-capacity rules.</p></section>
  <section class="workflow-step"><span>03 / REVIEW</span><h3>Inspect actions and gaps</h3><p>Challenge priorities, no-action reasons, ownership, channel mix, and field practicality before action.</p></section>
</div>

## Sample input

The public CSV is the exact built-in fictional demo fixture from the pinned 1.0.2 release: 80 HCP rows, 8 assigned
representatives, and the full required-plus-optional universe columns used by the planner.

<div class="sample-actions" markdown="1">
  [Download fictional input](../examples/next-best-engagement/input.csv){ .opp-button .opp-button--primary }
  [Inspect sample manifest](../examples/next-best-engagement/manifest.yml){ .opp-button }
</div>

## Interpreted sample output

<div class="sample-interpretation" markdown="1">

The downloadable JSON shows that `HCP-E-003` is a priority-1 `in_person_visit`, while `HCP-E-015` is `unassigned`
with reason `no_consent` because neither email nor phone consent is explicitly true. The downloadable JSON was
generated from that same pinned fixture on 2026-08-30. Its metrics show **80 input HCPs, 76 eligible HCPs, 76 planned
actions, and 4 unassigned HCPs with no-action reasons**. These counts describe one fictional demo universe only; they
are not a performance promise.

</div>

[Download generated output JSON](../examples/next-best-engagement/output.json){ .opp-button }

## Business value indicators

<div class="value-indicators" markdown="1">

| Indicator | What a business reviewer learns |
| --- | --- |
| Total universe, eligible, and planned | How filtering and constraints change the actionable population |
| Coverage and tier gaps | Where the plan falls short of configured coverage targets |
| No-action count and reasons | Where consent, timing, or score rules prevent an action |
| Representative visit utilization | Whether proposed in-person work fits configured capacity |
| Channel mix | Whether the plan over-relies on one permitted mode |

</div>

## Boundaries and human review

The planner does not send an email, book a meeting, perform a visit, or reassign account ownership. Confirm explicit
consent, suppression lists, local policy, current interaction history, assigned representative and territory, capacity,
and field practicality. Channel-diversity scoring does not replace these checks. Qualified business, privacy, and field
reviewers remain accountable for every public-beta action.

## Get started

Use the pinned 80-row fictional demo universe to inspect the consent and no-action logic, then consult the canonical
pinned guide for the full CSV contract, plan fingerprint, and export behavior.

[Open the pinned Next-Best-Engagement guide →](https://github.com/PharmaGenAI/open-pharma-plugins/blob/6bfc6ce43491d66b4ef45b1d3934a58648e1afc6/cookbooks/next-best-engagement/usage.md){ .opp-button .opp-button--primary }
Authorized repository access required.
