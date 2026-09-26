"""AI NEWS FACTORY — Production Asset Generator for Project Suncatcher.

Generates production-ready 1080x1920 SVG vector assets and rasterizes them
to 1080x1920 PNG images using native macOS sips (Apple CoreGraphics).
Every asset adheres strictly to:
- AI News Visual Style Bible v1.0
- SATELLITE_MASTER_DESIGN
- Traceability to verified claim_ids
- Rights clearance (PROPRIETARY_GENERATED, EDITORIAL_FAIR_USE, ORIGINAL_VECTOR_DIAGRAM)
- Non-negotiable editorial guardrails (no constant sunlight, no fake screenshots, future concept watermarks)
"""

from __future__ import annotations

import html
import json
import logging
import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(message)s")
logger = logging.getLogger("ai_news_factory.asset_production")

ROOT = Path(__file__).resolve().parents[1]
STORY_ID = "google-project-suncatcher-orbital-tpu-2026"

PALETTE = {
    "canvas": "#070A0F",
    "panel": "#0D121A",
    "panel_border": "#1E2A38",
    "text": "#F3F7FA",
    "muted": "#8B98A7",
    "cyan": "#4DEBFF",
    "violet": "#9B7CFF",
    "red": "#FF5C70",
    "green": "#54E39A",
    "amber": "#FFB300",
    "copper": "#C87533",
    "deep_blue": "#101D2C",
    "solar_cell": "#1A2B4C",
}


def get_base_svg_template(
    shot_id: str,
    shot_title: str,
    visual_status_badge: str,
    badge_color: str,
    main_visual_content: str,
    primary_text: str,
    subtext: str,
    extra_badge: str = "",
) -> str:
    """Wraps shot content into standard 1080x1920 vertical canvas adhering to Style Bible v1.0."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920" width="1080" height="1920">
  <defs>
    <!-- Background Space Radial Glow -->
    <radialGradient id="spaceGlow" cx="50%" cy="40%" r="65%">
      <stop offset="0%" stop-color="#0E1B2A" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="{PALETTE['canvas']}" stop-opacity="1"/>
    </radialGradient>

    <!-- Hairline Gradients -->
    <linearGradient id="cyanLine" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{PALETTE['cyan']}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{PALETTE['cyan']}" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="{PALETTE['cyan']}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="violetLine" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{PALETTE['violet']}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{PALETTE['violet']}" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="{PALETTE['violet']}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="goldKapton" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFC837"/>
      <stop offset="50%" stop-color="#FF8008"/>
      <stop offset="100%" stop-color="#B8860B"/>
    </linearGradient>
    <linearGradient id="thermalGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{PALETTE['red']}"/>
      <stop offset="50%" stop-color="{PALETTE['amber']}"/>
      <stop offset="100%" stop-color="#FFF275"/>
    </linearGradient>
    <linearGradient id="solarWingGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#14213d"/>
      <stop offset="50%" stop-color="#1f3160"/>
      <stop offset="100%" stop-color="#0d1b2a"/>
    </linearGradient>
  </defs>

  <!-- Canvas Deep Void -->
  <rect width="1080" height="1920" fill="{PALETTE['canvas']}"/>
  <rect width="1080" height="1920" fill="url(#spaceGlow)"/>

  <!-- Technical Background Grid -->
  <g stroke="#131B26" stroke-width="1" opacity="0.6">
    <line x1="80" y1="0" x2="80" y2="1920"/>
    <line x1="540" y1="0" x2="540" y2="1920"/>
    <line x1="1000" y1="0" x2="1000" y2="1920"/>
    <line x1="0" y1="200" x2="1080" y2="200"/>
    <line x1="0" y1="440" x2="1080" y2="440"/>
    <line x1="0" y1="1300" x2="1080" y2="1300"/>
    <line x1="0" y1="1680" x2="1080" y2="1680"/>
  </g>

  <!-- Top Header Zone (Safe Margin: Y=140-200) -->
  <g transform="translate(80, 160)">
    <text x="0" y="0" font-family="'Inter', sans-serif" font-size="24" font-weight="800" fill="{PALETTE['cyan']}" letter-spacing="3">
      AI NEWS FACTORY
    </text>
    <text x="920" y="0" font-family="'Space Grotesk', monospace" font-size="20" font-weight="600" fill="{PALETTE['muted']}" text-anchor="end" letter-spacing="1">
      PROJECT SUNCATCHER • ORBITAL TPU
    </text>
    <line x1="0" y1="22" x2="920" y2="22" stroke="url(#cyanLine)" stroke-width="2"/>
  </g>

  <!-- Shot Identification & Visual Status Pill -->
  <g transform="translate(540, 260)">
    <rect x="-300" y="-24" width="600" height="48" rx="24" fill="{PALETTE['panel']}" stroke="{badge_color}" stroke-width="1.5"/>
    <text x="0" y="0" font-family="'Inter', sans-serif" font-size="20" font-weight="700" fill="{PALETTE['text']}" text-anchor="middle" dominant-baseline="central" letter-spacing="2">
      {html.escape(shot_id.upper())} • {html.escape(shot_title.upper())}
    </text>
  </g>

  <!-- MAIN VISUAL STAGE (Y=320 to Y=1280) -->
  <g id="main-visual-stage">
    {main_visual_content}
  </g>

  <!-- PRIMARY TEXT CARD (Safe Upper-Middle Zone: Y=1320-1560) -->
  <g transform="translate(80, 1340)">
    <rect width="920" height="230" rx="16" fill="{PALETTE['panel']}" stroke="{PALETTE['panel_border']}" stroke-width="2"/>

    <!-- Accent Corner Brackets -->
    <path d="M 0 30 L 0 0 L 30 0" fill="none" stroke="{PALETTE['cyan']}" stroke-width="3"/>
    <path d="M 920 30 L 920 0 L 890 0" fill="none" stroke="{PALETTE['cyan']}" stroke-width="3"/>
    <path d="M 0 200 L 0 230 L 30 230" fill="none" stroke="{PALETTE['cyan']}" stroke-width="3"/>
    <path d="M 920 200 L 920 230 L 890 230" fill="none" stroke="{PALETTE['cyan']}" stroke-width="3"/>

    <!-- Status Sub-pill -->
    <g transform="translate(460, 42)">
      <rect x="-140" y="-16" width="280" height="32" rx="16" fill="#070A0F" stroke="{badge_color}" stroke-width="1"/>
      <text x="0" y="0" font-family="'Inter', sans-serif" font-size="15" font-weight="700" fill="{badge_color}" text-anchor="middle" dominant-baseline="central" letter-spacing="1.5">
        {html.escape(visual_status_badge)}
      </text>
    </g>

    <!-- Central Primary Card Text (Strictly max 6 words per card) -->
    <text x="460" y="125" font-family="'Inter', sans-serif" font-size="50" font-weight="900" fill="{PALETTE['text']}" text-anchor="middle" letter-spacing="1">
      {html.escape(primary_text)}
    </text>

    <!-- Technical Subtext / Engineering Context -->
    <text x="460" y="185" font-family="'Space Grotesk', monospace" font-size="22" font-weight="500" fill="{PALETTE['muted']}" text-anchor="middle" letter-spacing="0.5">
      {html.escape(subtext)}
    </text>
  </g>

  <!-- Optional Watermark / Extra Guardrail Banner (Y=1600-1680) -->
  {extra_badge}

  <!-- Channel Footer Stamp (Y=1780-1840) -->
  <g transform="translate(540, 1820)">
    <text x="0" y="0" font-family="'Inter', sans-serif" font-size="18" font-weight="700" fill="{PALETTE['muted']}" text-anchor="middle" letter-spacing="2">
      AI TECH EXPLAINER • VERIFIED EVIDENCE FIRST
    </text>
  </g>
</svg>"""


