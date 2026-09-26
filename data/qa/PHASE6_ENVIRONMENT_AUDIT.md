# PHASE 6 — ENVIRONMENT & PRODUCTION READINESS AUDIT
**Date:** September 26, 2026  
**Auditor:** AI News Factory Environment Inspector  
**Story Target:** `google-project-suncatcher-orbital-tpu-2026`  
**Mode:** READ-ONLY ENVIRONMENT AUDIT (No installs, no renders, no publication)

---

## STATUS: PARTIALLY_READY

> [!NOTE]
> The environment possesses high-performance core multimedia processing (FFmpeg 9.0.1 with Apple VideoToolbox hardware acceleration, Python 3.9 venv with core schema validators, macOS native multi-lingual speech synthesis, and Google Chrome). However, the **concrete executable automation scripts** for Phase 6 (asset generation, TTS audio rendering, subtitle generation, and video compositing) have not yet been written in `src/` or `scripts/`, and third-party API credentials (Veo/Flow, ElevenLabs, YouTube OAuth) remain unconfigured.

---

## 1. Environment & Runtime Specifications

| Category | Component / Tool | Version / Details | Status |
| :--- | :--- | :--- | :---: |
| **Operating System** | macOS (Darwin 24.6.0 x86_64) | macOS 15.8 (Build 24H23) | **AVAILABLE** |
| **Python Runtime** | System & Virtualenv | Python 3.9.6 (`/usr/bin/python3` and `./.venv/bin/python3`) | **AVAILABLE** |
| **Package Installer (Python)** | pip | pip 21.2.4 | **AVAILABLE** |
| **Node.js Runtime** | Node.js engine | Not in standard PATH | **MISSING** |
| **Package Installer (Node)** | npm | Not in standard PATH | **MISSING** |
| **Video Processing** | FFmpeg | FFmpeg 9.0.1 (`/usr/local/bin/ffmpeg`)<br>• `libx264`, `h264_videotoolbox` (Apple Silicon/Metal HW acceleration)<br>• `libx265`, `libsvtav1`, `libmp3lame`, `libopus`, `libvpx`, `aac` | **AVAILABLE** |
| **Image Processing CLI** | ImageMagick (`magick`, `convert`) | Not in standard PATH | **MISSING** |
| **Headless Browser CLI** | Google Chrome | Google Chrome 153.0.8010.53 (`/Applications/Google Chrome.app`) | **AVAILABLE** |
| **Browser Automation** | Playwright CLI / Python package | Not installed | **MISSING** |
| **Native TTS Engine** | macOS `say` CLI | `/usr/bin/say`<br>• English: `Samantha` (en_US), `Daniel` (en_GB), `Eddy`, `Flo`<br>• Vietnamese: `Linh` (vi_VN) | **AVAILABLE** |
| **Audio Processing CLI** | SoX | Not in standard PATH | **MISSING** |

---

## 2. Python & Node Package Inventory

### Python Packages Installed in `./.venv`
```text
Package                   Version
------------------------- ---------
annotated-types           0.7.0
attrs                     26.1.0
certifi                   2026.7.22
charset-normalizer        3.5.1
exceptiongroup            1.3.1
idna                      3.20
iniconfig                 2.1.0
jsonschema                4.25.1
jsonschema-specifications 2025.9.1
packaging                 26.3
pip                       21.2.4
pluggy                    1.6.0
pydantic                  2.13.5
pydantic_core             2.46.5
Pygments                  2.21.0
pytest                    8.4.2
python-dotenv             1.2.1
PyYAML                    6.0.3
referencing               0.36.2
requests                  2.32.5
rpds-py                   0.27.1
setuptools                58.0.4
tomli                     2.4.1
typing_extensions         4.16.0
typing-inspection         0.4.2
urllib3                   2.6.3
```

### Python Packages Missing for Video Production
* `Pillow` / `PIL` (Essential for programmatic image composition, diagram rasterization, and badge overlays)
* `opencv-python` (Optional for frame-by-frame analysis and motion synthesis)
* `moviepy` (Optional higher-level video editing wrapper)
* `google-genai` / `google-generativeai` (Google Veo / Gemini API integration)
* `openai` / `elevenlabs` / `edge-tts` (Optional cloud neural TTS engines)
* `srt` / `webvtt-py` (Subtitle track generation)

