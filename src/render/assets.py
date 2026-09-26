"""Modular Asset Engine for AI NEWS FACTORY.

Parses asset manifests and storyboards into a verified, deterministic asset registry.
Distinguishes classifications (ILLUSTRATIVE, DIAGRAM, SCREENSHOT, HYBRID, FUTURE_CONCEPT),
enforces intellectual property and rights boundaries, generates procedural SVG visual cards
compliant with AI News Visual Style Bible v1.0, and manages placeholder assets.
"""

from __future__ import annotations

import html
import json
import logging
import shutil
import subprocess
from pathlib import Path
from typing import Any

logger = logging.getLogger("ai_news_factory.render.assets")


class AssetEngine:
    """Manages visual asset discovery, rights validation, deterministic SVG cards, and registry generation."""

    CONTROLLED_CLASSIFICATIONS = {
        "OFFICIAL_SOURCE",
        "SCREENSHOT",
        "GENERATED",
        "DIAGRAM",
        "HYBRID",
        "ILLUSTRATIVE",
        "FUTURE_CONCEPT",
    }

    UNRESOLVED_RIGHTS_STATUSES = {
        "RIGHTS_REVIEW_REQUIRED",
        "UNKNOWN",
        "UNRESOLVED",
        "PENDING_CLEARANCE",
    }

    STYLE_PALETTE = {
        "canvas": "#070A0F",
        "panel": "#0D121A",
        "text": "#F3F7FA",
        "muted": "#8B98A7",
        "cyan": "#4DEBFF",
        "violet": "#9B7CFF",
        "red": "#FF5C70",
        "green": "#54E39A",
    }

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        self.config = config or {}

    def build_registry(
        self,
        manifest_data: dict[str, Any],
        storyboard_data: dict[str, Any],
        output_dir: Path,
    ) -> dict[str, Any]:
        """Builds a deterministic asset registry, validating rights and creating placeholder specs."""
        output_dir.mkdir(parents=True, exist_ok=True)
        assets_catalog = manifest_data.get("assets", [])
        storyboard_shots = storyboard_data.get("shots", [])

        asset_map = {a.get("asset_id"): a for a in assets_catalog if "asset_id" in a}

        registry_entries = []
        unresolved_rights_found = []
        shots_summary = []

        for shot in storyboard_shots:
            shot_id = shot.get("shot_id", "shot-00")
            shot_type = shot.get("shot_type", "SYSTEM_WIDE")
            visual_status = shot.get("visual_status", "ILLUSTRATIVE")
            on_screen_text = shot.get("text", "")
            voice_text = shot.get("voiceover_segment", "")
            duration = float(shot.get("end", 0.0)) - float(shot.get("start", 0.0))

            shot_assets = []
            for asset_spec in shot.get("asset_plan", []):
                asset_id = asset_spec.get("asset_id")
                asset_info = asset_map.get(asset_id, {})

                classification = asset_info.get("asset_classification") or asset_spec.get("asset_type", "ILLUSTRATIVE")
                rights_status = asset_info.get("rights_status") or asset_spec.get("rights_status", "UNKNOWN")

                # Rights Gate: Check for unresolved third-party rights
                if rights_status in self.UNRESOLVED_RIGHTS_STATUSES:
                    unresolved_rights_found.append({
                        "shot_id": shot_id,
                        "asset_id": asset_id,
                        "rights_status": rights_status,
                        "notes": "Third-party asset has unresolved copyright status.",
                    })

                # Resolve physical asset path or planned placeholder
                asset_file_name = f"{shot_id}.png"
                local_asset_path = output_dir / "generated" / asset_file_name
                placeholder_path = output_dir / "placeholders" / f"{shot_id}_card.svg"

                is_ready = local_asset_path.exists()
                status = "READY" if is_ready else "PLACEHOLDER"

                entry = {
                    "asset_id": asset_id or f"AST-{shot_id.upper()}",
                    "shot_id": shot_id,
                    "classification": classification,
                    "visual_status": visual_status,
                    "rights_status": rights_status,
                    "status": status,
                    "local_path": str(local_asset_path) if is_ready else str(placeholder_path),
                    "is_documentary": False if classification in ("ILLUSTRATIVE", "FUTURE_CONCEPT", "GENERATED", "DIAGRAM") else True,
                    "watermark_required": True if (visual_status == "FUTURE_CONCEPT" or classification == "FUTURE_CONCEPT") else False,
                    "watermark_text": "FUTURE CONCEPT / POSSIBLE FUTURE (NOT OPERATIONAL INFRASTRUCTURE)" if (visual_status == "FUTURE_CONCEPT" or classification == "FUTURE_CONCEPT") else None,
                    "prompt": asset_spec.get("prompt") or asset_info.get("prompt"),
                    "attribution": asset_spec.get("attribution") or asset_info.get("attribution_text"),
                }
                shot_assets.append(entry)
                registry_entries.append(entry)

            shots_summary.append({
                "shot_id": shot_id,
                "shot_type": shot_type,
                "duration": duration,
                "visual_status": visual_status,
                "on_screen_text": on_screen_text,
                "assets": shot_assets,
            })

        registry_doc = {
            "story_id": manifest_data.get("story_id") or storyboard_data.get("story_id", "unknown"),
            "style_bible_version": "v1.0",
            "registry_status": "BLOCKED" if unresolved_rights_found else "READY",
            "unresolved_rights_blockers": unresolved_rights_found,
            "total_shots": len(storyboard_shots),
            "total_assets_registered": len(registry_entries),
            "shots": shots_summary,
            "assets": registry_entries,
        }

        registry_file = output_dir / "asset_registry.json"
        with open(registry_file, "w", encoding="utf-8") as f:
            json.dump(registry_doc, f, indent=2)

        return registry_doc

    def generate_procedural_svg_card(
        self,
        shot_data: dict[str, Any],
        output_svg_path: Path,
        story_title: str = "PROJECT SUNCATCHER",
    ) -> Path:
        """Generates a high-precision 1080x1920 SVG graphic card adhering to Style Bible v1.0."""
        output_svg_path.parent.mkdir(parents=True, exist_ok=True)

        shot_id = shot_data.get("shot_id", "SHOT").upper()
        shot_type = shot_data.get("shot_type", "TECHNICAL EXPLAINER")
        on_screen_text = shot_data.get("text") or shot_data.get("on_screen_text", "")
        visual_status = shot_data.get("visual_status", "ILLUSTRATIVE")
        diagram_elements = shot_data.get("diagram_elements", "")

        is_future_concept = "FUTURE_CONCEPT" in visual_status or "FUTURE CONCEPT" in on_screen_text

        # Sanitize text
        text_safe = html.escape(on_screen_text)
        subtext_safe = html.escape(diagram_elements[:120] + ("..." if len(diagram_elements) > 120 else ""))
        shot_title_safe = html.escape(f"{shot_id} • {shot_type}")

        watermark_block = ""
        if is_future_concept:
            watermark_block = f"""
            <rect x="140" y="1520" width="800" height="64" rx="8" fill="{self.STYLE_PALETTE['panel']}" stroke="{self.STYLE_PALETTE['red']}" stroke-width="2"/>
            <text x="540" y="1562" font-family="Inter, sans-serif" font-size="22" font-weight="700" fill="{self.STYLE_PALETTE['red']}" text-anchor="middle" letter-spacing="2">
              FUTURE CONCEPT • NOT OPERATIONAL INFRASTRUCTURE
            </text>
            """

        svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920" width="1080" height="1920">
  <defs>
    <radialGradient id="spaceGlow" cx="50%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#0E1E2E" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="{self.STYLE_PALETTE['canvas']}" stop-opacity="1"/>
    </radialGradient>
    <linearGradient id="cyanLine" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{self.STYLE_PALETTE['cyan']}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{self.STYLE_PALETTE['cyan']}" stop-opacity="1"/>
      <stop offset="100%" stop-color="{self.STYLE_PALETTE['cyan']}" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <!-- Background Void -->
  <rect width="1080" height="1920" fill="{self.STYLE_PALETTE['canvas']}"/>
  <rect width="1080" height="1920" fill="url(#spaceGlow)"/>

  <!-- Technical Background Grid -->
  <g stroke="#131B26" stroke-width="1" opacity="0.6">
    <line x1="80" y1="0" x2="80" y2="1920"/>
    <line x1="540" y1="0" x2="540" y2="1920"/>
    <line x1="1000" y1="0" x2="1000" y2="1920"/>
    <line x1="0" y1="240" x2="1080" y2="240"/>
    <line x1="0" y1="640" x2="1080" y2="640"/>
    <line x1="0" y1="1280" x2="1080" y2="1280"/>
    <line x1="0" y1="1680" x2="1080" y2="1680"/>
  </g>

  <!-- Header Section (Top Safe Zone) -->
  <g transform="translate(80, 160)">
    <text x="0" y="0" font-family="Inter, sans-serif" font-size="24" font-weight="700" fill="{self.STYLE_PALETTE['cyan']}" letter-spacing="3">
      AI NEWS FACTORY
    </text>
    <text x="920" y="0" font-family="Space Grotesk, sans-serif" font-size="20" font-weight="500" fill="{self.STYLE_PALETTE['muted']}" text-anchor="end">
      {html.escape(story_title)}
    </text>
    <line x1="0" y1="20" x2="920" y2="20" stroke="url(#cyanLine)" stroke-width="2"/>
  </g>

  <!-- Shot Identification -->
  <g transform="translate(540, 480)">
    <rect x="-240" y="-36" width="480" height="52" rx="26" fill="{self.STYLE_PALETTE['panel']}" stroke="{self.STYLE_PALETTE['cyan']}" stroke-width="1.5"/>
    <text x="0" y="0" font-family="Inter, sans-serif" font-size="22" font-weight="700" fill="{self.STYLE_PALETTE['cyan']}" text-anchor="middle" dominant-baseline="central" letter-spacing="2">
      {shot_title_safe}
    </text>
  </g>

  <!-- Primary Focal Graphic Panel (Upper-Middle Safe Zone) -->
  <g transform="translate(100, 580)">
    <rect width="880" height="680" rx="16" fill="{self.STYLE_PALETTE['panel']}" stroke="#1E2A38" stroke-width="2"/>

    <!-- Accent Corner Brackets -->
    <path d="M 0 40 L 0 0 L 40 0" fill="none" stroke="{self.STYLE_PALETTE['cyan']}" stroke-width="4"/>
    <path d="M 880 40 L 880 0 L 840 0" fill="none" stroke="{self.STYLE_PALETTE['cyan']}" stroke-width="4"/>
    <path d="M 0 640 L 0 680 L 40 680" fill="none" stroke="{self.STYLE_PALETTE['cyan']}" stroke-width="4"/>
    <path d="M 880 640 L 880 680 L 840 680" fill="none" stroke="{self.STYLE_PALETTE['cyan']}" stroke-width="4"/>

    <!-- Central Primary Card Text -->
    <text x="440" y="310" font-family="Inter, sans-serif" font-size="56" font-weight="900" fill="{self.STYLE_PALETTE['text']}" text-anchor="middle" letter-spacing="1">
      {text_safe}
    </text>

    <!-- Visual Subtext / Diagram Cue -->
    <text x="440" y="400" font-family="Inter, sans-serif" font-size="26" font-weight="500" fill="{self.STYLE_PALETTE['muted']}" text-anchor="middle">
      {subtext_safe}
    </text>
  </g>

  <!-- Watermark / Legal Guardrail -->
  {watermark_block}

  <!-- Footer Channel Stamp -->
  <g transform="translate(540, 1800)">
    <text x="0" y="0" font-family="Inter, sans-serif" font-size="20" font-weight="600" fill="{self.STYLE_PALETTE['muted']}" text-anchor="middle" letter-spacing="1.5">
      AI TECH EXPLAINER • VERIFIED EVIDENCE FIRST
    </text>
  </g>