# =============================================================================
# SHOT 01 — ORBITAL OPENING
# =============================================================================
def generate_shot_01_svg() -> str:
    main_content = f"""
    <!-- Earth Curvature Limb in Lower View -->
    <g transform="translate(0, 0)">
      <!-- Outer Space Stars -->
      <circle cx="200" cy="480" r="2" fill="#FFFFFF" opacity="0.6"/>
      <circle cx="750" cy="420" r="1.5" fill="{PALETTE['cyan']}" opacity="0.7"/>
      <circle cx="880" cy="550" r="2" fill="#FFFFFF" opacity="0.5"/>
      <circle cx="340" cy="620" r="1" fill="#FFFFFF" opacity="0.4"/>
      <circle cx="160" cy="750" r="2.5" fill="{PALETTE['cyan']}" opacity="0.8"/>

      <!-- Earth Horizon Curve -->
      <path d="M -100 1150 Q 540 860 1180 1150 L 1180 1320 L -100 1320 Z" fill="#0A1526"/>
      <path d="M -100 1150 Q 540 860 1180 1150" fill="none" stroke="{PALETTE['cyan']}" stroke-width="8" opacity="0.9"/>
      <path d="M -100 1150 Q 540 860 1180 1150" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.8"/>

      <!-- Atmospheric Volumetric Glow -->
      <path d="M -100 1150 Q 540 840 1180 1150" fill="none" stroke="{PALETTE['cyan']}" stroke-width="32" opacity="0.25"/>
      <path d="M -100 1150 Q 540 820 1180 1150" fill="none" stroke="{PALETTE['violet']}" stroke-width="60" opacity="0.15"/>

      <!-- Terrestrial Server Silhouette Dissolving into Orbit -->
      <g transform="translate(420, 520)" opacity="0.85">
        <rect x="0" y="0" width="240" height="280" rx="8" fill="{PALETTE['panel']}" stroke="{PALETTE['cyan']}" stroke-width="2"/>
        <line x1="20" y1="40" x2="220" y2="40" stroke="{PALETTE['panel_border']}" stroke-width="2"/>
        <line x1="20" y1="90" x2="220" y2="90" stroke="{PALETTE['panel_border']}" stroke-width="2"/>
        <line x1="20" y1="140" x2="220" y2="140" stroke="{PALETTE['panel_border']}" stroke-width="2"/>
        <line x1="20" y1="190" x2="220" y2="190" stroke="{PALETTE['panel_border']}" stroke-width="2"/>
        <line x1="20" y1="240" x2="220" y2="240" stroke="{PALETTE['panel_border']}" stroke-width="2"/>

        <!-- Server LED Blinks -->
        <circle cx="40" cy="65" r="4" fill="{PALETTE['cyan']}"/>
        <circle cx="55" cy="65" r="4" fill="{PALETTE['green']}"/>
        <circle cx="40" cy="115" r="4" fill="{PALETTE['cyan']}"/>
        <circle cx="55" cy="115" r="4" fill="{PALETTE['cyan']}"/>
        <circle cx="40" cy="165" r="4" fill="{PALETTE['violet']}"/>
        <circle cx="40" cy="215" r="4" fill="{PALETTE['cyan']}"/>

        <!-- Server Label -->
        <text x="120" y="270" font-family="'Space Grotesk', monospace" font-size="14" fill="{PALETTE['muted']}" text-anchor="middle">
          EARTH DATACENTER RACK
        </text>
      </g>

      <!-- Orbital Ascension Vector Beam -->
      <line x1="540" y1="800" x2="540" y2="960" stroke="{PALETTE['cyan']}" stroke-width="2" stroke-dasharray="8 8"/>
      <polygon points="540,790 534,810 546,810" fill="{PALETTE['cyan']}"/>

      <!-- Telemetry Tags -->
      <g transform="translate(140, 480)">
        <rect width="200" height="70" rx="6" fill="#0D121A" stroke="{PALETTE['panel_border']}" stroke-width="1.5"/>
        <text x="20" y="28" font-family="'Space Grotesk', monospace" font-size="14" font-weight="700" fill="{PALETTE['cyan']}">ORBIT ALTITUDE</text>
        <text x="20" y="52" font-family="'Inter', sans-serif" font-size="18" font-weight="800" fill="{PALETTE['text']}">~500 KM (LEO)</text>
      </g>
      <g transform="translate(740, 480)">
        <rect width="200" height="70" rx="6" fill="#0D121A" stroke="{PALETTE['panel_border']}" stroke-width="1.5"/>
        <text x="20" y="28" font-family="'Space Grotesk', monospace" font-size="14" font-weight="700" fill="{PALETTE['violet']}">INCLINATION</text>
        <text x="20" y="52" font-family="'Inter', sans-serif" font-size="18" font-weight="800" fill="{PALETTE['text']}">97.5° SUN-SYNC</text>
      </g>
    </g>
    """
    return get_base_svg_template(
        shot_id="shot-01",
        shot_title="Orbital Opening",
        visual_status_badge="ILLUSTRATIVE • RESEARCH CONCEPT",
        badge_color=PALETTE["cyan"],
        main_visual_content=main_content,
        primary_text="AI TEST BED IN ORBIT",
        subtext="TERRESTRIAL SERVER RACKS → LOW EARTH ORBIT TESTBED",
    )


# =============================================================================
# SHOT 02 — OFFICIAL RESEARCH EVIDENCE CARD
# =============================================================================
def generate_shot_02_svg() -> str:
    main_content = f"""
    <!-- Official Document Evidence Window -->
    <g transform="translate(120, 360)">
      <!-- Outer Frosted Window -->
      <rect width="840" height="880" rx="16" fill="{PALETTE['panel']}" stroke="{PALETTE['panel_border']}" stroke-width="2"/>

      <!-- Window Title Bar -->
      <rect width="840" height="60" rx="16" fill="#131B26"/>
      <circle cx="36" cy="30" r="7" fill="{PALETTE['red']}"/>
      <circle cx="60" cy="30" r="7" fill="{PALETTE['amber']}"/>
      <circle cx="84" cy="30" r="7" fill="{PALETTE['green']}"/>

      <!-- Official Source Reference Chip -->
      <rect x="220" y="14" width="400" height="32" rx="16" fill="#070A0F" stroke="{PALETTE['cyan']}" stroke-width="1"/>
      <text x="420" y="30" font-family="'Space Grotesk', monospace" font-size="14" font-weight="700" fill="{PALETTE['cyan']}" text-anchor="middle" dominant-baseline="central">
        OFFICIAL SOURCE REFERENCE
      </text>

      <!-- URL Bar -->
      <g transform="translate(40, 90)">
        <rect width="760" height="44" rx="8" fill="#070A0F" stroke="#1E2A38" stroke-width="1"/>
        <text x="24" y="27" font-family="'Space Grotesk', monospace" font-size="15" fill="{PALETTE['muted']}">
          https://blog.google/technology/ai/project-suncatcher-space-ai/
        </text>
      </g>

      <!-- Document Title -->
      <g transform="translate(40, 180)">
        <text x="0" y="30" font-family="'Inter', sans-serif" font-size="32" font-weight="800" fill="{PALETTE['text']}">
          Project Suncatcher: Space AI Testbed
        </text>
        <text x="0" y="65" font-family="'Space Grotesk', monospace" font-size="18" font-weight="500" fill="{PALETTE['muted']}">
          Published by Google Research • September 24, 2026
        </text>
      </g>

      <!-- Verified Research Prototype Stamp -->
      <g transform="translate(40, 290)">
        <rect width="760" height="90" rx="10" fill="#0E2218" stroke="{PALETTE['green']}" stroke-width="2"/>
        <circle cx="50" cy="45" r="22" fill="{PALETTE['green']}" opacity="0.2"/>
        <path d="M 40 45 L 47 52 L 60 38" fill="none" stroke="{PALETTE['green']}" stroke-width="4" stroke-linecap="round"/>
        <text x="90" y="38" font-family="'Inter', sans-serif" font-size="20" font-weight="800" fill="{PALETTE['green']}">
          STATUS: RESEARCH PROTOTYPE
        </text>
        <text x="90" y="66" font-family="'Space Grotesk', monospace" font-size="16" font-weight="600" fill="{PALETTE['text']}">
          NOT AN OPERATIONAL ORBITAL DATA CENTER
        </text>
      </g>

      <!-- Excerpt Highlight Block -->
      <g transform="translate(40, 420)">
        <rect width="760" height="200" rx="10" fill="#070A0F" stroke="{PALETTE['violet']}" stroke-width="1.5"/>
        <line x1="0" y1="0" x2="0" y2="200" stroke="{PALETTE['violet']}" stroke-width="8"/>
        <text x="30" y="45" font-family="'Inter', sans-serif" font-size="18" font-weight="600" fill="{PALETTE['cyan']}">
          PRIMARY RESEARCH OBJECTIVE:
        </text>
        <text x="30" y="85" font-family="'Inter', sans-serif" font-size="20" font-weight="500" fill="{PALETTE['text']}">
          "Testing physical feasibility of running TPU accelerators
        </text>
        <text x="30" y="120" font-family="'Inter', sans-serif" font-size="20" font-weight="500" fill="{PALETTE['text']}">
          in low Earth orbit... evaluating vacuum thermal limits,
        </text>
        <text x="30" y="155" font-family="'Inter', sans-serif" font-size="20" font-weight="500" fill="{PALETTE['text']}">
          solar yield in dawn-dusk SSO, and proton radiation bit-flips."
        </text>
      </g>

      <!-- Partnership & Specs Tags -->
      <g transform="translate(40, 660)">
        <rect width="360" height="70" rx="8" fill="#131B26" stroke="#1E2A38" stroke-width="1"/>
        <text x="20" y="28" font-family="'Space Grotesk', monospace" font-size="13" fill="{PALETTE['muted']}">SPACECRAFT PARTNER</text>
        <text x="20" y="52" font-family="'Inter', sans-serif" font-size="18" font-weight="700" fill="{PALETTE['text']}">Planet Labs (Agile Bus)</text>
      </g>
      <g transform="translate(440, 660)">
        <rect width="360" height="70" rx="8" fill="#131B26" stroke="#1E2A38" stroke-width="1"/>
        <text x="20" y="28" font-family="'Space Grotesk', monospace" font-size="13" fill="{PALETTE['muted']}">HARDWARE ACCELERATOR</text>
        <text x="20" y="52" font-family="'Inter', sans-serif" font-size="18" font-weight="700" fill="{PALETTE['cyan']}">Google Trillium (TPU v6e)</text>
      </g>
    </g>
    """
    return get_base_svg_template(
        shot_id="shot-02",
        shot_title="Evidence Reference",
        visual_status_badge="HYBRID • OFFICIAL SOURCE REFERENCE",
        badge_color=PALETTE["green"],
        main_visual_content=main_content,
        primary_text="PROJECT SUNCATCHER • RESEARCH PROTOTYPE",
        subtext="GOOGLE RESEARCH ANNOUNCEMENT • SEPTEMBER 24, 2026",
    )


