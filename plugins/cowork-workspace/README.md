# cowork-workspace

The house rule for where things go in a Cowork environment.

Everything the agent produces or relies on lives under one root, `~/Projects/Cowork`:

- **`keys/`** — credentials. The same folder the read-only cloud plugins (`aws-readonly`, `azure-readonly`, `gcp-readonly`, `x-readonly`) read from.
- **`artifacts/<project>/`** — generated files and project output: reports, exports, scripts, scratch files, downloads, anything not part of a tracked git repo.
- **the root** — settings and configuration.

The plugin routes every write before it happens and keeps stray files out of `$HOME`, the Desktop, Downloads, `/tmp`, and a repo's working tree. It also governs cleanup.

## Skill

| Skill | What it does |
|---|---|
| `cowork-workspace` | Triggers whenever the agent is about to write a file, save or read a credential, generate an artifact, or set up working state, and on asks like "save this", "write that out", or "put it somewhere". |

## Setup

No credentials. Install the plugin and the skill triggers automatically. It pairs with the read-only cloud plugins, which read their keys from the `keys/` folder this plugin defines.
