# agentic-skills

A collection of agentic skills and plugins for Claude Code / Claude Cowork.

## Layout

- `skills/` — individual skills, each in its own folder with a `SKILL.md`.
- `plugins/` — packaged plugins, each with a `.claude-plugin/plugin.json`.

This repo is also a Claude Code plugin marketplace (`.claude-plugin/marketplace.json`), so the plugins below can be installed directly.

## Plugins

| Plugin | Description |
| --- | --- |
| [`aws-readonly`](plugins/aws-readonly/README.md) | Safe AWS access for Claude. Read-only commands run automatically under a read-only profile; every write is handed back to you as a paste-able CLI command. Credentials come from a read-only key file you mount in your Cowork folder. **Only ever give it read-only keys.** |
| [`azure-readonly`](plugins/azure-readonly/README.md) | Safe Azure access for Claude. Read-only commands run automatically as a `Reader` service principal; every write is handed back to you as a paste-able `az` CLI command. Credentials come from a read-only service principal file you mount in your Cowork folder. **Only ever give it a `Reader` service principal.** |
| [`x-readonly`](plugins/x-readonly/README.md) | Read-only X (Twitter) lookups for Claude — profiles, recent posts, search, follower counts, and posts by id via the X API v2. Uses an app bearer token you mount in your Cowork folder. **Strictly read-only:** never posts, deletes, likes, or follows. |

## Skills

| Skill | Description |
| --- | --- |
| [`tyrion`](skills/tyrion/SKILL.md) | Strategic and tactical thinking coach for consequential decisions, project scoping, tradeoffs, and negotiations — with a triage gate that catches "how" before "why". |
| [`policy-writing`](skills/policy-writing/SKILL.md) | Draft, rewrite, or review GRC policies and charters in one consistent ISP house format and a plain professional voice. Covers policies and charters only (not procedures or plans). Enforces hard style rules: no em dashes, no AI slop, auditable requirements. |
| [`control-writing`](skills/control-writing/SKILL.md) | Design, write, review, or rationalize security and compliance controls so they are measurable, actionable, cost-efficient, and risk-aligned. Carries the full NIST SP 800-53 Rev 5 catalog as a machine-readable reference and pushes back on bad control design rather than writing good copy for a weak control. |
