# azure-readonly

Safe Azure access for Claude.

Claude runs **read-only** Azure commands for you as a Reader service principal, and **hands every write back to you** as a copy-paste CLI command that you run yourself. Claude never executes a state-changing Azure call.

---

## ⚠️ ONLY USE A READ-ONLY SERVICE PRINCIPAL FOR YOUR ENVIRONMENT

**The single most important rule of this plugin: the Azure credentials you give it must be read-only.**

This plugin's safety model rests entirely on that one fact. The skill instructs Claude to:

- run reads itself as the Reader service principal, and
- refuse to execute writes — handing them back to you as commands you run under your own privileged login.

But Claude is not a security boundary. If the credential you provide can mutate state, then a mistake, a confused instruction, or a prompt-injection in some tool output could result in real changes to your tenant. **The read-only-ness of the service principal is the actual guardrail.** Claude's behavior is the convenience layer on top of it.

So:

- ✅ Create an app registration / service principal and grant it **only** the built-in `Reader` role (or tighter) at the subscription or resource-group scope you want Claude to see.
- ✅ Give the plugin **only** that credential.
- ❌ Do **not** give it `Contributor`, `Owner`, `User Access Administrator`, or your own interactive/SSO login.
- ❌ Do **not** assume Claude "won't run writes anyway" — enforce it with the role.

If the credential can write, this plugin provides no protection. Don't do it.

> **Why a service principal and not a `--profile`?** The Azure CLI has no per-command profile flag the way AWS does. The active identity is simply whatever is logged into the `az` config directory in use. This plugin therefore isolates Claude into its **own `az` config directory** logged in as the Reader service principal, kept separate from your normal `az login`. The guardrail is the Reader role plus that isolation — there is no per-command identity flag to rely on.

---

## How it works

- **Reads** → Claude executes them as the Reader service principal, via the `az` CLI running with a dedicated `AZURE_CONFIG_DIR`.
- **Writes** → Claude does not run them. It produces a ready-to-paste `az` command (with `--what-if` first where supported) for you to run under your own privileged login, in your own terminal.

Two skills ship with the plugin:

| Skill | What it does |
|---|---|
| `azure` | The execution rules. Triggers on any Azure request and enforces read-only-for-Claude / writes-handed-off. |
| `azure-check` | A quick preflight that confirms which Azure identity Claude is operating as before a long session. |

---

## Setup

### 1. Create a read-only Azure service principal

In the subscription you want Claude to read, create a service principal and assign it the built-in `Reader` role:

```bash
az ad sp create-for-rbac \
  --name "claude-readonly" \
  --role "Reader" \
  --scopes "/subscriptions/<your-subscription-id>"
```

This prints an `appId`, `password`, and `tenant`. That trio is the credential. Again: it must not be able to change anything — `Reader` and nothing broader.

(For tighter scope, point `--scopes` at a specific resource group instead of the whole subscription. For multiple subscriptions, add more `--scopes` or create additional assignments.)

### 2. Put the credential in a file in your Cowork folder

This plugin reads credentials from a file you **mount in your Cowork folder** — the folder you make available to Claude (commonly `~/cowork/`). Do not paste secrets into chat and do not commit them to a repo.

Create a file at, for example, `~/cowork/azure-credentials` (a simple env file):

```bash
# Reader service principal — read-only, never able to change state.
AZURE_CLIENT_ID=00000000-0000-0000-0000-000000000000
AZURE_CLIENT_SECRET=<your-reader-sp-secret>
AZURE_TENANT_ID=11111111-1111-1111-1111-111111111111
AZURE_SUBSCRIPTION_ID=22222222-2222-2222-2222-222222222222
```

Lock the file down:

```bash
chmod 0600 ~/cowork/azure-credentials
```

### 3. Log Claude's isolated `az` context in as the Reader SP

So Claude's identity stays separate from your own `az login`, give it a dedicated config directory and log the service principal into *that*:

```bash
export AZURE_CONFIG_DIR="$HOME/cowork/azure-config"
set -a; source "$HOME/cowork/azure-credentials"; set +a

az login --service-principal \
  --username "$AZURE_CLIENT_ID" \
  --password "$AZURE_CLIENT_SECRET" \
  --tenant "$AZURE_TENANT_ID"

az account set --subscription "$AZURE_SUBSCRIPTION_ID"
```

Every `az` command Claude runs must have `AZURE_CONFIG_DIR="$HOME/cowork/azure-config"` in effect, so it acts as the Reader service principal. Your **own** terminal — without that `AZURE_CONFIG_DIR`, or with a different one — keeps using your normal privileged login, which is where the write-handoff commands get run.

> Prefer a certificate over a client secret if you can: `az login --service-principal --username <appId> --password <path-to-cert.pem> --tenant <tenant>`.

### 4. Verify

Run the `azure-check` skill, or simply (with the read-only `AZURE_CONFIG_DIR` in effect):

```bash
az account show -o json
```

Confirm `user.type` is `servicePrincipal`, `user.name` is your Reader app ID, and the subscription is the expected one. If it is, you're ready — ask Claude any Azure question and it will operate as the Reader principal automatically.

---

## Customizing names and scope

`claude-readonly`, `~/cowork/azure-config`, and the subscription are defaults/examples. If yours differ, tell Claude at the start of the session (e.g. "my read-only config dir is `~/cowork/az-audit` and the subscription is `Sandbox`") and it will substitute them. Claude still only ever *executes* as the Reader service principal.

---

## What this plugin does NOT do

- It does not make a `Contributor`/`Owner` credential safe. A read-only `Reader` service principal is the guardrail (see the warning above).
- It does not run writes for you. By design, those are always handed back to you to run under your own login.
- It does not store or transmit your client secret. The credential stays in your mounted Cowork file; never echo it into chat.
