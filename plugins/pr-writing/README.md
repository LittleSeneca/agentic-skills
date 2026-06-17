# pr-writing

Pull request titles, branch names, and PR descriptions that are consistent and scannable.

This plugin enforces three things so a reviewer can read a PR at a glance:

- **Titles and commit subjects** follow the Conventional Commits spec (type, optional scope, imperative subject).
- **Branch names** use a short owner-prefixed kebab slug that maps cleanly to the commit, e.g. `claude/fix-debug-menu` for `fix: safely assign debug menu to window`.
- **PR descriptions** lead with a one-line TL;DR and stay short, well-formatted, and easy to skim.

## Skill

| Skill | What it does |
|---|---|
| `pr-writing` | Triggers when you open a PR, draft or rewrite a title or description, name a branch, or write a commit message. Reference material (Conventional Commits, branch naming, the PR description template) lives under `references/`. |

## Setup

No credentials. Install the plugin and the skill triggers automatically.
