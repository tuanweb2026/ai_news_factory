"""Modular Subtitle Engine for AI NEWS FACTORY.

Generates standard SubRip (.srt) and Advanced SubStation Alpha (.ass) subtitles
from approved script shot timings, enforcing safe margins and maximum word count constraints
in strict accordance with AI News Visual Style Bible v1.0.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger("ai_news_factory.render.subtitles")


class SubtitleEngine:
    """Generates styled, mobile-safe SRT and ASS subtitle tracks from approved scripts."""

    DEFAULT_CONFIG: dict[str, Any] = {
        "max_words_per_card": 6,
        "font_name": "Inter",
        "font_size": 44,
        # ASS Color format: &HAABBGGRR (Alpha, Blue, Green, Red)
        # Primary #F3F7FA -> R=FA, G=F7, B=F3 -> &H00FAF7F3
        "primary_color": "&H00FAF7F3",
        # Secondary Accent #4DEBFF (Cyan) -> R=FF, G=EB, B=4D -> &H004DEBFF
        "accent_color": "&H004DEBFF",
        # Outline #070A0F -> R=0F, G=0A, B=07 -> &H000F0A07
        "outline_color": "&H000F0A07",
        # Shadow Semi-transparent black
        "shadow_color": "&H80000000",
        "outline_width": 3.0,
        "shadow_depth": 1.5,
        "margin_v": 240,  # Safe zone bottom margin clearing mobile UI overlay
        "margin_lr": 80,
    }

    def __init__(self, config: dict[str, Any] | None = None, config_path: Path | None = None) -> None:
        self.config = self._load_config(config, config_path)
        self.max_words_per_card = int(self.config.get("max_words_per_card", 6))
        self.font_name = self.config.get("font_name", "Inter")
        self.font_size = int(self.config.get("font_size", 44))
        self.primary_color = self.config.get("primary_color", "&H00FAF7F3")
        self.accent_color = self.config.get("accent_color", "&H004DEBFF")
        self.outline_color = self.config.get("outline_color", "&H000F0A07")
        self.shadow_color = self.config.get("shadow_color", "&H80000000")
        self.outline_width = float(self.config.get("outline_width", 3.0))
        self.shadow_depth = float(self.config.get("shadow_depth", 1.5))
        self.margin_v = int(self.config.get("margin_v", 240))
        self.margin_lr = int(self.config.get("margin_lr", 80))

    def _load_config(self, config: dict[str, Any] | None, config_path: Path | None) -> dict[str, Any]:
        """Loads subtitle parameters from factory.yaml or returns defaults."""
        if config is not None:
            return config

        target_path = config_path or Path(__file__).resolve().parents[2] / "config" / "factory.yaml"
        if target_path.exists():
            try:
                with open(target_path, "r", encoding="utf-8") as f:
                    root_cfg = yaml.safe_load(f) or {}
                render_cfg = root_cfg.get("render", {})
                sub_cfg = render_cfg.get("subtitles", {})
                merged = dict(self.DEFAULT_CONFIG)
                merged.update(sub_cfg)
                if "max_words_per_card" in render_cfg:
                    merged["max_words_per_card"] = render_cfg["max_words_per_card"]
                return merged
            except Exception as e:
                logger.warning(f"Could not parse subtitle config from {target_path}: {e}")

        return dict(self.DEFAULT_CONFIG)

    @staticmethod
    def format_timestamp_srt(seconds: float) -> str:
        """Formats floating-point seconds into standard SRT timestamp HH:MM:SS,mmm."""
        total_ms = int(round(seconds * 1000))
        hours = total_ms // 3600000
        rem = total_ms % 3600000
        mins = rem // 60000
        rem = rem % 60000
        secs = rem // 1000
        ms = rem % 1000
        return f"{hours:02d}:{mins:02d}:{secs:02d},{ms:03d}"

    @staticmethod
    def format_timestamp_ass(seconds: float) -> str:
        """Formats floating-point seconds into ASS timestamp H:MM:SS.cc (centiseconds)."""
        total_cs = int(round(seconds * 100))
        hours = total_cs // 360000
        rem = total_cs % 360000
        mins = rem // 6000
        rem = rem % 6000
        secs = rem // 100
        cs = rem % 100
        return f"{hours}:{mins:02d}:{secs:02d}.{cs:02d}"

    def extract_subtitle_cues(self, script_data: dict[str, Any], lang: str = "en") -> list[dict[str, Any]]:
        """Extracts subtitle events from shots, checking word limits without rewriting factual text."""
        shots = script_data.get("shots", [])
        if not shots:
            raise ValueError("Script data contains no 'shots' array.")

        cues = []
        is_vietnamese = lang.lower().startswith("vi")

        for idx, shot in enumerate(shots, start=1):
            start = float(shot.get("start", 0.0))
            end = float(shot.get("end", 0.0))

            if is_vietnamese and "vietnamese_voice" in shot:
                text = shot["vietnamese_voice"].strip()
            else:
                text = shot.get("voice", "").strip()

            on_screen_text = shot.get("on_screen_text", "").strip()
            # Count alphanumeric words, ignoring typographical divider symbols like '•' or '|'
            card_words = len([w for w in on_screen_text.split() if any(c.isalnum() for c in w)]) if on_screen_text else 0

            # Guardrail: on-screen text must not exceed maximum words per card
            if card_words > self.max_words_per_card:
                logger.warning(
                    f"Shot {shot.get('shot_id', idx)} on-screen text exceeds max words ({card_words} > {self.max_words_per_card}): '{on_screen_text}'"
                )

            cues.append({
                "index": idx,
                "shot_id": shot.get("shot_id", f"shot-{idx:02d}"),
                "start": start,
                "end": end,
                "voice_text": text,
                "on_screen_text": on_screen_text,
                "card_words": card_words,
            })

        return cues

    def generate_srt(self, script_data: dict[str, Any], output_path: Path, lang: str = "en") -> Path:
        """Generates a standard SubRip (.srt) subtitle file."""
        cues = self.extract_subtitle_cues(script_data, lang=lang)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        lines = []
        for cue in cues:
            start_str = self.format_timestamp_srt(cue["start"])
            end_str = self.format_timestamp_srt(cue["end"])
            lines.append(str(cue["index"]))
            lines.append(f"{start_str} --> {end_str}")
            lines.append(cue["voice_text"])
            lines.append("")

        content = "\n".join(lines).strip() + "\n"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        return output_path

    def generate_ass(self, script_data: dict[str, Any], output_path: Path, lang: str = "en") -> Path:
        """Generates a styled Advanced SubStation Alpha (.ass) subtitle file for 1080x1920 vertical video."""
        cues = self.extract_subtitle_cues(script_data, lang=lang)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        header = f"""[Script Info]