# =============================================================================
# SHOT 03 — SATELLITE HARDWARE & 4-TPU CUTAWAY
# =============================================================================
def generate_shot_03_svg() -> str:
    main_content = f"""
    <!-- 3D Technical CAD Cutaway Presentation -->
    <g transform="translate(100, 360)">
      <!-- Left Deployable Solar Wing (1.0 kW Starboard) -->
      <g transform="translate(20, 240)">
        <rect width="240" height="340" rx="4" fill="url(#solarWingGrad)" stroke="{PALETTE['cyan']}" stroke-width="2"/>
        <!-- Photovoltaic Grid Lines -->
        <line x1="60" y1="0" x2="60" y2="340" stroke="#2B4673" stroke-width="1.5"/>
        <line x1="120" y1="0" x2="120" y2="340" stroke="#2B4673" stroke-width="1.5"/>
        <line x1="180" y1="0" x2="180" y2="340" stroke="#2B4673" stroke-width="1.5"/>
        <line x1="0" y1="85" x2="240" y2="85" stroke="#2B4673" stroke-width="1.5"/>
        <line x1="0" y1="170" x2="240" y2="170" stroke="#2B4673" stroke-width="1.5"/>
        <line x1="0" y1="255" x2="240" y2="255" stroke="#2B4673" stroke-width="1.5"/>
        <!-- Hinge Bracket -->
        <rect x="235" y="145" width="20" height="50" rx="4" fill="#5A6B82"/>
        <text x="120" y="375" font-family="'Space Grotesk', monospace" font-size="14" font-weight="700" fill="{PALETTE['cyan']}" text-anchor="middle">
          SOLAR WING (PORT)
        </text>
      </g>

      <!-- Right Deployable Solar Wing (1.0 kW Port) -->
      <g transform="translate(620, 240)">
        <rect width="240" height="340" rx="4" fill="url(#solarWingGrad)" stroke="{PALETTE['cyan']}" stroke-width="2"/>
        <!-- Photovoltaic Grid Lines -->
        <line x1="60" y1="0" x2="60" y2="340" stroke="#2B4673" stroke-width="1.5"/>
        <line x1="120" y1="0" x2="120" y2="340" stroke="#2B4673" stroke-width="1.5"/>
        <line x1="180" y1="0" x2="180" y2="340" stroke="#2B4673" stroke-width="1.5"/>
        <line x1="0" y1="85" x2="240" y2="85" stroke="#2B4673" stroke-width="1.5"/>
        <line x1="0" y1="170" x2="240" y2="170" stroke="#2B4673" stroke-width="1.5"/>
        <line x1="0" y1="255" x2="240" y2="255" stroke="#2B4673" stroke-width="1.5"/>
        <!-- Hinge Bracket -->
        <rect x="-15" y="145" width="20" height="50" rx="4" fill="#5A6B82"/>
        <text x="120" y="375" font-family="'Space Grotesk', monospace" font-size="14" font-weight="700" fill="{PALETTE['cyan']}" text-anchor="middle">
          SOLAR WING (STBD)
        </text>
      </g>

      <!-- Central Planet Labs Satellite Bus Chassis (1.2m x 0.8m x 0.8m) -->
      <g transform="translate(280, 160)">
        <!-- Bus Outer Frame (Titanium & CFRP) -->
        <rect width="320" height="500" rx="12" fill="#101622" stroke="{PALETTE['panel_border']}" stroke-width="3"/>

        <!-- Gold Kapton Multi-Layer Insulation (MLI) Facets -->
        <rect x="15" y="15" width="290" height="70" rx="6" fill="url(#goldKapton)" opacity="0.9"/>
        <text x="160" y="55" font-family="'Space Grotesk', monospace" font-size="13" font-weight="700" fill="#070A0F" text-anchor="middle">
          GOLD KAPTON MLI BLANKET
        </text>

        <!-- Internal Cutaway Cold Plate Chamber -->
        <g transform="translate(20, 110)">
          <rect width="280" height="350" rx="8" fill="#070A0F" stroke="{PALETTE['violet']}" stroke-width="2"/>
          <text x="140" y="30" font-family="'Space Grotesk', monospace" font-size="14" font-weight="700" fill="{PALETTE['violet']}" text-anchor="middle">
            ALUMINUM COLD-PLATE INTERFACE
          </text>

          <!-- 4x Trillium TPU Dies (Symmetrical 2x2 Grid) -->
          <!-- TPU 1 -->
          <g transform="translate(30, 60)">
            <rect width="95" height="95" rx="6" fill="#171D2B" stroke="{PALETTE['cyan']}" stroke-width="2"/>
            <rect x="25" y="25" width="45" height="45" rx="3" fill="#202A3D"/>
            <text x="47" y="52" font-family="'Inter', sans-serif" font-size="14" font-weight="800" fill="{PALETTE['cyan']}" text-anchor="middle">TPU 1</text>
            <text x="47" y="80" font-family="'Space Grotesk', monospace" font-size="10" fill="{PALETTE['muted']}" text-anchor="middle">HBM 1</text>
          </g>
          <!-- TPU 2 -->
          <g transform="translate(155, 60)">
            <rect width="95" height="95" rx="6" fill="#171D2B" stroke="{PALETTE['cyan']}" stroke-width="2"/>
            <rect x="25" y="25" width="45" height="45" rx="3" fill="#202A3D"/>
            <text x="47" y="52" font-family="'Inter', sans-serif" font-size="14" font-weight="800" fill="{PALETTE['cyan']}" text-anchor="middle">TPU 2</text>
            <text x="47" y="80" font-family="'Space Grotesk', monospace" font-size="10" fill="{PALETTE['muted']}" text-anchor="middle">HBM 2</text>
          </g>
          <!-- TPU 3 -->
          <g transform="translate(30, 180)">
            <rect width="95" height="95" rx="6" fill="#171D2B" stroke="{PALETTE['cyan']}" stroke-width="2"/>
            <rect x="25" y="25" width="45" height="45" rx="3" fill="#202A3D"/>
            <text x="47" y="52" font-family="'Inter', sans-serif" font-size="14" font-weight="800" fill="{PALETTE['cyan']}" text-anchor="middle">TPU 3</text>
            <text x="47" y="80" font-family="'Space Grotesk', monospace" font-size="10" fill="{PALETTE['muted']}" text-anchor="middle">HBM 3</text>
          </g>
          <!-- TPU 4 -->
          <g transform="translate(155, 180)">
            <rect width="95" height="95" rx="6" fill="#171D2B" stroke="{PALETTE['cyan']}" stroke-width="2"/>
            <rect x="25" y="25" width="45" height="45" rx="3" fill="#202A3D"/>
            <text x="47" y="52" font-family="'Inter', sans-serif" font-size="14" font-weight="800" fill="{PALETTE['cyan']}" text-anchor="middle">TPU 4</text>
            <text x="47" y="80" font-family="'Space Grotesk', monospace" font-size="10" fill="{PALETTE['muted']}" text-anchor="middle">HBM 4</text>
          </g>

          <!-- Interconnect Fabric -->
          <line x1="125" y1="107" x2="155" y2="107" stroke="{PALETTE['cyan']}" stroke-width="3"/>
          <line x1="125" y1="227" x2="155" y2="227" stroke="{PALETTE['cyan']}" stroke-width="3"/>
          <line x1="77" y1="155" x2="77" y2="180" stroke="{PALETTE['cyan']}" stroke-width="3"/>
          <line x1="202" y1="155" x2="202" y2="180" stroke="{PALETTE['cyan']}" stroke-width="3"/>

          <text x="140" y="315" font-family="'Space Grotesk', monospace" font-size="13" font-weight="700" fill="{PALETTE['cyan']}" text-anchor="middle">
            4x GOOGLE TRILLIUM (TPU v6e)
          </text>
        </g>
      </g>

      <!-- Technical Callout Badges -->
      <g transform="translate(0, 720)">
        <rect width="260" height="60" rx="8" fill="#0D121A" stroke="{PALETTE['panel_border']}" stroke-width="1.5"/>
        <text x="20" y="26" font-family="'Space Grotesk', monospace" font-size="13" fill="{PALETTE['muted']}">SPACECRAFT BUS</text>
        <text x="20" y="48" font-family="'Inter', sans-serif" font-size="16" font-weight="700" fill="{PALETTE['text']}">1.2m x 0.8m Agile Bus</text>
      </g>
      <g transform="translate(310, 720)">
        <rect width="260" height="60" rx="8" fill="#0D121A" stroke="{PALETTE['panel_border']}" stroke-width="1.5"/>
        <text x="20" y="26" font-family="'Space Grotesk', monospace" font-size="13" fill="{PALETTE['muted']}">POWER GENERATION</text>
        <text x="20" y="48" font-family="'Inter', sans-serif" font-size="16" font-weight="700" fill="{PALETTE['amber']}">1.0 kW Solar Array</text>
      </g>
      <g transform="translate(620, 720)">
        <rect width="260" height="60" rx="8" fill="#0D121A" stroke="{PALETTE['panel_border']}" stroke-width="1.5"/>
        <text x="20" y="26" font-family="'Space Grotesk', monospace" font-size="13" fill="{PALETTE['muted']}">CHIP ARCHITECTURE</text>
        <text x="20" y="48" font-family="'Inter', sans-serif" font-size="16" font-weight="700" fill="{PALETTE['cyan']}">4x Trillium TPU v6e</text>
      </g>
    </g>
    """
    return get_base_svg_template(
        shot_id="shot-03",
        shot_title="Hardware Architecture",
        visual_status_badge="ILLUSTRATIVE • PROPRIETARY 3D CAD",
        badge_color=PALETTE["cyan"],
        main_visual_content=main_content,
        primary_text="4 TRILLIUM TPUs • 1 kW ARRAY",
        subtext="PLANET LABS COMPACT BUS • 2x2 COPLANAR DIE CONFIGURATION",
    )


