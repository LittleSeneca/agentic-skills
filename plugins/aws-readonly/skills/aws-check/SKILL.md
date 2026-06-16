---
name: aws-check
description: Verify AWS credentials are loaded under the read-only profile before a long AWS session. Use when starting AWS work, when AWS commands return auth or permission errors, or when the user asks to confirm which AWS identity Claude is operating as.
---

# AWS credential check

A two-minute preflight to confirm the read-only profile is wired up correctly before doing real AWS work. Run this when starting an AWS-heavy session or when something looks off with credentials.

> Profile name `readonly` below is a placeholder — substitute whatever read-only profile the user has configured. See the plugin README for setup.

## Step 1 — Confirm identity

Run the caller-identity check through the AWS API MCP server or CLI:

```
aws sts get-caller-identity --profile readonly
```

Report back the `Account`, `UserId`, and `Arn`. Confirm with the user that the ARN is the **expected read-only principal**. If it isn't what they expect, **stop** — do not run further AWS commands until it's resolved.

## Step 2 — Confirm it's actually read-only (optional but recommended)

The whole safety model depends on these credentials being read-only. A cheap sanity check is to confirm the profile can read but the user understands it cannot write. You can list a low-sensitivity resource to prove reads work:

```
aws ec2 describe-regions --profile readonly
```

If a read like this fails with an auth error, the credentials or the mounted key file are misconfigured — surface it and point the user at the plugin README setup steps.

## What good looks like

- `get-caller-identity` returns the expected read-only ARN.
- Reads succeed.
- Everyone understands writes will be **handed off** as paste-able CLI commands, never executed by Claude (see the `aws` skill).

If all three hold, you're clear to proceed.
