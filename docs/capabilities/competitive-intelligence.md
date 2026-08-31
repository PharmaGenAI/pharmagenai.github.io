---
title: Competitive Intelligence
description: Collect bounded public-source market evidence once and project reproducible briefings and timelines from the same immutable run.
---

<section class="capability-header" aria-labelledby="capability-title">
  <div>
    <p class="dossier-kicker">Capability 02 · Read the landscape</p>
    <h1 id="capability-title">Competitive Intelligence</h1>
    <p class="capability-header__summary">Build one evidence run for a defined competitor question, then reuse its fingerprinted records for a briefing and timeline.</p>
  </div>
  <aside class="capability-header__proof" aria-label="Release evidence">
    <strong>Capability 1.1.0</strong><br>
    Distribution 2.4.0 · source d9bca69<br>
    Fictional sample · public beta
  </aside>
</section>

## The problem

Landscape updates are hard to compare when every briefing repeats different searches. A failed provider can also be
mistaken for a trustworthy zero-result response, turning a coverage gap into a false market conclusion.

## Objective

Collect trials, regulatory records, publications, and configured news evidence into an immutable run, expose source
coverage and limitations, and render multiple business views from the same evidence fingerprint.

## How it helps

- Tracks explicit drug and company identities rather than relying on an ambiguous topic alone.
- Distinguishes `complete`, `partial`, `failed`, `not_configured`, and `not_applicable` source states.
- Binds report and timeline artifacts to the same `run_records_sha256` so their evidence base can be compared.

## How the plugin works

<section class="plugin-flow" aria-label="Competitive Intelligence input, tools, and expected output">
  <div class="plugin-flow__stage plugin-flow__stage--input">
    <span class="plugin-flow__label">Input</span>
    <h3>Bounded market question</h3>
    <p>Tracked drug and company identities, aliases, therapeutic scope, source selection, and decision horizon.</p>
  </div>
  <span class="plugin-flow__arrow" aria-hidden="true">→</span>
  <div class="plugin-flow__stage plugin-flow__stage--tools">
    <span class="plugin-flow__label">Tools</span>
    <h3>Collect once, project many views</h3>
    <ul class="plugin-flow__tools" aria-label="Competitive Intelligence tools">
      <li><code>ci_status</code></li><li><code>ci_track</code></li><li><code>ci_refresh</code></li>
      <li><code>ci_scan_trials</code></li><li><code>ci_trial_detail</code></li><li><code>ci_scan_regulatory</code></li>
      <li><code>ci_scan_news</code></li><li><code>ci_scan_publications</code></li><li><code>ci_extract_events</code></li>
      <li><code>ci_landscape</code></li><li><code>ci_report</code></li><li><code>ci_timeline</code></li>
    </ul>
  </div>
  <span class="plugin-flow__arrow" aria-hidden="true">→</span>
  <div class="plugin-flow__stage plugin-flow__stage--output">
    <span class="plugin-flow__label">Expected output</span>
    <h3>Evidence run, briefing, and timeline</h3>
    <p>Immutable source records plus HTML, JSON, and CSV views bound to the same evidence fingerprint.</p>
  </div>
</section>

## A three-step workflow

<div class="capability-workflow">
  <section class="workflow-step"><span>01 / BOUND</span><h3>Define the watch question</h3><p>Name the fictional or governed entities, aliases, therapeutic scope, sources, and decision horizon.</p></section>
  <section class="workflow-step"><span>02 / COLLECT</span><h3>Create one evidence run</h3><p>Retrieve source records once and inspect coverage, record counts, limitations, and errors.</p></section>
  <section class="workflow-step"><span>03 / PROJECT</span><h3>Review consistent views</h3><p>Generate a briefing and calendar-filtered timeline from the same immutable run fingerprint.</p></section>
</div>

## Sample input

The fictional YAML names one simulated drug and company, asks a bounded quarterly question, and makes the requested
sources and output views explicit.

<div class="sample-actions" markdown="1">
  [Download fictional input](../examples/competitive-intelligence/input.yml){ .opp-button .opp-button--primary }
  [Inspect sample manifest](../examples/competitive-intelligence/manifest.yml){ .opp-button }
</div>

## Interpreted sample output

<div class="sample-interpretation" markdown="1">

The representative excerpt shows one simulated trial record under `complete` coverage and a `not_configured` web
source. The trial observation can enter review; the missing web provider cannot be interpreted as evidence that no
news exists. The briefing and timeline carry the same fictional run hash.

</div>

[Download representative output JSON](../examples/competitive-intelligence/output.json){ .opp-button }

## Business value indicators

<div class="value-indicators" markdown="1">

| Indicator | What a business reviewer learns |
| --- | --- |
| Coverage by entity and source | Whether each requested evidence lane is trustworthy or inconclusive |
| Returned records versus total available | Whether the displayed slice may omit relevant records |
| Run fingerprint reuse | Whether briefing and timeline share the same evidence base |
| Undated or excluded events | What the calendar view leaves out |
| High-impact findings confirmed | Which observations have been checked against linked primary sources |

</div>

## Boundaries and human review

A complete source can legitimately return zero records; failed and not-configured sources cannot. Confirm high-impact
findings against the linked primary record, assess query scope and retrieval time, and apply approved controls to
stored evidence. This public-beta workflow supports qualified commercial and medical review; it does not prove that a
market event did or did not occur outside the collected coverage.

## Get started

Use the fictional run to practise interpreting coverage before findings, then consult the canonical pinned guide for
provider setup and immutable artifact behavior.

[Open the pinned Competitive Intelligence guide →](https://github.com/PharmaGenAI/open-pharma-plugins/blob/d9bca693455c3c0d055d39e01806e9ad0a292400/cookbooks/competitive-intelligence/usage.md){ .opp-button .opp-button--primary }
