# AI NEWS VISUAL STYLE BIBLE v1.0

## 0. Creative north star

**Positioning:** AI NEWS + TECH EXPLAINER + VISUAL STORYTELLING.

The channel does not merely announce what happened. It makes the viewer understand **what happened, why it matters, and how the underlying mechanism works** in 20–40 seconds.

### Signature promise

> **“Don't just tell me what AI did. Show me how it works.”**

### Creative reference

The visual grammar may borrow broad, non-proprietary principles seen in modern technical explainers:
- dark technical canvas;
- restrained neon accents;
- large kinetic typography;
- diagrams and system flows;
- UI-like cards;
- evidence screenshots;
- progressive disclosure;
- fast but readable cuts;
- sound effects tied to information events.

Do NOT copy another creator's exact frames, logos, layouts, scripts, phrases, music, or distinctive artwork.

---

# 1. MASTER VIDEO SPEC

Default:
- Aspect ratio: 9:16
- Resolution: 1080x1920 final
- Duration: 20–40 seconds
- Default target: 30 seconds
- FPS: 30
- Voice: clear, confident, conversational
- Music: low, unobtrusive, no copyrighted commercial track
- Captions: burned-in or platform-native; always proofread
- Visual density: one primary idea per shot
- Average shot length: 1.2–2.8 seconds
- Hook appears within first 0.5–1.0 seconds
- Source/evidence visible by ~8–15 seconds when practical
- CTA final 2–3 seconds

---

# 2. THE 30-SECOND RHYTHM

## 0.0–2.0s — HOOK

Goal: create an information gap.

Good patterns:
- “AI just learned to ___.”
- “This changes how AI agents work.”
- “The surprising part isn't the new model.”
- “Most people are missing one detail about this AI release.”
- “Watch what happens after the AI makes a mistake.”

Rules:
- 4–9 spoken words if possible.
- Put the central noun/verb on screen.
- Never promise more than the evidence supports.
- No fake urgency.

Visual:
- one bold object or diagram;
- 2–5 word headline;
- immediate motion.

SFX:
- short impact + subtle whoosh.

## 2.0–6.0s — CONTEXT

Answer: what happened?

Show:
- official announcement screenshot;
- product/model name;
- publication date;
- source badge.

Use a small source chip:
`SOURCE • Google DeepMind • 26 Sep 2026`

## 6.0–14.0s — MECHANISM

This is the signature section.

Turn the abstract idea into a diagram:

`INPUT → MODEL → TOOL → ACTION → RESULT`

or

`PLAN → EXECUTE → TEST → FAIL → REPAIR → PASS`

or

`MODEL → CONTEXT → TOOLS → MEMORY → LOOP`

Animation:
- reveal one node at a time;
- arrows move only when the narration reaches them;
- do not animate everything simultaneously.

## 14.0–23.0s — EVIDENCE + WHY IT MATTERS

Use one strong piece of evidence:
- official screenshot;
- benchmark chart;
- product demo frame;
- research figure;
- quoted fact, paraphrased unless exact quotation is essential.

Then answer:
**“Why should a normal person care?”**

## 23.0–28.0s — BIG INSIGHT

One sentence.

Example:
> “The important shift is from AI that answers to AI that acts.”

Do not add three conclusions.

## 28.0–32.0s — CTA

Examples:
- “Follow for verified AI updates every day.”
- “Follow for the next AI shift, explained visually.”
- “Save this — the agent era is moving fast.”

CTA must never imply a guarantee such as “you'll never miss anything.”

---

# 3. TYPOGRAPHY SYSTEM

Use a modern sans-serif family with strong weights.

Preferred:
1. Inter
2. Manrope
3. Space Grotesk
4. IBM Plex Sans

Hierarchy:
- H1: ExtraBold, 72–110 px equivalent at 1080x1920
- H2: Bold, 46–70 px
- Body: Medium, 34–46 px
- Labels: Medium, 22–30 px
- Source chip: 20–26 px

Rules:
- maximum 7 words in a single large headline;
- maximum 2 text blocks per shot;
- never put essential text close to the bottom 15% where platform UI may cover it;
- highlight only one or two keywords.

---

# 4. COLOR SYSTEM

