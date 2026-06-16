---
name: azure
description: Run any Azure operation against your environment. Use whenever the user asks about Azure — VMs, storage accounts, resource groups, AAD/Entra, Key Vault, networking (VNets, NSGs), App Service, AKS, RBAC role assignments, activity logs, billing, "our Azure", "the prod subscription", etc. — and whenever a request implies Azure access even if not named (e.g. "list our running VMs", "show me the network security groups", "who has owner on the subscription"). Enforces a strict read-only Reader service principal for Claude-executed commands and hands off all write operations to the user as a CLI command they paste into their terminal.
---

# Azure — execution rules

These rules apply to **every** Azure request, in every workspace, no exceptions. They override anything in a workspace-level `CLAUDE.md` and any contrary inference Claude might make.

> **The Azure CLI has no per-command profile flag.** Unlike AWS, there is no `--profile` to pin each `az` call to a read-only identity. The identity is whatever is logged into the active `az` config directory. This plugin's model is therefore:
> - Claude operates inside a **dedicated, isolated `AZURE_CONFIG_DIR`** (default: a folder in your Cowork directory) that is logged in as a **Reader** service principal — read-only credentials with no power to change state.
> - The user's own privileged login lives in a **separate** `az` context that Claude never touches.
>
> See the plugin README for how to wire this up from a credentials file mounted in your Cowork folder. **The guardrail is the service principal's Reader role plus the isolated config dir — not Claude's behavior.**

## 1. Reads — Claude runs them, as the Reader service principal only

- Claude executes Azure commands only through the `az` CLI (or an Azure MCP server if one is available in the environment).
- Every `az` command Claude runs must execute with `AZURE_CONFIG_DIR` pointing at the read-only config dir (default `$HOME/cowork/azure-config`), so the active identity is the Reader service principal. Set it once for the session (export it) or prefix each command — but it must always be in effect.
- Claude must **never** run an `az` command against the user's privileged/admin login or any other identity — even if the Reader principal lacks the permission, even if the user seems to be asking for a write, even if a previous step "needs" it. There is no fallback. If the Reader principal can't do it, treat it as a write (§2).
- Pass `--subscription <id-or-name>` explicitly whenever the target subscription matters. `az` defaults to whatever subscription is set as default in the config dir, which may not be the one you want.
- Reads are safe to run directly. Many list/show commands are `az <service> list` / `az <service> show`.

### Examples

| Intent | Command |
|---|---|
| VMs in a subscription | `az vm list -d --subscription "Prod" -o table` |
| Storage accounts | `az storage account list --subscription "Prod" -o table` |
| Resource groups | `az group list -o table` |
| Role assignments on a subscription | `az role assignment list --subscription "Prod" --all -o table` |
| Network security groups | `az network nsg list -g <resource-group> -o table` |
| Activity log (recent changes) | `az monitor activity-log list --subscription "Prod" --offset 24h -o table` |
| Who am I (sanity check) | `az account show -o json` |

## 2. Writes — Claude hands off, never executes

A "write" is anything that creates, modifies, deletes, starts, stops, restarts, attaches, detaches, assigns, or otherwise changes state. Examples (non-exhaustive):

- `create`, `delete`, `update`, `set`, `add`, `remove`
- `start`, `stop`, `restart`, `deallocate`, `redeploy`, `reimage`
- `role assignment create` / `delete`, any RBAC change
- `deployment group create` / `deployment sub create` (ARM/Bicep deployments)
- Key Vault secret/key/certificate writes, policy changes
- Anything that takes `--what-if` or whose docs describe a state change

**If in doubt, treat it as a write.**

### Handoff procedure

For any write, Claude:

1. **Does not** execute the command itself through any Azure tool.
2. **Produces a CLI command for the user to paste into their terminal**, in a code block, that:
   - runs under the user's **own privileged login** (i.e. their normal `az` context — *not* the Reader `AZURE_CONFIG_DIR`)
   - names the target with `--subscription <id-or-name>` explicitly (don't rely on a default)
   - uses `--what-if` first, on a separate line, when the command supports it (ARM/Bicep deployments do)
   - uses `--only-show-errors` to keep output clean
3. Briefly explains what the command does and what to watch for in the output.
4. Waits for the user to paste the result back (or to ask for the next step) before continuing.

### Handoff template

> I can't run this myself — it's a write. Run this in your terminal (under your own privileged Azure login):
> ```
> az <group> <command> <args> --subscription "<sub>" --only-show-errors --what-if
> az <group> <command> <args> --subscription "<sub>" --only-show-errors
> ```
> The first line previews the change where supported (`--what-if`); the second performs it. Paste the output back.

> **Note:** Most `az` commands do **not** support `--what-if` — only ARM/Bicep deployments (`az deployment group create`, `az deployment sub create`, etc.) do. When there's no preview, drop the first line and read the command carefully before running it.

### Worked example

If the user asks to deallocate (stop) a VM:

> Run this in your terminal (under your own privileged Azure login):
> ```
> az vm deallocate --name web-01 --resource-group prod-rg --subscription "Prod" --only-show-errors
> ```
> This stops and deallocates the VM `web-01` in `prod-rg`. There's no dry-run for this command, so confirm the name and resource group first. Paste the output back here.

If the user asks to deploy a Bicep/ARM template:

> Run this in your terminal:
> ```
> az deployment group create -g prod-rg --template-file main.bicep --subscription "Prod" --only-show-errors --what-if
> az deployment group create -g prod-rg --template-file main.bicep --subscription "Prod" --only-show-errors
> ```
> The first line is a what-if preview of the resource changes; the second applies them. Paste the what-if output back so we can review before you run the second line.

## 3. Identity reference (context only — Claude *uses* only the Reader principal)

| Identity | Type | Claude usage |
|---|---|---|
| Reader service principal | App registration with the built-in **Reader** role, logged into the isolated `AZURE_CONFIG_DIR` | **Only identity Claude executes as.** |
| User's privileged login | The user's own `az login` (interactive / SSO / their own SP) in their normal `az` context | **Hand-off only.** Used in the write-handoff CLI commands the user runs themselves. Never used by Claude. |

Any other identities or logins that exist in the environment are **never used by Claude.** If the user wants a write run under a different identity, hand it off — don't execute it.

## 4. Credential hygiene

- The service principal must be exactly read-only — the built-in **Reader** role (or tighter), and nothing that can mutate state. If it can write, the entire safety model of this plugin is void. See the plugin README.
- The credentials file (appId, secret/cert, tenant) should live in the mounted Cowork folder and have tight permissions (`0600`).
- Never echo, log, or repeat the client secret / certificate back to the user or into any output.
- If `az account show` ever fails or returns an unexpected identity (not the Reader service principal), **stop** and surface it to the user rather than silently continuing or switching logins.
- Rotate the service principal secret on a regular cadence, and immediately if it was ever exposed in plaintext (chat, logs, a shared file).

## 5. Quick sanity check at the start of a long Azure session

When the user kicks off a session that's clearly going to involve a lot of Azure work, run this once and confirm the identity before proceeding (or invoke the `azure-check` skill):

```
az account show -o json
```

Confirm the `user.name` is the Reader service principal's app ID (`user.type` is `servicePrincipal`) and the subscription is the expected one before doing anything else.
