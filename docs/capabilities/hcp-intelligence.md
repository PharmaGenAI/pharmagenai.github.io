---
title: HCP Intelligence
description: Build reviewable HCP and HCO profiles from public-source evidence, with identity, provenance, confidence, and coverage kept visible.
---

<section class="capability-header" aria-labelledby="capability-title">
  <div>
    <p class="dossier-kicker">Capability 01 · Know the account</p>
    <h1 id="capability-title">HCP Intelligence</h1>
    <p class="capability-header__summary">Turn a named HCP or HCO research request into a structured public-source profile that an account team can inspect—not a score that hides its evidence.</p>
  </div>
  <aside class="capability-header__proof" aria-label="Release evidence">
    <strong>Capability 1.0.2</strong><br>
    Distribution 2.4.0 · source d9bca69<br>
    Fictional sample · public beta
  </aside>
</section>

## The problem

Account preparation often spreads identity clues, affiliations, publications, trials, grants, and web findings
across disconnected searches. A namesake or stale affiliation can then travel into a briefing without its uncertainty.

## Objective

Create one reviewable HCP or HCO profile in which factual claims retain source URLs, access dates, confidence, and
disambiguation notes. The objective is better-prepared human research and account discussion—not automated targeting.

## How it helps

- Searches supported public sources including PubMed, ClinicalTrials.gov, ORCID, NIH RePORTER, and configured web providers.
- Keeps account identity, evidence-backed claims, source coverage, confidence, and profile completeness together.
- Supports CSV batch work with an exact dry-run scope gate and reviewable JSON, CSV, and manifest artifacts.

## How the plugin works

<section class="plugin-flow" aria-label="HCP Intelligence input, tools, and expected output">
  <div class="plugin-flow__stage plugin-flow__stage--input">
    <span class="plugin-flow__label">Input</span>
    <h3>Account identity and scope</h3>
    <p>A governed account ID or CSV with name, country, account type, specialty, and institution clues.</p>
  </div>
  <span class="plugin-flow__arrow" aria-hidden="true">→</span>
  <div class="plugin-flow__stage plugin-flow__stage--tools">
    <span class="plugin-flow__label">Tools</span>
    <h3>Account and public-source research</h3>
    <ul class="plugin-flow__tools" aria-label="HCP Intelligence tools">
      <li><code>list_accounts</code></li><li><code>get_account</code></li><li><code>update_account</code></li>
      <li><code>search_publications</code></li><li><code>search_guidelines</code></li><li><code>search_clinical_trials</code></li>
      <li><code>search_grants</code></li><li><code>search_orcid</code></li><li><code>search_congresses</code></li>
      <li><code>search_hcp_web</code></li><li><code>search_hco_web</code></li>
    </ul>
  </div>
  <span class="plugin-flow__arrow" aria-hidden="true">→</span>
  <div class="plugin-flow__stage plugin-flow__stage--output">
    <span class="plugin-flow__label">Expected output</span>
    <h3>Cited profile and batch record</h3>
    <p>Evidence-backed profile JSON; batch work also writes a summary CSV and manifest with completion status.</p>
  </div>
</section>

## A three-step workflow

<div class="capability-workflow">
  <section class="workflow-step"><span>01 / IDENTIFY</span><h3>Resolve the subject</h3><p>Supply a governed ID, name, country, account type, and useful affiliation or specialty clues.</p></section>
  <section class="workflow-step"><span>02 / RESEARCH</span><h3>Gather public evidence</h3><p>Search the relevant sources and preserve URLs, dates, provider coverage, and namesake evidence.</p></section>
  <section class="workflow-step"><span>03 / REVIEW</span><h3>Inspect the profile</h3><p>Check identity, confidence, missing coverage, recency, and every partial or failed record before use.</p></section>
</div>

## Sample input

The downloadable CSV uses the pinned batch header: `id,name,specialty,country,account_type,institution`. Its two rows
are explicitly fictional and show one HCP and one HCO without exposing a real person or customer.

<div class="sample-actions" markdown="1">
  [Download fictional input](../examples/hcp-intelligence/input.csv){ .opp-button .opp-button--primary }
  [Inspect sample manifest](../examples/hcp-intelligence/manifest.yml){ .opp-button }
</div>

## Interpreted sample output

<div class="sample-interpretation" markdown="1">

The representative JSON excerpt gives the fictional title **medium confidence** because only one simulated
institutional source supports it. Its `profile_completeness` is 0.42 and the review flags call out absent
corroboration. That is a reason to continue verification, not a measure of HCP value or commercial priority.

</div>

[Download representative output JSON](../examples/hcp-intelligence/output.json){ .opp-button }

## Business value indicators

<div class="value-indicators" markdown="1">

| Indicator | What a business reviewer learns |
| --- | --- |
| Identity exceptions | Where namesake or affiliation conflicts still need resolution |
| Claim source coverage | Which material profile statements have linked evidence |
| Source status and recency | Which providers succeeded and when evidence was accessed |
| Partial or failed account count | Where a batch is incomplete and must not be treated as finished |
| Profile completeness | A review aid for missing fields—not a quality or influence score |

</div>

## Boundaries and human review

Public-source results may be incomplete, stale, or refer to a namesake. Confirm identity, source authority, data
rights, privacy, consent, retention, and operational relevance. If optional synthesis is used, confirm the selected
provider is approved for the submitted account fields and evidence. This public-beta capability does not determine
whether an HCP should be targeted; qualified people remain accountable for that decision.

## Get started

Inspect the small fictional files first, then use the canonical pinned guide for current inputs, provider gates,
and batch completion rules.

[Open the pinned HCP Intelligence guide →](https://github.com/PharmaGenAI/open-pharma-plugins/blob/d9bca693455c3c0d055d39e01806e9ad0a292400/cookbooks/hcp-intelligence/usage.md){ .opp-button .opp-button--primary }
