# Specification template

A specification is the agreed target a change is built against. It exists so the
user and the implementer are pointed at the same thing before any code is
written, and so "done" is a checkable claim rather than a feeling. Scale it to
the work: three bullets for a small fix, the full template for a feature. Never
zero.

Write it from answers, not assumptions. If a section would only contain a guess,
that is a question to ask the user, not a blank to fill.

## Full template

```markdown
# <Task name> — Specification

**Goal:** <one sentence. The outcome in plain language: what the user can do
after this that they cannot do now. Not a restatement of the task title — the
point of the work.>

## Background / why
<2–4 sentences. What problem this solves, why now, and any context the
implementer needs that isn't obvious from the code.>

## In scope
- <each concrete thing this change includes>
- <be specific enough that "did we do this?" has a yes/no answer>

## Out of scope / non-goals
- <each thing this change explicitly does NOT include>
- <non-goals are the strongest defense against scope creep — list them even when
  they feel obvious>

## Constraints
- **Stack / tools:** <language, framework, libraries to use or avoid>
- **Patterns:** <existing conventions in the repo to follow>
- **Do not touch:** <files, systems, or behaviors that must stay as they are>
- **Requirements:** <performance, security, compatibility, accessibility, etc.>

## Inputs and outputs
<Concrete data shapes where they matter: API request/response, file formats,
function signatures, schema, the shape of the UI. Name the edge cases that must
be handled.>

## Approach
<The plan at a reviewable altitude — enough that the user can sanity-check the
direction, not a line-by-line script. Call out the few decisions that carry
risk. If there are real alternatives, name the one chosen and why.>

## Acceptance criteria
- [ ] <a checkable statement of done — behavior, not implementation>
- [ ] <how it will be verified: a test, a command, a demo step>
- [ ] <one criterion per row; a reviewer should be able to tick each>

## Open questions
- <anything still unresolved that the user needs to answer — track it here rather
  than guessing past it>
```

## Short form (small tasks)

For a small, well-bounded change, this is enough — in chat or a few lines in the
repo — as long as the user okays it before you build:

```markdown
**Goal:** <one sentence>
**In scope:** <bullet or two>
**Out of scope:** <the obvious thing this is NOT>
**Done when:** <the checkable acceptance condition>
```

## Notes on use

- **Confirm before building.** The spec is not done because you wrote it; it is
  done when the user agrees it is the right target. "Does this match what you
  want?" is the gate.
- **Keep it current.** If implementation reveals the spec was wrong, fix the spec
  and reconfirm before continuing. A spec that silently diverges from the work is
  worse than none.
- **Where it lives:** chat for small tasks; a committed file (`SPEC.md` or
  `docs/specs/<slug>.md`) for substantial ones, so it is reviewable and survives
  the session. A planning step should produce this artifact before execution.
- **Acceptance criteria are behavior, not code.** "Returns 422 on invalid input"
  is checkable; "refactor the validator" is not. Write the ones a reviewer or a
  test can verify.
