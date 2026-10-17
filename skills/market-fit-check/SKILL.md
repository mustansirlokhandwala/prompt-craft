---
name: market-fit-check
description: Checks whether a product, app, feature or component is worth building before any code is written. Market research finds what already exists, the gaps and how to stand out. Data finds who would use it, how many there are, the impact, and whether it serves the 80% or only the 20%. Run only when the user explicitly asks for it — by name (/market-fit-check), or by asking for a market-fit check, market research or data validation of an idea. Never start it on your own just because the user is building something; it is slow and costs many tokens.
disable-model-invocation: true
---

# Market Fit Check

Answer one question with evidence: **should this be built, and in what form?** Every claim needs a source or a clearly labeled estimate. A confident guess here costs months later.

## Step 0: Pin the idea and the scope

- Write the idea in one line: "<who> can <do what> so that <benefit>". If you can't, use the `idea-shaper` skill first.
- Choose a depth and tell the user what it will cost before starting:
  - **Quick scan**: about 10 searches, the top 5 competitors and rough numbers. Usually 30–60k tokens.
  - **Deep dive**: 25+ searches, reading reviews and sizing each user group. Usually 150k+ tokens. Ask the user before starting one.
- If the user only gave the idea, run a quick scan. If web search isn't available, say so: work only from what the user provides and mark everything else as unverified.

## Part A: Market research

### A1. Find everything that already solves this

Search for three kinds of alternative:

| Kind | Examples | Where to look |
|---|---|---|
| Direct | Products built for exactly this job | Product Hunt, G2, Capterra, app stores, GitHub, Google |
| Indirect | Spreadsheets, Notion templates, agencies, manual workarounds, "do nothing" | Reddit, Hacker News, forums, YouTube tutorials |
| Platform risk | A feature inside a big product that could do this tomorrow | The big players' docs, changelogs and roadmaps |

The workaround people use today is your real competitor, even when no product exists.

### A2. Compare the competitors

| Name | What it does | For whom | Price | Strength | Top complaint | Source |
|---|---|---|---|---|---|---|

Take the "top complaint" column from 1–3 star reviews, Reddit threads and GitHub issues, not from the competitors' marketing.

### A3. Find the gaps

Look for patterns across the complaints:

- **Underserved group**: a user group everyone ignores, such as a profession, country, language, budget or skill level
- **Missing job**: a step in the workflow nobody covers
- **Price gap**: everything is too expensive or too limited for a group
- **Experience gap**: everything is powerful but hard to use, or simple but limited
- **Platform gap**: a device, tool or integration nobody supports

### A4. Decide how to stand out

Fill this in:

> For **<specific user>** who **<need or pain>**, **<product>** is a **<category>** that **<key benefit>**. Unlike **<main alternative>**, it **<the one difference that matters>**.

If the space is crowded, pick **one** way to be different and commit to it: a narrower audience, a specific job, deep integration, price, ease of use, or trust (privacy, local data, open source). "Better, cheaper and easier" is not a position.

## Part B: Data

### B1. Who would use it?

List 2–4 user groups. For each one:

| Group | Description | How many (estimate + method) | Pain level (1–5) | Can they pay? | Where they gather |
|---|---|---|---|---|---|

Size each group both ways, and show the math:

- **Top-down**: total market from a cited source × the share that matches your user.
- **Bottom-up**: number of reachable target users × likely adoption × how often they'd use it.

If the two estimates disagree by more than 10×, say so and explain which one you trust.

### B2. Is there real demand?

Collect signals and cite each one:

- Search interest and its trend (Google Trends, keyword tools)
- People asking for it or complaining about it (Reddit, forums, X, support communities), with links
- Competitors' traction: users, revenue, funding, growth
- Money already spent on workarounds: freelancers, agencies, paid templates
- Job posts or tools that show the task is done often

Label each signal **strong**, **weak** or **none found**. "None found" is useful data too.

### B3. How much impact?

- **For one user**: time or money saved, or the outcome gained, × how often. For example: "Saves 2 hours a week for a freelance designer, about 100 hours a year."
- **In total**: impact per user × realistic users in year one.

### B4. The 80% or the 20%?

List the main use cases and estimate the share of target users who need each one, with evidence:

| Use case | Share of target users who need it | Evidence |
|---|---|---|

- **The core** is the smallest set of use cases that covers about 80% of users. Build that first.
- A use case needed by fewer than 20% of users is an edge case. Leave it out of version 1, unless that 20% is your deliberate niche **and** they feel the pain strongly **and** they will pay. Say clearly which situation this is.

### B5. The riskiest assumption

Name the one assumption that would kill the idea if it were wrong. Then give the cheapest test for it, with a pass mark set in advance. For example: "a landing page plus a $50 ad to the target group; it passes at 5% or more email sign-ups." Other cheap tests: 5 user interviews, a survey, a fake-door button, a manual concierge version.

## Step 3: Report

Lead with the verdict:

```
## Verdict: <Build it / Build it with a twist / Rethink it / Don't build it> — confidence: <high/medium/low>
<2–3 sentences: why, and the twist or the change if there is one>

**Position:** <the positioning statement>
**Core (the 80%):** <use cases for version 1>
**Leave out for now (the 20%):** <use cases>
**Riskiest assumption → test:** <assumption> → <test and pass mark>

<the A2 competitor table, the B1 user groups table, the B4 use cases table>

**Sources:** <numbered list of links, each with the date it was published or accessed>
```

## Rules

- **Never invent a number, a competitor or a quote.** Every figure has a source link or is labeled `[ESTIMATE: <method>]`.
- Keep facts (what a source says) separate from inference (what you conclude). Mark the inferences.
- Prefer sources from the last 2 years and say when a source is older.
- Say when the data is thin, and say what research would settle it.
- A "don't build it" or "it already exists" verdict is a good result. It saved the user time. Say it plainly, then suggest the nearest gap worth building for.
- After the verdict, offer the next step: a product spec, or a prompt for the first build using the `prompt-improver` format.