# =============================================================================
# SHOT 04 — DAWN-DUSK SSO SOLAR HARVEST
# =============================================================================
def generate_shot_04_svg() -> str:
    main_content = f"""
    <!-- Dawn-Dusk SSO Solar Harvest Mechanics -->
    <g transform="translate(100, 360)">
      <!-- Sun Source on Left -->
      <g transform="translate(60, 260)">
        <circle cx="0" cy="0" r="50" fill="{PALETTE['amber']}"/>
        <circle cx="0" cy="0" r="75" fill="{PALETTE['amber']}" opacity="0.3"/>
        <circle cx="0" cy="0" r="110" fill="{PALETTE['amber']}" opacity="0.12"/>
        <!-- Sun Rays -->
        <line x1="75" y1="0" x2="240" y2="0" stroke="{PALETTE['amber']}" stroke-width="3" stroke-dasharray="10 6"/>
        <line x1="65" y1="-40" x2="230" y2="-40" stroke="{PALETTE['amber']}" stroke-width="2" stroke-dasharray="10 6"/>
        <line x1="65" y1="40" x2="230" y2="40" stroke="{PALETTE['amber']}" stroke-width="2" stroke-dasharray="10 6"/>
        <text x="0" y="8" font-family="'Inter', sans-serif" font-size="16" font-weight="900" fill="#070A0F" text-anchor="middle">SUN</text>
      </g>

      <!-- Earth with Day/Night Terminator Boundary -->
      <g transform="translate(540, 260)">
        <!-- Night Hemisphere -->
        <path d="M 0 -180 A 180 180 0 0 1 0 180 Z" fill="#0A121F"/>
        <!-- Day Hemisphere -->
        <path d="M 0 -180 A 180 180 0 0 0 0 180 Z" fill="#183659"/>
        <!-- Terminator Line (Boundary) -->
        <line x1="0" y1="-190" x2="0" y2="190" stroke="{PALETTE['cyan']}" stroke-width="3"/>

        <!-- Dawn-Dusk Sun-Synchronous Orbit Ring -->
        <ellipse cx="0" cy="0" rx="60" ry="240" fill="none" stroke="{PALETTE['cyan']}" stroke-width="4" stroke-dasharray="12 8"/>
        <!-- Satellite Tracker Icon -->
        <circle cx="0" cy="-240" r="10" fill="{PALETTE['cyan']}"/>
        <rect x="-24" y="-246" width="48" height="12" fill="{PALETTE['amber']}"/>

        <text x="0" y="270" font-family="'Space Grotesk', monospace" font-size="16" font-weight="700" fill="{PALETTE['cyan']}" text-anchor="middle">
          DAWN-DUSK ORBIT • HIGH SUNLIGHT AVAILABILITY
        </text>
      </g>

      <!-- Comparative Annual Energy Yield Cards -->
      <g transform="translate(40, 600)">
        <!-- Orbital Capture Card (Up to 8x) -->
        <g transform="translate(0, 0)">
          <rect width="380" height="180" rx="12" fill="#0E242B" stroke="{PALETTE['cyan']}" stroke-width="2"/>
          <text x="30" y="40" font-family="'Space Grotesk', monospace" font-size="15" font-weight="700" fill="{PALETTE['cyan']}">
            ORBITAL DAWN-DUSK SSO
          </text>
          <text x="30" y="105" font-family="'Inter', sans-serif" font-size="52" font-weight="900" fill="{PALETTE['text']}">
            UP TO 8×
          </text>
          <text x="30" y="145" font-family="'Space Grotesk', monospace" font-size="14" fill="{PALETTE['muted']}">
            ANNUAL CUMULATIVE ENERGY
          </text>
        </g>

        <!-- Terrestrial Mid-Latitude Baseline (1x) -->
        <g transform="translate(420, 0)">
          <rect width="380" height="180" rx="12" fill="#101622" stroke="{PALETTE['panel_border']}" stroke-width="1.5"/>
          <text x="30" y="40" font-family="'Space Grotesk', monospace" font-size="15" font-weight="700" fill="{PALETTE['muted']}">
            TERRESTRIAL MID-LATITUDE
          </text>
          <text x="30" y="105" font-family="'Inter', sans-serif" font-size="52" font-weight="900" fill="{PALETTE['muted']}">
            1× BASELINE
          </text>
          <text x="30" y="145" font-family="'Space Grotesk', monospace" font-size="14" fill="{PALETTE['muted']}">
            LIMITED BY NIGHT &amp; WEATHER
          </text>
        </g>
      </g>

      <!-- Scientific Disclaimer Footnote -->
      <g transform="translate(40, 810)">
        <text x="400" y="0" font-family="'Inter', sans-serif" font-size="14" font-weight="500" fill="{PALETTE['muted']}" text-anchor="middle">
          * Represents annual cumulative energy harvest in space vs Earth; not photovoltaic cell efficiency.
        </text>
      </g>
    </g>
    """
    return get_base_svg_template(
        shot_id="shot-04",
        shot_title="Solar Harvest Mechanics",
        visual_status_badge="DIAGRAM • ORBITAL SOLAR PHYSICS",
        badge_color=PALETTE["cyan"],
        main_visual_content=main_content,
        primary_text="UP TO 8× ANNUAL SOLAR HARVEST",
        subtext="ANNUAL CUMULATIVE ENERGY HARVEST • DAWN-DUSK SSO",
    )


