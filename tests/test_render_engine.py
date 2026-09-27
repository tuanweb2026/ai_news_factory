"""Unit tests for AI NEWS FACTORY Modular Production Render Engine.

Tests audio engine timing calculations, subtitle generation, asset registry,
procedural SVG rendering, compositor configuration, render validation,
and end-to-end safety gates.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any

import pytest
import yaml

from src.render.audio import AudioEngine
from src.render.subtitles import SubtitleEngine
from src.render.assets import AssetEngine
from src.render.compositor import VideoCompositor
from src.render.validate_render import RenderValidator
from src.render.render_pipeline import RenderPipeline

ROOT = Path(__file__).resolve().parents[1]


# -----------------------------------------------------------------------------
# Fixtures
# -----------------------------------------------------------------------------

@pytest.fixture
def sample_script() -> dict[str, Any]:
    return {
        "status": "PASS",
        "story_id": "test-story-ai-2026",
        "duration_target_seconds": 10.0,
        "hook": "AI models are scaling beyond earth.",
        "spoken_script": "AI models are scaling beyond earth. New tests prove orbital compute works.",
        "cta": "Follow for verified AI updates.",
        "shots": [
            {
                "shot_id": "shot-01",
                "start": 0.0,
                "end": 4.0,
                "purpose": "HOOK",
                "voice": "AI models are scaling beyond earth.",
                "vietnamese_voice": "Mô hình AI đang mở rộng ra ngoài Trái Đất.",
                "on_screen_text": "AI BEYOND EARTH",
                "visual_intent": "Deep space Earth horizon.",
                "fact_id": "claim-01",
            },
            {
                "shot_id": "shot-02",
                "start": 4.0,
                "end": 10.0,
                "purpose": "EXPLANATION",
                "voice": "New tests prove orbital compute works.",
                "vietnamese_voice": "Thử nghiệm mới chứng minh điện toán quỹ đạo hiệu quả.",
                "on_screen_text": "ORBITAL COMPUTE • PROVEN",
                "visual_intent": "Satellite 3D diagram.",
                "fact_id": "claim-02",
            },
        ],
    }


@pytest.fixture
def sample_storyboard() -> dict[str, Any]:
    return {
        "status": "PASS",
        "story_id": "test-story-ai-2026",
        "shots": [
            {
                "shot_id": "shot-01",
                "start": 0.0,
                "end": 4.0,
                "shot_type": "MACRO_TECH",
                "visual_status": "ILLUSTRATIVE",
                "text": "AI BEYOND EARTH",
                "diagram_elements": "Orbital altitude 500km",
                "asset_plan": [
                    {
                        "asset_type": "GENERATED",
                        "rights_status": "ORIGINAL_AI_SYNTHESIZED",
                    }
                ],
            },
            {
                "shot_id": "shot-02",
                "start": 4.0,
                "end": 10.0,
                "shot_type": "DIAGRAM",
                "visual_status": "FUTURE_CONCEPT",
                "text": "ORBITAL COMPUTE • PROVEN",
                "diagram_elements": "Constellation link",
                "asset_plan": [
                    {
                        "asset_type": "FUTURE_CONCEPT",
                        "rights_status": "PROPRIETARY_GENERATED",
                    }
                ],
            },
        ],
    }


@pytest.fixture
def sample_manifest() -> dict[str, Any]:
    return {
        "story_id": "test-story-ai-2026",
        "manifest_metadata": {
            "story_title": "Test AI Orbital Mission",
        },
        "assets": [
            {
                "asset_id": "AST-01",
                "asset_classification": "GENERATED",
                "rights_status": "ORIGINAL_AI_SYNTHESIZED",
            },
            {
                "asset_id": "AST-02",
                "asset_classification": "FUTURE_CONCEPT",
                "rights_status": "PROPRIETARY_GENERATED",
            },
        ],
    }


# -----------------------------------------------------------------------------
# Test Cases
# -----------------------------------------------------------------------------

def test_factory_config_audio_and_render():
    """Verifies factory.yaml has valid audio and render configurations."""
    cfg_file = ROOT / "config" / "factory.yaml"
    assert cfg_file.exists()
    with open(cfg_file, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    assert "audio" in cfg
    assert cfg["audio"]["tts"]["backend"] in ("microsoft_azure_speech", "macos_say", "edge_tts", "elevenlabs")
    assert cfg["audio"]["sample_rate"] == 48000
    assert cfg["audio"]["channels"] == 2
    assert cfg["audio"]["target_lufs"] == -16

    assert "video" in cfg
    assert cfg["video"]["width"] == 1080
    assert cfg["video"]["height"] == 1920
    assert cfg["video"]["fps"] == 30

    assert "render" in cfg
    assert cfg["render"]["encoder"] in ("videotoolbox", "libx264")
    assert "subtitles" in cfg["render"]
    assert cfg["render"]["max_words_per_card"] == 6


def test_audio_engine_timing_and_dry_run(sample_script):
    """Verifies AudioEngine calculates shot timings, word counts, and WPM accurately."""
    engine = AudioEngine()
    shots = engine.extract_shots(sample_script, lang="en")
    assert len(shots) == 2
    assert shots[0]["shot_id"] == "shot-01"
    assert shots[0]["duration"] == 4.0

    with tempfile.TemporaryDirectory() as tmp_dir:
        dry_plan = engine.dry_run(sample_script, Path(tmp_dir), lang="en")
        assert dry_plan["status"] == "DRY_RUN"
        assert dry_plan["total_duration"] == 10.0
        assert len(dry_plan["shot_plan"]) == 2
        assert dry_plan["sample_rate"] == 48000
        assert dry_plan["channels"] == 2
        assert dry_plan["target_lufs"] == -16.0


def test_audio_engine_vietnamese_voice(sample_script):
    """Verifies AudioEngine extracts Vietnamese script text and configures Linh voice."""
    engine = AudioEngine()
    shots_vi = engine.extract_shots(sample_script, lang="vi")
    assert len(shots_vi) == 2
    assert "Mô hình AI" in shots_vi[0]["voice_text"]
    assert engine.get_voice_name("vi") == "Linh"
    assert engine.get_voice_name("en") in ("en-US-AriaNeural", "Samantha")


def test_subtitle_engine_formatting_and_word_counts(sample_script):
    """Verifies SubtitleEngine generates compliant SRT and ASS formats and handles divider symbols."""
    engine = SubtitleEngine()

    # Timestamp tests
    assert engine.format_timestamp_srt(1.25) == "00:00:01,250"
    assert engine.format_timestamp_srt(65.5) == "00:01:05,500"
    assert engine.format_timestamp_ass(1.25) == "0:00:01.25"
    assert engine.format_timestamp_ass(65.5) == "0:01:05.50"

    # Cue extraction & word count check
    cues = engine.extract_subtitle_cues(sample_script, lang="en")
    assert len(cues) == 2
    # "AI BEYOND EARTH" -> 3 words
    assert cues[0]["card_words"] == 3
    # "ORBITAL COMPUTE • PROVEN" -> 3 alphanumeric words (bullet ignored)
    assert cues[1]["card_words"] == 3
    assert cues[1]["card_words"] <= engine.max_words_per_card

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        sub_files = engine.generate_all(sample_script, tmp_path, lang="en")

        srt_file = sub_files["srt"]
        ass_file = sub_files["ass"]
        assert srt_file.exists()
        assert ass_file.exists()

        srt_content = srt_file.read_text(encoding="utf-8")
        assert "00:00:00,000 --> 00:00:04,000" in srt_content
        assert "AI models are scaling beyond earth." in srt_content

        ass_content = ass_file.read_text(encoding="utf-8")
        assert "PlayResX: 1080" in ass_content
        assert "PlayResY: 1920" in ass_content
        assert "Inter" in ass_content
        assert "&H00FAF7F3" in ass_content
        assert "MarginV, Effect, Text" in ass_content


def test_asset_engine_registry_and_svg_generation(sample_manifest, sample_storyboard):
    """Verifies AssetEngine builds registry, detects watermarks, and creates procedural SVG cards."""
    engine = AssetEngine()

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        registry = engine.build_registry(sample_manifest, sample_storyboard, tmp_path)

        assert registry["registry_status"] == "READY"
        assert len(registry["assets"]) == 2
        assert registry["assets"][1]["watermark_required"] is True

        # Test procedural SVG generation
        shot_02 = sample_storyboard["shots"][1]
        svg_file = tmp_path / "shot-02_card.svg"
        engine.generate_procedural_svg_card(shot_02, svg_file, story_title="Test AI Orbital Mission")

        assert svg_file.exists()
        svg_content = svg_file.read_text(encoding="utf-8")
        assert 'viewBox="0 0 1080 1920"' in svg_content
        assert "AI NEWS FACTORY" in svg_content
        assert "Test AI Orbital Mission" in svg_content
        assert "FUTURE CONCEPT • NOT OPERATIONAL INFRASTRUCTURE" in svg_content


def test_asset_engine_blocks_unresolved_rights(sample_storyboard):
    """Verifies AssetEngine blocks registry when an asset has unresolved rights."""
    unresolved_manifest = {
        "story_id": "test-story-ai-2026",
        "assets": [
            {
                "asset_id": "AST-UNRESOLVED",
                "asset_classification": "SCREENSHOT",
                "rights_status": "RIGHTS_REVIEW_REQUIRED",
            }
        ],
    }
    storyboard_with_unresolved = {
        "story_id": "test-story-ai-2026",
        "shots": [
            {
                "shot_id": "shot-01",
                "start": 0.0,
                "end": 4.0,
                "asset_plan": [
                    {
                        "asset_id": "AST-UNRESOLVED",
                        "rights_status": "RIGHTS_REVIEW_REQUIRED",
                    }
                ],
            }
        ],
    }

    engine = AssetEngine()
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        registry = engine.build_registry(unresolved_manifest, storyboard_with_unresolved, tmp_path)
        assert registry["registry_status"] == "BLOCKED"
        assert len(registry["unresolved_rights_blockers"]) == 1
        assert registry["unresolved_rights_blockers"][0]["asset_id"] == "AST-UNRESOLVED"


def test_compositor_dry_run(sample_storyboard):
    """Verifies VideoCompositor produces correct dry-run plan and FFmpeg commands."""
    compositor = VideoCompositor()
    assert compositor.width == 1080
    assert compositor.height == 1920
    assert compositor.fps == 30
    assert compositor.encoder in ("h264_videotoolbox", "libx264")

    plan = compositor.dry_run(sample_storyboard, Path("/tmp/final.mp4"))
    assert plan["status"] == "DRY_RUN"
    assert plan["calculated_duration"] == 10.0
    assert plan["total_shots"] == 2
    assert "1080x1920 (9:16)" in plan["dimensions"]


def test_render_validator_checks():
    """Verifies RenderValidator handles missing files and tolerance configurations."""
    validator = RenderValidator(tolerance_seconds=0.5)
    assert validator.tolerance_seconds == 0.5

    # Non-existent file fails gracefully
    is_valid, report = validator.validate_video(Path("/tmp/non_existent_video_12345.mp4"), expected_duration=35.0)
    assert is_valid is False
    assert report["status"] == "FAIL"
    assert "does not exist" in report["error"]


def test_suncatcher_production_artifacts_discovery_and_dry_run():
    """End-to-end integration test verifying Suncatcher production artifacts pass all safety gates in dry-run mode."""
    story_id = "google-project-suncatcher-orbital-tpu-2026"
    pipeline = RenderPipeline()
    artifacts = pipeline.find_story_artifacts(story_id)

    assert "script" in artifacts
    assert "storyboard" in artifacts
    assert "manifest" in artifacts
    assert "qa_report" in artifacts
    assert "traceability" in artifacts

    with open(artifacts["script"], "r", encoding="utf-8") as f:
        script_data = json.load(f)
    with open(artifacts["storyboard"], "r", encoding="utf-8") as f:
        storyboard_data = json.load(f)
    with open(artifacts["manifest"], "r", encoding="utf-8") as f:
        manifest_data = json.load(f)
    with open(artifacts["qa_report"], "r", encoding="utf-8") as f:
        qa_data = json.load(f)

    # Evaluate safety gates
    passed, blockers = pipeline.evaluate_safety_gates(
        story_id, artifacts, script_data, storyboard_data, qa_data, manifest_data
    )
    assert passed is True, f"Safety gates blocked with: {blockers}"
    assert len(blockers) == 0

    # Dry run execution
    with tempfile.TemporaryDirectory() as tmp_dir:
        out_dir = Path(tmp_dir)
        dry_run_report = pipeline.execute_dry_run(
            story_id=story_id,
            output_dir=out_dir,
            artifacts=artifacts,
            script_data=script_data,
            storyboard_data=storyboard_data,
            manifest_data=manifest_data,
            qa_data=qa_data,
            lang="en",
        )
        assert dry_run_report["mode"] == "DRY_RUN"
        assert dry_run_report["safety_gates_status"] == "CLEARED"
        assert dry_run_report["target_duration_seconds"] == 35.0
        assert dry_run_report["total_voice_segments"] == 8
        assert dry_run_report["total_storyboard_shots"] == 9
        assert len(dry_run_report["assets_inventory"]) == 9
