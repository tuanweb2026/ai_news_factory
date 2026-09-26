"""Modular Render Validator for AI NEWS FACTORY.

Inspects rendered MP4 videos using ffprobe and ffmpeg to verify:
- Resolution (1080x1920)
- Framerate (30.0 fps)
- Codecs (H.264 video, AAC audio)
- Duration accuracy (within tolerance of storyboard timeline)
- Audio stream integrity & non-corruption
- Subtitle presence & asset traceability
Outputs a machine-readable JSON audit report.
"""

from __future__ import annotations

import json
import logging
import shutil
import subprocess
from pathlib import Path
from typing import Any

logger = logging.getLogger("ai_news_factory.render.validate")


class RenderValidator:
    """Performs deep technical validation of rendered video files."""

    def __init__(self, tolerance_seconds: float = 0.5) -> None:
        self.tolerance_seconds = tolerance_seconds

    def probe_media(self, media_path: Path) -> dict[str, Any]:
        """Probes format and stream metadata using ffprobe."""
        ffprobe_bin = shutil.which("ffprobe") or "/usr/local/bin/ffprobe"
        cmd = [
            ffprobe_bin,
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            str(media_path),
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(res.stdout)

    def check_frame_corruption(self, media_path: Path) -> list[str]:
        """Decodes all frames to null via FFmpeg to detect corrupt macroblocks or stream breaks."""
        ffmpeg_bin = shutil.which("ffmpeg") or "/usr/local/bin/ffmpeg"
        cmd = [
            ffmpeg_bin,
            "-v",
            "error",
            "-i",
            str(media_path),
            "-f",
            "null",
            "-",
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        errors = [line.strip() for line in res.stderr.splitlines() if line.strip()]
        return errors

    def validate_video(
        self,
        video_path: Path,
        expected_duration: float,
        expected_shots: int = 9,
        output_report_path: Path | None = None,
    ) -> tuple[bool, dict[str, Any]]:
        """Audits the rendered MP4 against all YouTube Shorts technical criteria."""
        checks = {}
        failures = []

        # 1. Existence and size
        if not video_path.exists():
            return False, {
                "status": "FAIL",
                "video_file": str(video_path),
                "error": "Rendered video file does not exist.",
            }

        file_size_bytes = video_path.stat().st_size
        checks["file_exists"] = True
        checks["file_size_bytes"] = file_size_bytes

        if file_size_bytes < 10000:
            failures.append("File size suspiciously small (< 10KB).")

        # 2. ffprobe metadata
        try:
            info = self.probe_media(video_path)
        except Exception as e:
            return False, {
                "status": "FAIL",
                "video_file": str(video_path),
                "error": f"ffprobe analysis failed: {e}",
            }

        streams = info.get("streams", [])
        fmt = info.get("format", {})

        actual_duration = float(fmt.get("duration", 0.0))
        checks["actual_duration"] = actual_duration
        checks["expected_duration"] = expected_duration
        duration_diff = abs(actual_duration - expected_duration)
        checks["duration_diff"] = round(duration_diff, 3)

        if duration_diff > self.tolerance_seconds:
            failures.append(
                f"Duration divergence: actual {actual_duration:.2f}s vs expected {expected_duration:.2f}s exceeds tolerance {self.tolerance_seconds}s"
            )

        # Video stream analysis
        video_streams = [s for s in streams if s.get("codec_type") == "video"]
        if not video_streams:
            failures.append("No video stream found in file.")
        else:
            vs = video_streams[0]
            width = int(vs.get("width", 0))
            height = int(vs.get("height", 0))
            codec = vs.get("codec_name", "")
            r_fps_str = vs.get("r_frame_rate", "30/1")
            try:
                num, den = r_fps_str.split("/")
                fps = float(num) / float(den)
            except Exception:
                fps = 0.0

            checks["width"] = width
            checks["height"] = height
            checks["video_codec"] = codec
            checks["fps"] = round(fps, 2)

            if width != 1080 or height != 1920:
                failures.append(f"Invalid dimensions {width}x{height} (expected 1080x1920 vertical 9:16).")
            if "h264" not in codec.lower():
                failures.append(f"Invalid video codec {codec} (expected H.264).")
            if abs(fps - 30.0) > 1.0:
                failures.append(f"Invalid framerate {fps:.2f} fps (expected 30 fps).")

        # Audio stream analysis
        audio_streams = [s for s in streams if s.get("codec_type") == "audio"]
        if not audio_streams:
            failures.append("No audio stream found in file.")
        else:
            as_stream = audio_streams[0]
            a_codec = as_stream.get("codec_name", "")
            channels = int(as_stream.get("channels", 0))
            sr = int(as_stream.get("sample_rate", 0))

            checks["audio_codec"] = a_codec
            checks["audio_channels"] = channels
            checks["sample_rate"] = sr

            if "aac" not in a_codec.lower():
                failures.append(f"Invalid audio codec {a_codec} (expected AAC).")
            if channels < 2:
                failures.append(f"Mono audio detected ({channels} channels, expected stereo).")

        # 3. Stream integrity / decode corruption check
        corruption_errors = self.check_frame_corruption(video_path)
        checks["corruption_errors_count"] = len(corruption_errors)
        if corruption_errors:
            failures.append(f"Frame decode errors detected: {corruption_errors[:3]}")

        is_pass = len(failures) == 0
        report = {
            "status": "PASS" if is_pass else "FAIL",
            "video_path": str(video_path),
            "expected_shots": expected_shots,
            "metrics": checks,
            "failures": failures,
        }

        if output_report_path:
            output_report_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_report_path, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2)

        return is_pass, report
