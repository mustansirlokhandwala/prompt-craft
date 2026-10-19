# Contributing

Thanks for helping. Every change goes through a pull request, and the maintainer reviews each one before it merges.

## Steps

1. Fork the repo and create a branch: `git checkout -b add-<skill-name>` or `fix-<what>`.
2. Make one change per pull request: one new skill, or one fix.
3. Run the tests: `python3 -m unittest discover tests`. They also run on Linux and macOS when you open the pull request.
4. Commit and push to your fork, then open a pull request and fill in the checklist.

## Adding a skill

- Make a folder `skills/<skill-name>/` with a `SKILL.md`. The folder name uses lowercase letters, numbers and hyphens.
- Start `SKILL.md` with frontmatter: `name` (same as the folder) and `description` (what it does and when to use it, under 1,024 characters).
- Keep it short. Every description loads in every session, and the full skill loads each time it's used. Measure it with `python3 skills/token-budget/scripts/estimate_tokens.py skills/<skill-name>/SKILL.md`.
- Add a before/after example to the pull request, so the reviewer can see it work.
- If the skill comes with a script, add tests for it in `tests/`.

## Commit messages

- One line, under 72 characters, starting with a verb: `Add idea-shaper skill`, `Fix uninstall removing linked skills`.
- If the reason isn't obvious, add a blank line and a short paragraph explaining why.

## What gets merged

- It solves a real problem for people using AI tools, and doesn't copy a skill that's already here.
- The tests pass.
- The writing is plain and short. No filler, no hype.
