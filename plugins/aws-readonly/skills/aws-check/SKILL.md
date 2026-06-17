---
name: aws-check
description: Verify AWS credentials are loaded under the read-only profile before a long AWS session. Use when starting AWS work, when AWS commands return auth or permission errors, or when the user asks to confirm which AWS identity Claude is operating as.
---

# AWS credential check

A two-minute preflight to confirm the read-only profile is wired up correctly before doing real AWS work. Run this when starting an AWS-heavy session or when something looks off with credentials.

Credentials and the `aws` binary are managed by `tools/env.sh`. If `aws` is not found, run the `tools-setup` skill first.

## Step 1 — Confirm identity

```bash
source ~/Projects/Cowork/tools/env.sh
aws sts get-caller-identity
```

Report back the `Account`, `UserId`, and `Arn`. Confirm with the user that the ARN is the **expected read-only principal**. If it isn't what they expect, **stop** — do not run further AWS commands until it's resolved.

Also confirm which profile resolved: `echo "Profile: $AWS_DEFAULT_PROFILE"`. This should be the read-only profile from the first header in `~/Projects/Cowork/keys/aws-credentials`.

## Step 2 — Confirm it's actually read-only (optional but recommended)

The whole safety model depends on these credentials being read-only. A cheap sanity check is to confirm the profile can read but the user understands it cannot write. You can list a low-sensitivity resource to prove reads work:

```bash
source ~/Projects/Cowork/tools/env.sh
aws ec2 describe-regions
```

If a read like this fails with an auth error, the credentials or the key file are misconfigured — surface it and point the user at the plugin README setup steps.

## What good looks like

- `get-caller-identity` returns the expected read-only ARN.
- Reads succeed.
- Everyone understands writes will be **handed off** as paste-able CLI commands, never executed by Claude (see the `aws` skill).

If all three hold, you're clear to proceed.
