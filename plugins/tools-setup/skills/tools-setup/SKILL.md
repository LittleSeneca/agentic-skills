---
name: tools-setup
description: Install aws, gh, and gcloud as persistent standalone binaries into ~/Projects/Cowork/tools/ and wire up credentials. Use when a cloud skill fails with "command not found", when setting up a new machine, or when the user says "set up CLI tools", "install aws/gh/gcloud", or "bootstrap my tools".
---

# tools-setup — bootstrap cloud CLIs

Installs `aws`, `gh`, and `gcloud` as persistent standalone binaries in `~/Projects/Cowork/tools/` and creates `tools/env.sh`, which all cloud skills source to put the binaries on PATH and load credentials. The install is idempotent — skip any binary that already exists at the right path.

## Layout after setup

```
~/Projects/Cowork/tools/
├── bin/
│   ├── aws          → shell wrapper (relative, session-safe)
│   ├── gh           → installs/<ver>/bin/gh (relative wrapper)
│   └── gcloud       → google-cloud-sdk/bin/gcloud (relative wrapper)
├── aws-cli-<arch>/  # AWS CLI v2 standalone extracted here
├── google-cloud-sdk/
├── installs/        # downloaded archives, gh binary
└── env.sh           # source this — the only file skills need to touch
```

> **Why shell wrappers, not symlinks?**
> AWS CLI's `--bin-dir` flag creates symlinks with absolute paths baked in. In
> Cowork's sandboxed bash environment the session mount point changes each run
> (e.g. `/sessions/abc123/mnt/Cowork/`), so absolute symlinks immediately break.
> Shell wrappers that compute their target via `dirname "$0"` are session-safe.

## Step 0 — Prerequisites

```bash
TOOLS="$HOME/Projects/Cowork/tools"
KEYS="$HOME/Projects/Cowork/keys"
mkdir -p "$TOOLS/bin" "$TOOLS/installs"
ARCH=$(uname -m)   # aarch64 or x86_64
```

Confirm `$KEYS/aws-credentials`, `$KEYS/gcloud-credentials.json`, and `$KEYS/github-credentials` all exist before proceeding. If any are missing, stop and tell the user which file is missing — do not continue.

## Step 1 — AWS CLI

Skip if `$TOOLS/bin/aws` already exists **and** `$TOOLS/bin/aws --version` succeeds.
If the file exists but `--version` fails, the wrapper is broken (stale absolute symlink from a
previous install) — delete it and reinstall.

```bash
if [ "$ARCH" = "aarch64" ]; then
  URL="https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip"
  CLI_DIR="aws-cli-arm64"
else
  URL="https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip"
  CLI_DIR="aws-cli-x86_64"
fi

cd "$TOOLS/installs"
curl -fsSL "$URL" -o awscli.zip
unzip -q awscli.zip

# Install into tools/<CLI_DIR>/ but do NOT use --bin-dir (it creates absolute symlinks).
./aws/install --install-dir "$TOOLS/$CLI_DIR" --update
rm -rf awscli.zip aws/
```

After extraction, write a **relative shell wrapper** instead of relying on the installer's symlinks:

```bash
cat > "$TOOLS/bin/aws" << 'AWSEOF'
#!/bin/bash
# Relative wrapper — finds the actual dist/aws under tools/aws-cli-*/
TOOLS="$(cd "$(dirname "$0")/.." && pwd)"
AWS_BIN=$(find "$TOOLS" -maxdepth 6 -name "aws" -path "*/dist/aws" 2>/dev/null | sort -V | tail -1)
if [ -z "$AWS_BIN" ]; then
  echo "aws: binary not found under $TOOLS — run the tools-setup skill to reinstall" >&2
  exit 127
fi
exec "$AWS_BIN" "$@"
AWSEOF
chmod +x "$TOOLS/bin/aws"

# Same treatment for aws_completer
cat > "$TOOLS/bin/aws_completer" << 'COMPEOF'
#!/bin/bash
TOOLS="$(cd "$(dirname "$0")/.." && pwd)"
COMP=$(find "$TOOLS" -maxdepth 6 -name "aws_completer" -path "*/dist/aws_completer" 2>/dev/null | sort -V | tail -1)
[ -n "$COMP" ] && exec "$COMP" "$@"
COMPEOF
chmod +x "$TOOLS/bin/aws_completer"
```

Verify: `$TOOLS/bin/aws --version` should print the AWS CLI version.

## Step 2 — GitHub CLI (gh)

Skip if `$TOOLS/bin/gh` already exists and `$TOOLS/bin/gh --version` succeeds.

Resolve the latest release version from the GitHub API, then download the correct archive:

```bash
VER=$(curl -fsSL https://api.github.com/repos/cli/cli/releases/latest | grep '"tag_name"' | sed 's/.*"v\([^"]*\)".*/\1/')
if [ "$ARCH" = "aarch64" ]; then
  SUFFIX="linux_arm64"
else
  SUFFIX="linux_amd64"
fi

cd "$TOOLS/installs"
curl -fsSL "https://github.com/cli/cli/releases/download/v${VER}/gh_${VER}_${SUFFIX}.tar.gz" -o gh.tar.gz
tar -xzf gh.tar.gz
cp "gh_${VER}_${SUFFIX}/bin/gh" "$TOOLS/bin/gh"
rm -rf gh.tar.gz "gh_${VER}_${SUFFIX}/"
chmod +x "$TOOLS/bin/gh"
```

Verify: `$TOOLS/bin/gh --version` should print the gh version.

## Step 3 — gcloud SDK

