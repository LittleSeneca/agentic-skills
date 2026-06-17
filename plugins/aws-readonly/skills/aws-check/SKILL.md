---
name: aws-check
description: Verify AWS credentials are loaded under the read-only profile before a long AWS session. Use when starting AWS work, when AWS commands return auth or permission errors, or when the user asks to confirm which AWS identity Claude is operating as.
---

# AWS credential check

A two-minute preflight to confirm the read-only profile is wired up correctly before doing real AWS work. Run this when starting an AWS-heavy session or when something looks off with credentials.

## Step 1 — Bootstrap

Use the portable bootstrap (handles both native terminal and Cowork sandbox):

```bash
_COWORK_ENV=$(find /sessions /Users -maxdepth 6 -name "env.sh" \
  -path "*/Cowork/tools/env.sh" 2>/dev/null | head -1)
[ -z "$_COWORK_ENV" ] && _COWORK_ENV="$HOME/Projects/Cowork/tools/env.sh"
source "$_COWORK_ENV"
```

If `aws --version` fails after this, the `tools/bin/aws` wrapper is a broken absolute symlink
from a prior session. Fix it without re-downloading — the actual CLI files are still present:

```bash
TOOLS="$(dirname "$_COWORK_ENV")"
cat > "$TOOLS/bin/aws" << 'AWSEOF'
#!/bin/bash
TOOLS="$(cd "$(dirname "$0")/.." && pwd)"
AWS_BIN=$(find "$TOOLS" -maxdepth 6 -name "aws" -path "*/dist/aws" 2>/dev/null | sort -V | tail -1)
[ -z "$AWS_BIN" ] && { echo "aws: binary not found under $TOOLS — run tools-setup" >&2; exit 127; }
exec "$AWS_BIN" "$@"
AWSEOF
chmod +x "$TOOLS/bin/aws"
source "$_COWORK_ENV"
```

If the binary truly isn't there, run the `tools-setup` skill.

## Step 2 — Confirm identity

```bash
aws sts get-caller-identity --profile "$AWS_DEFAULT_PROFILE"
echo "Profile: $AWS_DEFAULT_PROFILE"
```

Report back the `Account`, `UserId`, and `Arn`. Confirm with the user that the ARN is the **expected read-only principal**. If it isn't what they expect, **stop** — do not run further AWS commands until it's resolved.

## Step 3 — Confirm reads work (optional but recommended)

```bash
aws ec2 describe-regions --profile "$AWS_DEFAULT_PROFILE" --query 'Regions[].RegionName' --output text
```

If this fails with an auth error, the credentials or key file are misconfigured — surface it and point the user at the plugin README setup steps.

## What good looks like

- `get-caller-identity` returns the expected read-only ARN.
- Reads succeed.
- Everyone understands writes will be **handed off** as paste-able CLI commands, never executed by Claude (see the `aws` skill).

If all three hold, you're clear to proceed.