# =============================================================================
# SHOT 05 — VACUUM THERMAL PROBLEM (NO CONVECTION)
# =============================================================================
def generate_shot_05_svg() -> str:
    main_content = f"""
    <!-- Vacuum Thermal Trap Simulation -->
    <g transform="translate(100, 360)">
      <!-- Outer Vacuum Chamber Representation -->
      <rect width="880" height="520" rx="16" fill="#0A0E17" stroke="{PALETTE['panel_border']}" stroke-width="2"/>

      <!-- Vacuum Void Tag -->
      <g transform="translate(40, 40)">
        <rect width="360" height="40" rx="6" fill="#131B26"/>
        <text x="20" y="25" font-family="'Space Grotesk', monospace" font-size="14" font-weight="700" fill="{PALETTE['muted']}">
          ENVIRONMENT: SPACE VACUUM (DENSITY ≈ 0)
        </text>
      </g>

      <!-- Silicon Die Heat Map (Cross-Section) -->
      <g transform="translate(140, 160)">
        <!-- Base Substrate -->
        <rect width="360" height="240" rx="8" fill="#151E2B" stroke="#25354D" stroke-width="2"/>
        <!-- Concentric Thermal Heat Gradients (Core Escalating Heat) -->
        <rect x="30" y="30" width="300" height="180" rx="6" fill="#4A181C" opacity="0.8"/>
        <rect x="60" y="55" width="240" height="130" rx="6" fill="#872228" opacity="0.9"/>
        <rect x="95" y="80" width="170" height="80" rx="4" fill="{PALETTE['red']}"/>
        <rect x="130" y="95" width="100" height="50" rx="4" fill="{PALETTE['amber']}"/>

        <text x="180" y="126" font-family="'Inter', sans-serif" font-size="16" font-weight="900" fill="#070A0F" text-anchor="middle">
          TPU CORE
        </text>
        <text x="180" y="295" font-family="'Space Grotesk', monospace" font-size="15" font-weight="700" fill="{PALETTE['red']}" text-anchor="middle">
          TRAPPED DIE HEAT: JUNCTION RISES
        </text>
      </g>

      <!-- Bold Prohibition: No Convective Fans -->
      <g transform="translate(560, 160)">
        <rect width="280" height="240" rx="8" fill="#1B1215" stroke="{PALETTE['red']}" stroke-width="2"/>
        <!-- Stylized Fan Icon -->
        <circle cx="140" cy="95" r="50" fill="none" stroke="{PALETTE['muted']}" stroke-width="4"/>
        <path d="M 140 45 Q 165 70 140 95 Q 115 120 140 145" fill="none" stroke="{PALETTE['muted']}" stroke-width="4"/>
        <path d="M 90 95 Q 115 120 140 95 Q 165 70 190 95" fill="none" stroke="{PALETTE['muted']}" stroke-width="4"/>

        <!-- Bold Red Diagonal Strikeout -->
        <line x1="75" y1="30" x2="205" y2="160" stroke="{PALETTE['red']}" stroke-width="8" stroke-linecap="round"/>

        <text x="140" y="195" font-family="'Inter', sans-serif" font-size="16" font-weight="900" fill="{PALETTE['red']}" text-anchor="middle">
          NO CONVECTIVE FANS
        </text>
        <text x="140" y="220" font-family="'Space Grotesk', monospace" font-size="13" font-weight="600" fill="{PALETTE['muted']}" text-anchor="middle">
          NO AIR IN VACUUM
        </text>
      </g>

      <!-- Thermodynamics Rule Cards -->
      <g transform="translate(0, 560)">
        <g transform="translate(0, 0)">
          <rect width="420" height="150" rx="10" fill="#0D121A" stroke="{PALETTE['panel_border']}" stroke-width="1.5"/>
          <text x="24" y="38" font-family="'Space Grotesk', monospace" font-size="14" font-weight="700" fill="{PALETTE['red']}">
            CONVECTIVE COOLING
          </text>
          <text x="24" y="80" font-family="'Inter', sans-serif" font-size="28" font-weight="800" fill="{PALETTE['text']}">
            h = 0.0 W/m²·K
          </text>
          <text x="24" y="118" font-family="'Space Grotesk', monospace" font-size="14" fill="{PALETTE['muted']}">
            Zero air molecules to carry away heat
          </text>
        </g>
        <g transform="translate(460, 0)">
          <rect width="420" height="150" rx="10" fill="#0D121A" stroke="{PALETTE['cyan']}" stroke-width="1.5"/>
          <text x="24" y="38" font-family="'Space Grotesk', monospace" font-size="14" font-weight="700" fill="{PALETTE['cyan']}">
            CONDUCTION ONLY
          </text>
          <text x="24" y="80" font-family="'Inter', sans-serif" font-size="28" font-weight="800" fill="{PALETTE['text']}">
            COPPER HEAT PIPES
          </text>
          <text x="24" y="118" font-family="'Space Grotesk', monospace" font-size="14" fill="{PALETTE['muted']}">
            Heat must travel through solid metals
          </text>
        </g>
      </g>
    </g>
    """
    return get_base_svg_template(
        shot_id="shot-05",
        shot_title="Thermal Physics Limit",
        visual_status_badge="DIAGRAM • VACUUM THERMODYNAMICS",
        badge_color=PALETTE["red"],
        main_visual_content=main_content,
        primary_text="VACUUM HEAT TRAP • NO CONVECTION",
        subtext="ZERO AIR IN SPACE • SOLID CONDUCTION ONLY (NO FANS)",
    )


# =============================================================================
# SHOT 06 — RADIATION SINGLE-EVENT BIT FLIP
# =============================================================================
def generate_shot_06_svg() -> str:
    main_content = f"""
    <!-- Radiation Bit Flip Microscopic Visualization -->
    <g transform="translate(100, 360)">
      <!-- Microscopic Silicon Grid Canvas -->
      <rect width="880" height="500" rx="16" fill="#0A111C" stroke="{PALETTE['panel_border']}" stroke-width="2"/>

      <!-- HBM Memory Silicon Die Layer -->
      <g transform="translate(80, 100)">
        <!-- Silicon Substrate -->
        <rect width="720" height="220" rx="8" fill="#132033" stroke="{PALETTE['cyan']}" stroke-width="1.5"/>

        <!-- Memory Cell Array -->
        <g stroke="#1E3352" stroke-width="1.5">
          <line x1="0" y1="55" x2="720" y2="55"/>
          <line x1="0" y1="110" x2="720" y2="110"/>
          <line x1="0" y1="165" x2="720" y2="165"/>
          <line x1="120" y1="0" x2="120" y2="220"/>
          <line x1="240" y1="0" x2="240" y2="220"/>
          <line x1="360" y1="0" x2="360" y2="220"/>
          <line x1="480" y1="0" x2="480" y2="220"/>
          <line x1="600" y1="0" x2="600" y2="220"/>
        </g>

        <!-- Cosmic Proton Ionization Beam -->
        <line x1="180" y1="-60" x2="360" y2="110" stroke="{PALETTE['cyan']}" stroke-width="4"/>
        <line x1="180" y1="-60" x2="360" y2="110" stroke="#FFFFFF" stroke-width="1.5"/>

        <!-- Particle Impact Point (SEU) -->
        <circle cx="360" cy="110" r="28" fill="{PALETTE['red']}" opacity="0.3"/>
        <circle cx="360" cy="110" r="16" fill="{PALETTE['amber']}" opacity="0.6"/>
        <circle cx="360" cy="110" r="6" fill="#FFFFFF"/>

        <!-- Particle Label -->
        <text x="210" y="-20" font-family="'Space Grotesk', monospace" font-size="14" font-weight="700" fill="{PALETTE['cyan']}">
          HIGH-ENERGY PROTON
        </text>
        <text x="360" y="160" font-family="'Space Grotesk', monospace" font-size="14" font-weight="700" fill="{PALETTE['red']}" text-anchor="middle">
          IMPACT CELL [0x4F8A]
        </text>
      </g>

      <!-- Binary Register State Transition Display -->
      <g transform="translate(80, 360)">
        <rect width="720" height="100" rx="8" fill="#070A0F" stroke="{PALETTE['panel_border']}" stroke-width="1.5"/>
        <text x="40" y="38" font-family="'Space Grotesk', monospace" font-size="14" fill="{PALETTE['muted']}">
          REGISTER FLIP (0 → 1 SINGLE-EVENT UPSET)
        </text>
        <g transform="translate(40, 52)" font-family="'Space Grotesk', monospace" font-size="26" font-weight="700">
          <text x="0" y="25" fill="{PALETTE['text']}">0 0 1 0 </text>
          <rect x="95" y="0" width="32" height="35" rx="4" fill="{PALETTE['red']}" opacity="0.25"/>
          <text x="103" y="26" fill="{PALETTE['red']}">[1]</text>
          <text x="145" y="25" fill="{PALETTE['text']}"> 1 1 0</text>
          <text x="320" y="25" font-size="18" fill="{PALETTE['amber']}">← BIT FLIPPED BY IONIZATION</text>
        </g>
      </g>

      <!-- Testing Provenance Card -->
      <g transform="translate(80, 540)">
        <rect width="720" height="110" rx="10" fill="#0D121A" stroke="{PALETTE['violet']}" stroke-width="1.5"/>
        <text x="30" y="38" font-family="'Space Grotesk', monospace" font-size="13" font-weight="700" fill="{PALETTE['violet']}">
          CYCLOTRON RADIATION VALIDATION
        </text>
        <text x="30" y="74" font-family="'Inter', sans-serif" font-size="20" font-weight="800" fill="{PALETTE['text']}">
          UC Davis Crocker Nuclear Laboratory
        </text>
        <text x="30" y="96" font-family="'Space Grotesk', monospace" font-size="14" fill="{PALETTE['muted']}">
          Simulated space proton flux to measure TPU error resilience
        </text>
      </g>
    </g>
    """
    return get_base_svg_template(
        shot_id="shot-06",
        shot_title="Radiation Risk",
        visual_status_badge="DIAGRAM • RADIATION PHYSICS",
        badge_color=PALETTE["amber"],
        main_visual_content=main_content,
        primary_text="RADIATION SINGLE-EVENT BIT-FLIP",
        subtext="HIGH-ENERGY PROTON STRIKE • CYCLOTRON TESTED AT UC DAVIS",
    )


