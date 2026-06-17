# x-readonly

Read-only X (Twitter) lookups for Claude.

Claude can look up X profiles, recent posts, search results, follower counts, and individual posts by id — all through the **X API v2**, using a bearer token you mount in your Cowork folder. It is **strictly read-only**: it never posts, deletes, likes, follows, retweets, or sends DMs.

---

## ⚠️ READ-ONLY BY DESIGN — USE A TOKEN WITH LEAST PRIVILEGE

This plugin only ever performs read calls. To keep that guarantee real:

- ✅ Provide an **app Bearer Token** from a project in the [X Developer Portal](https://developer.x.com). Bearer-token (app-only) auth can only read public data — it cannot post or act on behalf of a user.
- ❌ Do **not** wire up user-context OAuth 1.0a/2.0 write tokens just because you have them. The skill won't use them, and keeping write credentials out of the file removes the risk entirely.
- ❌ Do **not** ask Claude to post, delete, like, or follow. It will decline — but the token should also not be able to.

Claude's behavior is the convenience layer; an app-only read token is the actual guardrail.

---

## How it works

Two skills ship with the plugin:

| Skill | What it does |
|---|---|
| `x-api` | The lookups. Triggers on X/Twitter requests and runs read-only X API v2 calls (profile, posts, search, follower count, post-by-id). |
| `x-check` | A quick preflight that confirms the bearer token is mounted and the API is reachable. |

Credentials are read from a file in your **Cowork keys folder** (`~/Projects/Cowork/keys/`) — never pasted into chat or committed to a repo.

---

## Setup

### 1. Get an X API bearer token

1. Go to the [X Developer Portal](https://developer.x.com) and create (or open) a Project + App.
2. Under the app's **Keys and tokens**, generate/copy the **Bearer Token**.
3. A Free or Basic tier is enough for read lookups; higher tiers raise rate limits and search history depth.

### 2. Put the token in your Cowork keys folder

Create a file at, for example, `~/Projects/Cowork/keys/x-credentials` (the dedicated key store inside the Cowork folder you make available to Claude). It's a simple `key=value` file. For read-only lookups, **only `bearer_token` is required**:

```ini
bearer_token=AAAAAAAAAAAAAAAAAAAA...your-app-bearer-token...
# Optional: the account to use when you don't name one.
default_handle=your_handle
```

> You can keep other X keys in this file if you use it elsewhere, but this plugin reads only `bearer_token` and `default_handle`. The fewer write-capable secrets you store, the better.

Lock the file down:

```bash
chmod 0600 ~/Projects/Cowork/keys/x-credentials
```

### 3. (Optional) Point the plugin at a different path

By default the skills look at `~/Projects/Cowork/keys/x-credentials`. To use another location, set:

```bash
export X_CREDENTIALS_FILE="$HOME/Projects/Cowork/keys/x/bearer-token"
```

### 4. Verify

Run the `x-check` skill, or test directly (this prints only the HTTP status, not your token):

```bash
BEARER="$(grep -E '^bearer_token' ~/Projects/Cowork/keys/x-credentials | head -1 | cut -d= -f2- | tr -d ' \"')"
curl -s -o /dev/null -w "HTTP %{http_code}\n" \
  -H "Authorization: Bearer $BEARER" \
  "https://api.twitter.com/2/users/by/username/XDevelopers"
```

`HTTP 200` means you're ready. Then ask Claude things like "what are my latest posts", "how many followers does @someone have", or "search my recent posts for X".

---

## Usage examples

- "Look up @handle's profile and follower count."
- "Show me my last 10 posts."
- "Search my recent posts for 'launch'."
- "Fetch this post by id: 1234567890."
- "Who does @handle follow the most?" (read-only metrics only)

If you don't name a handle, the plugin uses `default_handle` from your credentials file.

---

## What this plugin does NOT do

- It does not post, delete, like, follow, retweet, or send DMs — ever. Read-only by design.
- It does not access protected/private accounts beyond what the token is entitled to.
- It does not store or transmit your token. The token stays in your mounted Cowork file; it's never echoed into chat.
