#!/usr/bin/env python3
"""Composites AUTOPILOT_SHORT.mp4 from generated PNG frames and master voice audio
using FFmpeg concat demuxer and validates technical output.
"""

import json
import shutil
import subprocess
from pathlib import Path
from src.render.validate_render import RenderValidator

def main():
    story_dir = Path("data/rendered/microsoft-copilot-autopilot-redesign-2026")
    video_dir = story_dir / "video"
    video_dir.mkdir(parents=True, exist_ok=True)
    
    output_mp4 = video_dir / "AUTOPILOT_SHORT.mp4"
    audio_wav = story_dir / "audio" / "voice" / "voice_master.wav"
    srt_path = story_dir / "subtitles" / "en.srt"
    assets_dir = Path("data/visuals/production_assets_autopilot")
    
    script_path = Path("data/scripts/MICROSOFT_AUTOPILOT_SHORT_SCRIPT_20260930.json")
    with open(script_path, "r", encoding="utf-8") as f:
        script_data = json.load(f)
        
    shots = script_data.get("shots", [])
    
    # Write concat list
    concat_txt = video_dir / "concat_list.txt"
    lines = []
    for shot in shots:
        shot_id = shot["shot_id"]
        shot_dur = shot["end"] - shot["start"]
        png_path = assets_dir.resolve() / f"{shot_id}.png"
        lines.append(f"file '{png_path}'")
        lines.append(f"duration {shot_dur:.2f}")
    
    # Repeat the last frame so the final duration is held
    if shots:
        last_id = shots[-1]["shot_id"]
        last_png = assets_dir.resolve() / f"{last_id}.png"
        lines.append(f"file '{last_png}'")
        
    with open(concat_txt, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
        
    print(f"Concat list written to {concat_txt}")
    
    ffmpeg_bin = shutil.which("ffmpeg") or "/usr/local/bin/ffmpeg"
    
    cmd = [
        ffmpeg_bin,
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_txt),
        "-i", str(audio_wav),
        "-i", str(srt_path),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        "-c:a", "aac",
        "-b:a", "192k",
        "-c:s", "mov_text",
        "-metadata:s:s:0", "language=eng",
        "-shortest",
        str(output_mp4),
    ]
    
    print("Running FFmpeg composition...")
    subprocess.run(cmd, check=True)
    print(f"Video composite created at: {output_mp4}")
    
    # Validate
    validator = RenderValidator()
    qa_report_path = story_dir / "RENDER_VALIDATION_REPORT.json"
    passed, report = validator.validate_video(
        video_path=output_mp4,
        expected_duration=30.0,
        expected_shots=5,
        output_report_path=qa_report_path,
    )
    print(f"Validation status: {'PASS' if passed else 'FAIL'}")
    print(json.dumps(report, indent=2))
    
    if not passed:
        raise RuntimeError("Video validation failed!")

if __name__ == "__main__":
    main()
