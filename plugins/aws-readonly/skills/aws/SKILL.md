---
name: aws
description: Run any AWS operation against your environment. Use whenever the user asks about AWS — EC2 instances, S3 buckets, IAM, CloudTrail, RDS, Lambda, VPC, security groups, KMS, billing, "our AWS", "the prod account", etc. — and whenever a request implies AWS access even if not named (e.g. "list our running servers", "show me the security groups", "is the bastion up"). Enforces a strict read-only profile for Claude-executed commands and hands off all write operations to the user as a CLI command they paste into their terminal.
---

# AWS — execution rules

These rules apply to **every** AWS request, in every workspace, no exceptions. They override anything in a workspace-level `CLAUDE.md` and any contrary inference Claude might make.

> **Profile name.** This plugin assumes a read-only profile named `avatarfleet-readonly` in the credentials file at `~/Projects/Cowork/keys/aws-credentials`. If the user has a different profile name, substitute it everywhere below.

## 1. Reads — Claude runs them with boto3, never the CLI

Claude runs all reads using **boto3** (Python). This avoids relying on the `aws` CLI symlink, which breaks in sandbox environments.

### Credential preamble

Prepend this to every bash snippet that calls boto3. It resolves the credentials file whether running in the Cowork sandbox or a native shell:

```bash
CREDS=$(ls /sessions/*/mnt/Cowork/keys/aws-credentials 2>/dev/null | head -1)
[ -z "$CREDS" ] && CREDS="$HOME/Projects/Cowork/keys/aws-credentials"
export AWS_SHARED_CREDENTIALS_FILE="$CREDS"
export AWS_PROFILE="avatarfleet-readonly"
PYPATH=$(ls /sessions/*/mnt/Cowork/tools/python-packages 2>/dev/null | head -1)
[ -z "$PYPATH" ] && PYPATH="$HOME/Projects/Cowork/tools/python-packages"
export PYTHONPATH="$PYPATH:$PYTHONPATH"
```

### Read pattern

After the preamble, call boto3 inline:

```bash
python3 -c "
import boto3, json
s = boto3.Session()
client = s.client('<service>', region_name='<region>')
result = client.<method>(<args>)
print(json.dumps(result, default=str, indent=2))
"
```

boto3 picks up `AWS_SHARED_CREDENTIALS_FILE` and `AWS_PROFILE` automatically.

### Common read examples

| Intent | boto3 call |
|---|---|
| Identity sanity check | `s.client('sts').get_caller_identity()` |
| List S3 buckets | `s.client('s3').list_buckets()` |
| EC2 instances in a region | `s.client('ec2', region_name='us-east-2').describe_instances()` |
| IAM users | `s.client('iam').list_users()` |
| CloudTrail events | `s.client('cloudtrail', region_name='ca-central-1').lookup_events()` |
| S3 bucket region | `s.client('s3').get_bucket_location(Bucket='<name>')` |
| Security groups | `s.client('ec2', region_name='us-east-1').describe_security_groups()` |

Full worked example — list S3 buckets and their regions:

```bash
CREDS=$(ls /sessions/*/mnt/Cowork/keys/aws-credentials 2>/dev/null | head -1)
[ -z "$CREDS" ] && CREDS="$HOME/Projects/Cowork/keys/aws-credentials"
export AWS_SHARED_CREDENTIALS_FILE="$CREDS"
export AWS_PROFILE="avatarfleet-readonly"
PYPATH=$(ls /sessions/*/mnt/Cowork/tools/python-packages 2>/dev/null | head -1)
[ -z "$PYPATH" ] && PYPATH="$HOME/Projects/Cowork/tools/python-packages"
export PYTHONPATH="$PYPATH:$PYTHONPATH"

python3 -c "
import boto3, json
s = boto3.Session()
buckets = s.client('s3').list_buckets().get('Buckets', [])
for b in buckets:
    loc = s.client('s3').get_bucket_location(Bucket=b['Name'])
    b['Region'] = loc.get('LocationConstraint') or 'us-east-1'
print(json.dumps(buckets, default=str, indent=2))
"
```

## 2. Writes — Claude hands off, never executes

A "write" is anything that creates, modifies, deletes, starts, stops, attaches, detaches, tags, or otherwise changes state:

- `create_*`, `delete_*`, `put_*`, `update_*`, `modify_*`
- `run_*`, `start_*`, `stop_*`, `terminate_*`, `reboot_*`
- `attach_*`, `detach_*`, `associate_*`, `authorize_*`, `revoke_*`
- IAM policy/role/user/group changes

**If in doubt, treat it as a write.**

### Handoff procedure

For any write, Claude:

1. **Does not execute it** — not via boto3, not via CLI, not via any tool.
2. **Produces a CLI command for the user to paste into their terminal**, with:
   - `--profile avatarfleet-production` (or the user's write profile)
   - `--no-cli-pager`
   - `--region <region>` explicitly
   - `--dry-run` first (separate line), if the API supports it
3. Briefly explains what it does and what to watch for.
4. Waits for the user to paste the result back.

### Handoff template

> I can't run this myself — it's a write. Run this in your terminal:
> ```
> aws <service> <action> <args> --profile avatarfleet-production --region <region> --no-cli-pager --dry-run
> aws <service> <action> <args> --profile avatarfleet-production --region <region> --no-cli-pager
> ```
> First line is dry-run (look for `DryRunOperation`). Second line performs the change. Paste the output back.

## 3. Profile reference

| Profile | Type | Claude usage |
|---|---|---|
| `avatarfleet-readonly` | Read-only IAM key | **Only profile boto3 uses for reads** |
| `avatarfleet-production` | Write/admin credentials | **Hand-off only** — user runs this themselves |

## 4. Credential hygiene

- Never echo, log, or repeat `aws_secret_access_key` values.
- If `sts.get_caller_identity()` returns an unexpected ARN, **stop** before proceeding.
- Credentials file: `~/Projects/Cowork/keys/aws-credentials`, permissions `0600`.
- Rotate the read-only key on a regular cadence; immediately if ever exposed in plaintext.

## 5. Quick sanity check

```bash
CREDS=$(ls /sessions/*/mnt/Cowork/keys/aws-credentials 2>/dev/null | head -1)
[ -z "$CREDS" ] && CREDS="$HOME/Projects/Cowork/keys/aws-credentials"
export AWS_SHARED_CREDENTIALS_FILE="$CREDS"
export AWS_PROFILE="avatarfleet-readonly"
PYPATH=$(ls /sessions/*/mnt/Cowork/tools/python-packages 2>/dev/null | head -1)
[ -z "$PYPATH" ] && PYPATH="$HOME/Projects/Cowork/tools/python-packages"
export PYTHONPATH="$PYPATH:$PYTHONPATH"

python3 -c "
import boto3
i = boto3.Session().client('sts').get_caller_identity()
print('Account:', i['Account'])
print('ARN:    ', i['Arn'])
"
```

Confirm the ARN is the expected read-only principal before proceeding. Or invoke the `aws-check` skill.
