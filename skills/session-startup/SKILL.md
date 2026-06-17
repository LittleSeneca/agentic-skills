---
name: session-startup
description: >
  Run the safe-start checklist before doing real work in a project: confirm you
  are in a git worktree rather than editing the repo's main checkout directly,
  pull the current state from origin so you are not building on a stale tree, and
  refuse to start coding from a vague ask until there is a written specification
  to build against. Use this skill at the beginning of any coding session, when
  the user says "let's start", "work on this project", "build me X", "implement
  Y", "fix this", or hands over a task that is not yet specified, and any time
  you are about to make your first edit in a repo this session. It enforces three
  gates in order: (1) you are on an isolated worktree, not the bare repo; (2) the
  local tree is current with origin; (3) the work is defined by a specification
  document before any code is written. Reach for it even when the user does not
  say "worktree", "pull", or "spec" by name but is clearly about to have you
  change code in a shared repository.
---

# Session Startup

This skill is the pre-flight checklist for working inside a project. It runs
before the first edit, not after the first bug. The cost of skipping it is paid
later and with interest: work done on the wrong branch, work built on a stale
tree, or a confident implementation of the wrong thing.

There are three gates. Run them **in order**. Do not pass a later gate while an
earlier one is still failing — being current with origin does not matter if you
are editing the wrong checkout, and a clean worktree does not matter if nobody
has said what to build.

1. **Isolation** — you are in a worktree, not writing directly to the repo.
2. **Freshness** — your local tree reflects origin (usually a `git pull`).
3. **Specification** — the work is defined in writing before any code is written.

The first two gates are mechanical and you should clear them yourself, quietly,
without making the user watch. The third gate is a conversation, and it is the
one that most often needs you to stop and push back.

## Gate 1 — Isolation: work in a worktree, not the repo

Never make your first edit in the repository's primary checkout. Use a git
worktree so your work is isolated on its own branch and the user's main checkout
stays untouched.

Check where you are before you touch anything:

```bash
git rev-parse --is-inside-work-tree   # are we even in a repo?
git worktree list                     # which checkout is this?
git rev-parse --show-toplevel         # the path of this checkout
git branch --show-current             # the branch we are on
```

Decide:

- **Already in a dedicated worktree on a feature branch** (the common case when a
  harness has placed you in one — the toplevel path contains `worktrees/` or the
  branch is clearly a task branch like `claude/...`): you are good. Note it and
  move to Gate 2.
- **In the primary checkout, on the default branch** (`main`/`master`): stop.
  Do not edit here. Create a worktree on a new branch and move into it:

  ```bash
  git worktree add ../<repo>-<short-slug> -b claude/<type>-<short-slug>
  ```

  Use the branch-naming convention from the `pr-writing` skill for the slug.
  Then do the rest of the work there.
