"""Modular Audio Engine for AI NEWS FACTORY.

Synthesizes voice segments per shot using macOS native speech synthesis (`say`)
or configured TTS backends, preserves exact shot timing, normalizes audio to target LUFS,
and generates master voice tracks traceable to shot IDs.
"""

from __future__ import annotations

import json
import logging
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger("ai_news_factory.render.audio")


class AudioEngine:
    """Manages shot-level speech synthesis and master voice track assembly."""

    DEFAULT_CONFIG: dict[str, Any] = {
        "tts": {
            "backend": "macos_say",
            "english_voice": "Samantha",
            "vietnamese_voice": "Linh",
        },
        "sample_rate": 48000,
        "channels": 2,
        "target_lufs": -16,
        "ducking": {
            "enabled": True,
            "music_attenuation_db": -18,
            "sfx_attenuation_db": -6,
        },
    }

    def __init__(self, config: dict[str, Any] | None = None, config_path: Path | None = None) -> None:
        self.config = self._load_config(config, config_path)
        self.tts_config = self.config.get("tts", self.DEFAULT_CONFIG["tts"])
        self.sample_rate = int(self.config.get("sample_rate", self.DEFAULT_CONFIG["sample_rate"]))
        self.channels = int(self.config.get("channels", self.DEFAULT_CONFIG["channels"]))
        self.target_lufs = float(self.config.get("target_lufs", self.DEFAULT_CONFIG["target_lufs"]))

    def _load_config(self, config: dict[str, Any] | None, config_path: Path | None) -> dict[str, Any]:
        """Loads audio configuration from dict, factory.yaml, or fallback defaults."""
        if config is not None:
            return config

        target_path = config_path or Path(__file__).resolve().parents[2] / "config" / "factory.yaml"
        if target_path.exists():
            try:
                with open(target_path, "r", encoding="utf-8") as f:
                    root_cfg = yaml.safe_load(f) or {}
                if "audio" in root_cfg:
                    return root_cfg["audio"]
            except Exception as e:
                logger.warning(f"Could not parse config from {target_path}: {e}")

        return self.DEFAULT_CONFIG

    def get_voice_name(self, lang: str = "en") -> str:
        """Returns the configured voice name for the requested language."""
        if lang.lower().startswith("vi"):
            return self.tts_config.get("vietnamese_voice", "Linh")
        return self.tts_config.get("english_voice", "en-US-AriaNeural")

    def extract_shots(self, script_data: dict[str, Any], lang: str = "en") -> list[dict[str, Any]]:
        """Extracts shot voice segments and exact timestamps from script JSON."""
        shots = script_data.get("shots", [])
        if not shots:
            raise ValueError("Script data contains no 'shots' array.")

        extracted = []
        is_vietnamese = lang.lower().startswith("vi")

        for shot in shots:
            shot_id = shot.get("shot_id") or f"shot-{len(extracted) + 1:02d}"
            start = float(shot.get("start", 0.0))
            end = float(shot.get("end", 0.0))
            duration = max(0.0, end - start)

            if is_vietnamese and "vietnamese_voice" in shot:
                voice_text = shot["vietnamese_voice"]
            else:
                voice_text = shot.get("voice", "")

            extracted.append({
                "shot_id": shot_id,
                "start": start,
                "end": end,
                "duration": duration,
                "purpose": shot.get("purpose", ""),
                "voice_text": voice_text,
                "on_screen_text": shot.get("on_screen_text", ""),
                "fact_id": shot.get("fact_id", ""),
            })

        return extracted

    def synthesize_shot(
        self,
        shot_id: str,
        text: str,
        output_wav: Path,
        lang: str = "en",
        target_duration: float | None = None,
    ) -> Path:
        """Synthesizes a single voice segment using macOS `say` and formats to spec via FFmpeg."""
        output_wav.parent.mkdir(parents=True, exist_ok=True)
        if not text.strip():
            # Generate silent wav for empty text
            self._generate_silence(output_wav, duration=target_duration or 1.0)
            return output_wav

        voice = self.get_voice_name(lang)
        backend = self.tts_config.get("backend", "macos_say")

        if backend in ("microsoft_azure_speech", "edge_tts"):
            # Use Microsoft Azure Speech Neural via edge-tts or configured CLI
            edge_tts_bin = (
                shutil.which("edge-tts")
                or str(Path(__file__).resolve().parents[2] / ".venv" / "bin" / "edge-tts")
            )
            rate_val = self.tts_config.get("rate", "+26%")
            pitch_val = self.tts_config.get("pitch", "+0Hz")
            
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_mp3:
                tmp_mp3_path = Path(tmp_mp3.name)

            try:
                cmd_tts = [
                    edge_tts_bin,
                    "--voice", voice,
                    "--rate", str(rate_val),
                    "--pitch", str(pitch_val),
                    "--text", text,
                    "--write-media", str(tmp_mp3_path),
                ]
                subprocess.run(cmd_tts, capture_output=True, text=True, check=True)

                # Convert to target WAV specifications
                ffmpeg_bin = shutil.which("ffmpeg") or "/usr/local/bin/ffmpeg"
                cmd_ffmpeg = [
                    ffmpeg_bin,
                    "-y",
                    "-i", str(tmp_mp3_path),
                    "-ar", str(self.sample_rate),
                    "-ac", str(self.channels),
                    str(output_wav),
                ]
                subprocess.run(cmd_ffmpeg, capture_output=True, text=True, check=True)
            finally:
                if tmp_mp3_path.exists():
                    tmp_mp3_path.unlink()

            return output_wav

        elif backend == "macos_say":
            with tempfile.NamedTemporaryFile(suffix=".aiff", delete=False) as tmp_aiff:
                tmp_aiff_path = Path(tmp_aiff.name)

            try:
                # 1. Invoke /usr/bin/say
                say_bin = shutil.which("say") or "/usr/bin/say"
                cmd_say = [say_bin, "-v", voice, "-o", str(tmp_aiff_path), text]
                res = subprocess.run(cmd_say, capture_output=True, text=True, check=True)

                # 2. Convert to clean WAV with configured sample rate and channels
                ffmpeg_bin = shutil.which("ffmpeg") or "/usr/local/bin/ffmpeg"
                cmd_ffmpeg = [
                    ffmpeg_bin,
                    "-y",
                    "-i",
                    str(tmp_aiff_path),
                    "-ar",
                    str(self.sample_rate),
                    "-ac",
                    str(self.channels),
                    str(output_wav),
                ]
                subprocess.run(cmd_ffmpeg, capture_output=True, text=True, check=True)
            finally:
                if tmp_aiff_path.exists():
                    tmp_aiff_path.unlink()

            return output_wav
        else:
            raise NotImplementedError(f"TTS backend '{backend}' not implemented. Supported: 'microsoft_azure_speech', 'edge_tts', 'macos_say'.")

    def _generate_silence(self, output_wav: Path, duration: float) -> Path:
        """Generates silent WAV audio of specified duration."""
        ffmpeg_bin = shutil.which("ffmpeg") or "/usr/local/bin/ffmpeg"
        cmd = [
            ffmpeg_bin,
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"anullsrc=r={self.sample_rate}:cl=stereo",
            "-t",
            str(max(0.1, duration)),
            "-ar",
            str(self.sample_rate),
            "-ac",
            str(self.channels),
            str(output_wav),
        ]
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        return output_wav

    def get_audio_duration(self, audio_path: Path) -> float:
        """Measures exact duration in seconds using ffprobe."""
        ffprobe_bin = shutil.which("ffprobe") or "/usr/local/bin/ffprobe"
        cmd = [
            ffprobe_bin,
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(audio_path),
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(res.stdout.strip())

    def build_voice_track(
        self,
        script_data: dict[str, Any],
        output_dir: Path,
        lang: str = "en",
    ) -> tuple[Path, dict[str, Any]]:
        """Synthesizes all shots, places them precisely on the timeline, and normalizes master voice."""
        voice_dir = output_dir / "voice"
        voice_dir.mkdir(parents=True, exist_ok=True)

        shots = self.extract_shots(script_data, lang=lang)
        timing_records = []
        shot_files = []

        total_script_duration = max(shot["end"] for shot in shots) if shots else 35.0

        for shot in shots:
            shot_file = voice_dir / f"{shot['shot_id']}.wav"
            self.synthesize_shot(
                shot_id=shot["shot_id"],
                text=shot["voice_text"],
                output_wav=shot_file,
                lang=lang,
                target_duration=shot["duration"],
            )
            actual_duration = self.get_audio_duration(shot_file)
            shot_files.append((shot, shot_file, actual_duration))

            timing_records.append({
                "shot_id": shot["shot_id"],
                "start": shot["start"],
                "end": shot["end"],
                "target_duration": shot["duration"],
                "actual_duration": round(actual_duration, 3),
                "voice_text": shot["voice_text"],
                "file": str(shot_file.name),
            })

        # Save shot timing manifest
        timing_manifest_path = voice_dir / "shot_timing.json"
        with open(timing_manifest_path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "story_id": script_data.get("story_id", "unknown"),
                    "language": lang,
                    "voice": self.get_voice_name(lang),
                    "total_duration": total_script_duration,
                    "shots": timing_records,
                },
                f,
                indent=2,
            )

        # Assemble master timeline using silence padding and adelay/amix
        master_voice_unnorm = voice_dir / "voice_master_unnorm.wav"
        master_voice = voice_dir / "voice_master.wav"

        # Build FFmpeg complex filter to place each shot at its exact start offset
        filter_inputs = []
        filter_graphs = []
        mix_inputs = []

        ffmpeg_bin = shutil.which("ffmpeg") or "/usr/local/bin/ffmpeg"

        # Base background silence track
        base_cmd = [ffmpeg_bin, "-y"]
        base_cmd += ["-f", "lavfi", "-i", f"anullsrc=r={self.sample_rate}:cl=stereo", "-t", str(total_script_duration)]

        for i, (shot, shot_file, _) in enumerate(shot_files, start=1):
            base_cmd += ["-i", str(shot_file)]
            delay_ms = int(shot["start"] * 1000)
            filter_graphs.append(f"[{i}:a]adelay={delay_ms}|{delay_ms}[d{i}]")
            mix_inputs.append(f"[d{i}]")

        filter_graphs.append(f"[0:a]{''.join(mix_inputs)}amix=inputs={len(shot_files) + 1}:dropout_transition=0:normalize=0[aout]")
        filter_str = ";".join(filter_graphs)

        base_cmd += [
            "-filter_complex",
            filter_str,
            "-map",
            "[aout]",
            "-t",
            str(total_script_duration),
            "-ar",
            str(self.sample_rate),
            "-ac",
            str(self.channels),
            str(master_voice_unnorm),
        ]

        subprocess.run(base_cmd, capture_output=True, text=True, check=True)

        # Normalize audio using FFmpeg loudnorm filter
        norm_cmd = [
            ffmpeg_bin,
            "-y",
            "-i",
            str(master_voice_unnorm),
            "-af",
            f"loudnorm=I={self.target_lufs}:TP=-1.5:LRA=11",
            "-ar",
            str(self.sample_rate),
            "-ac",
            str(self.channels),
            str(master_voice),
        ]
        subprocess.run(norm_cmd, capture_output=True, text=True, check=True)

        if master_voice_unnorm.exists():
            master_voice_unnorm.unlink()

        return master_voice, {"status": "SUCCESS", "timing": timing_records, "voice_master": str(master_voice)}

    def dry_run(
        self,
        script_data: dict[str, Any],
        output_dir: Path,
        lang: str = "en",
    ) -> dict[str, Any]:
        """Calculates voice plan, timings, and generated commands without executing them."""
        shots = self.extract_shots(script_data, lang=lang)
        voice = self.get_voice_name(lang)
        total_duration = max(shot["end"] for shot in shots) if shots else 35.0

        plan = []
        for shot in shots:
            words = len(shot["voice_text"].split())
            wpm = round((words / max(0.1, shot["duration"])) * 60, 1)
            plan.append({
                "shot_id": shot["shot_id"],
                "start": shot["start"],
                "end": shot["end"],
                "duration": shot["duration"],
                "words": words,
                "estimated_wpm": wpm,
                "voice_text": shot["voice_text"],
                "simulated_output": str(output_dir / "voice" / f"{shot['shot_id']}.wav"),
            })

        return {
            "status": "DRY_RUN",
            "voice_configured": voice,
            "sample_rate": self.sample_rate,
            "channels": self.channels,
            "target_lufs": self.target_lufs,
            "total_shots": len(shots),
            "total_duration": total_duration,
            "shot_plan": plan,
            "master_voice_target": str(output_dir / "voice" / "voice_master.wav"),
            "ffmpeg_command_sample": f"ffmpeg -y -f lavfi -i anullsrc=r={self.sample_rate}:cl=stereo -t {total_duration} ... -af loudnorm=I={self.target_lufs}:TP=-1.5:LRA=11 {output_dir / 'voice' / 'voice_master.wav'}",
        }
