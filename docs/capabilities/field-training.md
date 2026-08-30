---
title: Field Training
description: Turn supplied approved PDF or PPTX sources into source-grounded learning, assessment, and role-play drafts for qualified review.
---

<section class="capability-header" aria-labelledby="capability-title">
  <div>
    <p class="dossier-kicker">Capability 05 · Equip the field</p>
    <h1 id="capability-title">Field Training</h1>
    <p class="capability-header__summary">Build learning and practice materials from the exact approved source set, with page- or slide-level excerpts attached to generated claims.</p>
  </div>
  <aside class="capability-header__proof" aria-label="Release evidence">
    <strong>Capability 1.1.1</strong><br>
    Distribution 2.2.1 · source 6bfc6ce<br>
    Fictional sample · public beta
  </aside>
</section>

## The problem

Training drafts can drift from their source material, omit safety context, or silently mix old documents into a new
request. Review becomes slow when a learner, facilitator, or MLR reviewer cannot trace a message to an exact passage.

## Objective

Turn one or more supplied, approved PDF or PPTX paths into a learning package, assessment, pre-session role-play kit,
or post-session scorecard while retaining source-set isolation and exact page or slide excerpts.

## How it helps

- Stops when any requested source path is missing, unreadable, or unsupported instead of rendering a partial set.
- Grounds messages, model answers, and approved responses through structured `SourceReference` records.
- Validates and saves structured JSON plus self-contained interactive HTML for offline review and facilitation.

## How the plugin works

<section class="plugin-flow" aria-label="Field Training input, tools, and expected output">
  <div class="plugin-flow__stage plugin-flow__stage--input">
    <span class="plugin-flow__label">Input</span>
    <h3>Exact approved source set</h3>
    <p>Absolute PDF or PPTX paths plus a requested output type and name; every supplied file must validate.</p>
  </div>
  <span class="plugin-flow__arrow" aria-hidden="true">→</span>
  <div class="plugin-flow__stage plugin-flow__stage--tools">
    <span class="plugin-flow__label">Tools</span>
    <h3>Ingest, ground, and render</h3>
    <ul class="plugin-flow__tools" aria-label="Field Training tools">
      <li><code>ingest_document</code></li><li><code>list_documents</code></li><li><code>search_content</code></li>
      <li><code>get_document_page</code></li><li><code>render_output</code></li>
    </ul>
  </div>
  <span class="plugin-flow__arrow" aria-hidden="true">→</span>
  <div class="plugin-flow__stage plugin-flow__stage--output">
    <span class="plugin-flow__label">Expected output</span>
    <h3>Grounded learning artifact</h3>
    <p>Schema-valid JSON and self-contained HTML for a learning package, assessment, role-play kit, or scorecard.</p>
  </div>
</section>

## A three-step workflow

<div class="capability-workflow">
  <section class="workflow-step"><span>01 / INGEST</span><h3>Lock the source set</h3><p>Provide the exact approved PDF or PPTX paths and verify every document ID, page, and slide.</p></section>
  <section class="workflow-step"><span>02 / GROUND</span><h3>Draft from excerpts</h3><p>Create learning or practice content while attaching each claim to a matching source passage.</p></section>
  <section class="workflow-step"><span>03 / REVIEW</span><h3>Validate and render</h3><p>Inspect sourcing, fair balance, schema validity, interactive behavior, and final rendered fidelity.</p></section>
</div>

## Sample input

The fictional YAML represents a path-first learning-package request and includes one simulated approved-source excerpt
so the grounding relationship can be inspected. The named PDF is not distributed and the YAML is not a runtime source
document; production ingestion supports approved PDF and PPTX files.

<div class="sample-actions" markdown="1">
  [Download fictional input](../examples/field-training/input.yml){ .opp-button .opp-button--primary }
  [Inspect sample manifest](../examples/field-training/manifest.yml){ .opp-button }
</div>

## Interpreted sample output

<div class="sample-interpretation" markdown="1">

The representative learning-module excerpt keeps benefit and safety context connected and cites the exact fictional
sentence on page 3. Reviewers should compare that excerpt with the ingested page, then inspect the complete source set,
message balance, and rendered artifact before field use.

</div>

[Download representative output JSON](../examples/field-training/output.json){ .opp-button }

## Business value indicators

<div class="value-indicators" markdown="1">

| Indicator | What a business reviewer learns |
| --- | --- |
| Supplied versus ingested documents | Whether the full approved source set entered the request |
| Claims with exact source excerpts | Whether each message can be traced to a page or slide |
| Unsupported or inaccurate flags | Which statements need revision or removal |
| Safety and fair-balance coverage | Whether review should challenge an unbalanced learning story |
| Rendered-artifact QA exceptions | Whether content is hidden, clipped, stale, or interaction-dependent |

</div>

## Boundaries and human review

Use only the exact approved source documents for the request. Generated learning and role-play materials remain drafts
for qualified medical, legal, regulatory, learning, and accessibility review; they are not permission for field use.
Review off-label risk, unsupported claims, fair balance, source-set isolation, exact excerpts, and final rendering. Every
public-beta output must be validated after content changes.

## Get started

Inspect the fictional source-to-message trace, then use the canonical pinned guide for supported file types, output
schemas, path-first prompts, and renderer behavior.

[Open the pinned Field Training guide →](https://github.com/PharmaGenAI/open-pharma-plugins/blob/6bfc6ce43491d66b4ef45b1d3934a58648e1afc6/cookbooks/field-training/usage.md){ .opp-button .opp-button--primary }
