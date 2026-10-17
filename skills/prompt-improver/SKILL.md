---
name: prompt-improver
description: Turns a weak or vague prompt into a clear, complete, token-efficient one, and explains what changed so the user learns. Use when the user asks to improve, rewrite, fix, tighten or review a prompt, pastes a prompt for feedback, says "make this prompt better", or invokes /prompt-improver. Also use when the user is writing a system prompt, agent instructions or a reusable template.
---

# Prompt Improver

Rewrite the user's prompt so a model gets it right on the first try, with the fewest tokens in and out. Teach as you go: the user should write the next prompt better without you.

## Step 1: Find the intent

Before changing a word, answer these for yourself:

- **Goal**: what does the user actually want to happen? (Not what they typed — what they need.)
- **Deliverable**: what artifact comes back? (code, list, email, decision, table)
- **Audience**: who reads the output?
- **Done**: how would the user judge the answer good?

Write the intent as one sentence. If you cannot, the prompt is ambiguous: go to Step 3.

## Step 2: Find the missing pieces

Check the prompt against this list. Each missing item is a reason the model will guess.

| Piece | Ask yourself |
|---|---|
| Context | What background does the model need that only the user knows? |
| Task | Is there one clear action verb? ("summarize", "compare", "fix") |
| Inputs | Is the data, code or text the model must use included or referenced? |
| Constraints | Length, tone, tools, libraries, things to avoid? |
| Output format | Shape of the answer: bullets, JSON schema, table, code only? |
| Success criteria | What makes the answer correct or complete? |
| Examples | Would one input→output example remove ambiguity? |

## Step 3: Fill the gaps

- Infer what you safely can from the prompt, the conversation and common sense. Mark each inference in the rewrite as `[ASSUMED: ...]` so the user can correct it.
- Ask only about gaps that would change the answer and that you cannot infer. Maximum 3 questions, each with a suggested default. If nothing blocks you, do not ask — deliver.
- Never invent facts, data or numbers the user must supply. Leave a clear placeholder: `{{paste the error log here}}`.

## Step 4: Make it efficient

Every token in the prompt is paid for on every call, and every vague request invites a long answer.

- Cut filler: greetings, "please", "I was wondering if", repeated instructions, hedging.
- State the output size: "in 5 bullets", "under 150 words", "code only, no explanation".
- Ask only for what is needed: "return the changed function" beats "return the whole file".
- Put stable context (role, rules, reference docs) first and the changing request last — this lets prompt caching reuse the prefix.
- Split one giant prompt into steps only when the steps genuinely depend on each other's output.
- Prefer a reference over a paste: "the attached file" or a path, not the same text twice.

## Step 5: Make it accurate

- Ground the model: "Use only the text below. If the answer is not in it, say so."
- Allow uncertainty: "If you are unsure, say which part and why."
- Define vague words: "short" → "under 100 words"; "best" → "fastest at runtime".
- For reasoning tasks, ask the model to think through the steps before the final answer.
- For structured output, give the exact schema or a filled example.
- Use clear sections (headings or XML-style tags like `<context>`, `<task>`, `<format>`) when the prompt mixes instructions with data.

## Step 6: Respond in this format

Keep your whole reply short. Do not repeat the original prompt back.

```
**Intent:** <one sentence>

**Improved prompt:**
<the rewritten prompt in a fenced block, ready to copy>

**What changed (and why):**
- <change> — <the problem it prevents>   (3 to 5 bullets, most important first)

**Assumptions:** <list of [ASSUMED] items, or "none">

**Score:** before X/10 → after Y/10 · est. prompt tokens: before ~A → after ~B
```

Score on: clear intent, enough context, specific constraints, defined output, no waste (2 points each).

Estimate tokens as characters ÷ 4. If the rewrite is longer than the original, say why the extra tokens pay for themselves (fewer retries, shorter answers). If the task the prompt describes will be expensive to run, hand off to the `token-budget` skill's warning.

## Example

**Original:** `can you help me write something for my team about the new deploy process thanks`

**Intent:** Announce the new deploy process to the engineering team so they can follow it from Monday.

**Improved prompt:**
```
Write a Slack announcement to my engineering team about our new deploy process.

Context: {{list the 3–5 key changes in the process}}
Audience: engineers who deploy weekly. [ASSUMED]
Starts: Monday. [ASSUMED]

Format:
- One-line summary at the top
- A numbered list of the steps that changed
- One line on where to ask questions
- Under 150 words, friendly but direct, no emojis
```

**What changed (and why):**
- Named the channel and audience — sets tone and length.
- Added a placeholder for the actual changes — the model cannot know them and would invent them.
- Fixed the format and length — prevents a 600-word essay.
- Removed "can you help me" and "thanks" — no effect on output, costs tokens.

**Assumptions:** audience deploys weekly; starts Monday.

**Score:** before 2/10 → after 9/10 · est. prompt tokens: before ~20 → after ~85 (the extra context replaces at least one retry).
