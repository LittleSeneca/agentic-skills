# Branch naming — reference

A branch name is the terse handle for a change; the PR title is the readable
sentence. They describe the same change in two registers and should agree on the
type.

## Format

```
<prefix>/<type>-<short-slug>
```

```
claude/fix-debug-menu          →  fix: safely assign debug menu to window
claude/feat-json-output        →  feat(cli): add --json output flag
claude/refactor-token-scanner  →  refactor(parser): extract token scanner into its own module
claude/docs-rate-limits        →  docs: document the rate-limit headers
claude/chore-bump-eslint       →  chore(deps): bump eslint to 9.x
```

## Parts

- **prefix** — `claude/` by default, since Claude is creating the branch. If the
  repo uses a different scheme (author initials, a team id, or a ticket key as
  the prefix), match that instead. Check `git branch -a` and recent merged PRs
  before picking a scheme.
- **type** — the Conventional Commit type, so the branch and the eventual commit
  line up: `fix-`, `feat-`, `refactor-`, `perf-`, `docs-`, `chore-`, `test-`.
- **slug** — the subject compressed to 2–4 keywords, kebab-case.

## Rules

- **kebab-case only.** Lowercase words joined by single hyphens. No spaces,
  underscores, capitals, dots, or extra slashes inside the slug.
- **Short.** 2–4 words after the type. The branch is a handle, not a sentence —
  the full description lives in the PR title.
- **Drop filler.** "the", "a", "and", articles, and prepositions usually go.
  `debug-menu`, not `assign-the-debug-menu-to-window`.
- **Stay unique and recognizable.** Enough to tell it apart from other branches
  at a glance.

## With a ticket / issue id

When the repo wants traceability, put the id right after the type:

```
claude/fix-482-debug-menu      →  fix: safely assign debug menu to window  (Closes #482)
claude/feat-PROJ-1234-sso      →  feat(auth): add SSO login
```

## Mapping a title back to a slug

1. Take the type → branch type (`fix:` → `fix-`).
2. Take the subject, drop filler words, keep the 2–3 nouns/verbs that identify it.
3. kebab-case them.

`fix(auth): reject expired refresh tokens` → `claude/fix-reject-expired-tokens`
(or the tighter `claude/fix-expired-tokens`).
