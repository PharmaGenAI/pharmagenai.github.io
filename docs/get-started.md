---
title: Get started
description: Business-first guidance for choosing an Open Pharma Plugins capability, installing the right surface, and reviewing a fictional first output safely.
---

# Get started with one governed workflow

Start with the commercial decision, not the installation command. Choose the narrowest capability that
supports the work in front of you, inspect a fictional example, then let a platform owner connect governed
data, provider keys, and review checkpoints only after the team agrees the output shape is useful.

## Choose the first capability

<div class="outcome-list">
  <section class="outcome-row">
    <span class="outcome-id">01</span>
    <h3>Prepare for an account conversation</h3>
    <p>Use HCP Intelligence when the first output should be a cited public-source profile for an HCP or HCO.</p>
    <span class="version-tag">HCP</span>
  </section>
  <section class="outcome-row">
    <span class="outcome-id">02</span>
    <h3>Review one market question</h3>
    <p>Use Competitive Intelligence when the first output should be a traceable evidence run, briefing, or timeline.</p>
    <span class="version-tag">CI</span>
  </section>
  <section class="outcome-row">
    <span class="outcome-id">03</span>
    <h3>Compare coverage scenarios</h3>
    <p>Use Territory Alignment when the first output should be an assignment and route trade-off scenario.</p>
    <span class="version-tag">TA</span>
  </section>
  <section class="outcome-row">
    <span class="outcome-id">04</span>
    <h3>Prioritise the next engagement</h3>
    <p>Use Next-Best-Engagement when the first output should be a constrained plan with assigned owner and no-action reasons.</p>
    <span class="version-tag">NBE</span>
  </section>
  <section class="outcome-row">
    <span class="outcome-id">05</span>
    <h3>Equip the field from approved content</h3>
    <p>Use Field Training when the first output should be a source-grounded learning, assessment, or role-play draft.</p>
    <span class="version-tag">FT</span>
  </section>
  <section class="outcome-row">
    <span class="outcome-id">06</span>
    <h3>Prepare campaign review material</h3>
    <p>Use Campaign Studio when the first output should be a structured draft package for qualified MLR review.</p>
    <span class="version-tag">CS</span>
  </section>
</div>

[Match the capability to the business outcome →](outcomes/index.md){ .opp-button .opp-button--primary }
[Inspect the fictional examples first →](examples/index.md){ .opp-button }

## Pick the install surface

Open Pharma Plugins supports two installation options. Choose the agent-harness path for the complete plugin
experience, or use the published Python distribution for a Python-managed MCP server.

<div class="install-options" markdown="1">
  <section class="install-option" markdown="1">
  <div class="install-option__label">Option 1 · Agent harness</div>

### Install in Claude Code, Codex, or GitHub Copilot CLI

Use this option when the plugin should run inside Claude Code, Codex, or GitHub Copilot CLI. The repository
installer adds the Skill and MCP tools through the harness's native plugin system.

1. Clone the repository and enter its directory.
2. Inspect `install.sh` before execution.
3. Run `bash install.sh`, choose Claude Code, Codex, or GitHub Copilot CLI, then select the capability.
4. Follow the installer verification step before using governed inputs.

```bash
git clone https://github.com/PharmaGenAI/open-pharma-plugins.git
cd open-pharma-plugins
less install.sh
bash install.sh
```

  [Open the Open Pharma Plugins repository →](https://github.com/PharmaGenAI/open-pharma-plugins)
  </section>

  <section class="install-option install-option--python" markdown="1">
  <div class="install-option__label">Option 2 · Python distribution</div>

### Install the published package

Use this option when you want the published Python distribution or need to manage the MCP server from a Python
environment. This example installs HCP Intelligence.

```bash
python -m pip install "open-pharma-plugins[hcp-intelligence]==2.4.0"
```

Confirm the installed entry point:

```bash
open-pharma-plugins-hcp-intelligence --version
open-pharma-plugins-hcp-intelligence --check-system
```
  </section>
</div>

Python 3.10 to 3.13 is supported. Option 1 requires `uv` and `uvx`; install them from the official `uv`
instructions before running `bash install.sh`. Keep keys in `~/.open-pharma-plugins/config`, not in prompts.

## Review a fictional first output before using governed data

Use the site examples as the first demo because they do not require live credentials, operational files, or
provider calls.

1. Open the capability page that matches the decision you are testing.
2. Download the fictional input, representative output, and manifest for that capability.
3. Confirm the output shape, review boundary, and evidence fields with the business owner before enabling real sources.

The one current runtime-generated public sample is the pinned fictional Next-Best-Engagement fixture. The other
public samples are representative artifacts that show format and review boundaries, not proof that a release
workflow regenerated them.

## Handoff: business user and platform owner

| Role | First responsibility | What to review before the next step |
| --- | --- | --- |
| Business user | Choose the workflow, define the question, and confirm the fictional output is decision-useful | Business scope, accountable reviewer, and whether the output is a draft, recommendation, or evidence brief |
| Platform owner | Install the plugin surface, configure provider keys or local directories, and constrain file access | Python version, `uvx` availability for guided installs, key placement in `~/.open-pharma-plugins/config`, and least-privilege runtime access |
| Qualified reviewer | Validate evidence, content, privacy, policy, and approval boundaries | Identity, permissions, source support, fair balance, consent, territory rules, and release suitability |

## Outputs and permissions to expect

<div class="preview-dossier" markdown="1">
  <div class="preview-label">Public-source research</div>
  <div markdown="1">
### HCP Intelligence and Competitive Intelligence

Expect structured JSON and evidence-backed summaries. Provider keys may be needed for configured web search or
optional synthesis, and public APIs receive the query terms needed for retrieval.
  </div>
</div>

<div class="preview-dossier" markdown="1">
  <div class="preview-label">Governed operations</div>
  <div markdown="1">
### Territory Alignment and Next-Best-Engagement

Expect scenario or plan outputs that depend on governed HCP, representative, consent, interaction, and
assignment data. Review assignment ownership, eligibility rules, capacity assumptions, and export paths before
operational use.
  </div>
</div>

<div class="preview-dossier" markdown="1">
  <div class="preview-label">Approved content</div>
  <div markdown="1">
### Field Training and Campaign Studio

Expect drafts, scorecards, rendered assets, or review packages grounded in supplied approved sources or claims.
These outputs support qualified medical, legal, and regulatory review; they are not approval evidence.
  </div>
</div>

<aside class="evidence-note evidence-note--boundary" aria-labelledby="first-run-boundary">
  <h2 id="first-run-boundary">Do not start with live secrets in prompts or sample files</h2>
  <p>Keep credentials in the configured local file or process environment, not in tool arguments or copied example content. Keep unrelated sensitive files outside the server's readable scope. Validate the fictional first result with the accountable team before enabling operational inputs or external providers.</p>
</aside>

[Read the trust and governance boundaries →](trust-governance.md){ .opp-button .opp-button--primary }
[Open the pinned technical documentation →](technical-reference.md){ .opp-button }
