# agentic-skills

Skills and plugins for Claude Code and Claude Cowork, built for governance, risk, and compliance (GRC) and infrastructure security work.

This repo is also a Claude Code plugin marketplace, so the plugins below install directly from it.

<p align="center">
  <a href="https://xkcd.com/1838/">
    <img src="https://imgs.xkcd.com/comics/machine_learning.png"
         alt="XKCD 1838: Machine Learning. 'This is your machine learning system?' 'Yup! You pour the data into this big pile of linear algebra, then collect the answers on the other side.' 'What if the answers are wrong?' 'Just stir the pile until they start looking right.'"
         width="320">
  </a>
  <br>
  <em><a href="https://xkcd.com/1838/">XKCD 1838: Machine Learning</a>. The aim here is to do a little less stirring.</em>
</p>

## Why this exists

An agent spends most of its budget before it does any real work. It opens the same files, relearns the same conventions, and works out where to begin, every session, and it keeps none of it. On a large or unfamiliar project that ramp-up can eat a large share of the tokens and leave nothing behind.

Seneca said it of life: it is not that we have a short time, but that we waste much of it. The same holds for a context window.

My work is mostly GRC and infrastructure security. Both start from the same ground every time: the same standards, the same house format, the same safety rules. These skills and plugins load that ground once, so the agent begins a task already standing on it instead of paying to find it again.

Two principles run through all of it.

Spend the budget on the work, not the warm-up. Each skill carries the standard, the format, and the decisions an agent would otherwise rebuild from nothing. It starts at the task, not at the search for the task.

Ground every answer in established practice. The GRC skills carry real reference material (the NIST SP 800-53 Rev 5 catalog, NIST SP 800-34, ISO 22301, NIST SP 800-61, CSF 2.0) and one consistent house format. The infrastructure plugins are read-only by default and hand every write back to you to run yourself. The output should be auditable and safe, not merely fast.

## Layout

- `skills/`: individual skills, each in its own folder with a `SKILL.md`.
- `plugins/`: packaged plugins, each with a `.claude-plugin/plugin.json`.
- `.claude-plugin/marketplace.json`: the marketplace manifest that lists the installable plugins.

## Plugins

The plugins share one design principle: Claude gets read-only access to your cloud and accounts, and every write is handed back to you as a command you run yourself. You mount the credentials from a file in your Cowork folder, and you only ever give these plugins read-only keys.

| Plugin | Description |
| --- | --- |
| [`aws-readonly`](plugins/aws-readonly/README.md) | Safe AWS access. Read-only commands run automatically under a read-only profile. Every write is handed back to you as a paste-able CLI command. Only ever give it read-only keys. |
| [`azure-readonly`](plugins/azure-readonly/README.md) | Safe Azure access. Read-only commands run automatically as a `Reader` service principal. Every write is handed back to you as a paste-able `az` CLI command. Only ever give it a `Reader` service principal. |
| [`gcp-readonly`](plugins/gcp-readonly/README.md) | Safe Google Cloud access. Read-only commands run automatically under a read-only `gcloud` configuration. Every write is handed back to you as a paste-able CLI command. Only ever give it a read-only service account. |
| [`x-readonly`](plugins/x-readonly/README.md) | Read-only X (Twitter) lookups: profiles, recent posts, search, follower counts, and posts by id via the X API v2. Uses an app bearer token you mount in your Cowork folder. Never posts, deletes, likes, or follows. |

## Skills

| Skill | Description |
| --- | --- |
| [`tyrion`](skills/tyrion/SKILL.md) | Strategic and tactical thinking coach for consequential decisions, project scoping, tradeoffs, and negotiations, with a triage gate that catches "how" before "why". |
| [`seneca`](skills/seneca/SKILL.md) | Write any human-read text in the voice of Seneca the Younger, in style and substance. A global, always-on lens for docs, READMEs, blog posts, letters, release notes, and posts. Enforces hard style rules (no em dashes, no AI slop) and a measured, aphoristic register. Opinion content argues from Stoic ethics. Skips machine-facing text (LLM prompts, code, config, commit messages). |
| [`policy-writing`](skills/policy-writing/SKILL.md) | Draft, rewrite, or review GRC policies and charters in one consistent ISP house format and a plain professional voice. Covers policies and charters only, not procedures or plans. Enforces hard style rules: no em dashes, no AI slop, auditable requirements. |
| [`control-writing`](skills/control-writing/SKILL.md) | Design, write, review, or rationalize security and compliance controls so they are measurable, actionable, cost-efficient, and risk-aligned. Carries the full NIST SP 800-53 Rev 5 catalog as a machine-readable reference and pushes back on bad control design rather than writing good copy for a weak control. |
| [`process-writing`](skills/process-writing/SKILL.md) | Draft, rewrite, or review the operational documents an organization has to execute under pressure: BCP, DR, IR plans, COOP, BIA, and the procedures and runbooks that operationalize a policy. Carries the universal contingency-planning backbone (NIST SP 800-34, ISO 22301/22317/27031, NIST SP 800-61, CSF 2.0) and pushes back on a plan nobody can actually run. |
| [`pr-writing`](skills/pr-writing/SKILL.md) | Write pull request titles, branch names, and PR descriptions that are consistent and scannable. Enforces Conventional Commits for titles and commits, a `claude/`-prefixed kebab branch slug that maps to the commit, and PR descriptions that lead with a TL;DR and stay short and well-formatted. |

## Installing the plugins

Add this repo as a marketplace in Claude Code, then install the plugins you want:

```
/plugin marketplace add LittleSeneca/agentic-skills
/plugin install aws-readonly
```

Each plugin's own `README.md` covers the credential file it expects and where to mount it. Read it before you mount a key, and mount a read-only key only.

## Using the skills

Copy a skill folder from `skills/` into your `.claude/skills/` directory, or point Claude Code at this repo. Each skill's `SKILL.md` documents when it triggers and how it behaves.

Carry the context once. Spend the rest on the work.
