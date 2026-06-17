# PR description template — reference

The goal: a reviewer who has not seen the code understands the change in ten
seconds (TL;DR) and knows how to verify it in thirty (How to test). Lead with the
TL;DR, keep it short, format for skimming, scale to the change.

## The template

```markdown
**TL;DR:** <one plain-language sentence — what this does and why>

## What & why
<2–4 sentences. The problem, why now, the approach taken. Link the issue/doc.>

## Changes
- <the few changes that matter>
- <skip anything the diff makes obvious>

## How to test
1. <copy-pasteable steps a reviewer runs to verify>

## Notes
<optional: tradeoffs, follow-ups, open questions, screenshots, risk>

Closes #<issue>
```

Drop any section that would be empty. Never leave an empty heading.

## Formatting habits that make a description skimmable

- **Bold the TL;DR** and put it first, before any heading.
- Bullets for changes and lists; short paragraphs (2–4 sentences) for prose.
- Fenced code blocks for commands, errors, config, and identifiers.
- Bold the few words in a paragraph that carry the most signal.
- Tables only when comparing things (before/after, option matrix).
- Screenshots/GIFs for any visible UI change, under a `## Notes` or
  `## Screenshots` heading.
- `Closes #123` / `Fixes #123` in a footer so the issue auto-closes on merge.

---

## Example — small PR (typo / one-liner)

Scale down. A TL;DR and maybe one bullet is the whole thing.

```markdown
**TL;DR:** Fix a typo in the onboarding email subject ("Wecome" → "Welcome").

Closes #771
```

Title: `fix: correct typo in onboarding email subject`
Branch: `claude/fix-onboarding-typo`

---

## Example — medium PR (a bug fix with context)

```markdown
**TL;DR:** Stop the upload worker from retrying non-retryable 4xx errors,
which was hammering the API and masking real client bugs.

## What & why
The worker retried every failed upload with exponential backoff, including
`400`/`422` responses that will never succeed. Under a malformed-batch
incident last week this turned one bad client into ~12k requests/min. We now
only retry `429` and `5xx`.

## Changes
- Classify upload failures into retryable (`429`, `5xx`) and terminal (`4xx`)
- Fail fast on terminal errors and surface them to the caller
- Add a metric (`upload.retry.skipped`) for skipped retries

## How to test
1. `npm test -- upload-worker`
2. Run `scripts/replay-batch.sh fixtures/malformed.json` — it now errors once
   instead of looping.

## Notes
Backoff config is unchanged. Follow-up: alert on `upload.retry.skipped` spikes.

Closes #1290
```

Title: `fix(uploads): stop retrying non-retryable 4xx errors`
Branch: `claude/fix-upload-retries`

---

## Example — large PR (a feature)

```markdown
**TL;DR:** Add multi-region failover to the upload service so a single region
outage no longer drops uploads.

## What & why
We currently pin uploads to `us-east-1`; the March outage lost ~40 min of
uploads. This adds a region-aware client that fails over to `us-west-2` on
health-check failure, with the design from the [failover RFC](link).

## Changes
- New `RegionRouter` that picks a healthy region per request
- Health checks per region with a 5s TTL cache
- Config: `UPLOAD_REGIONS` (ordered preference list)
- Backfills metrics with a `region` label

## How to test
1. `npm run test:integration -- failover`
2. Local: `make sim-region-down REGION=us-east-1` and confirm uploads
   succeed via `us-west-2` (watch `region` in the logs).

## Notes
- **Out of scope:** cross-region read replication (tracked in #1455).
- **Risk:** failover adds one health-check RTT to cold requests; cached path
  is unaffected.
- Rollout behind the `multi_region_uploads` flag, default off.

Closes #1402
```

Title: `feat(uploads): add multi-region failover`
Branch: `claude/feat-multiregion-failover`