Skip if `$TOOLS/bin/gcloud` already exists and `$TOOLS/bin/gcloud --version` succeeds.

```bash
if [ "$ARCH" = "aarch64" ]; then
  URL="https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-arm.tar.gz"
else
  URL="https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-x86_64.tar.gz"
fi

cd "$TOOLS"
curl -fsSL "$URL" -o installs/gcloud.tar.gz
tar -xzf installs/gcloud.tar.gz   # extracts to google-cloud-sdk/
rm installs/gcloud.tar.gz
ln -sf "$TOOLS/google-cloud-sdk/bin/gcloud" "$TOOLS/bin/gcloud"
chmod +x "$TOOLS/bin/gcloud"
```

Verify: `$TOOLS/bin/gcloud --version` should print the gcloud version.

## Step 4 — Write env.sh

Write (or overwrite) `$TOOLS/env.sh`:

```bash
cat > "$TOOLS/env.sh" << 'ENVEOF'
#!/bin/bash
# Source at the top of any skill bash block. Idempotent.
COWORK_TOOLS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COWORK_KEYS="$(cd "$COWORK_TOOLS/../keys" && pwd)"
export PATH="$COWORK_TOOLS/bin:$PATH"

# AWS
export AWS_SHARED_CREDENTIALS_FILE="$COWORK_KEYS/aws-credentials"
export AWS_DEFAULT_PROFILE="$(grep '^\[' "$COWORK_KEYS/aws-credentials" 2>/dev/null | head -1 | tr -d '[]')"

# gh — persistent config dir (avoids $HOME/.config/gh clobbering)
export GH_CONFIG_DIR="$COWORK_TOOLS/config/gh"

# gcloud — activate service account if not already active
if command -v gcloud &>/dev/null; then
  _ACCT=$(gcloud config get-value account 2>/dev/null)
  if [ -z "$_ACCT" ] || [ "$_ACCT" = "(unset)" ]; then
    gcloud auth activate-service-account \
      --key-file="$COWORK_KEYS/gcloud-credentials.json" \
      --quiet 2>/dev/null
  fi
fi
ENVEOF
chmod +x "$TOOLS/env.sh"
```

## Step 5 — Wire up gh authentication

```bash
mkdir -p "$TOOLS/config/gh"
export GH_CONFIG_DIR="$TOOLS/config/gh"
GH_TOKEN_VAL=$(awk -F'= *' '/^token/ {print $2}' "$KEYS/github-credentials" | tr -d ' \r\n')
echo "$GH_TOKEN_VAL" | "$TOOLS/bin/gh" auth login --with-token
```

Verify: `GH_CONFIG_DIR="$TOOLS/config/gh" $TOOLS/bin/gh api user --jq '.login'` should return the expected GitHub username.

## Step 6 — Wire up gcloud authentication

```bash
source "$TOOLS/env.sh"
gcloud auth activate-service-account \
  --key-file="$KEYS/gcloud-credentials.json" \
  --quiet
```

Verify: `gcloud config get-value account` returns the service account email.

## Step 7 — Verify AWS credentials

```bash
source "$TOOLS/env.sh"
aws sts get-caller-identity
```

Should return a JSON object with the ARN for the read-only principal. If it fails with a credentials error, check that `$KEYS/aws-credentials` has valid keys under the first profile header.

## Final check

Run all three verifications in sequence and report the results:

```bash
source "$HOME/Projects/Cowork/tools/env.sh"
echo "--- AWS ---"
aws sts get-caller-identity --output text --query 'Arn'
echo "--- GitHub ---"
gh api user --jq '.login'
echo "--- gcloud ---"
gcloud config get-value account
```

Expected output:
- AWS: the ARN for your read-only IAM principal
- GitHub: `littleseneca` (or the configured username)
- gcloud: the service account email from `gcloud-credentials.json`

If all three pass, setup is complete. Subsequent sessions source `tools/env.sh` and the binaries are ready instantly — no installation step needed.

## Repairing a broken aws wrapper

If `aws` is in `tools/bin/` but fails with "Permission denied" or "No such file or directory",
the old install left an absolute symlink from a previous Cowork session. Fix it in one line —
no re-download needed, the actual CLI files are still there:

```bash
TOOLS="$HOME/Projects/Cowork/tools"
cat > "$TOOLS/bin/aws" << 'AWSEOF'
#!/bin/bash
TOOLS="$(cd "$(dirname "$0")/.." && pwd)"
AWS_BIN=$(find "$TOOLS" -maxdepth 6 -name "aws" -path "*/dist/aws" 2>/dev/null | sort -V | tail -1)
[ -z "$AWS_BIN" ] && { echo "aws: binary not found under $TOOLS — run tools-setup" >&2; exit 127; }
exec "$AWS_BIN" "$@"
AWSEOF
chmod +x "$TOOLS/bin/aws"
```

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `aws: Permission denied` or broken symlink | Old absolute symlink from prior session | Run the "Repairing a broken aws wrapper" block above |
| `aws sts get-caller-identity` → `NoCredentialProviders` | `aws-credentials` file path wrong or file missing | Check `$AWS_SHARED_CREDENTIALS_FILE` |
| `aws` returns wrong account | First profile in credentials file is not the read-only one | Move the read-only profile to the top of `aws-credentials` |
| `gh api user` → `not logged in` | `GH_CONFIG_DIR` not set or `gh auth login` failed | Re-run Step 5 |
| `gcloud config get-value account` → `(unset)` | Service account activation failed | Check that `gcloud-credentials.json` exists and is valid JSON |