; Script generated by AI NEWS FACTORY Subtitle Engine v1.0
Title: {script_data.get("story_id", "AI Tech News Explainer")}
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{self.font_name},{self.font_size},{self.primary_color},{self.accent_color},{self.outline_color},{self.shadow_color},-1,0,0,0,100,100,0.5,0,1,{self.outline_width},{self.shadow_depth},2,{self.margin_lr},{self.margin_lr},{self.margin_v},1
Style: OnScreenCard,{self.font_name},52,{self.primary_color},{self.accent_color},{self.outline_color},{self.shadow_color},-1,0,0,0,100,100,1.0,0,1,3.5,2.0,8,{self.margin_lr},{self.margin_lr},480,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        events = []
        for cue in cues:
            start_str = self.format_timestamp_ass(cue["start"])
            end_str = self.format_timestamp_ass(cue["end"])

            # Clean narration subtitle (bottom-center safe zone, Style: Default)
            voice_escaped = cue["voice_text"].replace("\n", "\\N")
            events.append(f"Dialogue: 0,{start_str},{end_str},Default,,0,0,0,,{voice_escaped}")

        content = header + "\n".join(events) + "\n"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        return output_path

    def generate_all(self, script_data: dict[str, Any], output_dir: Path, lang: str = "en") -> dict[str, Path]:
        """Generates both SRT and ASS files in the specified output directory."""
        output_dir.mkdir(parents=True, exist_ok=True)
        code = "vi" if lang.lower().startswith("vi") else "en"
        srt_path = output_dir / f"{code}.srt"
        ass_path = output_dir / f"{code}.ass"

        self.generate_srt(script_data, srt_path, lang=lang)
        self.generate_ass(script_data, ass_path, lang=lang)

        return {"srt": srt_path, "ass": ass_path}

    def dry_run(self, script_data: dict[str, Any], output_dir: Path, lang: str = "en") -> dict[str, Any]:
        """Calculates subtitle manifest and validates word limits without writing to disk."""
        cues = self.extract_subtitle_cues(script_data, lang=lang)
        code = "vi" if lang.lower().startswith("vi") else "en"

        return {
            "status": "DRY_RUN",
            "language": lang,
            "target_srt": str(output_dir / f"{code}.srt"),
            "target_ass": str(output_dir / f"{code}.ass"),
            "total_cues": len(cues),
            "max_words_per_card_allowed": self.max_words_per_card,
            "cues": cues,
            "safe_margins": {
                "margin_v": self.margin_v,
                "margin_lr": self.margin_lr,
                "font": self.font_name,
                "size": self.font_size,
            },
        }
