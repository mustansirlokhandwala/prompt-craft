# prompt-craft

Skills for working smarter with AI in Claude Code, Claude.ai and Antigravity. Fix weak prompts, budget tokens, shape rough ideas, design well without design skills, write clear replies, test real use cases and check market fit before you build.

| Skill | What it does |
|---|---|
| [`prompt-improver`](skills/prompt-improver/SKILL.md) | Finds the real intent, fills the missing pieces, rewrites the prompt for accuracy and efficiency, and explains each change so you learn. |
| [`token-budget`](skills/token-budget/SKILL.md) | Estimates tokens in and out, warns before a task goes over budget, and suggests cheaper ways to get the same result. |
| [`idea-shaper`](skills/idea-shaper/SKILL.md) | Turns a rough idea you can't quite explain into a one-page concept and a ready-to-use prompt, one easy question at a time. |
| [`design-brief`](skills/design-brief/SKILL.md) | Professional-looking results without design skills: offers 3 directions, turns your pick into exact colors, fonts and layout, then checks the result. |
| [`clear-writer`](skills/clear-writer/SKILL.md) | Turns rough notes or broken English into a short, direct reply that sounds human, not like AI. |
| [`market-fit-check`](skills/market-fit-check/SKILL.md) | Before you build: finds what already exists and how to stand out, sizes who would use it, and checks whether you're solving for the 80% or the 20%. Ends with a build / rethink verdict, with sources. **Runs only when you ask for it.** |
| [`usecase-tests`](skills/usecase-tests/SKILL.md) | Before code is submitted: writes tests from what the code should do (not what it does), breaks the code on purpose to prove the tests catch bugs, and reports coverage. |

## Install

**One command for Claude Code and Antigravity** (macOS and Linux):

```bash
curl -fsSL https://raw.githubusercontent.com/mustansirlokhandwala/prompt-craft/main/install.sh | bash
```

It sets up every tool it finds:
- links the skills into `~/.claude/skills/` and Antigravity's skills folder;
- adds the always-on rules to `~/.claude/CLAUDE.md` and `~/.gemini/GEMINI.md`, inside a marked block, without touching anything else in those files (it backs each file up once first);
- never replaces a skill of yours that has the same name.

Run the same command again to update. To set up only one tool, add `-s -- --claude` or `-s -- --antigravity` to the end of the command.

**Uninstall:**

```bash
curl -fsSL https://raw.githubusercontent.com/mustansirlokhandwala/prompt-craft/main/install.sh | bash -s -- --uninstall
```

This removes only what the installer added. Your own skills and instructions stay.

If you've cloned the repo, run `./install.sh` or `./install.sh --uninstall` from it instead. The installed skills then link to your clone, so a `git pull` updates them.

**Claude Code plugin:** use this instead of the installer, not as well as it, or the rules load twice.

```bash
claude plugin marketplace add mustansirlokhandwala/prompt-craft
```

```bash
claude plugin install prompt-craft@prompt-craft
```

**Claude.ai:** zip a skill folder (for example `skills/prompt-improver`) and upload it under Settings → Capabilities → Skills.

**Windows:** the installer doesn't support Windows yet. Use the plugin, or follow the manual steps in [docs/always-on.md](docs/always-on.md).

## Use

Just ask:

- "Improve this prompt: *write me a blog post about AI*"
- "/prompt-improver can u fix my code its broken"
- "How many tokens will this take?" (with files attached)
- "I have an idea for an app but I can't explain it"
- "Make me a landing page for my bakery" or "my slides look amateur"
- "/market-fit-check an app for splitting rent between roommates"
- "Reply to this client: sorry we're late, can deliver Thursday"

The token-budget skill also warns on its own when you paste a lot of text or start a big multi-step task.

## Always on

Skills load only when a request matches them. To apply prompt-craft to **every** prompt, load the short rules in [`rules/always-on.md`](rules/always-on.md) (~300 tokens) into the agent's standing context:

- **Installer:** automatic, for both Claude Code and Antigravity.
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

Run the tests (the installer tests use a temporary home folder and never touch your real setup):

```bash
python3 -m unittest discover tests
```

With coverage (needs `pip install coverage`):

```bash
coverage run --branch -m unittest discover tests && coverage report -m
```

## Before you use it

- **Token counts are estimates.** Characters ÷ 4 is within about 20% for English text and code. Other languages can use 2–4× more tokens, especially Chinese, Japanese and Korean. Don't use these numbers for billing.
- **The thresholds are defaults, not your plan's limits.** Prices and limits differ by model and plan. Edit rule 4 in [`rules/always-on.md`](rules/always-on.md) to match yours.
- **The plugin runs a shell hook.** It only prints the rules file. Read [`hooks/hooks.json`](hooks/hooks.json) before installing, as you should with any plugin.
- **Always-on costs about 300 tokens per session.** That's the price of the rules staying in context.
- **Review rewritten prompts.** Guesses marked `[ASSUMED]` may be wrong. Never put passwords, keys or private data into prompts.
- **Requirements.** The estimator needs Python 3. It only reads files locally and sends nothing anywhere. On Windows, the hook runs through Git Bash, which Claude Code uses there. Antigravity folder paths vary between versions.

## License

MIT. Provided as-is, without warranty.

Not affiliated with or endorsed by Anthropic or Google. Claude, Antigravity and Gemini are trademarks of their respective owners.
