# Conventional Commits — reference

The spec: <https://www.conventionalcommits.org/en/v1.0.0/>. This is the
authoritative format for PR titles and commit subjects in this skill.

## Grammar

```
<type>[(scope)][!]: <description>

[optional body]

[optional footer(s)]
```

- **type** — required. One of the types below.
- **scope** — optional. A noun in parentheses naming the section of the codebase
  affected: `feat(parser):`, `fix(api):`.
- **!** — optional. Placed right before the colon to flag a breaking change:
  `feat(api)!:`.
- **description** — required. Imperative, lowercase, no trailing period.
- **body** — optional. Free-form, after a blank line. Explains the *what* and
  *why*, not the *how*.
- **footer** — optional. `Closes #123`, `Reviewed-by:`, and especially
  `BREAKING CHANGE: <description>` for breaking changes.

## Types

| Type | Use it for | SemVer |
| --- | --- | --- |
| `feat` | A new feature or capability visible to a user of the code/API | **minor** |
| `fix` | A bug fix — corrects wrong behavior | **patch** |
| `docs` | Documentation only (README, comments, docstrings) | — |
| `style` | Formatting, whitespace, semicolons — no logic change | — |
| `refactor` | Code change that neither fixes a bug nor adds a feature | — |
| `perf` | A change that improves performance | — |
| `test` | Adding or correcting tests | — |
| `build` | Build system or external dependencies (npm, webpack, Docker) | — |
| `ci` | CI configuration and scripts (GitHub Actions, pipelines) | — |
| `chore` | Routine maintenance that doesn't touch src or tests | — |
| `revert` | Reverts a previous commit | — |

Only `feat` and `fix` drive version bumps under the spec. A breaking change of
any type drives a **major** bump.

## Choosing the right type

The type is a claim about the *nature* of the change, not its size.

- New behavior a caller can use → `feat`.
- Wrong behavior made right → `fix`.
- Same behavior, cleaner code → `refactor`.
- Faster, same behavior → `perf`.
- Only docs/tests/build/ci moved → the matching type.

When two types both seem to apply, ask "what's the headline?" A refactor that
also happens to fix a bug is a `fix` if the fix is the point, a `refactor` if the
cleanup is the point and the bug fix is incidental — and ideally those are two
PRs.

## Subject-line rules

- **Imperative mood.** "add", "fix", "remove" — completes "If applied, this
  commit will ___". Not "added", "adds", "adding".
- **Lowercase first word**, no trailing period.
- **≤ 50 characters** preferred, **72** hard cap. The title is the squash-merge
  subject; long subjects get truncated in `git log --oneline` and GitHub lists.
- **Describe the change, not the file.** "fix: reject expired tokens" beats
  "fix: update auth.ts".

## Breaking changes

Two ways to flag, use both when possible:

```
feat(api)!: return 422 for validation errors

BREAKING CHANGE: validation failures now respond 422 instead of 400.
Clients keying on 400 must update.
```

The `!` is the at-a-glance signal; the `BREAKING CHANGE:` footer is the
migration note tooling extracts for changelogs.

## Common mistakes to fix on sight

| Bad | Better | Why |
| --- | --- | --- |
| `Fixed login bug` | `fix: reject login with empty password` | No type; past tense; vague |
| `feat: updates` | `feat(cli): add --json output flag` | Vague; no scope; not imperative |
| `fix: Refactored the parser.` | `refactor(parser): split scanner out` | Wrong type; capital; period |
| `chore: add retry logic to API client` | `feat(api): retry failed requests` | New behavior is a feat, not a chore |
