"""Master Render Pipeline for AI NEWS FACTORY.

Orchestrates the entire technical transformation from verified facts, scripts,
storyboards, and asset manifests into final 1080x1920 30fps vertical Shorts.
Enforces non-negotiable safety gates, immutable input artifacts, structured logging,
dry-run preview planning, and post-render validation.
"""

from __future__ import annotations

import argparse
import datetime
import json
import logging
import os
import shutil
import sys
from pathlib import Path
from typing import Any

from .audio import AudioEngine
from .subtitles import SubtitleEngine
from .assets import AssetEngine
from .compositor import VideoCompositor
from .validate_render import RenderValidator

ROOT = Path(__file__).resolve().parents[2]


class RenderPipeline:
    """End-to-end production orchestrator for vertical technical Shorts."""

    def __init__(self, root_dir: Path | None = None) -> None:
        self.root = root_dir or ROOT
        self.audio_engine = AudioEngine()
        self.subtitle_engine = SubtitleEngine()
        self.asset_engine = AssetEngine()
        self.compositor = VideoCompositor()
        self.validator = RenderValidator()
        self.logger = logging.getLogger("ai_news_factory.render.pipeline")

    def _setup_logging(self, output_dir: Path, story_id: str) -> Path:
        """Sets up file logging for the story production run."""
        output_dir.mkdir(parents=True, exist_ok=True)
        log_file = output_dir / "production.log"

        handler = logging.FileHandler(log_file, encoding="utf-8")
        formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [STORY: %(name)s] %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        return log_file

    def find_story_artifacts(self, story_id: str) -> dict[str, Path]:
        """Discovers production artifacts associated with story_id across data directories."""
        artifacts: dict[str, Path] = {}

        # 1. Script
        scripts_dir = self.root / "data" / "scripts"
        for p in scripts_dir.glob("*.json"):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if data.get("story_id") == story_id:
                    artifacts["script"] = p
                    break
            except Exception:
                continue

        # 2. Storyboard
        visuals_dir = self.root / "data" / "visuals"
        for p in visuals_dir.glob("*.json"):
            if "manifest" in p.name.lower():
                continue
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if data.get("story_id") == story_id and "shots" in data:
                    artifacts["storyboard"] = p
                    break
            except Exception:
                continue

        # 3. Asset Manifest
        for p in visuals_dir.glob("*.json"):
            if "manifest" in p.name.lower():
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    if data.get("story_id") == story_id:
                        artifacts["manifest"] = p
                        break
                except Exception:
                    continue

        # 4. QA Report
        qa_dir = self.root / "data" / "qa"
        for p in qa_dir.glob("*.json"):
            if "traceability" in p.name.lower():
                continue
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if data.get("story_id") == story_id:
                    artifacts["qa_report"] = p
                    break
            except Exception:
                continue

        # 5. Claim Traceability
        for p in qa_dir.glob("*.json"):
            if "traceability" in p.name.lower():
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    if data.get("story_id") == story_id:
                        artifacts["traceability"] = p
                        break
                except Exception:
                    continue

        # 6. Verified News
        verified_dir = self.root / "data" / "verified"
        for p in verified_dir.glob("*.json"):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if data.get("story_id") == story_id:
                    artifacts["verified"] = p
                    break
            except Exception:
                continue

        return artifacts

    def evaluate_safety_gates(
        self,
        story_id: str,
        artifacts: dict[str, Path],
        script_data: dict[str, Any],
        storyboard_data: dict[str, Any],
        qa_data: dict[str, Any],
        manifest_data: dict[str, Any],
    ) -> tuple[bool, list[str]]:
        """Evaluates non-negotiable safety gates before allowing rendering."""
        blockers = []

        # Gate 1: Required input files exist
        for req in ["script", "storyboard", "manifest", "qa_report", "traceability"]:
            if req not in artifacts or not artifacts[req].exists():
                blockers.append(f"Missing required artifact: {req}")

        # Gate 2: QA approval status
        qa_status = qa_data.get("status") or qa_data.get("final_status")
        if qa_status not in ("APPROVED_FOR_RENDER", "PASS"):
            blockers.append(f"QA status is '{qa_status}' (must be 'APPROVED_FOR_RENDER' or 'PASS').")

        # Gate 3: Script validation status
        if script_data.get("status") != "PASS":
            blockers.append(f"Script status is '{script_data.get('status')}' (must be 'PASS').")

        # Gate 4: Storyboard validation status
        if storyboard_data.get("status") != "PASS":
            blockers.append(f"Storyboard status is '{storyboard_data.get('status')}' (must be 'PASS').")

        # Gate 5: Unresolved rights in asset manifest
        for asset in manifest_data.get("assets", []):
            rs = asset.get("rights_status", "UNKNOWN")
            if rs in AssetEngine.UNRESOLVED_RIGHTS_STATUSES:
                blockers.append(f"Asset '{asset.get('asset_id')}' has unresolved rights status: {rs}")

        # Gate 6: Script and Storyboard timeline synchrony
        script_shots = script_data.get("shots", [])
        story_shots = storyboard_data.get("shots", [])
        script_duration = max(float(s.get("end", 0.0)) for s in script_shots) if script_shots else 0.0
        story_duration = max(float(s.get("end", 0.0)) for s in story_shots) if story_shots else 0.0
        if abs(script_duration - story_duration) > 0.5:
            blockers.append(
                f"Timeline duration divergence: script is {script_duration:.1f}s, storyboard is {story_duration:.1f}s (tolerance: 0.5s)."
            )

        return len(blockers) == 0, blockers

    def execute_dry_run(
        self,
        story_id: str,
        output_dir: Path,
        artifacts: dict[str, Path],
        script_data: dict[str, Any],
        storyboard_data: dict[str, Any],
        manifest_data: dict[str, Any],
        qa_data: dict[str, Any],
        lang: str = "en",
    ) -> dict[str, Any]:
        """Calculates end-to-end production plan, required commands, and asset inventory without rendering."""
        gates_passed, blockers = self.evaluate_safety_gates(
            story_id, artifacts, script_data, storyboard_data, qa_data, manifest_data
        )

        audio_plan = self.audio_engine.dry_run(script_data, output_dir / "audio", lang=lang)
        sub_plan = self.subtitle_engine.dry_run(script_data, output_dir / "subtitles", lang=lang)
        comp_plan = self.compositor.dry_run(storyboard_data, output_dir / "video" / "final.mp4")

        # Asset inventory
        asset_summary = []
        for shot in storyboard_data.get("shots", []):
            shot_id = shot.get("shot_id")
            for a in shot.get("asset_plan", []):
                local_asset_path = output_dir / "assets" / "generated" / f"{shot_id}.png"
                prod_asset_path = self.root / "data" / "visuals" / "production_assets" / f"{shot_id}.png"
                is_ready = local_asset_path.exists() or prod_asset_path.exists()
                status = "READY" if is_ready else "PLACEHOLDER"
                file_target = str(local_asset_path) if local_asset_path.exists() else (str(prod_asset_path) if prod_asset_path.exists() else str(output_dir / "assets" / "placeholders" / f"{shot_id}_card.svg"))
                asset_summary.append({
                    "shot_id": shot_id,
                    "asset_id": a.get("asset_id", f"AST-{shot_id.upper()}"),
                    "type": a.get("asset_type", "ILLUSTRATIVE"),
                    "status": status,
                    "file_path": file_target,
                })

        dry_run_report = {
            "mode": "DRY_RUN",
            "story_id": story_id,
            "timestamp": datetime.datetime.now().isoformat(),
            "safety_gates_status": "CLEARED" if gates_passed else "BLOCKED",
            "blockers": blockers,
            "artifacts_resolved": {k: str(v.relative_to(self.root)) for k, v in artifacts.items()},
            "target_duration_seconds": audio_plan["total_duration"],
            "total_voice_segments": len(script_data.get("shots", [])),
            "total_storyboard_shots": len(storyboard_data.get("shots", [])),
            "video_spec": {
                "dimensions": f"{self.compositor.width}x{self.compositor.height} (9:16 vertical)",
                "fps": self.compositor.fps,
                "encoder": self.compositor.encoder,
            },
            "audio_spec": {
                "engine": self.audio_engine.tts_config.get("backend", "macos_say"),
                "voice": self.audio_engine.get_voice_name(lang),
                "sample_rate": self.audio_engine.sample_rate,
                "channels": self.audio_engine.channels,
                "target_lufs": self.audio_engine.target_lufs,
            },
            "subtitles_spec": {
                "format": ["SRT", "ASS"],
                "font": self.subtitle_engine.font_name,
                "size": self.subtitle_engine.font_size,
                "max_words_per_card": self.subtitle_engine.max_words_per_card,
            },
            "assets_inventory": asset_summary,
            "output_directory_structure": {
                "root": str(output_dir),
                "audio": str(output_dir / "audio"),
                "subtitles": str(output_dir / "subtitles"),
                "assets": str(output_dir / "assets"),
                "video": str(output_dir / "video"),
                "qa": str(output_dir / "qa"),
            },
            "simulated_render_commands": [
                f"# 1. Voice synthesis sample",
                f"say -v {self.audio_engine.get_voice_name(lang)} -o {output_dir / 'audio' / 'voice' / 'shot-01.aiff'} \"{script_data.get('shots', [{}])[0].get('voice', '')}\"",
                f"# 2. Voice track assembly & normalization",
                audio_plan["ffmpeg_command_sample"],
                f"# 3. Video assembly & subtitle burn-in",
                comp_plan["simulated_ffmpeg_cmd"],
            ],
        }

        return dry_run_report

    def render(
        self,
        story_id: str,
        output_dir: Path | None = None,
        lang: str = "en",
    ) -> dict[str, Any]:
        """Executes real video rendering across audio, subtitles, assets, and compositing."""
        out_dir = Path(output_dir).resolve() if output_dir else (self.root / "data" / "rendered" / story_id).resolve()
        out_dir.mkdir(parents=True, exist_ok=True)
        log_file = self._setup_logging(out_dir, story_id)

        self.logger.info(f"Initiating production render for story: {story_id}")

        artifacts = self.find_story_artifacts(story_id)

        # Load input artifacts (READ ONLY)
        with open(artifacts["script"], "r", encoding="utf-8") as f:
            script_data = json.load(f)
        with open(artifacts["storyboard"], "r", encoding="utf-8") as f:
            storyboard_data = json.load(f)
        with open(artifacts["manifest"], "r", encoding="utf-8") as f:
            manifest_data = json.load(f)
        with open(artifacts["qa_report"], "r", encoding="utf-8") as f:
            qa_data = json.load(f)

        # Safety Gate Check
        passed, blockers = self.evaluate_safety_gates(
            story_id, artifacts, script_data, storyboard_data, qa_data, manifest_data
        )
        if not passed:
            self.logger.error(f"Render safety gate failed: {blockers}")
            raise RuntimeError(f"Rendering BLOCKED by safety gates:\n" + "\n".join(f" - {b}" for b in blockers))

        # 1. Synthesize Audio
        self.logger.info("Stage 1/5: Synthesizing voice and building master audio...")
        audio_dir = out_dir / "audio"
        voice_master_wav, _ = self.audio_engine.build_voice_track(script_data, audio_dir, lang=lang)

        mix_dir = audio_dir / "mix"
        final_audio_wav = mix_dir / "audio_master.wav"
        self.compositor.assemble_audio_mix(
            voice_path=voice_master_wav,
            output_mix_path=final_audio_wav,
            total_duration=max(float(s.get("end", 0.0)) for s in storyboard_data.get("shots", [])),
        )

        # 2. Author Subtitles
        self.logger.info("Stage 2/5: Authoring styled subtitles (SRT & ASS)...")
        sub_dir = out_dir / "subtitles"
        sub_paths = self.subtitle_engine.generate_all(script_data, sub_dir, lang=lang)
        ass_subtitle_path = sub_paths["ass"]

        # 3. Process Assets & Generate Procedural Visual Cards
        self.logger.info("Stage 3/5: Registering visual assets and generating visual cards...")
        assets_dir = out_dir / "assets"
        registry = self.asset_engine.build_registry(manifest_data, storyboard_data, assets_dir)

        # Generate cards for each shot
        shot_clips = []
        video_dir = out_dir / "video"
        video_dir.mkdir(parents=True, exist_ok=True)

        for shot in storyboard_data.get("shots", []):
            shot_id = shot.get("shot_id")
            shot_duration = float(shot.get("end", 0.0)) - float(shot.get("start", 0.0))

            # Visual Asset Resolution: prioritize production assets from Phase 6B
            png_path = assets_dir / "generated" / f"{shot_id}.png"
            prod_png = self.root / "data" / "visuals" / "production_assets" / f"{shot_id}.png"
            svg_path = assets_dir / "placeholders" / f"{shot_id}_card.svg"

            if not png_path.exists():
                png_path.parent.mkdir(parents=True, exist_ok=True)
                if prod_png.exists():
                    shutil.copy2(prod_png, png_path)
                else:
                    self.asset_engine.generate_procedural_svg_card(shot, svg_path, story_title=manifest_data.get("manifest_metadata", {}).get("story_title", story_id))
                    self.asset_engine.rasterize_svg_to_png(svg_path, png_path)

            # Build motion video clip
            clip_path = video_dir / f"clip_{shot_id}.mp4"
            self.compositor.build_shot_clip(
                image_path=png_path,
                duration=shot_duration,
                output_clip_path=clip_path,
            )
            shot_clips.append(clip_path)

        # 4. Composite Final Video
        self.logger.info("Stage 4/5: Compositing timeline with FFmpeg and burning subtitles...")
        final_mp4 = video_dir / "final.mp4"
        total_duration = max(float(s.get("end", 0.0)) for s in storyboard_data.get("shots", []))
        self.compositor.composite_final_video(
            shot_clips=shot_clips,
            audio_track=final_audio_wav,
            output_mp4_path=final_mp4,
            subtitle_path=ass_subtitle_path,
            total_duration=total_duration,
        )

        # 5. Technical Validation of Rendered Video
        self.logger.info("Stage 5/5: Running post-render technical validation...")
        qa_report_path = out_dir / "qa" / "render_validation.json"
        is_valid, validation_report = self.validator.validate_video(
            video_path=final_mp4,
            expected_duration=total_duration,
            expected_shots=len(storyboard_data.get("shots", [])),
            output_report_path=qa_report_path,
        )

        # 6. Generate Production Report
        try:
            rel_video = final_mp4.resolve().relative_to(self.root.resolve())
        except Exception:
            rel_video = final_mp4
        report_md = out_dir / "PRODUCTION_REPORT.md"
        with open(report_md, "w", encoding="utf-8") as f:
            f.write(f"""# PRODUCTION REPORT: {story_id}
**Render Timestamp:** {datetime.datetime.now().isoformat()}  
**Video File:** `{rel_video}`  
**Validation Status:** {'PASS' if is_valid else 'FAIL'}  
**Duration:** {validation_report.get('metrics', {}).get('actual_duration', 'N/A')}s (Target: {total_duration}s)  
**Resolution:** {validation_report.get('metrics', {}).get('width')}x{validation_report.get('metrics', {}).get('height')} @ {validation_report.get('metrics', {}).get('fps')} fps  
**Video Codec:** {validation_report.get('metrics', {}).get('video_codec')}  
**Audio Codec:** {validation_report.get('metrics', {}).get('audio_codec')}  
**Subtitles Burnt:** {ass_subtitle_path.name}  
""")

        self.logger.info(f"Production render complete. Output: {final_mp4} (Validation: {'PASS' if is_valid else 'FAIL'})")
        return {
            "status": "SUCCESS" if is_valid else "FAILED_VALIDATION",
            "video_path": str(final_mp4),
            "validation_report": validation_report,
            "production_report": str(report_md),
            "log_file": str(log_file),
        }