Base:
- Background: near-black / charcoal
- Primary text: off-white
- Accent A: electric cyan
- Accent B: violet
- Warning: restrained red
- Success: restrained green

Suggested palette:
- BG: #070A0F
- PANEL: #0D121A
- TEXT: #F3F7FA
- MUTED: #8B98A7
- CYAN: #4DEBFF
- VIOLET: #9B7CFF
- RED: #FF5C70
- GREEN: #54E39A

Do not flood the entire video with neon. Neon is a semantic signal.

CYAN = technology / active flow
VIOLET = AI / intelligence
RED = error / risk / contradiction
GREEN = verified / completed

---

# 5. VISUAL GRAMMAR

## A. System diagram

Use for mechanisms.

Example:
`USER → AGENT → TOOL → DATABASE → RESULT`

Animation:
1. node appears;
2. label appears;
3. arrow activates;
4. next node appears.

## B. Layer stack

Use for architecture.

Example:
`MODEL`
`+ TOOLS`
`+ CONTEXT`
`+ MEMORY`
`+ LOOP`
`= AGENT SYSTEM`

## C. Before / after

Use for upgrades.

Example:
`CHATBOT → AGENT`

## D. Failure / recovery loop

Use for agent stories.

`PLAN → ACT → TEST → FAIL → REASON → FIX → PASS`

## E. Benchmark bars

Use only with verified numbers.

Never visually imply that a benchmark measures “overall intelligence.”

Always show:
- benchmark name;
- evaluation condition if known;
- source.

## F. Evidence card

A source screenshot should sit inside a designed frame:
- source domain;
- publication date;
- highlighted relevant line/area;
- no fake UI elements that could be mistaken for the source.

---

# 6. SCREENSHOT POLICY

A screenshot is evidence, not decoration.

Before using it:
1. Identify owner/source.
2. Record URL.
3. Record access/publication date.
4. Determine whether the image is official, user-generated, press/media, or third-party.
5. Prefer official screenshots for product announcements.
6. Crop only what is necessary.
7. Do not alter wording in a way that changes meaning.
8. If rights are unclear, use the screenshot only as a small contextual reference where legally appropriate or replace it with an original diagram/AI-generated visualization.
9. Never fabricate a screenshot of a real product or news site.

Metadata schema:
`source_url`, `source_name`, `published_at`, `captured_at`, `asset_type`, `rights_status`, `attribution_required`.

---

# 7. AI-GENERATED VISUAL POLICY

Generated visuals must be clearly conceptual when they are not literal evidence.

Never generate a fake:
- news screenshot;
- official announcement;
- benchmark result;
- CEO quote;
- product UI that could be mistaken for the real UI.

If visualizing an invisible concept, label it:
`CONCEPTUAL VISUALIZATION`

Preferred visual prompt structure:

SUBJECT
+ ACTION
+ ENVIRONMENT
+ CAMERA
+ LIGHTING
+ MATERIAL
+ MOTION
+ COMPOSITION
+ STYLE
+ NEGATIVE CONSTRAINTS

---

# 8. VEO / FLOW MASTER PROMPT

Use this template for each cinematic shot:

> Vertical 9:16 cinematic technology explainer. A premium dark technical environment, near-black background, subtle volumetric haze, restrained electric-cyan and violet emissive accents, clean high-end documentary aesthetic. [SUBJECT] performs [ACTION]. Visualize the concept clearly rather than creating a fake real-world news event. Camera: [SHOT TYPE], [CAMERA MOTION]. Composition: strong central subject, generous negative space for later captions, clean silhouette, readable visual hierarchy. Lighting: controlled rim light, soft practical glow, realistic reflections, high contrast without crushed shadows. Motion: deliberate, physically plausible, synchronized to narration beats. No logos unless supplied as a verified asset. No fake UI, no fake headlines, no invented numbers, no watermark, no random text, no extra fingers/people, no visual clutter. Premium AI documentary / technical explainer aesthetic, coherent with the channel's dark-cyan-violet visual system.

---

# 9. SHOT TYPES

Use a controlled vocabulary.