### Node.js Packages Installed
* **None**. No `package.json` or `node_modules` exists in the workspace.

---

## 3. Project Tree & Architecture Inspection

```text
ai_news_factory/
├── .agents/                               # Subagent profiles & specialized skills
│   ├── agents/
│   │   ├── editorial-storyteller-agent/
│   │   ├── fact-checker-agent/
│   │   ├── news-hunter-agent/
│   │   ├── qa-publisher-agent/
│   │   └── visual-storyteller-agent/
│   └── skills/
│       ├── ai-news-qa/
│       ├── ai-news-research/
│       ├── ai-news-storytelling/
│       └── ai-news-visuals/
├── config/
│   └── factory.yaml                       # Factory master configuration (9:16, 1080x1920, 30fps)
├── data/
│   ├── inbox/                             # Phase 1 Candidate feeds (NEWS_CANDIDATES.json)
│   ├── verified/                          # Phase 2 Verified facts (VERIFIED_SUNCATCHER_20260926.json)
│   ├── scripts/                           # Phase 3 Master scripts & editorial notes
│   ├── visuals/                           # Phase 4 Storyboards, visual plans, asset manifests
│   ├── qa/                                # Phase 5 Red-team reports, traceability, remediation
│   └── rendered/                          # Target video output directory (Currently empty)
├── schemas/                               # JSON Schemas enforcing artifact contracts
│   ├── news_candidates.schema.json
│   ├── verified_news.schema.json
│   ├── script.schema.json
│   ├── visual_plan.schema.json
│   └── qa_report.schema.json
├── src/
│   └── validate_artifacts.py              # Core factory validation utility
├── tests/
│   └── test_factory_setup.py              # Test suite
├── .env.example                           # Configuration credentials template
├── AI_NEWS_FACTORY_RULES.md               # Constitution v1.0
├── AI_NEWS_VISUAL_STYLE_BIBLE_v1.0.md     # Visual standards
├── RUNBOOK.md                             # Phase-by-phase execution guide
├── START_HERE.md                          # Architecture orientation
├── pyproject.toml                         # Project metadata
└── requirements.txt                       # Python dependencies
```

---

## 4. Pipeline Component Evaluation

### TOOLS_AVAILABLE
1. **FFmpeg 9.0.1:** Full hardware-accelerated H.264/HEVC encoding via Apple VideoToolbox (`h264_videotoolbox`), scaling, filtering, audio mixing, concatenation, and framerate standardization (30 FPS, 1080x1920).
2. **macOS Native Speech Synthesizer (`/usr/bin/say`):** High-quality text-to-speech with zero external API dependencies. Supports natural English narration (`Samantha`, `Daniel`) and Vietnamese narration (`Linh`).
3. **Google Chrome 153:** Installed on macOS; capable of headless HTML5/CSS3/SVG rendering and high-DPI rasterization.
4. **Python 3.9 Environment (`./.venv`):** Pre-configured with Pydantic, JSON Schema, Requests, and YAML parser.
5. **Antigravity Tool Ecosystem:** Built-in `generate_image` tool for procedural and conceptual image generation.
6. **Production Storyboard & Assets:** All Shot 01–09 timing, prompts, negative constraints, audio cues, and text cards are 100% authored and validated in `data/visuals/` and `data/scripts/`.

### TOOLS_MISSING
1. **Node.js & npm:** Unavailable in current PATH, preventing Remotion or Node-based canvas rendering engines.
2. **ImageMagick (`magick` / `convert`):** Unavailable in current PATH, requiring image manipulations to use Python (Pillow) or FFmpeg filtergraphs.
3. **Dedicated Cloud AI Media SDKs:** `google-genai` / Veo API client, ElevenLabs SDK, and OpenAI SDK are not installed in `.venv`.
4. **Whisper / ASR Transcription:** No automated speech recognition model installed for automatic word-level caption alignment.

### EXISTING_RENDER_PIPELINE
* **Status:** **NOT IMPLEMENTED (NO SCRIPT)**
* **Detail:** While the inputs (`SUNCATCHER_SHORT_SCRIPT_20260926.json`, `SUNCATCHER_VISUAL_STORYBOARD_20260926.json`, `SUNCATCHER_ASSET_MANIFEST.json`) and output directory (`data/rendered/`) exist, there is no master render script (e.g. `src/render_short.py`) to orchestrate the composition.

