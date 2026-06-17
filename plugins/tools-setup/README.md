# tools-setup

One-time bootstrap that installs `aws`, `gh`, and `gcloud` as persistent standalone binaries into `~/Projects/Cowork/tools/` and wires up credentials for all three.

After setup, all cloud skills (`aws-readonly`, `gcp-readonly`, `avatarfleet-github`) source `tools/env.sh` at the top of every bash block. That single line puts the binaries on PATH, sets the correct credential environment variables, and activates the gcloud service account. No manual credential wiring per session.

---

## When to run

Run `tools-setup` once on each new machine. It is idempotent — any binary that is already installed and working is skipped.

Also run it if a cloud skill fails with `command not found` for `aws`, `gh`, or `gcloud`.

---

## What gets installed

| Binary | Location | Source |
|---|---|---|
| `aws` | `tools/bin/aws` | AWS CLI v2 standalone (architecture-matched) |
| `gh` | `tools/bin/gh` | GitHub CLI latest release (architecture-matched) |
| `gcloud` | `tools/bin/gcloud` | Google Cloud SDK (architecture-matched) |

All binaries land under `~/Projects/Cowork/tools/`, which is persistent across Cowork sessions. The `tools/bin/` directory is added to PATH by `env.sh`.

---

## Prerequisites

These three credential files must exist in `~/Projects/Cowork/keys/` before running setup:

| File | Used by | Format |
|---|---|---|
| `aws-credentials` | aws-readonly | INI, `[profile-name]` headers |
| `gcloud-credentials.json` | gcp-readonly | Service account JSON key |
| `github-credentials` | avatarfleet-github | INI, `[github-access]` section with `token = ghp_...` |

`tools-setup` will stop and tell you which file is missing rather than proceeding with partial credentials.

---

## After setup

Source `tools/env.sh` in any bash block to get everything:

```bash
source ~/Projects/Cowork/tools/env.sh
```

This exports:
- `PATH` — `tools/bin/` prepended
- `AWS_SHARED_CREDENTIALS_FILE` — points at `keys/aws-credentials`
- `AWS_DEFAULT_PROFILE` — auto-detected from the first profile header in `aws-credentials`
- `GH_CONFIG_DIR` — points at `tools/config/gh/` (persistent gh session)
- activates the gcloud service account if not already active

---

## Azure

Azure CLI (`az`) has no standalone binary distribution and requires `sudo apt` or `pip install`. It is intentionally out of scope for this plugin. See the `azure-readonly` plugin README for the current workaround.
