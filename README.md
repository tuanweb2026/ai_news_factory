# AI NEWS FACTORY v2 — Supervised Autopilot

A production-grade, multi-agent autonomous studio designed for Google Antigravity 2.0 to discover, triangulate, script, visualize, render, and publish high-retention technical AI news Shorts (1080x1920 @ 30fps) with strict factual verification.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Factory Status](https://img.shields.io/badge/Factory-SUPERVISED__AUTOPILOT-cyan.svg)](RUNBOOK.md)
[![QA Gates](https://img.shields.io/badge/13--Gate%20Red--Team-PASSED-brightgreen.svg)](schemas/qa_report.schema.json)

---

## ⚡ Key Highlights & Core Capabilities

- **Zero-Hallucination Triangulation**: Primary-source validation against official tech press and whitepapers. Never converts speculation or benchmarks into established fact.
- **Supervised Autopilot v2**: Fully automated pipeline transition:
  $$\text{Discovery} \rightarrow \text{Deduplication} \rightarrow \text{Candidate Selection} \rightarrow \text{Fact Check} \rightarrow \text{Scripting} \rightarrow \text{Visuals} \rightarrow \text{Audio} \rightarrow \text{Render} \rightarrow \text{Red-Team QA} \rightarrow \text{Human Review}$$
- **1080x1920 Vertical Render Engine**:
  - Procedural vector rendering (Apple CoreGraphics / SVG).
  - Subtle Ken Burns motion keyframing ($1.00 \times \rightarrow 1.06 \times$).
  - Dual-track sound design: calibrated TTS voiceover (Samantha / Linh) + ducked ambient tech drone bed (-24 dB).
  - Broadcast-compliant audio normalization: integrated loudness **-16.0 LUFS** (EBU R128), true peak **$\le -1.5$ dBTP**.
  - Embedded container timed subtitles (`mov_text` track) + external SRT/ASS tracks.
- **Resumable YouTube Data API v3**: Multi-chunk (8MB) upload bridge with channel identity verification and zero duplicate posting.

---

## 🏗️ Multi-Agent Architecture

```
                       ┌────────────────────────────────────────┐
                       │       SUPERVISED AUTOPILOT             │
                       │           ORCHESTRATOR                 │
                       └──────────────────┬─────────────────────┘
                                          │
       ┌──────────────────┬───────────────┴───────────────┬──────────────────┐
       ▼                  ▼                               ▼                  ▼
┌──────────────┐   ┌──────────────┐                ┌──────────────┐   ┌──────────────┐
│ NEWS HUNTER  │   │ FACT CHECKER │                │  EDITORIAL   │   │    VISUAL    │
│  Discovery   │──▶│ Triangulate  │───────────────▶│ STORYTELLER  │──▶│ STORYTELLER  │
│  Sweep (24h) │   │ Primary Docs │                │ Script (30s) │   │ Blueprint/SVG│
└──────────────┘   └──────────────┘                └──────────────┘   └──────────────┘
                                                                             │
                                                                             ▼
                                                                      ┌──────────────┐
                                                                      │ QA PUBLISHER │
                                                                      │ 13-Gate Audit│
                                                                      │ Gate Control │
                                                                      └──────────────┘
```

| Agent Role | Subagent Identity | Mission & Guardrails |
|:---|:---|:---|
| **Orchestrator** | `src/orchestrator.py` | State-machine controller managing transitions, candidate scoring, and policy precedence. |
| **News Hunter** | `news-hunter-agent` | Sweeps 24h frontier AI breakthroughs; filters clickbait; produces `NEWS_CANDIDATES.json`. |
| **Fact Checker** | `fact-checker-agent` | Verifies claims, timelines, numbers, and negative boundaries; produces `VERIFIED_NEWS.json`. |
| **Editorial Storyteller** | `editorial-storyteller-agent` | Authors punchy 30s scripts with instant $\le 2.0$s cognitive hooks; produces `SCRIPT.json`. |
| **Visual Storyteller** | `visual-storyteller-agent` | Generates dark technical visual systems (`#070A0F`), diagrams, and `VISUAL_PLAN.json`. |
| **QA + Publisher** | `qa-publisher-agent` | Hostile 13-gate adversarial red-team audit; controls local staging and controlled release. |

---

## 🎬 Published Shorts Case Studies

All videos are generated from scratch and verified under strict negative scientific boundaries:

### 1. Short #3 — Stanford & NVIDIA CLM-8B
- **Title**: *AI Agents Are Too Slow — Stanford & NVIDIA Just Fixed It*
- **YouTube Live**: [https://www.youtube.com/shorts/vsD3XGMhWvM](https://www.youtube.com/shorts/vsD3XGMhWvM)
- **Key Breakthrough**: Contrastive Language Model (CLM-8B) replaces token-by-token generation with vector state-action scoring, accelerating agent execution 9x.

### 2. Short #2 — Anthropic Claude ART Enzyme Discovery
- **Title**: *AI Discovers New CRISPR-Like Biology*
- **YouTube Live**: [https://www.youtube.com/shorts/1PhJ53ZexCU](https://www.youtube.com/shorts/1PhJ53ZexCU)
- **Key Breakthrough**: 1,000 Claude agents scanned 1.9B protein clusters in ~21h to find the ART enzyme system in phages. Wet-lab verified (Not human gene editing).

### 3. Short #1 — Google Project Suncatcher
- **Topic**: *Testing AI TPUs and Orbital Solar Data Centers in Space*
- **Artifacts**: Full 9-shot technical storyboard, vacuum thermal dissipation diagrams, and SpaceX Transporter-18 launch verification package.

---

## 🚀 Quickstart & Usage

### 1. Prerequisites
- Python 3.9+
- FFmpeg (with `videotoolbox` on macOS or `libx264`)
- macOS `say` TTS engine or external voice synthesis
- Apple `sips` (for CoreGraphics vector rasterization)

### 2. Installation
```bash
git clone https://github.com/tuanweb2026/ai_news_factory.git
cd ai_news_factory
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Validate Factory Integrity
```bash
python3 src/validate_artifacts.py
pytest tests/
```

### 4. Run Modular Video Render
```bash
# Dry run inspection and safety gate audit
python3 -m src.render.render_pipeline \
  --story-id stanford-nvidia-clm-8b-agent-model-2026 \
  --dry-run

# Full high-resolution 1080x1920 render
python3 -m src.render.render_pipeline \
  --story-id stanford-nvidia-clm-8b-agent-model-2026 \
  --render
```

---

## 🔒 Security & Publishing Protocol

1. **Zero Hardcoded Secrets**: No API keys, OAuth tokens, or client secrets are committed to the repository (enforced via `.gitignore`).
2. **Controlled Publication Gate**: Autonomous execution automatically halts at `READY_FOR_HUMAN_REVIEW`. No upload occurs without explicit `APPROVE & CLOSE` authorization.
3. **Reproducibility**: Every production run preserves claim traceability, shot keyframe captures, and loudnorm stats in `data/rendered/<story_id>/qa/`.

---

## 📜 License
Distributed under the MIT License. Built for pair-programming and autonomous agent workflows with Google Antigravity.