def main():
    parser = argparse.ArgumentParser(description="AI NEWS FACTORY Modular Production Render Pipeline")
    parser.add_argument("--story-id", required=True, help="Story ID to render (e.g. google-project-suncatcher-orbital-tpu-2026)")
    parser.add_argument("--dry-run", action="store_true", help="Execute dry-run inspection plan without rendering video")
    parser.add_argument("--render", action="store_true", help="Execute full video render")
    parser.add_argument("--lang", default="en", choices=["en", "vi"], help="Language voiceover/subtitles (default: en)")
    parser.add_argument("--output-dir", help="Custom output directory")

    args = parser.parse_args()

    pipeline = RenderPipeline()
    artifacts = pipeline.find_story_artifacts(args.story_id)

    if not artifacts.get("script") or not artifacts.get("storyboard"):
        print(f"❌ Error: Could not locate required production artifacts for story ID: {args.story_id}", file=sys.stderr)
        sys.exit(1)

    with open(artifacts["script"], "r", encoding="utf-8") as f:
        script_data = json.load(f)
    with open(artifacts["storyboard"], "r", encoding="utf-8") as f:
        storyboard_data = json.load(f)
    with open(artifacts["manifest"], "r", encoding="utf-8") as f:
        manifest_data = json.load(f)
    with open(artifacts["qa_report"], "r", encoding="utf-8") as f:
        qa_data = json.load(f)

    if args.output_dir:
        p = Path(args.output_dir)
        out_dir = p.resolve() if p.is_absolute() else (pipeline.root / p).resolve()
    else:
        out_dir = (pipeline.root / "data" / "rendered" / args.story_id).resolve()

    if args.dry_run or not args.render:
        report = pipeline.execute_dry_run(
            story_id=args.story_id,
            output_dir=out_dir,
            artifacts=artifacts,
            script_data=script_data,
            storyboard_data=storyboard_data,
            manifest_data=manifest_data,
            qa_data=qa_data,
            lang=args.lang,
        )
        print("\n" + "=" * 80)
        print(f"🎬 AI NEWS FACTORY RENDER PIPELINE — DRY RUN PLAN [{args.story_id}]")
        print("=" * 80)
        print(json.dumps(report, indent=2))
        sys.exit(0 if report["safety_gates_status"] == "CLEARED" else 1)

    if args.render:
        res = pipeline.render(story_id=args.story_id, output_dir=out_dir, lang=args.lang)
        print("\n" + "=" * 80)
        print(f"🎉 PRODUCTION RENDER COMPLETED [{args.story_id}]")
        print("=" * 80)
        print(json.dumps(res, indent=2))
        sys.exit(0 if res["status"] == "SUCCESS" else 1)


if __name__ == "__main__":
    main()
