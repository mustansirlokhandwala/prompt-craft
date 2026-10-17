# Making prompt-craft always on

Skills load **on demand**: the model sees each skill's name and description and loads the full instructions only when a request matches. That keeps them cheap, but it means they don't run on every prompt.

To apply prompt-craft to *every* prompt, load the short rules in [`rules/always-on.md`](../rules/always-on.md) (~350 tokens) into the agent's standing context. The rules handle intent, gaps, budget warnings and answer size on every request. They call the full skills only when needed.

| Tool | Always-on mechanism | Skills location |
|---|---|---|
| Claude Code (plugin) | Automatic: a `SessionStart` hook | Installed with the plugin |
| Claude Code (manual) | `~/.claude/CLAUDE.md` | `~/.claude/skills/` |
| Claude.ai | Profile preferences or Project instructions | Upload under Settings → Capabilities → Skills |
| Antigravity | `~/.gemini/GEMINI.md` or `.agents/rules/` (Always On) | `.agents/skills/` |

## Claude Code

### Option A: install the plugin (automatic)

```bash
claude plugin marketplace add mustansirlokhandwala/prompt-craft
```

```bash
claude plugin install prompt-craft@prompt-craft
```

The plugin's [`hooks/hooks.json`](../hooks/hooks.json) runs a `SessionStart` hook. The hook prints the rules, and Claude Code adds them to the session context at startup, resume, `/clear` and after compaction.

To turn it off, disable the plugin with `claude plugin disable prompt-craft`.

**Why `SessionStart` and not `UserPromptSubmit`?** Both inject context. `UserPromptSubmit` re-sends the rules with every prompt (~350 tokens × every message). `SessionStart` sends them once and they stay in context. If you find the model forgetting the rules in very long sessions, change `SessionStart` to `UserPromptSubmit` in `hooks/hooks.json`.

### Option B: manual, without the plugin

```bash
cat rules/always-on.md >> ~/.claude/CLAUDE.md
```

```bash
cp -r skills/* ~/.claude/skills/
```

To apply it to one project only, append the rules to that project's `CLAUDE.md` and copy the skills into its `.claude/skills/` instead.

## Claude.ai (web, desktop, mobile)

1. Zip each folder in `skills/` and upload it under **Settings → Capabilities → Skills**.
2. Paste the contents of `rules/always-on.md` into one of these:
   - **Settings → Profile → personal preferences**: applies to all your chats.
   - **Project → instructions**: applies only to chats in that project. Use this to share the setup with a team.

## Google Antigravity

Antigravity uses **rules** for always-on behavior and **skills** for on-demand procedures, the same split as Claude Code.

### Rules (always on)

Choose one:

- **All workspaces.** Append the rules to your global rules file:

  ```bash
  cat rules/always-on.md >> ~/.gemini/GEMINI.md
  ```

- **One workspace.** Copy the rules into the workspace's rules folder:

  ```bash
  mkdir -p .agents/rules && cp rules/always-on.md .agents/rules/prompt-craft.md
  ```

  Then open **Customizations → Rules**, select `prompt-craft` and set **Activation** to **Always On**.

Rule files are limited to 12,000 characters. This one is about 1,000.

### Skills (on demand)

Copy the skills into the workspace:

```bash
mkdir -p .agents/skills && cp -r skills/* .agents/skills/
```

To use them in every workspace, install them globally instead. Recent versions read `~/.gemini/config/skills/`. Use symlinks, so a `git pull` updates them:

```bash
for s in skills/*/; do ln -sfn "$PWD/$s" ~/.gemini/config/skills/; done
```

Older Antigravity versions use `.agent/` (singular) instead of `.agents/`. The global skills folder has moved between versions, so check **Customizations → Skills** in your version for the path it reads.

## Tips

- **Keep always-on text short.** It is paid for in every session. Put long procedures in skills, not in rules.
- **Change the thresholds.** Edit the numbers in rule 4 of `rules/always-on.md` to match your plan or budget.
- **Check it works.** Start a new session and send a vague prompt such as "make it better". The agent should state the intent it assumed before it does any work.
