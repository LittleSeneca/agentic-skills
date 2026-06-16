---
name: azure-check
description: Verify Azure credentials are loaded under the read-only Reader service principal before a long Azure session. Use when starting Azure work, when az commands return auth or permission errors, or when the user asks to confirm which Azure identity Claude is operating as.
---

# Azure credential check

A two-minute preflight to confirm the read-only service principal is wired up correctly before doing real Azure work. Run this when starting an Azure-heavy session or when something looks off with credentials.

> This check assumes Claude's `az` calls run with `AZURE_CONFIG_DIR` pointed at the isolated read-only config dir (default `$HOME/cowork/azure-config`), logged in as a **Reader** service principal. See the plugin README for setup.

## Step 1 — Confirm identity

Run the account check through the `az` CLI (with the read-only `AZURE_CONFIG_DIR` in effect):

```
az account show -o json
```

Report back the subscription `name` / `id`, the `user.name`, and `user.type`. Confirm with the user that:

- `user.type` is `servicePrincipal`, and
- `user.name` is the **expected Reader service principal** app ID, and
- the subscription is the one they expect.

If any of these isn't what they expect, **stop** — do not run further Azure commands until it's resolved.

## Step 2 — Confirm it's actually read-only (optional but recommended)

The whole safety model depends on this service principal being read-only (Reader role). A cheap sanity check is to confirm it can read. List a low-sensitivity resource to prove reads work:

```
az account list-locations -o table
```

If a read like this fails with an auth error, the credentials, the mounted key file, or the `AZURE_CONFIG_DIR` login are misconfigured — surface it and point the user at the plugin README setup steps.

To confirm the role assignment is genuinely Reader (and nothing broader), you can also check what the principal is granted:

```
az role assignment list --assignee <app-id> --all -o table
```

Confirm the role is `Reader` (or tighter) and not `Contributor`, `Owner`, or anything that can write.

## What good looks like

- `az account show` returns the expected Reader service principal (`user.type` = `servicePrincipal`) and subscription.
- Reads succeed.
- The principal's only role assignment is `Reader` (or tighter).
- Everyone understands writes will be **handed off** as paste-able CLI commands, run under the user's own privileged login, never executed by Claude (see the `azure` skill).

If those hold, you're clear to proceed.