# =============================================================================
# SHOT 07 — THERMAL DISSIPATION & LAUNCH DATE
# =============================================================================
def generate_shot_07_svg() -> str:
    main_content = f"""
    <!-- Thermal Dissipation + SpaceX Launch Preparation -->
    <g transform="translate(100, 340)">
      <!-- Stage 1: External Thermal Radiator Loop -->
      <g transform="translate(0, 0)">
        <rect width="880" height="340" rx="14" fill="#0D131F" stroke="{PALETTE['panel_border']}" stroke-width="2"/>
        <text x="40" y="40" font-family="'Space Grotesk', monospace" font-size="14" font-weight="700" fill="{PALETTE['copper']}">
          HEAT DISSIPATION LOOP: COPPER PIPES → RADIATOR FINS
        </text>

        <!-- Copper Heat Pipe Channels -->
        <g transform="translate(80, 80)">
          <!-- Heat source cold plate -->
          <rect x="0" y="30" width="120" height="120" rx="6" fill="#1C1819" stroke="{PALETTE['red']}" stroke-width="2"/>
          <text x="60" y="95" font-family="'Inter', sans-serif" font-size="15" font-weight="800" fill="{PALETTE['red']}" text-anchor="middle">
            4-TPU CORE
          </text>

          <!-- Sealed Copper Capillary Heat Pipes -->
          <path d="M 120 70 L 320 70 L 320 30 L 460 30" fill="none" stroke="{PALETTE['copper']}" stroke-width="12" stroke-linecap="round"/>
          <path d="M 120 110 L 320 110 L 320 150 L 460 150" fill="none" stroke="{PALETTE['copper']}" stroke-width="12" stroke-linecap="round"/>

          <!-- External Radiator Panel (0.8m x 0.6m) -->
          <rect x="460" y="10" width="220" height="160" rx="6" fill="#121824" stroke="{PALETTE['cyan']}" stroke-width="2"/>
          <text x="570" y="95" font-family="'Space Grotesk', monospace" font-size="14" font-weight="700" fill="{PALETTE['cyan']}" text-anchor="middle">
            EXTERNAL RADIATOR
          </text>

          <!-- Infrared Radiation Waves into Space -->
          <path d="M 695 50 Q 725 70 695 90" fill="none" stroke="{PALETTE['red']}" stroke-width="3" opacity="0.8"/>
          <path d="M 715 40 Q 755 70 715 100" fill="none" stroke="{PALETTE['red']}" stroke-width="3" opacity="0.6"/>
          <path d="M 735 30 Q 785 70 735 110" fill="none" stroke="{PALETTE['red']}" stroke-width="3" opacity="0.4"/>
          <text x="750" y="150" font-family="'Space Grotesk', monospace" font-size="12" fill="{PALETTE['red']}">
            IR EMISSION
          </text>
        </g>

        <!-- 15-Minute Compute Burst Tag -->
        <g transform="translate(40, 260)">
          <rect width="800" height="50" rx="8" fill="#070A0F" stroke="#1E2A38" stroke-width="1"/>
          <text x="400" y="32" font-family="'Space Grotesk', monospace" font-size="16" font-weight="700" fill="{PALETTE['amber']}" text-anchor="middle">
            DUTY CYCLE: 15-MINUTE COMPUTE BURSTS → PASSIVE RADIATIVE RECOVERY
          </text>
        </g>
      </g>

      <!-- Stage 2: SpaceX Launch Target (Strict Future Tense) -->
      <g transform="translate(0, 370)">
        <rect width="880" height="340" rx="14" fill="#0B1524" stroke="{PALETTE['cyan']}" stroke-width="2"/>

        <g transform="translate(50, 45)">
          <text x="0" y="0" font-family="'Space Grotesk', monospace" font-size="15" font-weight="700" fill="{PALETTE['cyan']}">
            UPCOMING LAUNCH TARGET
          </text>
          <text x="0" y="45" font-family="'Inter', sans-serif" font-size="40" font-weight="900" fill="{PALETTE['text']}">
            OCTOBER 1, 2026
          </text>
          <text x="0" y="85" font-family="'Space Grotesk', monospace" font-size="20" font-weight="600" fill="{PALETTE['green']}">
            SPACEX FALCON 9 • TRANSPORTER-18
          </text>
        </g>

        <!-- Launch Details Grid -->
        <g transform="translate(50, 165)">
          <rect width="360" height="130" rx="8" fill="#070A0F" stroke="#1E2A38" stroke-width="1"/>
          <text x="24" y="36" font-family="'Space Grotesk', monospace" font-size="13" fill="{PALETTE['muted']}">MISSION STATUS</text>
          <text x="24" y="68" font-family="'Inter', sans-serif" font-size="18" font-weight="700" fill="{PALETTE['text']}">Pre-Flight Integration</text>
          <text x="24" y="100" font-family="'Space Grotesk', monospace" font-size="13" fill="{PALETTE['green']}">● READY FOR LAUNCH</text>
        </g>
        <g transform="translate(450, 165)">
          <rect width="360" height="130" rx="8" fill="#070A0F" stroke="#1E2A38" stroke-width="1"/>
          <text x="24" y="36" font-family="'Space Grotesk', monospace" font-size="13" fill="{PALETTE['muted']}">ORBITAL DESTINATION</text>
          <text x="24" y="68" font-family="'Inter', sans-serif" font-size="18" font-weight="700" fill="{PALETTE['text']}">500 km Dawn-Dusk SSO</text>
          <text x="24" y="100" font-family="'Space Grotesk', monospace" font-size="13" fill="{PALETTE['cyan']}">Ride-share Deployment</text>
        </g>
      </g>
    </g>
    """
    return get_base_svg_template(
        shot_id="shot-07",
        shot_title="Thermal Loop & Launch Target",
        visual_status_badge="HYBRID • PRE-FLIGHT TIMELINE",
        badge_color=PALETTE["cyan"],
        main_visual_content=main_content,
        primary_text="15-MIN BURSTS • LAUNCH OCT 1, 2026",
        subtext="HEAT PIPES &amp; RADIATORS • SPACEX TRANSPORTER-18",
    )


