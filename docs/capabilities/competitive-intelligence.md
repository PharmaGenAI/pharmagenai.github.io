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
    Distribution 2.2.1 · source 6bfc6ce<br>
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

[Open the pinned Competitive Intelligence guide →](https://github.com/PharmaGenAI/open-pharma-plugins/blob/6bfc6ce43491d66b4ef45b1d3934a58648e1afc6/cookbooks/competitive-intelligence/usage.md){ .opp-button .opp-button--primary }
Authorized repository access required.