</svg>
"""
        with open(output_svg_path, "w", encoding="utf-8") as f:
            f.write(svg_content)

        return output_svg_path

    def rasterize_svg_to_png(self, svg_path: Path, png_path: Path) -> Path:
        """Rasterizes SVG to 1080x1920 PNG using native macOS sips, FFmpeg, or Chrome."""
        png_path.parent.mkdir(parents=True, exist_ok=True)

        # 1. Primary on macOS: native sips (Apple CoreGraphics vector engine)
        sips_bin = shutil.which("sips") or "/usr/bin/sips"
        if Path(sips_bin).exists():
            try:
                cmd_sips = [sips_bin, "-s", "format", "png", str(svg_path), "--out", str(png_path)]
                res = subprocess.run(cmd_sips, capture_output=True, text=True)
                if res.returncode == 0 and png_path.exists() and png_path.stat().st_size > 0:
                    return png_path
            except Exception as e:
                logger.warning(f"sips rasterization failed ({e}), trying FFmpeg...")

        # 2. Attempt FFmpeg native SVG rasterization
        ffmpeg_bin = shutil.which("ffmpeg") or "/usr/local/bin/ffmpeg"
        try:
            cmd = [
                ffmpeg_bin,
                "-y",
                "-i",
                str(svg_path),
                "-vf",
                "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
                str(png_path),
            ]
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            return png_path
        except Exception as e:
            logger.warning(f"FFmpeg SVG rasterization failed ({e}), attempting Chrome headless...")

        # Fallback: Chrome Headless
        chrome_bin = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        if Path(chrome_bin).exists():
            with tempfile.TemporaryDirectory() as user_data_dir:
                cmd_chrome = [
                    chrome_bin,
                    "--headless=new",
                    "--disable-gpu",
                    f"--user-data-dir={user_data_dir}",
                    "--window-size=1080,1920",
                    f"--screenshot={png_path}",
                    f"file://{svg_path.resolve()}",
                ]
                subprocess.run(cmd_chrome, capture_output=True, text=True, check=True)
                return png_path

        raise RuntimeError(f"Failed to rasterize SVG {svg_path} to PNG {png_path}")
