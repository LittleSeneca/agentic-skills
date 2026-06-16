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

## Setup

### 1. Create a read-only AWS key

In the AWS account you want Claude to read, create an IAM user with a read-only policy and generate an access key pair:

- Attach a read-only policy (`ReadOnlyAccess`, `ViewOnlyAccess`, or a tighter custom policy).
- Create an **access key** (access key ID + secret access key) for that user.

Again: this key must not be able to change anything.

### 2. Put the key in a credentials file in your Cowork folder

This plugin reads credentials from a file you **mount in your Cowork folder** — the folder you make available to Claude (commonly `~/cowork/`). Do not paste secrets into chat and do not commit them to a repo.

Create a standard AWS credentials file at, for example, `~/cowork/aws-credentials`:

```ini
[readonly]
aws_access_key_id = AKIAEXAMPLEONLYREADONLY
aws_secret_access_key = <your-read-only-secret-access-key>
region = us-east-2

# Optional: a name for your OWN write/admin profile.
# Claude never uses this — it only appears in the write-handoff commands
# that Claude tells YOU to run. Configure it however you normally would
# (SSO, IAM key, etc.); it does not have to live in this file.
[production]
# sso or iam config you manage yourself
```

Lock the file down:

```bash
chmod 0600 ~/cowork/aws-credentials
```

### 3. Point AWS at that file

Tell the AWS CLI / MCP server to use the mounted file as its shared credentials file. The simplest way is an environment variable in the environment Claude runs in:

```bash
export AWS_SHARED_CREDENTIALS_FILE="$HOME/cowork/aws-credentials"
```

(Alternatively, merge the `[readonly]` profile into your existing `~/.aws/credentials`. Either way, the goal is that `--profile readonly` resolves to your read-only key.)

### 4. Verify

Run the `aws-check` skill, or simply:

```bash
aws sts get-caller-identity --profile readonly
```

Confirm the returned ARN is the read-only principal you created. If it is, you're ready — ask Claude any AWS question and it will use `--profile readonly` automatically.

---

## Customizing profile names

`readonly` and `production` are defaults. If your profiles are named differently, tell Claude at the start of the session (e.g. "my read-only profile is `audit-ro` and my write profile is `prod-admin`") and it will substitute them. Claude still only ever *executes* under the read-only one.

---

## What this plugin does NOT do

- It does not make admin keys safe. Read-only keys are the guardrail (see the warning above).
- It does not run writes for you. By design, those are always handed back to you.
- It does not store or transmit your secret key. The key stays in your mounted Cowork file; never echo it into chat.
