"""Orchestrator and Autopilot Policy Engine for AI NEWS FACTORY v2.

Implements SUPERVISED_AUTOPILOT and SCHEDULED_AUTOPILOT state transitions:
DISCOVERY -> CANDIDATE_SELECTION_AUTONOMOUS -> CANDIDATE_SELECTED -> FACT_CHECK -> EDITORIAL -> VISUAL -> QA -> ASSETS -> ASSET_QA -> AUDIO -> AUDIO_QA -> RENDER -> RENDER_QA -> FINAL_RED_TEAM -> PUBLISH (or READY_FOR_HUMAN_REVIEW)

Explicit precedence:
AUTOPILOT_POLICY > LEGACY_PHASE_APPROVAL_GATES
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable

logger = logging.getLogger("ai_news_factory.orchestrator")


class PipelineState(str, Enum):
    DISCOVERY_RUNNING = "DISCOVERY_RUNNING"
    DISCOVERY_QA = "DISCOVERY_QA"
    CANDIDATE_SELECTION_AUTONOMOUS = "CANDIDATE_SELECTION_AUTONOMOUS"
    CANDIDATE_SELECTED = "CANDIDATE_SELECTED"
    FACT_CHECK_RUNNING = "FACT_CHECK_RUNNING"
    FACT_CHECK_COMPLETE = "FACT_CHECK_COMPLETE"
    EDITORIAL_RUNNING = "EDITORIAL_RUNNING"
    EDITORIAL_COMPLETE = "EDITORIAL_COMPLETE"
    VISUAL_RUNNING = "VISUAL_RUNNING"
    VISUAL_COMPLETE = "VISUAL_COMPLETE"
    QA_RUNNING = "QA_RUNNING"
    QA_COMPLETE = "QA_COMPLETE"
    ASSET_GENERATION_RUNNING = "ASSET_GENERATION_RUNNING"
    ASSET_QA_RUNNING = "ASSET_QA_RUNNING"
    ASSET_QA_COMPLETE = "ASSET_QA_COMPLETE"
    AUDIO_RUNNING = "AUDIO_RUNNING"
    AUDIO_QA_RUNNING = "AUDIO_QA_RUNNING"
    AUDIO_QA_COMPLETE = "AUDIO_QA_COMPLETE"
    RENDER_RUNNING = "RENDER_RUNNING"
    RENDER_QA_RUNNING = "RENDER_QA_RUNNING"
    RENDER_QA_COMPLETE = "RENDER_QA_COMPLETE"
    FINAL_RED_TEAM_RUNNING = "FINAL_RED_TEAM_RUNNING"
    PUBLISH_RUNNING = "PUBLISH_RUNNING"
    READY_FOR_HUMAN_REVIEW = "READY_FOR_HUMAN_REVIEW"
    PUBLISHED = "PUBLISHED"
    BLOCKED = "BLOCKED"
    HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"
    WAITING_FOR_HUMAN_CANDIDATE_SELECTION = "WAITING_FOR_HUMAN_CANDIDATE_SELECTION"


@dataclass
class CandidateEvaluationResult:
    story_id: str
    passed: bool
    overall_score: float
    rejection_reasons: list[str] = field(default_factory=list)


class AutopilotPolicy:
    """Evaluates candidates autonomously against factory editorial & research policies."""

    def __init__(
        self,
        min_freshness: float = 7.5,
        min_score: float = 8.0,
        min_sources: int = 1,
        existing_stories: set[str] | None = None,
    ) -> None:
        self.min_freshness = min_freshness
        self.min_score = min_score
        self.min_sources = min_sources
        self.existing_stories = existing_stories or set()

    def evaluate_candidate(self, candidate: dict[str, Any]) -> CandidateEvaluationResult:
        story_id = candidate.get("story_id", "")
        reasons = []

        # 1. Duplication check
        if story_id in self.existing_stories:
            reasons.append(f"Duplicate story already produced or in repository: {story_id}")

        # 2. Scores
        scores = candidate.get("scores", {})
        freshness = float(scores.get("freshness", 0.0))
        if freshness < self.min_freshness:
            reasons.append(f"Freshness {freshness:.1f} is below minimum requirement {self.min_freshness:.1f}")

        # Overall composite score
        score_vals = [float(v) for v in scores.values() if isinstance(v, (int, float))]
        overall_score = sum(score_vals) / len(score_vals) if score_vals else 0.0
        if overall_score < self.min_score:
            reasons.append(f"Composite score {overall_score:.2f} is below production threshold {self.min_score:.2f}")

        # 3. Sources check
        sources = candidate.get("sources", [])
        if len(sources) < self.min_sources:
            reasons.append(f"Sources count {len(sources)} is below minimum {self.min_sources}")

        # 4. Visual explainability check
        visual_exp = float(scores.get("visual_explainability", 0.0))
        if visual_exp < 7.0:
            reasons.append(f"Visual explainability score {visual_exp:.1f} is insufficient for a Short")

        # 5. Material claim & why_it_matters check
        if not candidate.get("why_it_matters") or not candidate.get("summary"):
            reasons.append("Missing essential why_it_matters or summary context")

        return CandidateEvaluationResult(
            story_id=story_id,
            passed=len(reasons) == 0,
            overall_score=overall_score,
            rejection_reasons=reasons,
        )

    def select_best_candidate(self, candidates: list[dict[str, Any]]) -> tuple[dict[str, Any] | None, list[CandidateEvaluationResult]]:
        evaluations: list[CandidateEvaluationResult] = []
        candidates_with_eval = []

        for c in candidates:
            res = self.evaluate_candidate(c)
            evaluations.append(res)
            if res.passed:
                candidates_with_eval.append((res.overall_score, c))

        if not candidates_with_eval:
            return None, evaluations

        # Sort by overall score descending
        candidates_with_eval.sort(key=lambda x: x[0], reverse=True)
        return candidates_with_eval[0][1], evaluations


class SupervisedAutopilotOrchestrator:
    """State-machine orchestrator enforcing v2 autonomous progress and scheduled publishing."""

    def __init__(self, mode: str = "SUPERVISED_AUTOPILOT", root_dir: Path | None = None) -> None:
        self.mode = mode
        self.root = root_dir or Path(__file__).resolve().parents[1]
        self.state: PipelineState = PipelineState.DISCOVERY_RUNNING
        self.selected_candidate: dict[str, Any] | None = None
        self.transition_log: list[dict[str, Any]] = []

    def log_transition(self, from_state: PipelineState, to_state: PipelineState, details: dict[str, Any]) -> None:
        entry = {
            "from_state": from_state.value,
            "to_state": to_state.value,
            "details": details,
        }
        self.transition_log.append(entry)
        logger.info(f"TRANSITION: {from_state.value} -> {to_state.value} | {details}")

    def get_existing_stories(self) -> set[str]:
        stories: set[str] = set()
        search_dirs = [
            self.root / "data" / "rendered",
            self.root / "data" / "verified",
            self.root / "data" / "scripts",
            self.root / "data" / "visuals",
            self.root / "data" / "publishing",
        ]
        for d in search_dirs:
            if not d.exists():
                continue
            for item in d.iterdir():
                if item.is_dir() and not item.name.startswith("production_assets"):
                    stories.add(item.name)
                elif item.suffix == ".json":
                    try:
                        with open(item, "r", encoding="utf-8") as f:
                            data = json.load(f)
                        sid = data.get("story_id")
                        if sid:
                            stories.add(sid)
                    except Exception:
                        pass
        return stories

    def execute_autonomous_candidate_selection(self, candidates_file: Path) -> dict[str, Any]:
        """Loads candidates and selects the best candidate automatically according to policy."""
        prev_state = self.state
        self.state = PipelineState.CANDIDATE_SELECTION_AUTONOMOUS
        self.log_transition(prev_state, self.state, {"candidates_file": str(candidates_file)})

        with open(candidates_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        candidates = data.get("candidates", [])
        existing = self.get_existing_stories()
        policy = AutopilotPolicy(existing_stories=existing)

        best_candidate, evals = policy.select_best_candidate(candidates)

        if not best_candidate:
            self.state = PipelineState.BLOCKED
            self.log_transition(
                PipelineState.CANDIDATE_SELECTION_AUTONOMOUS,
                PipelineState.BLOCKED,
                {"error": "NO_PASSING_CANDIDATE", "evaluations": [e.__dict__ for e in evals]},
            )
            raise RuntimeError("Autonomous candidate selection failed: no candidate satisfied policy requirements.")

        self.selected_candidate = best_candidate
        story_id = best_candidate["story_id"]

        # Transition to CANDIDATE_SELECTED
        self.state = PipelineState.CANDIDATE_SELECTED
        self.log_transition(
            PipelineState.CANDIDATE_SELECTION_AUTONOMOUS,
            PipelineState.CANDIDATE_SELECTED,
            {
                "selected_story": story_id,
                "title": best_candidate.get("title"),
                "policy_decision": "AUTONOMOUS",
                "next_stage": PipelineState.FACT_CHECK_RUNNING.value,
            },
        )

        # In AUTOPILOT: AUTOPILOT_POLICY > LEGACY_PHASE_APPROVAL_GATES
        # Advance immediately to FACT_CHECK_RUNNING
        self.state = PipelineState.FACT_CHECK_RUNNING
        self.log_transition(
            PipelineState.CANDIDATE_SELECTED,
            PipelineState.FACT_CHECK_RUNNING,
            {"story_id": story_id, "mode": self.mode},
        )

        return best_candidate

    def handle_post_render_red_team_pass(
        self,
        story_id: str,
        job_id: str,
        video_path: Path,
        metadata_path: Path,
        qa_report_path: Path,
        final_red_team_path: Path | None = None,
        publisher: Any | None = None,
        upload_handler: Callable[[str, Path, dict[str, Any]], dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Handles post final-red-team state transition depending on operating mode."""
        self.state = PipelineState.FINAL_RED_TEAM_RUNNING
        self.log_transition(
            PipelineState.RENDER_QA_COMPLETE,
            PipelineState.FINAL_RED_TEAM_RUNNING,
            {"story_id": story_id, "job_id": job_id},
        )

        if self.mode == "SCHEDULED_AUTOPILOT":
            # Scheduled job trigger authorizes automated publishing after all gates pass
            from .publisher import AutonomousPublisher, ScheduledJobResult

            pub = publisher or AutonomousPublisher(root_dir=self.root, mode="SCHEDULED_AUTOPILOT")
            self.state = PipelineState.PUBLISH_RUNNING
            self.log_transition(
                PipelineState.FINAL_RED_TEAM_RUNNING,
                PipelineState.PUBLISH_RUNNING,
                {"story_id": story_id, "mode": "SCHEDULED_AUTOPILOT"},
            )

            pub_report = pub.publish_scheduled_job(
                story_id=story_id,
                job_id=job_id,
                video_path=video_path,
                metadata_path=metadata_path,
                qa_report_path=qa_report_path,
                final_red_team_path=final_red_team_path,
                upload_handler=upload_handler,
            )

            if pub_report.get("result") == ScheduledJobResult.PUBLISHED.value:
                self.state = PipelineState.PUBLISHED
                self.log_transition(
                    PipelineState.PUBLISH_RUNNING,
                    PipelineState.PUBLISHED,
                    {"video_id": pub_report.get("youtube_video_id"), "url": pub_report.get("youtube_url")},
                )
            else:
                self.state = PipelineState.HUMAN_REVIEW_REQUIRED
                self.log_transition(
                    PipelineState.PUBLISH_RUNNING,
                    PipelineState.HUMAN_REVIEW_REQUIRED,
                    {"reason": pub_report.get("result"), "blockers": pub_report.get("blockers")},
                )

            return pub_report

        else:
            # SUPERVISED_AUTOPILOT: Stop at READY_FOR_HUMAN_REVIEW
            self.state = PipelineState.READY_FOR_HUMAN_REVIEW
            self.log_transition(
                PipelineState.FINAL_RED_TEAM_RUNNING,
                PipelineState.READY_FOR_HUMAN_REVIEW,
                {"story_id": story_id, "mode": self.mode},
            )
            return {
                "job_id": job_id,
                "story_id": story_id,
                "result": "READY_FOR_HUMAN_REVIEW",
                "state": self.state.value,
            }
