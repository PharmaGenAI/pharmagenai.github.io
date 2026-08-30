---
title: Open Pharma Plugins documentation
description: Business and technical documentation for evidence-led pharmaceutical commercial workflows.
hide:
  - toc
---

<section class="opp-hero" data-hero aria-labelledby="hero-title">
  <div class="opp-hero__copy">
    <p class="dossier-kicker">Open Pharma Plugins / Documentation</p>
    <h1 id="hero-title">Open Pharma Plugins</h1>
    <p class="opp-hero__lede">A set of reviewable workflows for pharmaceutical commercial teams. Understand the business problem, inspect a fictional input and output, then follow the technical guide when you are ready to implement.</p>
    <div class="opp-actions">
      <a class="opp-button opp-button--primary" href="get-started/">Get started</a>
      <a class="opp-button" href="#plugin-guides">Browse plugin guides</a>
    </div>
    <p class="release-line"><strong>Public beta</strong> · Distribution 2.2.1 · Pinned source <code>6bfc6ce</code></p>
  </div>
  <aside class="quick-install" aria-labelledby="quick-install-title">
    <p class="quick-install__label" id="quick-install-title">Quick install · public MCP server</p>
    <pre><code>python -m pip install \
  "open-pharma-plugins[hcp-intelligence]==2.2.1"</code></pre>
    <p>Start with one released capability. The full Skill + MCP installer requires an authorized repository checkout.</p>
    <a href="get-started/#pick-the-install-surface">See all installation options →</a>
  </aside>
</section>

<section class="reader-paths" aria-labelledby="reader-paths-title">
  <h2 id="reader-paths-title">Choose your reading path</h2>
  <div class="reader-paths__grid">
    <a class="reader-path" href="outcomes/">
      <span>For business teams</span>
      <strong>Start with the decision</strong>
      <p>See the problem, the capability, the expected outcome, and the human review boundary in plain language.</p>
      <em>Explore business outcomes →</em>
    </a>
    <a class="reader-path" href="get-started/">
      <span>For technical teams</span>
      <strong>Start with the implementation</strong>
      <p>Choose an install surface, inspect example files, and continue into version-pinned configuration and operations.</p>
      <em>Open the implementation path →</em>
    </a>
  </div>
</section>

## What problem does the portfolio solve?

<div class="problem-solution-map">
  <section>
    <span>Problem</span>
    <h3>Important work is fragmented</h3>
    <p>Research, planning, training, and campaign preparation often happen across disconnected searches, files, and handoffs. Evidence and assumptions can disappear between steps.</p>
  </section>
  <section>
    <span>Solution</span>
    <h3>Six focused, inspectable plugins</h3>
    <p>Each capability structures a narrow workflow and keeps its inputs, source support, constraints, and review status visible.</p>
  </section>
  <section>
    <span>Expected outcome</span>
    <h3>A decision-ready artifact</h3>
    <p>Teams receive a cited profile, evidence brief, scenario, engagement plan, learning draft, or campaign review package that a qualified person can examine.</p>
  </section>
</div>

## Plugin guides { #plugin-guides }

<p class="section-intro">Choose the question closest to the work in front of you. Every guide explains the problem, objective, workflow, fictional sample input, interpreted output, business value, and technical next step.</p>

<section class="evidence-ribbon" aria-labelledby="portfolio-title">
  <div class="evidence-ribbon__header">
    <strong id="portfolio-title">Six independent capabilities</strong>
    <p>Use one capability on its own, or connect outputs only where identifiers, provenance, and governance remain intact.</p>
  </div>
  <ol>
    <li><a href="capabilities/hcp-intelligence/"><span class="evidence-ribbon__step">01</span><strong>HCP Intelligence</strong><small>How do we prepare for an account conversation?</small><em>Cited public-source profile</em></a><span class="version-tag">HCP 1.0.2</span></li>
    <li><a href="capabilities/competitive-intelligence/"><span class="evidence-ribbon__step">02</span><strong>Competitive Intelligence</strong><small>What changed in the market?</small><em>Evidence brief and timeline</em></a><span class="version-tag">CI 1.1.0</span></li>
    <li><a href="capabilities/territory-alignment/"><span class="evidence-ribbon__step">03</span><strong>Territory Alignment</strong><small>Which coverage scenario works best?</small><em>Assignment and route scenario</em></a><span class="version-tag">TA 1.0.1</span></li>
    <li><a href="capabilities/next-best-engagement/"><span class="evidence-ribbon__step">04</span><strong>Next-Best-Engagement</strong><small>What should the team consider next?</small><em>Consent-aware engagement plan</em></a><span class="version-tag">NBE 1.0.2</span></li>
    <li><a href="capabilities/field-training/"><span class="evidence-ribbon__step">05</span><strong>Field Training</strong><small>How do we build learning from approved sources?</small><em>Learning and role-play draft</em></a><span class="version-tag">FT 1.1.1</span></li>
    <li><a href="capabilities/campaign-studio/"><span class="evidence-ribbon__step">06</span><strong>Campaign Studio</strong><small>How do we prepare material for review?</small><em>Campaign review package</em></a><span class="version-tag">CS 1.0.1</span></li>
  </ol>
</section>

## Documentation contents

<div class="docs-index">
  <section>
    <p>Understand</p>
    <h3>Purpose and outcomes</h3>
    <ul>
      <li><a href="outcomes/">Business outcomes</a> — match a decision to a capability</li>
      <li><a href="#plugin-guides">Plugin guides</a> — problem, solution, workflow, and value</li>
      <li><a href="trust-governance/">Trust and governance</a> — data, evidence, and review boundaries</li>
    </ul>
  </section>
  <section>
    <p>Try</p>
    <h3>Installation and examples</h3>
    <ul>
      <li><a href="get-started/">Get started</a> — public and authorized install paths</li>
      <li><a href="examples/">Fictional examples</a> — input, output, and manifest for every plugin</li>
      <li><a href="assets/data/release.json">Release snapshot</a> — machine-readable version provenance</li>
    </ul>
  </section>
  <section>
    <p>Operate</p>
    <h3>Technical references</h3>
    <ul>
      <li><a href="technical-reference/">Technical reference</a> — pinned configuration and repository guides</li>
      <li><a href="operations/release-sync/">Release sync</a> — website update and review contract</li>
      <li><a href="https://github.com/PharmaGenAI/pharmagenai.github.io">Website source</a> — public documentation repository</li>
    </ul>
  </section>
</div>

<aside class="evidence-note evidence-note--boundary" aria-labelledby="beta-boundary">
  <h2 id="beta-boundary">Human review is part of every workflow</h2>
  <p>Validate identity, source coverage, assumptions, data permissions, and rendered artifacts before operational use. Campaign and field-training materials are drafts for qualified medical, legal, and regulatory review—not evidence of approval. Recommendations do not replace accountable business, medical, legal, privacy, or regulatory judgement.</p>
</aside>

## Technical truth stays with the release

This site explains business use and provides fictional examples. Package versions, installation commands,
release notes, schemas, and technical behavior remain canonical in the authorized repository path linked from the
[technical reference page](technical-reference.md). The machine-readable [release snapshot](assets/data/release.json)
records the full pinned source commit `6bfc6ce43491d66b4ef45b1d3934a58648e1afc6`; the visible short SHA `6bfc6ce`
is derived from that full commit for display only.