### EXISTING_AUDIO_PIPELINE
* **Status:** **PARTIALLY READY (PRIMITIVES AVAILABLE, ADAPTER NEEDED)**
* **Detail:** The narration script with exact phonetics and timing is authored in English (103 words, 35.0s) and Vietnamese (130 words, 35.0s). The engine `/usr/bin/say` is available immediately and can output uncompressed AIFF/WAV audio that FFmpeg can process. However, a dedicated Python wrapper script (`src/generate_audio.py`) to parse `spoken_script`, invoke `say` (or cloud TTS), and balance audio levels is not yet written.

### EXISTING_ASSET_PIPELINE
* **Status:** **PARTIALLY READY (SPECIFICATIONS COMPLETE, ADAPTER NEEDED)**
* **Detail:** All 9 shots have complete Midjourney/FLUX prompts, Veo cinematic prompts, negative prompts, camera angles, color codes, and visual goals in `SUNCATCHER_VISUAL_STORYBOARD_20260926.json`. However, an automated asset generation script (e.g., calling image generation tools or rendering procedural SVG diagrams for Shot 02, Shot 04, Shot 05, Shot 06) is not yet written in `src/`.

### MISSING_COMPONENTS
1. `src/generate_audio.py`: Script to synthesize the 35.0s narration track via macOS `say` or cloud TTS, apply normalization, and export to `data/rendered/audio_master.wav`.
2. `src/generate_visual_assets.py`: Script to produce or collect the keyframe visual assets for Shots 01 through 09 based on `SUNCATCHER_ASSET_MANIFEST.json`.
3. `src/generate_subtitles.py`: Script to generate timed ASS / SRT subtitles from the script timing data for clean upper-middle safe-zone burn-in.
4. `src/composite_video.py` or `src/render_video.py`: Script to invoke FFmpeg to assemble images/video clips with crossfades, motion pans (Ken Burns / zoom), bind the master audio track, burn subtitles, and output `data/rendered/google-project-suncatcher-orbital-tpu-2026.mp4` (1080x1920 @ 30 FPS, H.264 / AAC).

---

## 5. Feasibility of Real Video Production with Current Tools

Can a real, high-quality 9:16 technical news video be rendered **right now** without installing heavy third-party external runtimes?

**YES, via an FFmpeg + Native TTS + Procedural Graphic Pipeline:**
1. **Narration:** Use macOS native `/usr/bin/say` with the high-fidelity `Samantha` (English) or `Linh` (Vietnamese) voice at ~176 WPM.
2. **Visual Keyframes:** Generate visual cards and diagram graphics using the built-in `generate_image` tool or procedural SVG/HTML rendering via Google Chrome headless, then rasterize to 1080x1920 PNGs.
3. **Motion & Compositing:** Use `/usr/local/bin/ffmpeg` with VideoToolbox hardware acceleration (`-c:v h264_videotoolbox`):
   - Apply dynamic zooms and slow orbital pans (`zoompan` filter).
   - Apply crossfade transitions between shot boundaries.
   - Mix background ambient audio and sound effects (`sfx`).
   - Burn high-contrast technical typography cards.
   - Encode final pristine 1080x1920 30fps vertical MP4 matching YouTube Shorts specifications.

---

## 6. RECOMMENDED_NEXT_STEP

Do NOT install random packages or modify configuration until the architecture is agreed upon.

### Recommended Path Forward:
1. **Design a Pure Python/FFmpeg Production Pipeline in `src/`:**
   - Create `src/render/` with modular components:
     - `src/render/audio.py`: Harness `/usr/bin/say` (or cloud TTS API if keys are provided) to render the 35.0s audio track.
     - `src/render/subtitles.py`: Generate standard SRT/ASS subtitle files from `SUNCATCHER_SHORT_SCRIPT_20260926.json` shot timings.
     - `src/render/compositor.py`: Harness `/usr/local/bin/ffmpeg` to assemble video segments, audio, and subtitles into `data/rendered/SUNCATCHER_SHORT_20260926.mp4`.
2. **Execute Phase 6 in Controlled Steps:**
   - Step 6A: Generate audio master and confirm 35.0s audio timing.
   - Step 6B: Synthesize/assemble 9 visual shot assets.
   - Step 6C: Perform test composite with FFmpeg.
   - Step 6D: Review final rendered MP4 against Style Bible v1.0.
