# aws-readonly

Safe AWS access for Claude.

Claude runs **read-only** AWS commands for you through a read-only profile, and **hands every write back to you** as a copy-paste CLI command that you run yourself. Claude never executes a state-changing AWS call.

---

## ⚠️ ONLY USE READ-ONLY KEYS FOR YOUR ENVIRONMENT

**The single most important rule of this plugin: the AWS credentials you give it must be read-only.**

This plugin's safety model rests entirely on that one fact. The skill instructs Claude to:

- run reads itself under the read-only profile, and
- refuse to execute writes — handing them back to you as commands you run under a separate, privileged profile.

But Claude is not a security boundary. If the key you provide can mutate state, then a mistake, a confused instruction, or a prompt-injection in some tool output could result in real changes to your account. **The read-only-ness of the key is the actual guardrail.** Claude's behavior is the convenience layer on top of it.

So:

- ✅ Provision an IAM user (or role) with a **read-only / least-privilege** policy — start from AWS-managed `ReadOnlyAccess` or `ViewOnlyAccess`, or tighter.
- ✅ Give the plugin **only** that key.
- ❌ Do **not** give it admin keys, `PowerUserAccess`, or your SSO/production credentials.
- ❌ Do **not** assume Claude "won't run writes anyway" — enforce it with the key.

If the credentials can write, this plugin provides no protection. Don't do it.

---

## How it works

- **Reads** → Claude executes them under your read-only profile (default name `readonly`), via the AWS API MCP server or the AWS CLI.
- **Writes** → Claude does not run them. It produces a ready-to-paste CLI command (with `--dry-run` first where supported) targeting your write/admin profile (default name `production`), and you run it in your own terminal.

Two skills ship with the plugin:

| Skill | What it does |
|---|---|
| `aws` | The execution rules. Triggers on any AWS request and enforces read-only-for-Claude / writes-handed-off. |
| `aws-check` | A quick preflight that confirms which AWS identity Claude is operating as before a long session. |

---

## Prerequisites

Before using this plugin for the first time on a new machine, run the **`tools-setup` skill**. It installs `aws` as a persistent standalone binary in `~/Projects/Cowork/tools/` and wires up credentials. Subsequent sessions source `tools/env.sh` and the binary is ready instantly.

---

## Setup

### 1. Create a read-only AWS key

In the AWS account you want Claude to read, create an IAM user with a read-only policy and generate an access key pair:

- Attach a read-only policy (`ReadOnlyAccess`, `ViewOnlyAccess`, or a tighter custom policy).
- Create an **access key** (access key ID + secret access key) for that user.

Again: this key must not be able to change anything.

### 2. Put the key in your Cowork keys folder

This plugin reads credentials from a file in your **Cowork keys folder** (`~/Projects/Cowork/keys/`), the dedicated key store inside the Cowork folder you make available to Claude. Do not paste secrets into chat and do not commit them to a repo.

Create a standard AWS credentials file at `~/Projects/Cowork/keys/aws-credentials`:

```ini
[your-readonly-profile-name]
aws_access_key_id = AKIAEXAMPLEONLYREADONLY
aws_secret_access_key = <your-read-only-secret-access-key>
region = us-east-2

# Optional: a name for your OWN write/admin profile.
# Claude never uses this — it only appears in the write-handoff commands
# that Claude tells YOU to run. Configure it however you normally would
# (SSO, IAM key, etc.); it does not have to live in this file.
[your-write-profile-name]
# sso or iam config you manage yourself
```

**Put the read-only profile first.** `tools/env.sh` auto-detects `AWS_DEFAULT_PROFILE` by reading the first `[header]` in this file — Claude will use whatever profile is listed first.

Lock the file down:

```bash
chmod 0600 ~/Projects/Cowork/keys/aws-credentials
```

### 3. Run tools-setup

`tools-setup` installs the `aws` binary, writes `tools/env.sh`, and verifies `aws sts get-caller-identity` returns the expected ARN. You do not need to set any environment variables manually — `env.sh` handles `AWS_SHARED_CREDENTIALS_FILE` and `AWS_DEFAULT_PROFILE` automatically.

### 4. Verify

Run the `aws-check` skill, or:

```bash
source ~/Projects/Cowork/tools/env.sh
aws sts get-caller-identity
```

Confirm the returned ARN is the read-only principal you created. If it is, you're ready — ask Claude any AWS question and it will source `env.sh` and use `$AWS_DEFAULT_PROFILE` automatically.

---

## Profile names

The profile name is whatever you put as the first header in `aws-credentials`. No configuration needed — `env.sh` reads it automatically. Claude still only ever *executes* under that first (read-only) profile; write commands are always handed off to you by name.

---

## What this plugin does NOT do

- It does not make admin keys safe. Read-only keys are the guardrail (see the warning above).
- It does not run writes for you. By design, those are always handed back to you.
- It does not store or transmit your secret key. The key stays in your mounted Cowork file; never echo it into chat.
