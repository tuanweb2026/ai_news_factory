"""Unit tests for AI NEWS FACTORY v2 Autonomous Publisher and Scheduled Autopilot.

Tests:
1. Scheduled autonomous publishing flow
2. All-QA-pass publish authorization
3. Any-QA-fail publish blocking (fail-closed)
4. Duplicate upload prevention (story_id & title similarity)
5. Authentication failure handling (token missing / invalid)
6. Retry behavior on transient upload transport errors
7. Idempotent publishing (prevent duplicate upload of already completed jobs)
8. Public-status verification
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
import pytest

from src.publisher import (
    AutonomousPublisher,
    DuplicateDetector,
    PublishGateStatus,
    ScheduledJobResult,
)
from src.orchestrator import (
    SupervisedAutopilotOrchestrator,
    PipelineState,
)


@pytest.fixture
def mock_story_env(tmp_path: Path) -> dict[str, Path]:
    story_id = "test-scheduled-ai-breakthrough-2026"
    video_dir = tmp_path / "video"
    video_dir.mkdir(parents=True, exist_ok=True)
    video_path = video_dir / "final_release_candidate.mp4"
    video_path.write_bytes(b"dummy_mp4_bytes_12345678")

    meta_dir = tmp_path / "publishing"
    meta_dir.mkdir(parents=True, exist_ok=True)
    meta_path = meta_dir / "YOUTUBE_METADATA.json"
    meta_doc = {
        "story_id": story_id,
        "youtube_metadata": {
            "title": "Autonomous Scheduled AI Breakthrough #shorts",
            "description": "Full factual breakdown of the new scheduled AI model.",
            "tags": ["AI", "Tech"],
            "category_id": "28",
            "privacy_status": "public",
        },
    }
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta_doc, f)

    qa_dir = tmp_path / "qa"
    qa_dir.mkdir(parents=True, exist_ok=True)
    qa_path = qa_dir / "QA_REPORT.json"
    qa_doc = {
        "story_id": story_id,
        "status": "PASS",
        "checks": [
            {"name": "Factual Accuracy", "status": "PASS"},
            {"name": "Scientific Boundaries", "status": "PASS"},
            {"name": "Visual Truth", "status": "PASS"},
            {"name": "Rights Clearance", "status": "PASS"},
            {"name": "Asset Production", "status": "PASS"},
            {"name": "Audio Loudness & Sync", "status": "PASS"},
            {"name": "Render Encoding", "status": "PASS"},
        ],
    }
    with open(qa_path, "w", encoding="utf-8") as f:
        json.dump(qa_doc, f)

    token_path = tmp_path / "token.json"
    token_path.write_text(json.dumps({"access_token": "mock_token", "refresh_token": "mock_refresh"}))

    return {
        "story_id": story_id,
        "video": video_path,
        "metadata": meta_path,
        "qa": qa_path,
        "token": token_path,
        "root": tmp_path,
    }


def test_scheduled_publish_all_gates_pass(mock_story_env: dict[str, Any]) -> None:
    publisher = AutonomousPublisher(
        root_dir=mock_story_env["root"],
        token_path=mock_story_env["token"],
        mode="SCHEDULED_AUTOPILOT",
        dry_run=True,
    )

    report = publisher.publish_scheduled_job(
        story_id=mock_story_env["story_id"],
        job_id="job_sched_001",
        video_path=mock_story_env["video"],
        metadata_path=mock_story_env["metadata"],
        qa_report_path=mock_story_env["qa"],
    )

    assert report["result"] == ScheduledJobResult.PUBLISHED.value
    assert report["youtube_video_id"] is not None
    assert report["privacy"] == "public"
    assert len(report["blockers"]) == 0


def test_scheduled_publish_fails_closed_on_qa_failure(mock_story_env: dict[str, Any]) -> None:
    # Corrupt QA report: one gate fails
    qa_doc = {
        "story_id": mock_story_env["story_id"],
        "status": "FAIL",
        "checks": [
            {"name": "Factual Accuracy", "status": "FAIL", "notes": "Unverified claim detected"},
            {"name": "Scientific Boundaries", "status": "PASS"},
        ],
    }
    with open(mock_story_env["qa"], "w") as f:
        json.dump(qa_doc, f)

    publisher = AutonomousPublisher(
        root_dir=mock_story_env["root"],
        token_path=mock_story_env["token"],
        mode="SCHEDULED_AUTOPILOT",
        dry_run=True,
    )

    report = publisher.publish_scheduled_job(
        story_id=mock_story_env["story_id"],
        job_id="job_sched_002",
        video_path=mock_story_env["video"],
        metadata_path=mock_story_env["metadata"],
        qa_report_path=mock_story_env["qa"],
    )

    # Must be blocked and set to HUMAN_REVIEW_REQUIRED (Fail-Closed)
    assert report["result"] == ScheduledJobResult.HUMAN_REVIEW_REQUIRED.value
    assert report["youtube_video_id"] is None
    assert any("QA report status is not PASS" in b for b in report["blockers"])


def test_duplicate_prevention_blocks_upload(mock_story_env: dict[str, Any]) -> None:
    # Create existing published record
    pub_dir = mock_story_env["root"] / "data" / "publishing" / mock_story_env["story_id"]
    pub_dir.mkdir(parents=True, exist_ok=True)
    existing_rec = {
        "story_id": mock_story_env["story_id"],
        "status": "PUBLISHED",
        "video_id": "existing_vid_999",
        "title": "Autonomous Scheduled AI Breakthrough #shorts",
    }
    with open(pub_dir / "YOUTUBE_PUBLISHED_RECORD.json", "w") as f:
        json.dump(existing_rec, f)

    publisher = AutonomousPublisher(
        root_dir=mock_story_env["root"],
        token_path=mock_story_env["token"],
        mode="SCHEDULED_AUTOPILOT",
        dry_run=True,
    )

    report = publisher.publish_scheduled_job(
        story_id=mock_story_env["story_id"],
        job_id="job_sched_dup",
        video_path=mock_story_env["video"],
        metadata_path=mock_story_env["metadata"],
        qa_report_path=mock_story_env["qa"],
    )

    # Must block duplicate upload
    assert report["result"] == ScheduledJobResult.DUPLICATE_UPLOAD_BLOCKED.value
    assert any("already published" in b for b in report["blockers"])


def test_duplicate_headline_similarity_block(mock_story_env: dict[str, Any]) -> None:
    detector = DuplicateDetector(root_dir=mock_story_env["root"])

    # Simulate published record with almost identical title
    pub_dir = mock_story_env["root"] / "data" / "publishing" / "other-story"
    pub_dir.mkdir(parents=True, exist_ok=True)
    with open(pub_dir / "YOUTUBE_PUBLISHED_RECORD.json", "w") as f:
        json.dump({"title": "Autonomous Scheduled AI Breakthrough #shorts"}, f)

    is_dup, reason = detector.is_duplicate(
        story_id="completely-new-id",
        headline="Autonomous Scheduled AI Breakthrough #shorts",
    )
    assert is_dup
    assert "High title similarity" in reason


def test_auth_missing_stops_at_youtube_auth_required(mock_story_env: dict[str, Any]) -> None:
    # Token path that does not exist
    non_existent_token = mock_story_env["root"] / "missing_token.json"

    publisher = AutonomousPublisher(
        root_dir=mock_story_env["root"],
        token_path=non_existent_token,
        mode="SCHEDULED_AUTOPILOT",
        dry_run=False,  # Enforce real token presence check
    )

    res = publisher.evaluate_publish_gates(
        story_id=mock_story_env["story_id"],
        video_path=mock_story_env["video"],
        metadata_path=mock_story_env["metadata"],
        qa_report_path=mock_story_env["qa"],
    )

    assert not res.allowed
    assert res.final_state == ScheduledJobResult.YOUTUBE_AUTH_REQUIRED
    assert any("token file missing" in b.lower() for b in res.blockers)


def test_upload_retry_behavior_on_transient_failure(mock_story_env: dict[str, Any]) -> None:
    publisher = AutonomousPublisher(
        root_dir=mock_story_env["root"],
        token_path=mock_story_env["token"],
        mode="SCHEDULED_AUTOPILOT",
        dry_run=True,
    )

    attempts = 0

    def mock_flaky_uploader(sid: str, vpath: Path, payload: dict[str, Any]) -> dict[str, Any]:
        nonlocal attempts
        attempts += 1
        if attempts < 2:
            raise RuntimeError("Transient transport 503 Service Unavailable")
        return {
            "id": "retry_success_vid",
            "title": payload["snippet"]["title"],
            "status": {"privacyStatus": "public"},
            "url": "https://www.youtube.com/watch?v=retry_success_vid",
            "shorts_url": "https://www.youtube.com/shorts/retry_success_vid",
        }

    # Simulate retry wrapper
    max_retries = 3
    result = None
    for a in range(1, max_retries + 1):
        try:
            result = publisher.execute_upload_resumable(
                video_path=mock_story_env["video"],
                metadata_path=mock_story_env["metadata"],
                story_id=mock_story_env["story_id"],
                upload_handler=mock_flaky_uploader,
            )
            break
        except RuntimeError:
            if a == max_retries:
                raise

    assert result is not None
    assert result["id"] == "retry_success_vid"
    assert attempts == 2


def test_orchestrator_scheduled_autopilot_end_to_end(mock_story_env: dict[str, Any]) -> None:
    orchestrator = SupervisedAutopilotOrchestrator(
        mode="SCHEDULED_AUTOPILOT",
        root_dir=mock_story_env["root"],
    )

    publisher = AutonomousPublisher(
        root_dir=mock_story_env["root"],
        token_path=mock_story_env["token"],
        mode="SCHEDULED_AUTOPILOT",
        dry_run=True,
    )

    report = orchestrator.handle_post_render_red_team_pass(
        story_id=mock_story_env["story_id"],
        job_id="sched_job_123",
        video_path=mock_story_env["video"],
        metadata_path=mock_story_env["metadata"],
        qa_report_path=mock_story_env["qa"],
        publisher=publisher,
    )

    # In SCHEDULED_AUTOPILOT: state automatically transitions to PUBLISHED
    assert orchestrator.state == PipelineState.PUBLISHED
    assert report["result"] == "PUBLISHED"
    assert report["youtube_video_id"] is not None

    states = [t["to_state"] for t in orchestrator.transition_log]
    assert PipelineState.PUBLISH_RUNNING.value in states
    assert PipelineState.PUBLISHED.value in states
    assert PipelineState.READY_FOR_HUMAN_REVIEW.value not in states
