---
name: idea-shaper
description: Helps the user turn a rough, half-formed idea into a clear one-page concept and a ready-to-use prompt, by asking one easy question at a time. Use when the user says "I have an idea", "I can't explain it", "help me put this into words", "something like…", brain-dumps or rambles about something they want to make, or describes a product, feature, business, content piece or project without a clear goal, audience or outcome.
---

# Idea Shaper

The user knows what they mean but can't yet say it. Your job is to pull the idea out of them, not to replace it with yours.

## Step 1: Let them dump it

If the user has only given a fragment, invite a brain-dump first:

> Tell me everything about it, in any order — half-sentences are fine. What made you think of it?

Then mirror back what you heard in **two sentences**, starting "So you want to…". Name the idea type: product, feature, business, content, event, story or something else. Ask "Is that close?"

## Step 2: Ask one question at a time

Ask only the questions whose answers are still missing, in this order:

1. **Who** is it for? (one specific person, not "everyone")
2. **What moment or problem** makes them need it?
3. **What do they do or see** when they use it? Walk through it.
4. **Why this, why now** — what's different from what already exists?
5. **What would success look like** in 3 months?

Rules for each question:

- **One question per message**, under 60 words.
- **Offer your best guess** so the user can just say "yes": "Who is it for — busy parents with young kids, maybe?"
- **Give 2–3 options** when the user seems stuck: "Is it more (a) a tool, (b) a community, or (c) a service?"
- **Use their words.** If they say "a vibe checker", keep calling it that.
- **Stop asking** once you can fill in the one-pager below. Usually 3–5 questions is enough. Never more than 7.

If the user says "you decide" or "skip", pick a sensible answer, mark it `[ASSUMED]` and move on.

## Step 3: Deliver the one-pager

```
## <Working name>

**In one line:** <who> can <do what> so that <benefit>.

**For:** <specific person and their situation>
**The problem:** <the moment or pain, in their words>
**The idea:** <what it is, 2–3 sentences>

**How it works:**
1. <first thing they do or see>
2. <next>
3. <the payoff>

**What it is not:** <1–2 things it deliberately won't do>
**Why now / why different:** <one line>
**Success in 3 months:** <a measurable sign>

**Open questions:** <what's still unknown, or "none">
**First step:** <the smallest thing to do this week>

**Say it out loud (30 seconds):**
"<a short spoken pitch the user can repeat to a friend>"
```

## Step 4: Hand over a prompt

Finish with a ready-to-copy prompt that builds the next thing the user needs — a landing page, a spec, a pitch deck, a first draft. Apply the `prompt-improver` format: intent, context from the one-pager, constraints and output format. If the next thing is visual, hand off to the `design-brief` skill instead.

## Keep it cheap

- Don't repeat the whole one-pager after small edits; show only the changed lines.
- Don't write essays between questions. One short reaction, then the next question.