- **In the primary checkout but on a feature branch** the user created for this
  work: acceptable if that is clearly the intent, but say so out loud
  ("working directly on `<branch>` in the main checkout, not a worktree — say the
  word if you'd rather I isolate it"). Prefer a worktree when the work is
  non-trivial or long-running.
- **Not in a git repo at all:** surface that. Offer to `git init` or to clone the
  right repo, but do not start writing files into an untracked directory as if it
  were a project.

Why a worktree and not just a branch: a worktree gives the branch its own working
directory, so builds, dependency installs, and half-finished edits never collide
with whatever the user is doing in their main checkout. They can keep working,
review your branch, or run the app from `main` while you build — nothing of yours
leaks into their tree until a PR merges.

## Gate 2 — Freshness: be current with origin

A worktree on a stale base produces merge pain and "works on my machine"
surprises. Before building, make the local tree current.

```bash
git fetch origin
git status -sb            # ahead/behind, and is the tree dirty?
git log --oneline -5      # what is the local tip?
```

Then bring it current. The usual move is a pull on the branch you are basing on:

```bash
git pull --ff-only origin <base-branch>     # typically main
```

Judgment, not ceremony:

- **Fast-forward when you can.** `--ff-only` keeps history clean and fails loudly
  rather than producing a surprise merge commit. If it can't fast-forward,
  rebase the worktree branch onto the updated base (`git rebase origin/main`)
  rather than letting divergence pile up.
- **Do not clobber uncommitted work.** If `git status` shows local changes you
  did not make, stop and ask before pulling or rebasing over them. The user's
  in-progress edits are not yours to discard.
- **A fetch can be enough.** If you only need to read or branch from origin's
  state, `git fetch` plus branching from `origin/main` avoids touching the
  working tree at all.
- **Note divergence honestly.** If the branch is already ahead of origin (work in
  flight), say so rather than blindly pulling.

Clear this gate quietly when it is routine. Only narrate it when something is off
— behind by a lot, a dirty tree, a non-fast-forward — because those are the cases
where the user's input actually changes what you do.

## Gate 3 — Specification: define the work before writing code

This is the gate that matters most and the one most often skipped. **Do not start
implementing from a vague ask.** A one-line request like "build me a dashboard"
or "add auth" is a direction, not a specification, and starting to code from it
means you are guessing — at the scope, the constraints, the definition of done —
and guesses compound into work that has to be thrown away.

The rule: **before the first line of implementation, there is a written
specification you and the user have agreed on.** Small tasks get a small spec;
large tasks get a fuller one. The point is that the target is written down, not
that the document is long.

### Push back on under-defined asks

When the ask is too thin to build from, say so plainly and turn it into
questions. Pushing back here is not friction; it is the cheapest part of the
whole job. Name what is missing rather than asking "can you give me more detail":

- **Outcome** — what does "done" look like? What can the user do after this that
  they can't now?
- **Scope and non-goals** — what is explicitly in, and what is explicitly *not*
  in this change? Non-goals prevent scope creep more than goals do.
- **Constraints** — language, framework, existing patterns to follow, things not
  to touch, performance or security requirements.
- **Inputs and outputs** — concrete data shapes, API contracts, file formats,
  edge cases.
- **Acceptance** — how will we verify it works? What does the test or the demo
  look like?

Ask the few questions whose answers actually change the implementation. Do not
interrogate; two or three sharp questions beat a checklist. If the user has
genuinely answered everything in their prompt, do not manufacture friction —
write the spec from what they gave you and confirm it.

Use `AskUserQuestion` when the open decisions are a small set of concrete
choices (which framework, which of two approaches, in-scope or not). Use plain
prose when the gap is open-ended ("what should the dashboard actually show?").

### Write the spec, then confirm it

Turn the answers into a short specification document and get a thumbs-up before
building. The structure lives in `references/spec-template.md`; the short form is:

```markdown
# <Task> — Specification

**Goal:** <one sentence: the outcome, in plain language>

## In scope
- <what this change includes>

## Out of scope / non-goals
- <what it explicitly does not include>

## Constraints
- <stack, patterns, things not to touch, requirements>

## Approach
- <the plan, at a high level — enough to review, not every line>

## Acceptance criteria
- [ ] <how we know it's done and correct>
```

Where the spec lives depends on the size of the work:

- **Small task:** the spec can be a few lines in chat that the user okays. Still
  write it down — agreement on three bullets beats a shared assumption.
- **Substantial task:** write it to a file in the repo (e.g. `SPEC.md`, or a
  `docs/specs/<slug>.md`) so it is reviewable, version-controlled, and survives
  the session. This is also what a planning step (`EnterPlanMode`, or the project's
  own planning skill) should produce before execution.

Then **stop and confirm.** "Here's the spec — does this match what you want
before I build it?" Only after the user agrees do you write implementation code.
If the work reveals the spec was wrong, update the spec first and reconfirm,
rather than silently drifting from the agreed target.

## Running the checklist

At the start of a coding session, walk the gates in order:

1. **Isolation** — check the worktree, create one if needed. Quiet unless action
   is required.
2. **Freshness** — fetch and bring current. Quiet unless something is off.
3. **Specification** — this is where you slow down. Push back on a thin ask, write
   the spec, confirm it, *then* build.

The first two are about not building in the wrong place or on the wrong base. The
third is about not building the wrong thing. All three are cheaper now than the
rework they prevent.
