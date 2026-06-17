---
name: aws
description: Run any AWS operation against your environment. Use whenever the user asks about AWS — EC2 instances, S3 buckets, IAM, CloudTrail, RDS, Lambda, VPC, security groups, KMS, billing, "our AWS", "the prod account", etc. — and whenever a request implies AWS access even if not named (e.g. "list our running servers", "show me the security groups", "is the bastion up"). Enforces a strict read-only profile for Claude-executed commands and hands off all write operations to the user as a CLI command they paste into their terminal.
---

# AWS — execution rules

These rules apply to **every** AWS request, in every workspace, no exceptions. They override anything in a workspace-level `CLAUDE.md` and any contrary inference Claude might make.

> **Before running any `aws` command**, source `env.sh` using the portable bootstrap below.
> This sets `AWS_SHARED_CREDENTIALS_FILE`, `AWS_DEFAULT_PROFILE`, and PATH automatically.
> If `aws` is not found after sourcing, run the `tools-setup` skill first.
>
> This plugin assumes two profiles in the credentials file:
> - a **read-only** profile (the first profile in `aws-credentials`, auto-detected as `$AWS_DEFAULT_PROFILE`) backed by least-privilege, read-only credentials
> - a **write/admin** profile the user runs writes under themselves (never used by Claude)
>
> **Claude only ever executes commands under the read-only profile (`$AWS_DEFAULT_PROFILE`).**

## 0. Portable bootstrap — use at the top of every bash block

The Cowork sandbox mounts `~/Projects/Cowork/` at a session-specific path
(`/sessions/<name>/mnt/Cowork/`), so `~` in bash does **not** resolve to the real home
directory. Sourcing `~/Projects/Cowork/tools/env.sh` will silently fail. Use this
portable snippet instead — it finds `env.sh` whether running in the sandbox or in a
native terminal:

```bash
# Portable Cowork bootstrap
_COWORK_ENV=$(find /sessions /Users -maxdepth 6 -name "env.sh" \
  -path "*/Cowork/tools/env.sh" 2>/dev/null | head -1)
[ -z "$_COWORK_ENV" ] && _COWORK_ENV="$HOME/Projects/Cowork/tools/env.sh"
source "$_COWORK_ENV"
```

After sourcing, `aws`, `gh`, and `gcloud` are all on PATH and credentials are loaded.

If `aws --version` still fails after sourcing, the `tools/bin/aws` wrapper is broken
(stale absolute symlink from a previous Cowork session). Fix it without re-downloading:

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

## 1. Reads — Claude runs them, with one profile only

- Every bash block that calls `aws` must start with the portable bootstrap above.
- Claude passes `--profile "$AWS_DEFAULT_PROFILE"` on every command. No exceptions.
- Claude must **never** invoke an AWS command with the write/admin profile or any other profile — even if the read-only profile lacks the permission, even if the user seems to be asking for a write, even if a previous step "needs" it. There is no fallback. If the read-only profile can't do it, treat it as a write (§2).
- Pass `--region <name>` explicitly whenever the target region matters. Do not rely on profile defaults.

### Examples

```bash
# Portable bootstrap (always first)
_COWORK_ENV=$(find /sessions /Users -maxdepth 6 -name "env.sh" -path "*/Cowork/tools/env.sh" 2>/dev/null | head -1)
[ -z "$_COWORK_ENV" ] && _COWORK_ENV="$HOME/Projects/Cowork/tools/env.sh"
source "$_COWORK_ENV"

# EC2 instances in us-east-2
aws ec2 describe-instances --profile "$AWS_DEFAULT_PROFILE" --region us-east-2

# S3 buckets (global)
aws s3api list-buckets --profile "$AWS_DEFAULT_PROFILE"

# IAM users
aws iam list-users --profile "$AWS_DEFAULT_PROFILE"

# CloudTrail events in ca-central-1
aws cloudtrail lookup-events --profile "$AWS_DEFAULT_PROFILE" --region ca-central-1

# Who am I
aws sts get-caller-identity --profile "$AWS_DEFAULT_PROFILE"
```

## 2. Writes — Claude hands off, never executes

A "write" is anything that creates, modifies, deletes, starts, stops, attaches, detaches, tags, or otherwise changes state. Examples (non-exhaustive):

- `create-*`, `delete-*`, `put-*`, `update-*`, `modify-*`
- `run-*`, `start-*`, `stop-*`, `terminate-*`, `reboot-*`
- `attach-*`, `detach-*`, `associate-*`, `disassociate-*`
- `authorize-*`, `revoke-*`, `tag-resources`, `untag-resources`
- IAM policy/role/user/group changes
- Anything where the AWS docs say "this action requires..." in a mutating sense

