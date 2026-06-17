---
name: pr-writing
description: >
  Write pull request titles, branch names, and PR descriptions that are
  consistent, scannable, and follow Conventional Commits. Use this skill
  whenever the user is opening a PR, drafting or rewriting a PR title or
  description, naming or renaming a branch, writing a commit message, or asks
  "what should I call this PR", "write the PR description", "fix this PR title",
  "name this branch", or "make this follow conventional commits". It enforces
  three things: (1) PR titles and commit subjects follow the Conventional
  Commits spec (type, optional scope, imperative subject); (2) branch names use
  a short owner-prefixed kebab slug that maps cleanly to the conventional commit
  (e.g. `claude/fix-debug-menu` for `fix: safely assign debug menu to window`); and
  (3) PR descriptions lead with a one-line TL;DR and stay short, well-formatted,
  and easy to skim. Reach for it even when the user does not say "conventional
  commits" by name but is clearly producing a PR, a branch, or a commit message
  and wants it to look professional and consistent.
---

# PR Writing

You are helping produce the three artifacts that wrap a code change: the
**branch name**, the **PR title** (which is also the squash-merge commit
subject), and the **PR description**. These are read far more often than they
are written — by reviewers deciding what to look at, by future engineers running
`git log` or `git blame`, and by tooling that generates changelogs and computes
semantic-version bumps. Treat them as part of the change, not paperwork after it.

Three rules govern everything below:

1. **Titles and commits follow Conventional Commits.** Always. This is not
   optional and it is the single most important thing this skill enforces.
2. **Branch names are a kebab slug that maps to the conventional commit.** The
   slug and the title describe the same change in two formats. Default prefix is
  `claude/`.
3. **Descriptions lead with a TL;DR and stay short and scannable.** A reviewer
   should understand the change in ten seconds and know how to verify it in
   thirty.

When in doubt about exact spec wording, the type table, or template structure,
read the reference files:

- `references/conventional-commits.md` — the full type list, scope/breaking-change
  rules, and the subject-line grammar.
- `references/branch-naming.md` — the slug convention and worked examples.
- `references/pr-description-template.md` — the description template plus filled
  examples for small, medium, and large PRs.

## First: figure out what the change actually is

Before writing anything, know the answer to three questions. Look at the diff,
the commits, or ask — do not guess.

- **What does this change do?** One sentence, in plain language. This becomes the
  TL;DR and drives the title.
- **What *type* is it?** `feat`, `fix`, `refactor`, `docs`, …? The type is the
  first word of the title and it is a claim about user-visible impact, not about
  how much code moved. A 400-line internal restructure that changes no behavior
  is a `refactor`, not a `feat`. A one-line change that fixes a real bug is a
  `fix`.
- **Is anything breaking?** If a consumer has to change how they call the code,
  it is a breaking change and must be marked (`!` after the type, or a
  `BREAKING CHANGE:` footer). Get this right — it drives major-version bumps.

If a single PR genuinely does several unrelated things, the best fix is usually
to split it. If it can't be split, pick the type of the *primary* change for the
title and enumerate the rest in the description.

## Rule 1 — PR titles and commit subjects: Conventional Commits

The format is:

```
<type>[optional scope][!]: <description>
```

Worked examples:

```
feat: add multi-region failover to the upload service
fix(auth): reject expired refresh tokens instead of silently renewing
refactor(parser): extract token scanner into its own module
docs: document the rate-limit headers
perf(search): cache the analyzer to cut p99 by 40%
feat(api)!: return 422 instead of 400 for validation errors
```

The non-negotiable rules:

- **A valid type is required.** Use the smallest accurate one. The common set:
  `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`,
  `chore`, `revert`. Full descriptions and when-to-use notes live in
  `references/conventional-commits.md`.
- **Scope is optional and goes in parentheses.** Use it when it adds real signal
  (the package, module, or surface touched: `fix(auth):`, `feat(billing):`).
  Skip it rather than inventing a vague one.
- **`feat` and `fix` are special.** They are the only types that, by spec, drive
  semantic-version bumps (minor and patch respectively). Don't reach for `feat`
  on a change that adds no capability just to make it sound bigger.
- **The description is a lowercase, imperative-mood phrase with no trailing
  period.** Write "add", "fix", "remove" — not "added", "adds", "this fixes". It
  should complete the sentence "If applied, this commit will ___".
- **Keep the title short.** Aim for ≤ 50 characters; hard cap around 72. Long
  titles get truncated in `git log --oneline`, GitHub's PR list, and changelog
  output, and some tooling rejects or mangles them — so put only the headline in
  the title and push detail into the description. If the title needs an "and",
  it's probably two PRs.
- **Mark breaking changes.** Put `!` before the colon and add a
  `BREAKING CHANGE:` footer in the body explaining the migration.

