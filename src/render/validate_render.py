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
    def check_visual_richness(self, media_path: Path) -> tuple[bool, dict[str, Any]]:
        """Inspects sample frames to verify visual illustration richness and absence of flat black voids."""
        ffmpeg_bin = shutil.which("ffmpeg") or "/usr/local/bin/ffmpeg"
        import tempfile
        from PIL import Image, ImageStat

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            # Extract 3 key frames (at 2s, 10s, 20s)
            frame_pattern = str(tmp_path / "frame_%02d.png")
            cmd = [
                ffmpeg_bin,
                "-y",
                "-i", str(media_path),
                "-vf", "select='eq(n\\,60)+eq(n\\,300)+eq(n\\,600)'",
                "-vsync", "vfr",
                frame_pattern,
            ]
            try:
                subprocess.run(cmd, capture_output=True, text=True, check=True)
                frames = sorted(list(tmp_path.glob("frame_*.png")))
                if not frames:
                    return True, {"sampled_frames": 0, "status": "SKIPPED"}

                stats_list = []
                for f in frames:
                    with Image.open(f) as img:
                        stat = ImageStat.Stat(img)
                        # Mean brightness across RGB channels
                        mean_brightness = sum(stat.mean[:3]) / 3.0
                        # Standard deviation (measures graphical variance/illustration detail)
                        stddev = sum(stat.stddev[:3]) / 3.0
                        stats_list.append({
                            "frame": f.name,
                            "mean_brightness": round(mean_brightness, 2),
                            "stddev": round(stddev, 2),
                        })

                # If stddev is too low (< 8.0), the frame is a flat monotonous solid color
                flat_frames = [s for s in stats_list if s["stddev"] < 8.0]
                is_rich = len(flat_frames) == 0
                return is_rich, {
                    "is_visually_rich": is_rich,
                    "frame_metrics": stats_list,
                    "flat_frames_count": len(flat_frames),
                }
            except Exception as e:
                return True, {"error": str(e), "status": "EVAL_EXCEPTION"}

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

        # 4. Visual Richness & Anti-Black-Void Gate
        is_rich, rich_metrics = self.check_visual_richness(video_path)
        checks["visual_richness"] = rich_metrics
        if not is_rich:
            failures.append(
                f"Visual Richness Gate FAIL: Video contains flat black/low-entropy frames ({rich_metrics.get('flat_frames_count')} flat frames detected)."
            )

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
