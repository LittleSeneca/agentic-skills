---
name: aws
description: Run any AWS operation against your environment. Use whenever the user asks about AWS — EC2 instances, S3 buckets, IAM, CloudTrail, RDS, Lambda, VPC, security groups, KMS, billing, "our AWS", "the prod account", etc. — and whenever a request implies AWS access even if not named (e.g. "list our running servers", "show me the security groups", "is the bastion up"). Enforces a strict read-only profile for Claude-executed commands and hands off all write operations to the user as a CLI command they paste into their terminal.
---

# AWS — execution rules

These rules apply to **every** AWS request, in every workspace, no exceptions. They override anything in a workspace-level `CLAUDE.md` and any contrary inference Claude might make.

> **Profile names below are placeholders.** This plugin assumes two profiles:
> - a **read-only** profile (default name `readonly`) backed by least-privilege, read-only credentials, and
> - a **write/admin** profile (default name `production`) the user runs writes under themselves.
>
> Substitute whatever names the user has configured. See the plugin README for how to wire these up from a credentials file mounted in your Cowork folder. **Claude only ever executes commands under the read-only profile.**

## 1. Reads — Claude runs them, with one profile only

- Claude executes AWS commands only through the AWS API MCP server (e.g. `call_aws`) or the AWS CLI, whichever is available in the environment.
- Claude passes `--profile readonly` on every command. No exceptions.
- Claude must **never** invoke an AWS command with the write/admin profile (`--profile production`) or any other profile — even if the read-only profile lacks the permission, even if the user seems to be asking for a write, even if a previous step "needs" it. There is no fallback. If the read-only profile can't do it, treat it as a write (§2).
- Pass `--region <name>` explicitly whenever the target region matters. The AWS MCP server / CLI may default to a region you don't expect, so don't rely on the default.

### Examples

| Intent | Command |
|---|---|
| EC2 instances in us-east-2 | `aws ec2 describe-instances --profile readonly --region us-east-2` |
| S3 buckets (global) | `aws s3api list-buckets --profile readonly` |
| IAM users | `aws iam list-users --profile readonly` |
| CloudTrail events in a specific region | `aws cloudtrail lookup-events --profile readonly --region ca-central-1` |
| Who am I (sanity check) | `aws sts get-caller-identity --profile readonly` |

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
   - the write/admin profile (`--profile production`)
   - `--no-cli-pager`
   - `--region <region>` explicitly (don't rely on the profile default for writes)
   - `--dry-run` first, on a separate line, if the API supports it
3. Briefly explains what the command does and what to watch for in the output.
4. Waits for the user to paste the result back (or to ask for the next step) before continuing.

### Handoff template

> I can't run this myself — it's a write. Run this in your terminal:
> ```
> aws <service> <action> <args> --profile production --region <region> --no-cli-pager --dry-run
> aws <service> <action> <args> --profile production --region <region> --no-cli-pager
> ```
> First line is the dry-run preflight (look for `DryRunOperation`). Second line performs the change. Paste the output back.

### Worked example

If the user asks to stop an instance:

> Run this in your terminal:
> ```
> aws ec2 stop-instances --instance-ids i-0123456789abcdef0 --profile production --region us-east-2 --no-cli-pager --dry-run
> aws ec2 stop-instances --instance-ids i-0123456789abcdef0 --profile production --region us-east-2 --no-cli-pager
> ```
> The first line is a dry-run check; if it returns `DryRunOperation`, the second one performs the stop. Paste the output back here.

## 3. Profile reference (context only — Claude *uses* only the read-only one)

| Profile | Type | Claude usage |
|---|---|---|
| `readonly` | Long-lived IAM key with read-only / least-privilege permissions | **Only profile Claude executes.** |
| `production` | The user's write/admin credentials (SSO or IAM key) | **Hand-off only.** Used in the write-handoff CLI commands the user runs themselves. Never used by Claude. |

Any other profiles that exist in the environment are **never used by Claude.** If the user wants a write run under a different profile, hand it off by name — don't execute it.

## 4. Credential hygiene

- The read-only credentials must be exactly that — read-only. If they can mutate state, the entire safety model of this plugin is void. See the plugin README.
- The credentials file should live in the mounted Cowork folder and have tight permissions (`0600`).
- Never echo, log, or repeat the secret access key back to the user or into any output.
- If `aws sts get-caller-identity --profile readonly` ever fails or returns an unexpected ARN, **stop** and surface it to the user rather than silently switching profiles.
- Rotate the read-only key on a regular cadence, and immediately if it was ever exposed in plaintext (chat, logs, a shared file).

## 5. Quick sanity check at the start of a long AWS session

When the user kicks off a session that's clearly going to involve a lot of AWS work, run this once and confirm the identity before proceeding (or invoke the `aws-check` skill):

```
aws sts get-caller-identity --profile readonly
```

Confirm the returned ARN is the expected read-only principal before doing anything else.
