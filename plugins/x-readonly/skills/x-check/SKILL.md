---
name: x-check
description: Verify the X (Twitter) API bearer token loads cleanly and can reach the X API v2 before a lookup-heavy session. Use when starting X work, when X lookups return 401/403/rate-limit errors, or when the user asks to confirm the token is configured.
---

# X API credential check

A quick preflight to confirm the X API bearer token is mounted and working before doing real lookups. Run this when starting X work or when something looks off with auth.

> The credentials path and default handle are user-configured — see the plugin README for setup.

## Step 1 — Confirm the credentials file is mounted

```bash
CREDS="${X_CREDENTIALS_FILE:-$HOME/Projects/Cowork/keys/x-credentials}"
test -f "$CREDS" && echo "found: $CREDS" || echo "MISSING: $CREDS"
```

If it's missing, the user hasn't put the credentials file in their Cowork keys folder (`~/Projects/Cowork/keys/`). Point them at the plugin README and stop.

## Step 2 — Confirm the token loads (without printing it)

```bash
CREDS="${X_CREDENTIALS_FILE:-$HOME/Projects/Cowork/keys/x-credentials}"
BEARER="$(grep -E '^bearer_token' "$CREDS" | head -1 | cut -d= -f2- | tr -d ' "'"'"'')"
DEFAULT_HANDLE="$(grep -E '^default_handle' "$CREDS" | head -1 | cut -d= -f2- | tr -d ' "@'"'"'')"
[ -n "$BEARER" ] && echo "bearer_token: loaded (${#BEARER} chars)" || echo "bearer_token: NOT FOUND"
echo "default_handle: ${DEFAULT_HANDLE:-<none set>}"
```

Report the length only — **never print the token itself.**

## Step 3 — Live call against the X API

Use the default handle if set, otherwise pick a known public account to test reachability:

```bash
H="${DEFAULT_HANDLE:-XDevelopers}"
curl -s -o /dev/null -w "HTTP %{http_code}\n" \
  -H "Authorization: Bearer $BEARER" \
  "https://api.twitter.com/2/users/by/username/$H"
```

- `HTTP 200` → token works, you're clear to proceed.
- `HTTP 401` → token missing/invalid. Re-check the credentials file.
- `HTTP 403` → token lacks access for this request (app permissions / product tier).
- `HTTP 429` → rate limited; wait and retry.

## What good looks like

- Credentials file present in the Cowork keys folder (`~/Projects/Cowork/keys/`).
- `bearer_token` loads and is non-empty.
- A live profile lookup returns `HTTP 200`.

If all three hold, hand off to the `x-api` skill for the actual lookups.
