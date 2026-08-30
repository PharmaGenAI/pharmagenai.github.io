---
title: Territory Alignment
description: Compare HCP-to-representative assignment scenarios with workload, travel, continuity, coverage, and exceptions visible for manager review.
---

<section class="capability-header" aria-labelledby="capability-title">
  <div>
    <p class="dossier-kicker">Capability 03 · Shape coverage</p>
    <h1 id="capability-title">Territory Alignment</h1>
    <p class="capability-header__summary">Model assignment choices and visit clusters while keeping changes, unassigned accounts, and operating trade-offs in view.</p>
  </div>
  <aside class="capability-header__proof" aria-label="Release evidence">
    <strong>Capability 1.0.1</strong><br>
    Distribution 2.2.1 · source 6bfc6ce<br>
    Fictional sample · public beta
  </aside>
</section>

## The problem

Territory choices affect workload, travel, relationship continuity, priority coverage, product expertise, and local
employment rules at once. A single assignment list hides the alternatives and the cost of each movement.

## Objective

Create named scenarios that make HCP-to-representative assignments, objective scores, raw metrics, unassigned records,
and manager overrides inspectable before a field operating decision is made.

## How it helps

- Loads governed HCP, representative, current-alignment, and constraint data as separate inputs.
- Models vacancies, new hires, pinned overrides, objective weights, and product/account constraints.
- Compares two to four scenarios and can produce map or visit-cluster artifacts for operational review.

## How the plugin works

<section class="plugin-flow" aria-label="Territory Alignment input, tools, and expected output">
  <div class="plugin-flow__stage plugin-flow__stage--input">
    <span class="plugin-flow__label">Input</span>
    <h3>Four governed datasets</h3>
    <p>HCPs, representatives, current alignment, and constraints CSVs plus named scenario settings and overrides.</p>
  </div>
  <span class="plugin-flow__arrow" aria-hidden="true">→</span>
  <div class="plugin-flow__stage plugin-flow__stage--tools">
    <span class="plugin-flow__label">Tools</span>
    <h3>Model, compare, and map</h3>
    <ul class="plugin-flow__tools" aria-label="Territory Alignment tools">
      <li><code>ta_status</code></li><li><code>ta_align</code></li><li><code>ta_evaluate</code></li>
      <li><code>ta_compare</code></li><li><code>ta_visualize</code></li><li><code>ta_cluster</code></li>
    </ul>
  </div>
  <span class="plugin-flow__arrow" aria-hidden="true">→</span>
  <div class="plugin-flow__stage plugin-flow__stage--output">
    <span class="plugin-flow__label">Expected output</span>
    <h3>Comparable operating scenarios</h3>
    <p>Scenario JSON and CSVs, comparison metrics, an interactive map, and representative visit routes.</p>
  </div>
</section>

## A three-step workflow

<div class="capability-workflow">
  <section class="workflow-step"><span>01 / GOVERN</span><h3>Prepare the operating inputs</h3><p>Confirm account ownership, field roster, coordinates, product expertise, consent, and constraints.</p></section>
  <section class="workflow-step"><span>02 / MODEL</span><h3>Generate named scenarios</h3><p>Apply vacancies, hires, overrides, and objective weights without overwriting the baseline choice.</p></section>
  <section class="workflow-step"><span>03 / DECIDE</span><h3>Compare trade-offs</h3><p>Review movements, workload, travel, priority coverage, unassigned HCPs, and route feasibility.</p></section>
</div>

## Sample input

The fictional YAML compresses the four runtime input concepts into one readable dossier: two HCPs, two employees,
current ownership, and an account-grouping constraint. It is representative—not a replacement for the supported CSVs.

<div class="sample-actions" markdown="1">
  [Download fictional input](../examples/territory-alignment/input.yml){ .opp-button .opp-button--primary }
  [Inspect sample manifest](../examples/territory-alignment/manifest.yml){ .opp-button }
</div>

## Interpreted sample output

<div class="sample-interpretation" markdown="1">

Both fictional HCPs remain with their existing representative, so relationship continuity scores highly and no
record is unassigned. The excerpt also concentrates the two-account workload on one representative; a manager should
challenge that trade-off rather than treating the composite score as the answer.

</div>

[Download representative output JSON](../examples/territory-alignment/output.json){ .opp-button }

## Business value indicators

<div class="value-indicators" markdown="1">

| Indicator | What a business reviewer learns |
| --- | --- |
| Priority coverage percentage | Whether high-priority accounts receive a feasible assignment |
| Reassignment percentage | How much relationship disruption a scenario introduces |
| Workload balance and territory summaries | Where demand or potential is concentrated by representative |
| Average and maximum travel estimate | Where geography may make a scenario impractical |
| Unassigned HCPs and reasons | Which governed records need an explicit manager decision |

</div>

## Boundaries and human review

Results are planning recommendations, not an automatic reorganisation. Confirm employment rules, accessibility,
consent, account ownership, travel constraints, product expertise, vacancies, and manager overrides. Opening an online
map can send coordinates to public tile providers; use an approved offline stack where required. Qualified operations
and field leaders must review every public-beta scenario before operational use.

## Get started

Inspect how the fictional scenario exposes continuity and concentration, then use the canonical pinned guide to learn
the separate CSV contracts and scenario tools.

[Open the pinned Territory Alignment guide →](https://github.com/PharmaGenAI/open-pharma-plugins/blob/6bfc6ce43491d66b4ef45b1d3934a58648e1afc6/cookbooks/territory-alignment/usage.md){ .opp-button .opp-button--primary }