1. MACRO_TECH — close-up circuit / chip / interface concept
2. SYSTEM_WIDE — architecture diagram in a spatial environment
3. UI_FLOAT — verified UI screenshot presented as an evidence card
4. DATA_FLOW — moving nodes and arrows
5. HUMAN_SCALE — person interacting with AI system
6. ABSTRACT_AGENT — conceptual agent loop
7. EVIDENCE_SCREEN — source/benchmark/research visual
8. BEFORE_AFTER — old vs new system
9. FAILURE_LOOP — error and recovery
10. CTA_LOCKUP — final branded composition

---

# 10. MOTION LANGUAGE

Default easing:
- fast ease-out for entrances;
- smooth ease-in-out for system flows;
- micro-bounce only for UI confirmation;
- no constant zooming.

Transitions:
- hard cut for new facts;
- 150–250ms digital wipe for related concepts;
- 250–450ms morph only when two visual states are logically connected;
- glitch only for actual error/security themes.

Avoid:
- excessive camera shake;
- random glitch;
- template-like spins;
- overused whoosh on every cut.

---

# 11. SFX LANGUAGE

VOICE = primary information channel.

SFX = information punctuation.

Use:
- impact: hook / major reveal
- tick: data point / node activation
- soft click: UI selection
- whoosh: scene transition
- low glitch: error or contradiction
- subtle confirmation: verified result

Mixing:
- voice clearly above music/SFX;
- music should support, never compete;
- no dramatic sound that changes the perceived seriousness of a factual news story.

---

# 12. NEWS STORY FORMULAS

## Formula A — New model

HOOK
→ WHAT CHANGED
→ CAPABILITY
→ EVIDENCE
→ WHY IT MATTERS
→ CTA

## Formula B — AI agent

HOOK
→ WHAT THE AGENT DID
→ SHOW THE LOOP
→ EVIDENCE
→ LIMITATION
→ CTA

## Formula C — Research breakthrough

HOOK
→ CLAIM
→ METHOD
→ RESULT
→ LIMITATION
→ WHY IT MATTERS
→ CTA

## Formula D — Product launch

HOOK
→ PRODUCT
→ FEATURE
→ REAL USE CASE
→ WHO IT AFFECTS
→ SOURCE
→ CTA

## Formula E — Controversy / conflict

HOOK
→ WHAT EACH SIDE CLAIMS
→ WHAT IS VERIFIED
→ WHAT IS UNKNOWN
→ WHY IT MATTERS
→ CTA

Never present disputed claims as settled facts.

---

# 13. RETENTION RULES

Every 2–4 seconds, introduce at least one:
- new visual state;
- new fact;
- new diagram node;
- new question;
- evidence;
- contrast.

But do not change visuals merely to create noise.

The viewer should always understand:
**Where are we? What are we learning? Why is the next second useful?**

---

# 14. CTA SYSTEM

Rotate among:
- `FOLLOW • AI explained visually`
- `FOLLOW • verified AI updates`
- `SAVE • you'll want this later`
- `FOLLOW • the next AI shift is coming`

Do not use:
- “Subscribe or you'll miss out forever”
- fake scarcity;
- fear-based claims;
- misleading “breaking” labels.

---

# 15. BRAND LOCKUP

Final frame:
- channel name/logo;
- one-line promise;
- follow/subscribe cue.

Example:
`AI NEWS LAB`
`AI — VERIFIED. EXPLAINED. VISUALIZED.`

Keep final lockup under 2.5 seconds.

---

# 16. QUALITY SCORE

Before render, calculate:

- Freshness: 0–10
- Source quality: 0–10
- Evidence strength: 0–10
- Information value: 0–10
- Visual explainability: 0–10
- Hook clarity: 0–10
- Originality of presentation: 0–10
- Safety/copyright confidence: 0–10

Minimum production threshold:
`weighted_score >= 8.0`

Mandatory hard gates:
- source verified;
- no material unsupported claim;
- visual plan contains no fabricated evidence;
- CTA present;
- source attribution captured.

---

# 17. THE GOLDEN RULE

**If the story cannot be explained visually, the agent must redesign the story — not compensate with more text.**

The visual system is the teacher.

The voice is the guide.

The source is the authority.

The AI model is the worker.

The QA agent is the gatekeeper.