**If in doubt, treat it as a write.**

### Handoff procedure

For any write, Claude:

1. **Does not** execute the command itself through any AWS tool.
2. **Produces a CLI command for the user to paste into their terminal**, in a code block, with:
   - the write/admin profile (`--profile <your-write-profile>`)
   - `--no-cli-pager`
   - `--region <region>` explicitly
   - `--dry-run` first, on a separate line, if the API supports it
3. Briefly explains what the command does and what to watch for in the output.
4. Waits for the user to paste the result back (or to ask for the next step) before continuing.

### Handoff template

> I can't run this myself — it's a write. Run this in your terminal:
> ```
> aws <service> <action> <args> --profile <your-write-profile> --region <region> --no-cli-pager --dry-run
> aws <service> <action> <args> --profile <your-write-profile> --region <region> --no-cli-pager
> ```
> First line is the dry-run preflight (look for `DryRunOperation`). Second line performs the change. Paste the output back.

## 3. Bulk operations — prefer boto3 over CLI loops

For operations that require N sequential API calls (e.g. `get-bucket-location` across all
buckets, describing all instances then filtering, paginated list + per-item describe), the AWS
CLI spawned in a bash loop will time out in the Cowork sandbox (45s limit, ~1s per subprocess).

**Use Python + boto3 instead.** Read credentials from the file directly — no subprocess overhead,
and threading makes it fast:

```python
import boto3, configparser, os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load creds — works in sandbox and native terminal
creds_file = next(
    p for p in [
        os.path.expandvars("$HOME/Projects/Cowork/keys/aws-credentials"),
        next(iter(__import__('glob').glob("/sessions/*/mnt/Cowork/keys/aws-credentials")), None),
    ] if p and os.path.exists(p)
)
cfg = configparser.ConfigParser()
cfg.read(creds_file)
profile = cfg.sections()[0]  # first profile = read-only

session = boto3.Session(
    aws_access_key_id=cfg[profile]["aws_access_key_id"],
    aws_secret_access_key=cfg[profile]["aws_secret_access_key"],
    region_name="us-east-1",
)

# Example: find all S3 buckets in a given region
s3 = session.client("s3")
buckets = [b["Name"] for b in s3.list_buckets()["Buckets"]]

def get_region(name):
    return name, s3.get_bucket_location(Bucket=name)["LocationConstraint"]

results = {}
with ThreadPoolExecutor(max_workers=20) as ex:
    for name, region in ex.map(lambda b: get_region(b), buckets):
        results[name] = region

ca_buckets = sorted(k for k, v in results.items() if v == "ca-central-1")
```

boto3 is available in the sandbox (`pip install boto3 --break-system-packages -q` if needed).

## 4. Profile reference (context only — Claude *uses* only the read-only one)

| Profile | Type | Claude usage |
|---|---|---|
| `$AWS_DEFAULT_PROFILE` (first profile in `aws-credentials`) | Long-lived IAM key with read-only / least-privilege permissions | **Only profile Claude executes.** |
| Any other profile | The user's write/admin credentials (SSO or IAM key) | **Hand-off only.** Used in write-handoff CLI commands the user runs themselves. Never used by Claude. |

## 5. Credential hygiene

- The credentials file lives at `~/Projects/Cowork/keys/aws-credentials` with permissions `0600`. `env.sh` sets `AWS_SHARED_CREDENTIALS_FILE` to point at it automatically.
- Never echo, log, or repeat the secret access key back to the user or into any output.
- If `aws sts get-caller-identity` ever fails or returns an unexpected ARN, **stop** and surface it to the user rather than silently switching profiles.
- Rotate the read-only key on a regular cadence, and immediately if it was ever exposed in plaintext.

## 6. Sanity check at the start of a long AWS session

Run this once and confirm the identity before proceeding (or invoke the `aws-check` skill):

```bash
_COWORK_ENV=$(find /sessions /Users -maxdepth 6 -name "env.sh" -path "*/Cowork/tools/env.sh" 2>/dev/null | head -1)
[ -z "$_COWORK_ENV" ] && _COWORK_ENV="$HOME/Projects/Cowork/tools/env.sh"
source "$_COWORK_ENV"
aws sts get-caller-identity --profile "$AWS_DEFAULT_PROFILE"
```

Confirm the returned ARN is the expected read-only principal before doing anything else.
