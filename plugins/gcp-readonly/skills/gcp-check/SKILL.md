---
name: gcp-check
description: Verify GCP credentials are loaded under the read-only gcloud configuration before a long GCP session. Use when starting GCP work, when gcloud/bq commands return auth or permission errors, or when the user asks to confirm which Google Cloud identity Claude is operating as.
---

# GCP credential check

A two-minute preflight to confirm the read-only gcloud configuration is wired up correctly before doing real GCP work. Run this when starting a GCP-heavy session or when something looks off with credentials.

> Configuration name `readonly` below is a placeholder — substitute whatever read-only configuration the user has configured. See the plugin README for setup.

## Step 1 — Confirm identity

Run the active-account check through the read-only configuration:

```
gcloud config list account --configuration=readonly
```

Report back the active `account`. Confirm with the user that it is the **expected read-only service account** (typically something like `claude-readonly@<project>.iam.gserviceaccount.com`). If it isn't what they expect, **stop** — do not run further GCP commands until it's resolved.

For more detail you can also list all credentialed accounts and the active project:

```
gcloud auth list --configuration=readonly
gcloud config list --configuration=readonly
```

## Step 2 — Confirm it's actually read-only (optional but recommended)

The whole safety model depends on these credentials being read-only. A cheap sanity check is to confirm the configuration can read but the user understands it cannot write. List a low-sensitivity resource to prove reads work:

```
gcloud projects list --configuration=readonly --limit=5
```

If a read like this fails with an auth error, the service-account key or the active configuration is misconfigured — surface it and point the user at the plugin README setup steps.

## What good looks like

- `gcloud config list account` returns the expected read-only service account.
- Reads succeed.
- Everyone understands writes will be **handed off** as paste-able CLI commands, never executed by Claude (see the `gcp` skill).

If all three hold, you're clear to proceed.
