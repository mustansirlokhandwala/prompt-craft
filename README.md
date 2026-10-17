# prompt-craft

Skills that turn weak prompts into good ones and stop you wasting tokens.

| Skill | What it does |
|---|---|
| [`prompt-improver`](skills/prompt-improver/SKILL.md) | Finds the real intent, fills the missing pieces, rewrites the prompt for accuracy and efficiency, and explains each change so you learn. |
| [`token-budget`](skills/token-budget/SKILL.md) | Estimates tokens in and out, warns before a task goes over budget, and suggests cheaper ways to get the same result. |

## Install

**Claude Code (plugin):**

```bash
claude plugin marketplace add mustansirlokhandwala/prompt-craft
```

```bash
claude plugin install prompt-craft@prompt-craft
```

**Claude Code (manual):** copy the folders in `skills/` into `~/.claude/skills/`.

**Claude.ai:** zip a skill folder (for example `skills/prompt-improver`) and upload it under Settings → Capabilities → Skills.

## Use

Just ask:

- "Improve this prompt: *write me a blog post about AI*"
- "/prompt-improver can u fix my code its broken"
- "How many tokens will this take?" (with files attached)

The token-budget skill also warns on its own when you paste a lot of text or start a big multi-step task.

## Always on

Skills load only when a request matches them. To apply prompt-craft to **every** prompt, load the short rules in [`rules/always-on.md`](rules/always-on.md) (~250 tokens) into the agent's standing context:

- **Claude Code plugin:** automatic. A `SessionStart` hook loads the rules in every session.
- **Claude Code manual:** append the rules to `~/.claude/CLAUDE.md`.
- **Claude.ai:** paste the rules into your profile preferences or a project's instructions.
- **Antigravity:** append the rules to `~/.gemini/GEMINI.md`, or copy them into `.agents/rules/` and set the rule to Always On.

Step-by-step setup for each tool is in [docs/always-on.md](docs/always-on.md).

Measure files from the command line:

```bash
python3 skills/token-budget/scripts/estimate_tokens.py notes.md src/*.py --budget 20000
```

## The five habits these skills teach

1. **Say what you want, not what to do first.** State the goal and what "done" looks like.
2. **Give the context only you have.** The model cannot know your audience, data or constraints.
3. **Define the output.** Format, length and what to leave out.
4. **Cut the filler.** Politeness and repetition cost tokens and change nothing.
5. **Allow "I don't know".** Grounded, honest answers beat confident guesses.

## Contributing

New skills are welcome. Each skill is a folder in `skills/` with a `SKILL.md` (frontmatter `name` and `description`, then instructions). Keep skills short — they cost tokens every time they load.

Run the tests:

```bash
python3 -m unittest discover tests
```

## License

MIT
