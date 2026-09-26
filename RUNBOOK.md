# RUNBOOK — AI NEWS FACTORY

## Phase 1 — Safe dry run

Prompt Orchestrator:

`Initialize AI NEWS FACTORY. Read the constitution, style bible, config and schemas. Validate the project. Do not search yet.`

Then:

`Run a 24-hour AI news discovery sweep. Find 10 candidates, verify source dates, score them, and write NEWS_CANDIDATES.json. Do not script or publish.`

## Phase 2 — One story

`Take the strongest verified candidate. Run the complete pipeline through QA, but stop before publishing.`

Expected artifacts:
- data/inbox/NEWS_CANDIDATES.json
- data/verified/VERIFIED_NEWS_<id>.json
- data/scripts/SCRIPT_<id>.json
- data/visuals/VISUAL_PLAN_<id>.json
- data/qa/QA_REPORT_<id>.json

## Phase 3 — Production integration

Add:
- image generation;
- video generation;
- TTS;
- FFmpeg;
- YouTube OAuth;
- analytics.

Each integration should be behind an adapter.

## Phase 4 — Scheduling

Use Antigravity Scheduled Tasks for discovery once the dry run is reliable. Antigravity supports recurring scheduled tasks and cron-style prompts. Keep publication disabled until QA has demonstrated stable results.

Suggested schedule for Vietnam:
- 07:30 — morning sweep
- 12:30 — midday sweep
- 18:30 — evening sweep
- 21:30 — optional second-pass sweep

Do not automatically publish all four. Let scoring select the best 1–3 stories.

## Phase 5 — Learning loop

After publishing, collect:
- views
- average percentage viewed
- retention curve
- likes
- comments
- subscribers gained
- shares

Use analytics to improve hooks and story structure, not to distort facts.
