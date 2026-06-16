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

## Skills

| Skill | Description |
| --- | --- |
| [`tyrion`](skills/tyrion/SKILL.md) | Strategic and tactical thinking coach for consequential decisions, project scoping, tradeoffs, and negotiations — with a triage gate that catches "how" before "why". |
