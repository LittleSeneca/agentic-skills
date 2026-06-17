# session-startup

The pre-flight checklist for a coding session.

Before the first edit in a repo, this plugin runs three gates in order:

1. **Worktree, not the bare repo.** Confirm you are on an isolated worktree rather than editing the main checkout directly.
2. **Current with origin.** Pull the current state so you are not building on a stale tree.
3. **Specification before code.** Refuse to start from a vague ask until there is a written, agreed specification to build against.

It pushes back on an under-defined task instead of guessing at scope.

## Skill

| Skill | What it does |
|---|---|
| `session-startup` | Triggers at the start of a coding session, on "let's start", "work on this project", "build me X", "implement Y", "fix this", or any time you are about to make a first edit. A spec template lives under `references/`. |

## Setup

No credentials. Install the plugin and the skill triggers automatically.
