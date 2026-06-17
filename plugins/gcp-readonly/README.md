# gcp-readonly

Safe Google Cloud access for Claude.

Claude runs **read-only** GCP commands for you through a read-only gcloud configuration, and **hands every write back to you** as a copy-paste CLI command that you run yourself. Claude never executes a state-changing GCP call.

---

## ⚠️ ONLY USE A READ-ONLY SERVICE ACCOUNT FOR YOUR ENVIRONMENT

**The single most important rule of this plugin: the GCP credentials you give it must be read-only.**

This plugin's safety model rests entirely on that one fact. The skill instructs Claude to:

- run reads itself under the read-only configuration, and
- refuse to execute writes — handing them back to you as commands you run under a separate, privileged configuration.

But Claude is not a security boundary. If the service account you provide can mutate state, then a mistake, a confused instruction, or a prompt-injection in some tool output could result in real changes to your environment. **The read-only-ness of the service account is the actual guardrail.** Claude's behavior is the convenience layer on top of it.

So:

- ✅ Create a service account with **read-only / least-privilege** roles — start from `roles/viewer`, `roles/iam.securityReviewer`, or tighter purpose-built roles.
- ✅ Give the plugin **only** that key.
- ❌ Do **not** give it `roles/editor`, `roles/owner`, or your own user credentials.
- ❌ Do **not** assume Claude "won't run writes anyway" — enforce it with the service account's roles.

If the credentials can write, this plugin provides no protection. Don't do it.

---

## How it works

- **Reads** → Claude executes them under your read-only configuration (default name `readonly`), via the `gcloud`, `gcloud storage`, and `bq` CLIs (or a GCP MCP server, if one is available).
- **Writes** → Claude does not run them. It produces a ready-to-paste CLI command (with a preview line such as `--dry-run` / `--validate-only` where the command supports one) targeting your write/admin configuration (default name `production`), and you run it in your own terminal.

Two skills ship with the plugin:

| Skill | What it does |
|---|---|
| `gcp` | The execution rules. Triggers on any GCP request and enforces read-only-for-Claude / writes-handed-off. |
| `gcp-check` | A quick preflight that confirms which GCP identity Claude is operating as before a long session. |

---

## Prerequisites

Before using this plugin for the first time on a new machine, run the **`tools-setup` skill**. It installs `gcloud` as a persistent standalone binary in `~/Projects/Cowork/tools/` and activates the service account. Subsequent sessions source `tools/env.sh` and are ready instantly.

---

## Setup

### 1. Create a read-only service account

In the GCP project (or organization) you want Claude to read, create a service account and grant it read-only roles, then generate a JSON key. Run these commands from your own terminal (not through Claude — these are writes):

```bash
# Create the service account
gcloud iam service-accounts create claude-readonly \
  --display-name="Claude read-only" --project=my-proj

# Grant read-only roles (viewer + security reviewer is a good starting point)
gcloud projects add-iam-policy-binding my-proj \
  --member="serviceAccount:claude-readonly@my-proj.iam.gserviceaccount.com" \
  --role="roles/viewer"
gcloud projects add-iam-policy-binding my-proj \
  --member="serviceAccount:claude-readonly@my-proj.iam.gserviceaccount.com" \
  --role="roles/iam.securityReviewer"

# Create a JSON key for that service account
gcloud iam service-accounts keys create ~/Projects/Cowork/keys/gcloud-credentials.json \
  --iam-account=claude-readonly@my-proj.iam.gserviceaccount.com
```

Again: this service account must not be able to change anything. For org-wide visibility, grant the roles at the organization or folder level instead of per-project.

### 2. Put the key in your Cowork keys folder

The credential file must be at `~/Projects/Cowork/keys/gcloud-credentials.json` — that is the path `tools/env.sh` expects. Do not paste the key into chat and do not commit it to a repo.

Lock it down:

```bash
chmod 0600 ~/Projects/Cowork/keys/gcloud-credentials.json
```

### 3. Create a `readonly` gcloud configuration

A gcloud *configuration* bundles an active account + project. Create one named `readonly` and bind it to the service account:

```bash
gcloud config configurations create readonly
gcloud auth activate-service-account \
  --key-file="$HOME/Projects/Cowork/keys/gcloud-credentials.json"
gcloud config set project my-proj --configuration=readonly
gcloud config set account claude-readonly@my-proj.iam.gserviceaccount.com --configuration=readonly
```

Keep your own write/admin credentials in a separate configuration (default name `production`) — Claude never uses it; it only appears in the write-handoff commands Claude tells *you* to run.

### 4. Run tools-setup

`tools-setup` installs the `gcloud` binary, writes `tools/env.sh`, and verifies the service account is active. You do not need to manually `gcloud auth activate-service-account` in each session — `env.sh` handles that.

### 5. Verify

Run the `gcp-check` skill, or:

```bash
source ~/Projects/Cowork/tools/env.sh
gcloud config get-value account
```

Confirm the returned account is the read-only service account you created. If it is, you're ready.

---

## Configuration names

`readonly` and `production` are defaults. If your configurations are named differently, tell Claude at the start of the session (e.g. "my read-only configuration is `audit-ro`") and it will substitute them. Claude still only ever *executes* under the read-only one.

---

## What this plugin does NOT do

- It does not make admin credentials safe. A read-only service account is the guardrail (see the warning above).
- It does not run writes for you. By design, those are always handed back to you.
- It does not store or transmit your key. The JSON key stays in your mounted Cowork file; never echo it into chat.
