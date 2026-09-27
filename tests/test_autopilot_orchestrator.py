"""Tests for AI NEWS FACTORY v2 Autopilot Orchestrator and Candidate Selection Policy."""

from __future__ import annotations

import json
import pytest
from pathlib import Path

from src.orchestrator import (
    SupervisedAutopilotOrchestrator,
    AutopilotPolicy,
    PipelineState,
    CandidateEvaluationResult,
)


@pytest.fixture
def sample_candidates_file(tmp_path: Path) -> Path:
    data = {
        "status": "PASS",
        "generated_at": "2026-09-26T20:36:00+07:00",
        "candidates": [
            {
                "story_id": "google-project-suncatcher-orbital-tpu-2026",  # Duplicate story
                "title": "Google Tests TPUs in Space",
                "summary": "Testing TPUs in orbit.",
                "sources": [{"url": "https://blog.google", "name": "Google"}],
                "published_at": "2026-09-26T00:00:00Z",
                "scores": {
                    "freshness": 9.5,
                    "importance": 9.5,
                    "novelty": 9.5,
                    "visual_explainability": 9.5,
                    "source_quality": 9.5,
                },
                "why_it_matters": "Space compute.",
            },
            {
                "story_id": "stale-story-2026",  # Stale story
                "title": "Old News",
                "summary": "Happened a week ago.",
                "sources": [{"url": "https://example.com", "name": "Example"}],
                "published_at": "2026-09-01T00:00:00Z",
                "scores": {
                    "freshness": 4.0,  # Below 7.5
                    "importance": 9.0,
                    "novelty": 8.0,
                    "visual_explainability": 8.0,
                    "source_quality": 8.0,
                },
                "why_it_matters": "Old milestone.",
            },
            {
                "story_id": "stanford-nvidia-clm-8b-agent-model-2026",  # Valid top candidate
                "title": "Stanford and NVIDIA Release CLM-8B",
                "summary": "Non-generative dual encoder running agents 9x faster.",
                "sources": [
                    {"url": "https://arxiv.org/abs/2609.clm8b", "name": "arXiv"},
                    {"url": "https://venturebeat.com/ai/clm-8b", "name": "VentureBeat"},
                ],
                "published_at": "2026-09-25T14:00:00Z",
                "scores": {
                    "freshness": 9.8,
                    "importance": 9.2,
                    "novelty": 9.5,
                    "visual_explainability": 9.6,
                    "source_quality": 9.4,
                },
                "why_it_matters": "Breaks inference latency bottleneck for autonomous agents.",
            },
            {
                "story_id": "deepmind-gemini-3-8-flash-live-avatar-2026",  # Valid alternative
                "title": "Google DeepMind Unveils Gemini 3.8 Live",
                "summary": "Live avatar video synthesis paired with reasoning.",
                "sources": [
                    {"url": "https://blog.google", "name": "Google Blog"},
                ],
                "published_at": "2026-09-23T15:00:00Z",
                "scores": {
                    "freshness": 9.2,
                    "importance": 8.9,
                    "novelty": 9.0,
                    "visual_explainability": 9.4,
                    "source_quality": 9.7,
                },
                "why_it_matters": "Interactive visual reasoning.",
            },
        ],
    }
    p = tmp_path / "NEWS_CANDIDATES.json"
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f)
    return p


def test_autopilot_candidate_selection_filters_duplicates_and_stale(sample_candidates_file: Path) -> None:
    existing = {"google-project-suncatcher-orbital-tpu-2026"}
    policy = AutopilotPolicy(existing_stories=existing)

    with open(sample_candidates_file, "r") as f:
        data = json.load(f)

    best, evals = policy.select_best_candidate(data["candidates"])

    assert best is not None
    # Must NOT select the duplicate suncatcher even though scores are high
    assert best["story_id"] == "stanford-nvidia-clm-8b-agent-model-2026"

    # Verify duplicate was rejected
    dup_eval = next(e for e in evals if e.story_id == "google-project-suncatcher-orbital-tpu-2026")
    assert not dup_eval.passed
    assert any("Duplicate" in r for r in dup_eval.rejection_reasons)

    # Verify stale story was rejected
    stale_eval = next(e for e in evals if e.story_id == "stale-story-2026")
    assert not stale_eval.passed
    assert any("Freshness" in r for r in stale_eval.rejection_reasons)


def test_orchestrator_autonomous_state_transition(sample_candidates_file: Path, tmp_path: Path) -> None:
    # Use isolated root_dir with existing duplicate story so stanford-nvidia-clm-8b is selected
    iso_root = tmp_path / "iso_root"
    dup_dir = iso_root / "data" / "rendered" / "google-project-suncatcher-orbital-tpu-2026"
    dup_dir.mkdir(parents=True, exist_ok=True)
    orchestrator = SupervisedAutopilotOrchestrator(mode="SUPERVISED_AUTOPILOT", root_dir=iso_root)

    selected = orchestrator.execute_autonomous_candidate_selection(sample_candidates_file)

    assert selected["story_id"] == "stanford-nvidia-clm-8b-agent-model-2026"
    # State MUST advance automatically to FACT_CHECK_RUNNING without waiting for human approval
    assert orchestrator.state == PipelineState.FACT_CHECK_RUNNING

    states = [t["to_state"] for t in orchestrator.transition_log]
    assert PipelineState.CANDIDATE_SELECTION_AUTONOMOUS.value in states
    assert PipelineState.CANDIDATE_SELECTED.value in states
    assert PipelineState.FACT_CHECK_RUNNING.value in states
    assert PipelineState.WAITING_FOR_HUMAN_CANDIDATE_SELECTION.value not in states


def test_orchestrator_fallback_when_top_fails(tmp_path: Path) -> None:
    # Test when top candidate fails policy, next valid candidate is automatically chosen
    data = {
        "candidates": [
            {
                "story_id": "bad-visuals-story",
                "summary": "Summary",
                "why_it_matters": "Matters",
                "sources": [{"url": "http", "name": "src"}],
                "scores": {"freshness": 9.0, "importance": 9.0, "novelty": 9.0, "visual_explainability": 5.0},
            },
            {
                "story_id": "valid-runner-up",
                "summary": "Summary",
                "why_it_matters": "Matters",
                "sources": [{"url": "http", "name": "src"}],
                "scores": {"freshness": 9.0, "importance": 9.0, "novelty": 9.0, "visual_explainability": 8.5},
            },
        ]
    }
    p = tmp_path / "candidates.json"
    with open(p, "w") as f:
        json.dump(data, f)

    orchestrator = SupervisedAutopilotOrchestrator(mode="SUPERVISED_AUTOPILOT")
    selected = orchestrator.execute_autonomous_candidate_selection(p)
    assert selected["story_id"] == "valid-runner-up"
    assert orchestrator.state == PipelineState.FACT_CHECK_RUNNING
