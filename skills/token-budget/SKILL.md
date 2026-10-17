---
name: token-budget
description: Estimates how many tokens a prompt or task will use, warns before it exceeds the expected budget, and suggests cheaper ways to get the same result. Use when the user asks about tokens, cost, usage, context size or "how expensive is this", when they paste or attach a large amount of text or many files, before a long multi-step or agentic task, or when the prompt-improver skill flags an expensive task.
---

# Token Budget

Help the user spend tokens on purpose. Warn **before** the expensive work starts, not after.

## Step 1: Measure

Estimate input tokens:

- For text in the conversation: characters ÷ 4 (English prose and code; roughly 0.75 words per token).
- For files: run `python3 scripts/estimate_tokens.py <files...>` from this skill's folder. Add `--budget N` to compare against a limit.
- For exact counts, the Claude API offers a token-counting endpoint; the estimate is enough for warnings.

Estimate output tokens from what the prompt asks for:

| Requested output | Rough output tokens |
|---|---|
| One-line answer, yes/no, a value | 10–50 |
| A paragraph or short list | 100–300 |
| An email, a function, a summary page | 300–1,000 |
| A full document, a multi-file change | 1,000–5,000+ |
| Agentic task (reads files, runs tools, iterates) | every step re-sends the whole conversation: multiply input by the number of steps |

## Step 2: Compare with the budget

Use the user's stated budget if they gave one. Otherwise use these defaults:

| Level | Single prompt (in + out) | Multi-step task (total) |
|---|---|---|
| Normal | under 10k | under 100k |
| **Warn** | 10k–50k | 100k–500k |
| **Stop and ask** | over 50k | over 500k |

At **Warn**: tell the user the estimate in one line, then continue.
At **Stop and ask**: give the estimate and the top savings, then ask whether to proceed before doing the work.

Output the warning like this:

```
⚠️ Token estimate: ~<in>k in + ~<out>k out ≈ <total>k (<level>).
Biggest cost: <what drives it>.
Cheaper option: <one concrete change> → ~<new total>k.
```

## Step 3: Suggest savings (biggest first)

Pick only the ones that apply:

1. **Send less context.** Only the relevant function, section or rows — not the whole file, document or dataset.
2. **Ask for less output.** "Return only the diff", "top 5", "under 200 words", "no explanation".
3. **Don't repeat yourself.** Refer to earlier text instead of re-pasting it; start a fresh conversation when the old context is no longer needed.
4. **Batch questions.** One prompt with three questions costs less than three prompts that each re-send the context.
5. **Keep the stable part first.** Fixed instructions and reference docs at the top let prompt caching reuse them cheaply.
6. **Right-size the model.** Simple extraction, formatting or classification rarely needs the largest model.
7. **Summarize, then work.** For huge inputs, summarize once and work from the summary.

## Rules

- Never cut context the task needs to be correct. A cheap wrong answer that needs a retry costs more than the right one.
- Give numbers, not adjectives: "~42k tokens", not "quite large".
- Keep the warning to three lines. The point is to save tokens, including your own.
