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

## Setup

### 1. Create a read-only service account

In the GCP project (or organization) you want Claude to read, create a service account and grant it read-only roles, then generate a JSON key:

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
gcloud iam service-accounts keys create ~/Projects/Cowork/keys/gcp-readonly-key.json \
  --iam-account=claude-readonly@my-proj.iam.gserviceaccount.com
```

Again: this service account must not be able to change anything. For org-wide visibility, grant the roles at the organization or folder level instead of per-project.

### 2. Put the key in your Cowork keys folder

This plugin reads credentials from a JSON key file in your **Cowork keys folder** (`~/Projects/Cowork/keys/`), the dedicated key store inside the Cowork folder you make available to Claude. Do not paste the key into chat and do not commit it to a repo.

The example above already writes the key to `~/Projects/Cowork/keys/gcp-readonly-key.json`. Lock it down:

```bash
chmod 0600 ~/Projects/Cowork/keys/gcp-readonly-key.json
```

### 3. Create a `readonly` gcloud configuration bound to that key

A gcloud *configuration* bundles an active account + project (the GCP analog of an AWS named profile). Activate the read-only service account and bind it to a dedicated configuration:

```bash
# Create and switch to a 'readonly' configuration
gcloud config configurations create readonly

# Activate the read-only service-account key
gcloud auth activate-service-account \
  --key-file="$HOME/Projects/Cowork/keys/gcp-readonly-key.json"

# Set the default project for this configuration
gcloud config set project my-proj --configuration=readonly
gcloud config set account claude-readonly@my-proj.iam.gserviceaccount.com --configuration=readonly
```

Keep your own write/admin credentials in a separate configuration (default name `production`) — Claude never uses it; it only appears in the write-handoff commands Claude tells *you* to run.

### 4. Verify

Run the `gcp-check` skill, or simply:

```bash
gcloud config list account --configuration=readonly
```

Confirm the returned account is the read-only service account you created. If it is, you're ready — ask Claude any GCP question and it will use `--configuration=readonly` automatically.

---

## Customizing configuration names

`readonly` and `production` are defaults. If your configurations are named differently, tell Claude at the start of the session (e.g. "my read-only configuration is `audit-ro` and my write configuration is `prod-admin`") and it will substitute them. Claude still only ever *executes* under the read-only one.

---

## What this plugin does NOT do

- It does not make admin credentials safe. A read-only service account is the guardrail (see the warning above).
- It does not run writes for you. By design, those are always handed back to you.
- It does not store or transmit your key. The JSON key stays in your mounted Cowork file; never echo it into chat.
