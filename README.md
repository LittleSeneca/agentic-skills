# agentic-skills

Plugins for Claude Code and Claude Cowork, built for governance, risk, and compliance (GRC) and infrastructure security work.

This repo is a Claude Code plugin marketplace, so everything below installs directly from it with one command. Each plugin is the installable package; the skills, the read-only execution rules, and the reference material it carries are what ship inside it.

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

My work is mostly GRC and infrastructure security. Both start from the same ground every time: the same standards, the same house format, the same safety rules. These plugins load that ground once, so the agent begins a task already standing on it instead of paying to find it again.

Two principles run through all of it.

Spend the budget on the work, not the warm-up. Each plugin carries the standard, the format, and the decisions an agent would otherwise rebuild from nothing. It starts at the task, not at the search for the task.

Ground every answer in established practice. The GRC plugin carries real reference material (the NIST SP 800-53 Rev 5 catalog, NIST SP 800-34, ISO 22301, NIST SP 800-61, CSF 2.0) and one consistent house format. The infrastructure plugins are read-only by default and hand every write back to you to run yourself. The output should be auditable and safe, not merely fast.

## Layout

- `plugins/`: every plugin, each with a `.claude-plugin/plugin.json` and the skills it ships under `skills/`.
- `.claude-plugin/marketplace.json`: the marketplace manifest that lists the installable plugins.

## Cloud access plugins

These plugins share one design principle: Claude gets read-only access to your cloud and accounts, and every write is handed back to you as a command you run yourself. You mount the credentials from a file in your Cowork folder, and you only ever give these plugins read-only keys.

| Plugin | Description |
| --- | --- |
| [`aws-readonly`](plugins/aws-readonly/README.md) | Safe AWS access. Read-only commands run automatically under a read-only profile. Every write is handed back to you as a paste-able CLI command. Only ever give it read-only keys. |
| [`azure-readonly`](plugins/azure-readonly/README.md) | Safe Azure access. Read-only commands run automatically as a `Reader` service principal. Every write is handed back to you as a paste-able `az` CLI command. Only ever give it a `Reader` service principal. |
| [`gcp-readonly`](plugins/gcp-readonly/README.md) | Safe Google Cloud access. Read-only commands run automatically under a read-only `gcloud` configuration. Every write is handed back to you as a paste-able CLI command. Only ever give it a read-only service account. |
| [`x-readonly`](plugins/x-readonly/README.md) | Read-only X (Twitter) lookups: profiles, recent posts, search, follower counts, and posts by id via the X API v2. Uses an app bearer token you mount in your Cowork folder. Never posts, deletes, likes, or follows. |

## Writing and workflow plugins

These carry the standards, house format, and decisions for GRC and day-to-day development work. No credentials; install one and its skills trigger automatically.

| Plugin | Description |
| --- | --- |
| [`grc-writing`](plugins/grc-writing/README.md) | The GRC writing family in one consistent ISP house format and plain professional voice. Bundles three skills: `policy-writing` (policies and charters), `control-writing` (measurable controls, carrying the full NIST SP 800-53 Rev 5 catalog), and `process-writing` (BCP, DR, IR, BIA, procedures, and runbooks, on the NIST SP 800-34 / ISO 22301 / NIST SP 800-61 / CSF 2.0 backbone). Enforces hard style rules and pushes back on weak design instead of polishing it. |
| [`pr-writing`](plugins/pr-writing/README.md) | Write pull request titles, branch names, and PR descriptions that are consistent and scannable. Enforces Conventional Commits for titles and commits, a `claude/`-prefixed kebab branch slug that maps to the commit, and PR descriptions that lead with a TL;DR and stay short and well-formatted. |
| [`seneca`](plugins/seneca/README.md) | Write any human-read text in the voice of Seneca the Younger, in style and substance. A global, always-on lens for docs, READMEs, blog posts, letters, release notes, and posts. Enforces hard style rules (no em dashes, no AI slop) and a measured, aphoristic register. Opinion content argues from Stoic ethics. Skips machine-facing text (LLM prompts, code, config, commit messages). |
| [`tyrion`](plugins/tyrion/README.md) | Strategic and tactical thinking coach for consequential decisions, project scoping, tradeoffs, and negotiations, with a triage gate that catches "how" before "why". |
| [`session-startup`](plugins/session-startup/README.md) | The pre-flight checklist for a coding session. Runs three gates in order before the first edit: work in an isolated worktree (not the bare repo), pull current with origin (not a stale tree), and define the work in a written, agreed specification before any code. Pushes back on under-defined asks instead of guessing at scope. |
| [`cowork-workspace`](plugins/cowork-workspace/README.md) | The house rule for where things go in a Cowork environment. Everything agentic lives under one root, `~/Projects/Cowork`: credentials in `keys/`, generated artifacts in `artifacts/<project>/`, settings at the root. Routes every write before it happens and keeps stray files out of `$HOME`, the Desktop, Downloads, `/tmp`, and a repo's tree. The same `keys/` folder the read-only plugins read from. |

## Installing

Add this repo as a marketplace in Claude Code, then install the plugins you want:

```
/plugin marketplace add LittleSeneca/agentic-skills
/plugin install aws-readonly
/plugin install grc-writing
```

Each plugin's own `README.md` covers what it ships and, for the cloud plugins, the credential file it expects and where to mount it. Read it before you mount a key, and mount a read-only key only.

Carry the context once. Spend the rest on the work.
