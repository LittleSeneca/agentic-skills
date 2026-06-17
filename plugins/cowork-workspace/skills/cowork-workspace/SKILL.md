---
name: cowork-workspace
description: >
  How to work inside this Cowork environment without leaving a mess. Everything
  the agent produces or relies on lives under one root, `~/Projects/Cowork`:
  credentials in `keys/`, generated files and project output in
  `artifacts/<project>/`, and settings and configuration at the root. Use this
  skill whenever you are about to write a file, save or read a key or credential,
  generate an artifact (a report, export, script, scratch file, download, or
  anything that is not part of a tracked git repo), or set up working state for a
  task — and any time the user asks where something should go, says "save this",
  "write that out", "put it somewhere", "generate a", or hands you a credential.
  It also governs cleanup: no stray files in `$HOME`, the Desktop, Downloads,
  `/tmp`, or a repo's working tree. Reach for it even when the user does not say
  "Cowork", "artifacts", or "keys" by name but is clearly about to have you put
  something on disk outside of a git repository.
---

# Cowork Workspace

This is the house rule for where things go. The agent's job is not only to produce
good work but to leave the filesystem in a state where the next session, and the
human, can find what was made and trust where the keys are. A correct answer
written to a random path is a half-finished answer.

There is exactly one root for everything agentic: **`~/Projects/Cowork`**. Keys,
generated artifacts, settings, and scratch state all live under it. Nothing the
agent creates for itself belongs anywhere else.

```
~/Projects/Cowork/
├── keys/                  # every credential the agent uses (read-only keys, tokens, SA files)
├── artifacts/             # everything the agent generates, one subfolder per project/task
│   └── <project>/         # reports, exports, scripts, scratch, downloads — grouped by project
└── <config/settings>      # working settings and configuration for the environment
```

Two rules carry the whole skill. Read them, then apply the routing below.

1. **Keys live in `~/Projects/Cowork/keys/`.** Every credential the agent reads —
   cloud keys, API tokens, service-account files, bearer tokens — comes from that
   folder. The agent never invents a new home for a secret.
2. **Generated files live in `~/Projects/Cowork/artifacts/<project>/`.** Anything
   the agent writes that is not a commit to a tracked git repository goes under
   `artifacts/`, inside a folder named for the project or task. The top-level
   bucket is always `artifacts`; the per-project folder lives under it.

## Where does this file go?

Decide before you write, not after. Walk it in order:

- **Is it a credential** (a key, token, secret, service-account JSON, config that
  holds a login)? → `~/Projects/Cowork/keys/`. Lock it down (`chmod 0600`), never
  echo it into chat, never commit it. See [Keys](#keys-cowork-keys).
- **Are you committing to a tracked git repository** you are already working in
  (source, tests, docs that belong to that repo)? → leave it in the repo. This
  skill does not pull a repo's own files into `artifacts/`. The Cowork root is for
  work that has no other home, not a place to scatter a project's tracked files.
- **Is it anything else the agent generated** — a report, a data export, a
  one-off script, a screenshot, a download, a scratch note, a draft, a build
  output you want to keep? → `~/Projects/Cowork/artifacts/<project>/`. Pick a
  short, stable, kebab-case project name and reuse it for everything in that task.
- **Is it environment settings or configuration** (not a secret) the agent or the
  user wants to persist for this workspace? → the Cowork root
  (`~/Projects/Cowork/`), in a clearly named file or dot-folder.

If none of the above fits and you are tempted to write to `$HOME`, the Desktop,
Downloads, `/tmp`, or the current directory just because it is convenient — stop.
That is the case this skill exists to catch. Route it into `artifacts/` instead.

## Artifacts

`artifacts/` is the default destination for everything the agent makes that is not
a commit to a repo. One folder per project or task, named for the work:

```
~/Projects/Cowork/artifacts/
├── caterpillar-questionnaire/
│   ├── draft-answers.md
│   └── source-exports/
├── q3-cost-review/
│   ├── findings.md
│   └── billing.csv
└── nuclei-triage/
    └── report-2026-06-17.md
```

How to use it:

- **Name the project folder once and reuse it.** All output from a task lands in
  the same `artifacts/<project>/` folder. Do not spray related files across
  several siblings. If the user has already named the effort, use that name.
- **Create the folder when you need it.** `mkdir -p
  ~/Projects/Cowork/artifacts/<project>` before the first write. Do not ask
  permission to make the folder; just put work in the right place.
- **Tell the user the path.** When you save something, say where it went
  (`~/Projects/Cowork/artifacts/<project>/<file>`) so they can open it. A saved
  file the user cannot locate is not saved.
- **Subfolder freely inside a project.** Group raw inputs, drafts, and final
  output within `artifacts/<project>/` however the task wants. The discipline is
  at the top two levels (`artifacts/` then the project), not below.

## Keys {#keys-cowork-keys}

`~/Projects/Cowork/keys/` is the single home for every credential the agent uses.
This is also where the cloud plugins in this repo (`aws-readonly`, `azure-readonly`,
`gcp-readonly`, `x-readonly`) read their keys from — the same folder, by design.

- **Read keys from `keys/`, never from elsewhere.** If a credential is expected
  but missing from `~/Projects/Cowork/keys/`, say so and point at the relevant
  plugin README; do not hunt for the secret in `$HOME`, shell history, or env
  dumps, and do not ask the user to paste it into chat.
- **Write keys only into `keys/`, locked down.** Any credential file the user has
  you create goes there with `chmod 0600`. One credential per purpose, named for
  what it is (`aws-credentials`, `gcp-readonly-key.json`, `x-credentials`).
- **Never echo a key into chat, a log, an artifact, or a commit.** Read it, use
  it, keep it in the file. A secret that reaches the transcript is a leaked
  secret. When a command would print a token, redirect or mask it.
- **Prefer read-only credentials.** This environment's whole posture is least
  privilege: the agent runs reads and hands writes back to the user. Keys in this
  folder should be read-only wherever the platform supports it.

## The discipline, in one line

Before any write, ask: secret, repo commit, or generated artifact? Secrets go to
`keys/`, repo files stay in the repo, everything else the agent makes goes to
`artifacts/<project>/`. Nothing the agent creates lands outside `~/Projects/Cowork`.
