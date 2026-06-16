---
name: x-api
description: Use this skill when the user mentions X, Twitter, tweets, or posts, references an X handle, or asks to look up an X profile, see someone's latest posts, search posts, check a follower count, or fetch a post by id. Runs read-only lookups against the X API v2 using a bearer token stored in a credentials file mounted in the user's Cowork folder. Defaults to the user's configured handle but can also read other public accounts when asked. Strictly read-only: never posts, deletes, likes, or follows.
---

# X (Twitter) read-only lookups

Read-only access to the X API v2. This skill **reads** public X data — profiles, posts, search results, follower counts. It **never** writes: no posting, deleting, liking, following, retweeting, DMs, or any other state-changing action. If the user asks for a write, decline and explain that this skill is read-only by design.

> All credentials and handles below are configured by the user, not hardcoded. See the plugin README for setup.

## Credentials

The bearer token lives in a credentials file mounted in the user's **Cowork folder** (default `~/cowork/x-credentials`). It is an `key=value` file; the only field this skill needs is `bearer_token`. An optional `default_handle` sets which account to use when the user doesn't name one.

**Never echo the token into chat, logs, command output, or any file.** Load it into a shell variable and reference the variable.

Load it like this (adjust the path if the user mounts it elsewhere):

```bash
CREDS="${X_CREDENTIALS_FILE:-$HOME/cowork/x-credentials}"
BEARER="$(grep -E '^bearer_token' "$CREDS" | head -1 | cut -d= -f2- | tr -d ' "'"'"'')"
DEFAULT_HANDLE="$(grep -E '^default_handle' "$CREDS" | head -1 | cut -d= -f2- | tr -d ' "@'"'"'')"
```

Then pass `-H "Authorization: Bearer $BEARER"` on each request. Don't print `$BEARER`.

## Which account?

- If the user names a handle, use it.
- If they don't, use `default_handle` from the credentials file.
- If neither exists, ask the user whose account they mean.

## Common lookups (X API v2)

Replace `$BEARER` / `$HANDLE` / `$ID` as set above. All are `GET` requests with the bearer header.

### Profile + follower count

```bash
curl -s -H "Authorization: Bearer $BEARER" \
  "https://api.twitter.com/2/users/by/username/$HANDLE?user.fields=description,public_metrics,created_at,verified,location"
```

`public_metrics` includes `followers_count`, `following_count`, `tweet_count`, `listed_count`.

### Latest posts for an account

First resolve the user id (from the profile call above, field `data.id`), then:

```bash
curl -s -H "Authorization: Bearer $BEARER" \
  "https://api.twitter.com/2/users/$ID/tweets?max_results=10&tweet.fields=created_at,public_metrics,referenced_tweets&exclude=retweets,replies"
```

Adjust `max_results` (5–100) and the `exclude` list as the user asks.

### Search recent posts

```bash
curl -s -H "Authorization: Bearer $BEARER" \
  --data-urlencode "query=from:$HANDLE keyword" \
  --data-urlencode "max_results=20" \
  --data-urlencode "tweet.fields=created_at,public_metrics" \
  -G "https://api.twitter.com/2/tweets/search/recent"
```

The recent-search endpoint covers roughly the last 7 days. Build the `query` from the user's intent (`from:`, `to:`, keywords, `-is:retweet`, etc.).

### Fetch a single post by id

```bash
curl -s -H "Authorization: Bearer $BEARER" \
  "https://api.twitter.com/2/tweets/$ID?tweet.fields=created_at,public_metrics,author_id&expansions=author_id&user.fields=username"
```

## Output

- Summarize results clearly: handle, follower count, post text + timestamp + engagement, etc.
- For lists of posts, a compact table or bulleted list works well.
- If a call returns an error (rate limit, 401, 403, not found), surface the status and message rather than guessing. A 401/403 usually means the token is missing, wrong, or lacks access — point the user at the `x-check` skill / plugin README.

## Hard rules

- **Read-only.** Never call write endpoints (`POST`/`PUT`/`DELETE` on tweets, likes, follows, DMs, etc.), even if asked. Decline and explain.
- **Public data only.** Don't attempt to access protected/private accounts or anything the token isn't entitled to.
- **Never reveal the token.** Not in output, not in a file, not on request.