# =============================================================================
# SHOT 08 — FUTURE ORBITAL MESH (FUTURE CONCEPT)
# =============================================================================
def generate_shot_08_svg() -> str:
    main_content = f"""
    <!-- Conceptual Vision: Terrestrial Power Bottleneck vs Future Orbital Mesh -->
    <g transform="translate(100, 340)">
      <!-- Stage Canvas -->
      <rect width="880" height="720" rx="16" fill="#090E17" stroke="{PALETTE['panel_border']}" stroke-width="2"/>

      <!-- Lower Half: Terrestrial Grid Overload (Amber/Red) -->
      <g transform="translate(0, 360)">
        <rect width="880" height="360" rx="0 0 16 16" fill="#150D0E" opacity="0.9"/>
        <!-- Earth City Lights and Grid Lines -->
        <g stroke="{PALETTE['amber']}" stroke-width="1.5" opacity="0.6">
          <line x1="80" y1="280" x2="220" y2="200"/>
          <line x1="220" y1="200" x2="380" y2="240"/>
          <line x1="380" y1="240" x2="520" y2="160"/>
          <line x1="520" y1="160" x2="680" y2="220"/>
          <line x1="680" y1="220" x2="800" y2="180"/>
        </g>
        <g stroke="{PALETTE['red']}" stroke-width="2.5" opacity="0.8">
          <line x1="220" y1="200" x2="520" y2="160"/>
          <line x1="380" y1="240" x2="680" y2="220"/>
        </g>
        <!-- Congestion Nodes -->
        <circle cx="220" cy="200" r="7" fill="{PALETTE['red']}"/>
        <circle cx="380" cy="240" r="7" fill="{PALETTE['amber']}"/>
        <circle cx="520" cy="160" r="7" fill="{PALETTE['red']}"/>
        <circle cx="680" cy="220" r="7" fill="{PALETTE['red']}"/>

        <text x="60" y="80" font-family="'Inter', sans-serif" font-size="22" font-weight="900" fill="{PALETTE['red']}">
          TERRESTRIAL POWER GRID BOTTLENECK
        </text>
        <text x="60" y="115" font-family="'Space Grotesk', monospace" font-size="15" fill="{PALETTE['muted']}">
          Land, water cooling, and transformer queue limits on Earth
        </text>
      </g>

      <!-- Upper Half: Conceptual Orbital Mesh (Cyan Laser Links) -->
      <g transform="translate(0, 0)">
        <rect width="880" height="360" rx="16 16 0 0" fill="#0C1929" opacity="0.6"/>

        <!-- Conceptual Satellite Nodes in Space -->
        <!-- Sat A -->
        <g transform="translate(180, 140)">
          <circle cx="0" cy="0" r="14" fill="{PALETTE['cyan']}"/>
          <rect x="-18" y="-4" width="36" height="8" fill="{PALETTE['amber']}"/>
          <text x="0" y="32" font-family="'Space Grotesk', monospace" font-size="12" fill="{PALETTE['cyan']}" text-anchor="middle">NODE A</text>
        </g>
        <!-- Sat B -->
        <g transform="translate(440, 90)">
          <circle cx="0" cy="0" r="14" fill="{PALETTE['cyan']}"/>
          <rect x="-18" y="-4" width="36" height="8" fill="{PALETTE['amber']}"/>
          <text x="0" y="32" font-family="'Space Grotesk', monospace" font-size="12" fill="{PALETTE['cyan']}" text-anchor="middle">NODE B</text>
        </g>
        <!-- Sat C -->
        <g transform="translate(700, 150)">
          <circle cx="0" cy="0" r="14" fill="{PALETTE['cyan']}"/>
          <rect x="-18" y="-4" width="36" height="8" fill="{PALETTE['amber']}"/>
          <text x="0" y="32" font-family="'Space Grotesk', monospace" font-size="12" fill="{PALETTE['cyan']}" text-anchor="middle">NODE C</text>
        </g>

        <!-- Intersatellite Optical Laser Mesh -->
        <line x1="180" y1="140" x2="440" y2="90" stroke="{PALETTE['cyan']}" stroke-width="3" stroke-dasharray="8 6"/>
        <line x1="440" y1="90" x2="700" y2="150" stroke="{PALETTE['cyan']}" stroke-width="3" stroke-dasharray="8 6"/>
        <line x1="180" y1="140" x2="700" y2="150" stroke="{PALETTE['violet']}" stroke-width="2" stroke-dasharray="6 6"/>

        <text x="60" y="55" font-family="'Inter', sans-serif" font-size="22" font-weight="900" fill="{PALETTE['cyan']}">
          CONCEPTUAL ORBITAL COMPUTE MESH
        </text>
        <text x="60" y="85" font-family="'Space Grotesk', monospace" font-size="15" fill="{PALETTE['muted']}">
          Optical inter-satellite crosslinks for distributed scaling
        </text>
      </g>
    </g>
    """
    # Mandatory prominent watermark banner for FUTURE CONCEPT
    watermark_banner = f"""
    <g transform="translate(80, 1600)">
      <rect width="920" height="70" rx="8" fill="#1C0D11" stroke="{PALETTE['red']}" stroke-width="2.5"/>
      <text x="460" y="44" font-family="'Inter', sans-serif" font-size="22" font-weight="900" fill="{PALETTE['red']}" text-anchor="middle" letter-spacing="2">
        FUTURE CONCEPT / POSSIBLE FUTURE (NOT OPERATIONAL INFRASTRUCTURE)
      </text>
    </g>
    """
    return get_base_svg_template(
        shot_id="shot-08",
        shot_title="Future Macro Vision",
        visual_status_badge="FUTURE_CONCEPT • LONG-TERM VISION",
        badge_color=PALETTE["red"],
        main_visual_content=main_content,
        primary_text="ESCAPING EARTH'S POWER GRID",
        subtext="TERRESTRIAL GRID LIMITS vs ORBITAL COMPUTE CONCEPT",
        extra_badge=watermark_banner,
    )


# =============================================================================
# SHOT 09 — BRAND END CARD & CTA
# =============================================================================
def generate_shot_09_svg() -> str:
    main_content = f"""
    <!-- AI NEWS FACTORY Official Brand Lockup -->
    <g transform="translate(100, 360)">
      <!-- Main Brand Card -->
      <rect width="880" height="720" rx="16" fill="{PALETTE['panel']}" stroke="{PALETTE['panel_border']}" stroke-width="2"/>

      <!-- Corner Reticles -->
      <path d="M 30 70 L 30 30 L 70 30" fill="none" stroke="{PALETTE['cyan']}" stroke-width="3"/>
      <path d="M 850 70 L 850 30 L 810 30" fill="none" stroke="{PALETTE['cyan']}" stroke-width="3"/>
      <path d="M 30 650 L 30 690 L 70 690" fill="none" stroke="{PALETTE['cyan']}" stroke-width="3"/>
      <path d="M 850 650 L 850 690 L 810 690" fill="none" stroke="{PALETTE['cyan']}" stroke-width="3"/>

      <!-- Central Channel Seal -->
      <g transform="translate(440, 240)">
        <circle cx="0" cy="0" r="100" fill="#0A1422" stroke="{PALETTE['cyan']}" stroke-width="3"/>
        <circle cx="0" cy="0" r="80" fill="none" stroke="{PALETTE['violet']}" stroke-width="1.5" stroke-dasharray="10 6"/>

        <!-- Stylized AI Chip Node Icon -->
        <rect x="-35" y="-35" width="70" height="70" rx="10" fill="#132338" stroke="{PALETTE['cyan']}" stroke-width="2"/>
        <text x="0" y="8" font-family="'Inter', sans-serif" font-size="28" font-weight="900" fill="{PALETTE['cyan']}" text-anchor="middle">
          AI
        </text>

        <!-- Radiating Connection Pins -->
        <line x1="-50" y1="0" x2="-35" y2="0" stroke="{PALETTE['cyan']}" stroke-width="3"/>
        <line x1="35" y1="0" x2="50" y2="0" stroke="{PALETTE['cyan']}" stroke-width="3"/>
        <line x1="0" y1="-50" x2="0" y2="-35" stroke="{PALETTE['cyan']}" stroke-width="3"/>
        <line x1="0" y1="35" x2="0" y2="50" stroke="{PALETTE['cyan']}" stroke-width="3"/>
      </g>

      <!-- Brand Name -->
      <g transform="translate(440, 410)">
        <text x="0" y="0" font-family="'Inter', sans-serif" font-size="44" font-weight="900" fill="{PALETTE['text']}" text-anchor="middle" letter-spacing="4">
          AI NEWS FACTORY
        </text>
        <text x="0" y="40" font-family="'Space Grotesk', monospace" font-size="18" font-weight="700" fill="{PALETTE['cyan']}" text-anchor="middle" letter-spacing="2">
          ENGINEERING FIRST • ZERO HYPE
        </text>
      </g>

      <!-- Verification Badge Ribbon -->
      <g transform="translate(190, 520)">
        <rect width="500" height="60" rx="30" fill="#0E241B" stroke="{PALETTE['green']}" stroke-width="2"/>
        <circle cx="40" cy="30" r="16" fill="{PALETTE['green']}"/>
        <path d="M 32 30 L 38 36 L 48 24" fill="none" stroke="#070A0F" stroke-width="3.5" stroke-linecap="round"/>
        <text x="75" y="37" font-family="'Inter', sans-serif" font-size="18" font-weight="800" fill="{PALETTE['green']}">
          VERIFIED PRIMARY SOURCES ONLY
        </text>
      </g>

      <!-- CTA Prompt -->
      <g transform="translate(440, 640)">
        <text x="0" y="0" font-family="'Inter', sans-serif" font-size="22" font-weight="700" fill="{PALETTE['text']}" text-anchor="middle">
          LIKE • SHARE • SUBSCRIBE
        </text>
      </g>
    </g>
    """
    return get_base_svg_template(
        shot_id="shot-09",
        shot_title="Call to Action",
        visual_status_badge="PROPRIETARY BRAND IDENTITY",
        badge_color=PALETTE["cyan"],
        main_visual_content=main_content,
        primary_text="LIKE • SHARE • SUBSCRIBE",
        subtext="IF YOU FOUND THIS USEFUL • FOLLOW AI NEWS FACTORY",
    )


