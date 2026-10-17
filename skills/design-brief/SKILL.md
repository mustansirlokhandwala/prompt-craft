---
name: design-brief
description: Gives people without design training professional-looking results. It turns "make it look good" into a concrete design brief (direction, colors, fonts, layout, imagery), then checks the result against a quality checklist. Use whenever the user asks for anything visual — a website, landing page, app screen, slide deck, poster, social post, logo, banner, newsletter, resume or document layout — or says the design looks bad, amateur, generic or "AI-made", or that they aren't good at design.
---

# Design Brief

Most bad AI-made design comes from a vague request, not a weak model. Don't make the user design: offer choices they can react to, then turn their pick into exact specs.

## Step 1: Pin the basics

Fill these from context. Ask only for what you can't infer, in one message:

- **What and where:** the medium and size (landing page, 16:9 slides, 1080×1350 Instagram post, A4 PDF).
- **For whom:** the audience, and the one thing it should make them do or feel.
- **Content:** the real text, data and images. If there are none yet, use the `idea-shaper` skill first, or write real draft copy. Never use lorem ipsum.
- **Must-haves:** existing brand colors, logo, fonts, or examples the user likes.

## Step 2: Offer 3 directions and recommend one

Give 3 short, named directions that suit the audience. Each gets one line on its feel and one line on its colors and type. Recommend one. For example:

> **A. Calm editorial** — spacious, serious, trustworthy. Off-white, ink black, one muted accent; a serif heading font with a clean sans for body text.
> **B. Bold product** — confident, modern, punchy. High contrast, one saturated accent; a heavy grotesque font, large headings.
> **C. Warm and human** — friendly, approachable. Soft warm neutrals, earthy accent; a rounded sans, generous corners.
> I'd pick **A**, because your audience is <reason>.

The user picks a letter, mixes them ("A with C's colors"), or says "you choose".

## Step 3: Turn the direction into specs

| Element | Spec rule |
|---|---|
| Palette | 1 background, 1 text color, 1 accent, 1–2 neutrals. Give hex values and the role of each. Body text must reach 4.5:1 contrast with its background. |
| Typography | At most 2 font families, from Google Fonts or system fonts. A size scale such as 14 / 16 / 20 / 28 / 40 / 56. Body text 16px or larger on screen. |
| Layout | One grid (12 columns for web, a 3×3 grid for posters). One spacing unit: 8px and multiples of it. |
| Hierarchy | One focal point per screen or slide. The reading order is obvious: heading → key message → action. |
| Imagery | One style only: photos, flat illustration, 3D or icons. Say where images come from. |
| Copy tone | 2–3 adjectives, and the headline written out. |

## Step 4: Write the brief as a prompt

Output the brief so it can be pasted into Claude, Antigravity or an image tool:

```
Create <deliverable> for <audience>. Goal: <what they should do or feel>.

Direction: <name> — <one-line feel>.
Palette: background <hex>, text <hex>, accent <hex> (buttons and links only), neutrals <hex>, <hex>.
Type: headings <font> <weight>, body <font> <size>; scale <sizes>.
Layout: <grid>, <spacing unit>, generous whitespace; focal point is <element>.
Imagery: <style and source>.
Content: <the real copy, or where it is>.
Avoid: purple-blue gradients, everything in identical cards, centered text everywhere, emoji as bullets, stock-photo clichés, more than 2 fonts.
Must work on: <mobile, print, projector>.
```

If you are building the deliverable yourself, follow the brief directly. Use the `frontend-design` skill for web UI if it is available.

## Step 5: Check before you deliver

Check every item. Fix anything that fails, then deliver:

- [ ] One clear focal point; you can tell what matters in 3 seconds
- [ ] At most 2 fonts and 1 accent color
- [ ] Text contrast at least 4.5:1; nothing important in light grey
- [ ] Everything aligns to the grid; spacing uses the spacing unit
- [ ] Real content, no placeholders; headings say something specific
- [ ] Enough whitespace; nothing crowds the edges
- [ ] Works at the target size (phone width for web, back-of-room for slides)
- [ ] Doesn't look like a template: at least one deliberate, distinctive choice

Tell the user in one line which direction you used, and give them one tweak to try ("For more energy, swap the accent to <hex>").
