---
name: aws-check
description: Verify AWS credentials are loaded under the read-only profile before a long AWS session. Use when starting AWS work, when AWS commands return auth or permission errors, or when the user asks to confirm which AWS identity Claude is operating as.
---

# AWS credential check

Confirm the read-only profile is wired up and working before doing real AWS work.

## Run the check

```bash
CREDS=$(ls /sessions/*/mnt/Cowork/keys/aws-credentials 2>/dev/null | head -1)
[ -z "$CREDS" ] && CREDS="$HOME/Projects/Cowork/keys/aws-credentials"
export AWS_SHARED_CREDENTIALS_FILE="$CREDS"
export AWS_PROFILE="avatarfleet-readonly"
PYPATH=$(ls /sessions/*/mnt/Cowork/tools/python-packages 2>/dev/null | head -1)
[ -z "$PYPATH" ] && PYPATH="$HOME/Projects/Cowork/tools/python-packages"
export PYTHONPATH="$PYPATH:$PYTHONPATH"

python3 -c "
import boto3
i = boto3.Session().client('sts').get_caller_identity()
print('Account:', i['Account'])
print('UserId: ', i['UserId'])
print('ARN:    ', i['Arn'])
"
```

## Interpret the result

- **boto3 not found** — run `pip install boto3 --break-system-packages` then retry.
- **Credentials file missing** — `$CREDS` resolved to nothing or the file is absent. Point the user at `~/Projects/Cowork/keys/aws-credentials` and ask them to populate it.
- **Unexpected ARN** — the profile is not the expected read-only principal. **Stop.** Do not run further AWS commands until the user confirms the identity or fixes the credentials.
- **`NoCredentialError` / `ProfileNotFound`** — the `aws-credentials` file doesn't have an `[avatarfleet-readonly]` section. Surface the error and ask the user to add it.

## What good looks like

```
Account: 019378881402
UserId:  AIDAXXXXXXXXXXXXXXXX
ARN:     arn:aws:iam::019378881402:user/claude-readonly
```

Once the ARN checks out, you're clear to proceed with the `aws` skill.