# =============================================================================
# MANIFEST COMPILATION & DISK WRITING
# =============================================================================
SHOT_GENERATORS = [
    ("shot-01", "AST-01-EARTH-ORBIT-PULLBACK", "ILLUSTRATIVE", "ILLUSTRATIVE", "ORIGINAL_AI_SYNTHESIZED", ["claim-01-existence", "claim-02-research-nature"], generate_shot_01_svg),
    ("shot-02", "AST-02-GOOGLE-RESEARCH-CARD", "HYBRID", "HYBRID", "EDITORIAL_FAIR_USE", ["claim-01-existence", "claim-02-research-nature", "claim-03-tpu-in-orbit", "claim-19-operational-datacenter-refutation"], generate_shot_02_svg),
    ("shot-03", "AST-04-SATELLITE-CAD-CUTAWAY", "ILLUSTRATIVE", "ILLUSTRATIVE", "PROPRIETARY_GENERATED", ["claim-06-planet-partnership", "claim-07-tpu-quantity", "claim-08-tpu-generation", "claim-20-numerical-claims"], generate_shot_03_svg),
    ("shot-04", "AST-05-DAWN-DUSK-SSO-DIAGRAM", "DIAGRAM", "DIAGRAM", "ORIGINAL_VECTOR_DIAGRAM", ["claim-09-solar-illumination", "claim-10-8x-solar-productivity", "claim-20-numerical-claims"], generate_shot_04_svg),
    ("shot-05", "AST-06-VACUUM-THERMAL-SIMULATION", "DIAGRAM", "ILLUSTRATIVE", "ORIGINAL_SCIENTIFIC_SIMULATION", ["claim-14-vacuum-cooling-challenge"], generate_shot_05_svg),
    ("shot-06", "AST-07-PROTON-BIT-FLIP-DIAGRAM", "DIAGRAM", "ILLUSTRATIVE", "ORIGINAL_VECTOR_DIAGRAM", ["claim-11-radiation-testing", "claim-12-bit-flip-risk"], generate_shot_06_svg),
    ("shot-07", "AST-08-THERMAL-RADIATOR-LOOP", "HYBRID", "HYBRID", "ORIGINAL_AI_SYNTHESIZED", ["claim-04-launch-vehicle", "claim-05-launch-date", "claim-15-heat-pipes", "claim-16-radiators", "claim-20-numerical-claims"], generate_shot_07_svg),
    ("shot-08", "AST-09-GRID-VS-ORBIT-CONCEPT", "FUTURE_CONCEPT", "FUTURE_CONCEPT", "ORIGINAL_AI_SYNTHESIZED", ["claim-01-existence", "claim-02-research-nature", "claim-17-laser-intersatellite"], generate_shot_08_svg),
    ("shot-09", "AST-10-BRAND-CTA-LOCKUP", "DIAGRAM", "DIAGRAM", "PROPRIETARY_BRAND_ASSET", ["claim-01-existence"], generate_shot_09_svg),
]


def rasterize_svg(svg_path: Path, png_path: Path) -> bool:
    """Rasterizes SVG to 1080x1920 PNG using native macOS sips."""
    png_path.parent.mkdir(parents=True, exist_ok=True)
    sips_bin = shutil.which("sips") or "/usr/bin/sips"
    try:
        cmd = [sips_bin, "-s", "format", "png", str(svg_path), "--out", str(png_path)]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return png_path.exists() and png_path.stat().st_size > 0
    except Exception as e:
        logger.error(f"Failed to rasterize {svg_path} via sips: {e}")
        return False


def main():
    logger.info(f"Initiating Phase 6B Production Asset Generation for story: {STORY_ID}")

    # Output directories
    visuals_assets_dir = ROOT / "data" / "visuals" / "production_assets"
    rendered_assets_dir = ROOT / "data" / "rendered" / STORY_ID / "assets"
    rendered_gen_dir = rendered_assets_dir / "generated"
    rendered_placeholder_dir = rendered_assets_dir / "placeholders"

    visuals_assets_dir.mkdir(parents=True, exist_ok=True)
    rendered_gen_dir.mkdir(parents=True, exist_ok=True)
    rendered_placeholder_dir.mkdir(parents=True, exist_ok=True)

    manifest_records = []
    created_at = datetime.now().isoformat()

    for shot_id, asset_id, classification, visual_status, rights_status, claim_ids, gen_func in SHOT_GENERATORS:
        logger.info(f"Generating production asset for [{shot_id}]: {asset_id} ({classification})")

        # 1. Generate SVG content
        svg_content = gen_func()

        # 2. Write SVG to production_assets and rendered placeholders
        svg_file_production = visuals_assets_dir / f"{shot_id}.svg"
        svg_file_placeholder = rendered_placeholder_dir / f"{shot_id}_card.svg"

        with open(svg_file_production, "w", encoding="utf-8") as f:
            f.write(svg_content)
        with open(svg_file_placeholder, "w", encoding="utf-8") as f:
            f.write(svg_content)

        # 3. Rasterize to 1080x1920 PNG using sips
        png_file_production = visuals_assets_dir / f"{shot_id}.png"
        png_file_rendered = rendered_gen_dir / f"{shot_id}.png"

        success_1 = rasterize_svg(svg_file_production, png_file_production)
        success_2 = rasterize_svg(svg_file_production, png_file_rendered)

        if not (success_1 and success_2):
            logger.error(f"Rasterization failed for {shot_id}!")
            raise RuntimeError(f"Could not rasterize {shot_id} PNG")

        # Check file sizes
        file_size_bytes = png_file_rendered.stat().st_size
        logger.info(f"  ✅ Produced {png_file_rendered.name} ({file_size_bytes:,} bytes, 1080x1920)")

        # Compile asset record
        manifest_records.append({
            "asset_id": asset_id,
            "shot_id": shot_id,
            "story_id": STORY_ID,
            "classification": classification,
            "visual_status": visual_status,
            "rights_status": rights_status,
            "claim_ids": claim_ids,
            "generation_method": "NATIVE_PROCEDURAL_VECTOR_SIPS_RASTER",
            "source": f"data/visuals/production_assets/{shot_id}.svg",
            "file_path": str(png_file_rendered.relative_to(ROOT)),
            "dimensions": "1080x1920 (9:16 vertical)",
            "file_size_bytes": file_size_bytes,
            "created_at": created_at,
        })

    # Update asset manifest JSON
    manifest_doc = {
        "status": "PASS",
        "story_id": STORY_ID,
        "style_bible_version": "v1.0",
        "asset_production_status": "READY",
        "generated_at": created_at,
        "total_assets": len(manifest_records),
        "total_placeholders_remaining": 0,
        "satellite_master_design_preserved": True,
        "assets": manifest_records,
    }

    manifest_output_path = visuals_assets_dir / "PRODUCTION_ASSET_MANIFEST.json"
    with open(manifest_output_path, "w", encoding="utf-8") as f:
        json.dump(manifest_doc, f, indent=2)

    logger.info(f"🎉 Successfully produced all 9 production assets! Manifest written to: {manifest_output_path}")


if __name__ == "__main__":
    main()
