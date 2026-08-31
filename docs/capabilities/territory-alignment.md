---
title: Territory Alignment
description: Compare HCP-to-representative assignment scenarios with workload, travel, continuity, coverage, and exceptions visible for manager review.
---

<section class="capability-header" aria-labelledby="capability-title">
  <div>
    <p class="dossier-kicker">Capability 03 · Shape coverage</p>
    <h1 id="capability-title">Territory Alignment</h1>
    <p class="capability-header__summary">Model assignment choices and visit clusters, then review changes, trade-offs, and provenance in a consolidated offline report.</p>
  </div>
  <aside class="capability-header__proof" aria-label="Release evidence">
    <strong>Capability 1.2.0</strong><br>
    Distribution 2.4.1 · source bf1518d<br>
    Fictional sample · public beta
  </aside>
</section>

## The problem

Territory choices affect workload, travel, relationship continuity, priority coverage, product expertise, and local
employment rules at once. A single assignment list hides the alternatives and the cost of each movement.

## Objective

Create immutable named scenarios that make HCP-to-representative assignments, objective scores, raw metrics,
unassigned records, manager overrides, and the exact saved input snapshot inspectable before a field decision is made.

## How it helps

- Loads governed HCP, representative, current-alignment, and constraint data as separate inputs and fingerprints the saved universe.
- Models vacancies, new hires, pinned overrides, objective weights, and product/account constraints without overwriting scenario names.
- Produces a self-contained offline report with KPIs, relative territory view, charts, review queue, changed assignments, provenance, and advanced exports.

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
    <h3>Model, compare, report, and route</h3>
    <ul class="plugin-flow__tools" aria-label="Territory Alignment tools">
      <li><code>ta_status</code></li><li><code>ta_align</code></li><li><code>ta_evaluate</code></li>
      <li><code>ta_compare</code></li><li><code>ta_visualize</code></li><li><code>ta_cluster</code></li>
    </ul>
  </div>
  <span class="plugin-flow__arrow" aria-hidden="true">→</span>
  <div class="plugin-flow__stage plugin-flow__stage--output">
    <span class="plugin-flow__label">Expected output</span>
    <h3>Decision-ready scenario reports</h3>
    <p>A consolidated offline HTML report, scenario JSON and formula-safe CSVs, comparison metrics, review queue, and representative visit routes.</p>
  </div>
</section>

## A three-step workflow

<div class="capability-workflow">
  <section class="workflow-step"><span>01 / GOVERN</span><h3>Prepare the operating inputs</h3><p>Confirm account ownership, field roster, coordinates, product expertise, consent, and constraints.</p></section>
  <section class="workflow-step"><span>02 / MODEL</span><h3>Save immutable scenarios</h3><p>Apply vacancies, hires, overrides, and objective weights while preserving the exact input snapshot and baseline.</p></section>
  <section class="workflow-step"><span>03 / DECIDE</span><h3>Review the offline report</h3><p>Compare movements, workload, travel, priority coverage, review exceptions, unassigned HCPs, and route feasibility.</p></section>
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
| Input fingerprints and review queue | Whether compared scenarios use the same governed universe and which exceptions need action |

</div>

## Boundaries and human review

Results are planning recommendations, not an automatic reorganisation. Confirm employment rules, accessibility,
consent, account ownership, travel constraints, product expertise, vacancies, and manager overrides. The default
consolidated report is self-contained and makes no network requests. A separately requested public basemap loads
CARTO/OpenStreetMap resources and may disclose map extent or coordinates to those providers. Qualified operations and
field leaders must review every public-beta scenario before operational use.

## Get started

Inspect how the fictional scenario exposes continuity and concentration, then use the canonical pinned guide to learn
the separate CSV contracts, immutable scenario snapshots, consolidated reports, and route-planning tools.

[Open the pinned Territory Alignment guide →](https://github.com/PharmaGenAI/open-pharma-plugins/blob/bf1518dee6a56f8410feb3058672bfbb479d0bc8/cookbooks/territory-alignment/usage.md){ .opp-button .opp-button--primary }