If a title someone wrote doesn't fit the spec, rewrite it and briefly say what
you changed and why ("retyped as `fix` since this changes behavior, not just
structure").

## Rule 2 — Branch names

Branch names use a short owner prefix and a kebab-case slug:

```
<prefix>/<type>-<short-slug>
```

The slug is the conventional commit, compressed. The canonical example:

```
branch:  claude/fix-debug-menu
commit:  fix: safely assign debug menu to window
```

`claude` is the prefix, `fix` is the commit type, and `debug-menu` is the
subject squeezed to its keywords. The branch and the title are the same change
in two registers — the branch is the terse handle, the title is the readable
sentence.

Rules:

- **Prefix** with `claude/` by default, since Claude is creating the branch. If
  the repo already uses a different convention (author initials, a team or
  ticket id), match what the repo uses — check `git branch -a` or recent merged
  PRs before inventing a scheme.
- **Lead the slug with the conventional type** (`fix-`, `feat-`, `refactor-`,
  `docs-`) so the branch and the eventual commit agree.
- **kebab-case only** — lowercase words joined by hyphens. No spaces,
  underscores, slashes inside the slug, capitals, or punctuation.
- **Keep it short** — 2 to 4 words after the type. The full sentence lives in the
  title; the branch just needs to be unique and recognizable.
- If the work tracks an issue, `claude/fix-1234-debug-menu` (id after the type)
  is a good pattern when the repo wants traceability.

More worked examples are in `references/branch-naming.md`.

## Rule 3 — PR descriptions: TL;DR first, short, scannable

A PR description is read by a reviewer who has not seen the code and has limited
time. Optimize for fast comprehension, not completeness. The structure:

```markdown
**TL;DR:** <one sentence — what this does and why, in plain language>

## What & why
<2–4 sentences of context. What problem, why now, what approach.>

## Changes
- <the handful of changes that matter, as bullets>
- <skip the obvious; a reviewer can read the diff>

## How to test
1. <concrete steps a reviewer runs to verify>

## Notes
<optional: tradeoffs, follow-ups, things you're unsure about, screenshots>
```

Principles, in priority order:

1. **Lead with a bold one-line TL;DR.** It is the first thing in the body, always.
   If a reviewer reads only that line, they should still know what the PR does.
   Keep it to one sentence in plain language — not a restatement of the title.
2. **Short beats complete.** A description that fits on one screen gets read. Cut
   anything the diff already says. Don't narrate every file.
3. **Use formatting to make it skimmable.** Headings, bullets, and short
   paragraphs — not walls of prose. Bold the few words that carry the most
   signal. Use fenced code blocks for commands, errors, and identifiers.
4. **Make verification trivial.** "How to test" should be copy-pasteable steps,
   not "see the tests". A reviewer who can verify in 30 seconds approves faster.
5. **Surface risk and unknowns honestly.** Call out tradeoffs, things you're
   unsure about, and follow-up work in a Notes section. This builds trust and
   focuses review on the parts that need it.
6. **Scale the template to the change.** A one-line typo fix needs only a TL;DR
   and maybe one bullet — do not force empty headings onto it. A large feature
   earns every section. Drop sections that would be empty; never leave
   `## Screenshots` with nothing under it.
7. **Link, don't paste.** Reference the issue (`Closes #1234`), the design doc,
   or the prior PR rather than reproducing them. Use `Closes`/`Fixes` keywords so
   the issue auto-closes on merge.

Full filled examples at three sizes are in
`references/pr-description-template.md`.

## Putting it together — a worked example

A change that fixes a crash when the debug menu loads before `window` exists:

```
branch:  claude/fix-debug-menu

title:   fix: safely assign debug menu to window

body:
**TL;DR:** Guard the debug-menu global so it no longer crashes when the
bundle loads before `window` is defined (e.g. during SSR).

## What & why
The debug menu assigned itself to `window` at module load. In the SSR path
`window` is undefined, so the bundle threw on import and took the whole page
down. This wraps the assignment in a `typeof window` guard.

## Changes
- Guard the `window.__debugMenu` assignment behind a `typeof window !== "undefined"` check

## How to test
1. `npm run build && npm run ssr`
2. Load any page — it renders instead of 500ing.

Closes #482
```

## When you actually create the PR

If you're driving `git`/`gh` (or the github skill) to open the PR, not just
drafting text:

- **Verify the type against the diff** before committing to it — read what
  actually changed.
- **Match the repo's existing conventions** where they're stronger than the
  defaults here. If every merged PR uses `area:` scopes or a ticket prefix,
  follow that. Check recent history first.
- **Keep the squash-merge subject clean.** On squash merges the PR title becomes
  the commit subject, so the title must be a valid Conventional Commit on its
  own.
- Don't push, open, or merge anything the user didn't ask you to. Draft first,
  act on confirmation.
