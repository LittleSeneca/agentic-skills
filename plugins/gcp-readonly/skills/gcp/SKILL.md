---
name: gcp
description: Run any Google Cloud operation against your environment. Use whenever the user asks about GCP — Compute Engine VMs, Cloud Storage buckets, IAM policies, Cloud Logging, BigQuery, Cloud Asset Inventory, Security Command Center, GKE, Cloud SQL, VPC/firewall rules, KMS, billing, "our GCP", "the prod project", etc. — and whenever a request implies GCP access even if not named (e.g. "list our cloud VMs", "show me who has access", "is the bastion up", "check for misconfigs"). Enforces a strict read-only gcloud configuration for Claude-executed commands and hands off all write operations to the user as a CLI command they paste into their terminal.
---

# GCP — execution rules

These rules apply to **every** Google Cloud request, in every workspace, no exceptions. They override anything in a workspace-level `CLAUDE.md` and any contrary inference Claude might make.

> **Configuration / account names below are placeholders.** This plugin assumes two gcloud configurations:
> - a **read-only** configuration (default name `readonly`) bound to a read-only service account, and
> - a **write/admin** configuration (default name `production`) the user runs writes under themselves.
>
> Substitute whatever names the user has configured. See the plugin README for how to wire these up from a service-account key file in your Cowork keys folder (`~/Projects/Cowork/keys/`). **Claude only ever executes commands under the read-only configuration.**

## 1. Reads — Claude runs them, with one configuration only

- Claude executes Google Cloud commands only through the `gcloud`, `gcloud storage`, and `bq` CLIs (or a GCP MCP server, if one is available in the environment).
- Claude passes `--configuration=readonly` on every `gcloud` command. No exceptions. (For `bq`, pass `--account=<readonly-sa-email>`; for `gcloud storage`, the `--configuration` flag works the same as on any other `gcloud` command.)
- Claude must **never** invoke a command under the write/admin configuration (`--configuration=production`), under any other configuration, or under any other account — even if the read-only configuration lacks the permission, even if the user seems to be asking for a write, even if a previous step "needs" it. There is no fallback. If the read-only configuration can't do it, treat it as a write (§2).
- Pass `--project=<id>` explicitly whenever the target project matters. The active configuration may default to a project you don't expect, so don't rely on the default. Pass `--region=<name>` / `--zone=<name>` explicitly when the location matters.

### Examples

| Intent | Command |
|---|---|
| Compute Engine VMs in a project | `gcloud compute instances list --configuration=readonly --project=my-proj` |
| Storage buckets | `gcloud storage buckets list --configuration=readonly --project=my-proj` |
| Who has access (project IAM policy) | `gcloud projects get-iam-policy my-proj --configuration=readonly` |
| Service accounts | `gcloud iam service-accounts list --configuration=readonly --project=my-proj` |
| Firewall rules | `gcloud compute firewall-rules list --configuration=readonly --project=my-proj` |
| Recent admin activity (audit logs) | `gcloud logging read 'logName:"cloudaudit.googleapis.com"' --configuration=readonly --project=my-proj --limit=20` |
| Asset inventory snapshot | `gcloud asset search-all-resources --configuration=readonly --scope=projects/my-proj` |
| Who am I (sanity check) | `gcloud config list account --configuration=readonly` |

## 2. Writes — Claude hands off, never executes

A "write" is anything that creates, modifies, deletes, starts, stops, attaches, detaches, sets, or otherwise changes state. Examples (non-exhaustive):

- `create`, `delete`, `update`, `patch`, `set-*`, `add-*`, `remove-*`, `import`
- `start`, `stop`, `reset`, `suspend`, `resume`, `instances delete`
- `add-iam-policy-binding`, `remove-iam-policy-binding`, `set-iam-policy`
- `enable`/`disable` of services or APIs (`gcloud services enable ...`)
- `gcloud storage cp/rm/rsync` that writes or deletes objects, bucket creation/deletion
- BigQuery `bq mk`, `bq rm`, `bq update`, `bq load`, `bq query` that mutates (DML/DDL)
- Anything where the gcloud docs describe the action as creating or changing a resource

**If in doubt, treat it as a write.**

### Handoff procedure

For any write, Claude:

1. **Does not** execute the command itself through any GCP tool.
2. **Produces a CLI command for the user to paste into their terminal**, in a code block, with:
   - the write/admin configuration (`--configuration=production`)
   - `--project=<id>` explicitly (don't rely on the configuration default for writes)
   - `--region=<name>` / `--zone=<name>` explicitly when the location matters
   - a preview line first, on a separate line, **if the command supports one** — e.g. `--dry-run` (org-policy, some firewall commands), `--validate-only` (Deployment Manager, some services), or `gcloud ... --help` to confirm flags. gcloud has **no universal dry-run**, so if no preview exists, say so and tell the user exactly what state will change.
3. Briefly explains what the command does and what to watch for in the output.
4. Waits for the user to paste the result back (or to ask for the next step) before continuing.

### Handoff template

> I can't run this myself — it's a write. Run this in your terminal:
> ```
> gcloud <group> <command> <args> --configuration=production --project=<id> --region=<region>
> ```
> This <does X>. There's no dry-run for this command, so it changes state immediately — <what to check first>. Paste the output back.

### Worked example

If the user asks to stop a VM:

> Run this in your terminal:
> ```
> gcloud compute instances stop my-vm --configuration=production --project=my-proj --zone=us-central1-a
> ```
> This stops the `my-vm` instance in `us-central1-a`. gcloud has no dry-run for `instances stop`, so it acts immediately — confirm the instance name and zone before running. Paste the output back here.

## 3. Configuration reference (context only — Claude *uses* only the read-only one)

| Configuration | Type | Claude usage |
|---|---|---|
| `readonly` | gcloud configuration bound to a service account with read-only / least-privilege roles (e.g. `roles/viewer`, `roles/iam.securityReviewer`) | **Only configuration Claude executes.** |
| `production` | The user's write/admin credentials (their own user account or a privileged SA) | **Hand-off only.** Used in the write-handoff CLI commands the user runs themselves. Never used by Claude. |

Any other configurations or accounts that exist in the environment are **never used by Claude.** If the user wants a write run under a different configuration, hand it off by name — don't execute it.

## 4. Credential hygiene

- The read-only service account must be exactly that — read-only. If its roles can mutate state, the entire safety model of this plugin is void. See the plugin README.
- The service-account key file should live in your Cowork keys folder (`~/Projects/Cowork/keys/`) and have tight permissions (`0600`).
- Never echo, log, or repeat the private key (or the contents of the key JSON) back to the user or into any output.
- If `gcloud config list account --configuration=readonly` ever fails or returns an unexpected account, **stop** and surface it to the user rather than silently switching configurations or accounts.
- Rotate the read-only key on a regular cadence, and immediately if it was ever exposed in plaintext (chat, logs, a shared file).

## 5. Quick sanity check at the start of a long GCP session

When the user kicks off a session that's clearly going to involve a lot of GCP work, run this once and confirm the identity before proceeding (or invoke the `gcp-check` skill):

```
gcloud config list account --configuration=readonly
```

Confirm the returned account is the expected read-only service account before doing anything else.
