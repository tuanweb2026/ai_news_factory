# AI NEWS FACTORY v1.0 — START HERE

## Mission

Build a 5-agent AI news Shorts factory:

1. NEWS HUNTER — finds fresh AI news.
2. FACT CHECKER — verifies claims and sources.
3. EDITORIAL STORYTELLER — converts verified facts into a 20–40s short.
4. VISUAL STORYTELLER — converts the story into a consistent visual language inspired by modern AI-tech explainers, without copying another creator.
5. QA + PUBLISHER — red-teams the package, validates quality, then prepares/publishes to YouTube when the required credentials/integration are configured.

An ORCHESTRATOR is the manager. It is not counted as a content agent.

## Core principle

Agents do NOT pass casual chat as the source of truth.

They pass versioned artifacts:

NEWS_CANDIDATES.json
→ VERIFIED_NEWS.json
→ SCRIPT.json
→ VISUAL_PLAN.json
→ RENDER_MANIFEST.json
→ QA_REPORT.json
→ PUBLISH_RECORD.json

Every artifact has:
- id
- version
- status
- timestamps
- source references
- confidence
- next_action

## Safety / quality gates

Never publish when:
- a material factual claim has no source;
- the date is unclear for a "latest" claim;
- a source is only a social post and no reliable corroboration exists;
- the visual implies facts not supported by the source;
- copyright/license status of third-party media is unknown;
- the video contains an unverified number, quote, benchmark, or superlative;
- QA status is not PASS.

For fast-moving news, prefer primary sources and at least one independent reputable source. If sources conflict, preserve the conflict and escalate instead of inventing a resolution.

## Recommended first run

In Antigravity 2.0:
1. Open this folder as a Project.
2. Open the Agent panel.
3. Use the Orchestrator as the main agent.
4. Ask it: `Initialize AI NEWS FACTORY and validate every file in the project. Do not publish anything.`
5. Then ask: `Run a dry-run news sweep for the last 24 hours. Produce candidates only.`
6. Review the artifacts.
7. Then run: `Run one complete dry-run for the strongest candidate. Stop before external publishing.`
8. Only after QA is consistently PASS should you connect publishing credentials/MCP.

## Current implementation boundary

This repository defines the agents, rules, schemas, visual style, scoring and workflow.

External production services such as YouTube OAuth, image/video generation, TTS and optional MCP servers require credentials or integrations that are intentionally not hard-coded here.

Do not place API keys in Markdown, JSON, Git, prompts or source files. Use the platform's secret/credential mechanism or environment variables.
