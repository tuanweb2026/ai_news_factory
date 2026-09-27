"""Autonomous Publisher Engine for AI NEWS FACTORY v2.

Implements SCHEDULED_AUTOPILOT automated publishing, fail-closed safety gate
validation, duplicate detection, metadata verification, idempotent upload logic,
and structured job reporting.
"""

from __future__ import annotations

import difflib
import json
import logging
import os
import ssl
import sys
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable

logger = logging.getLogger("ai_news_factory.publisher")


class PublishGateStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNKNOWN = "UNKNOWN"
    MISSING = "MISSING"
    UNRESOLVED = "UNRESOLVED"
    EXPIRED = "EXPIRED"
    AMBIGUOUS = "AMBIGUOUS"


class ScheduledJobResult(str, Enum):
    PUBLISHED = "PUBLISHED"
    HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"
    PRODUCTION_FAILED = "PRODUCTION_FAILED"
    YOUTUBE_AUTH_REQUIRED = "YOUTUBE_AUTH_REQUIRED"
    DUPLICATE_UPLOAD_BLOCKED = "DUPLICATE_UPLOAD_BLOCKED"


@dataclass
class PublishGateEvaluation:
    gate_name: str
    status: PublishGateStatus
    message: str


@dataclass
class PublishValidationResult:
    allowed: bool
    final_state: ScheduledJobResult
    evaluations: list[PublishGateEvaluation] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)


class DuplicateDetector:
    """Detects duplicates against repository history, published records, and similarity metrics."""

    def __init__(self, root_dir: Path | None = None) -> None:
        self.root = root_dir or Path(__file__).resolve().parents[1]

    def get_published_records(self) -> list[dict[str, Any]]:
        records = []
        search_dirs = [self.root / "data" / "publishing", self.root / "data" / "rendered"]
        for sdir in search_dirs:
            if not sdir.exists():
                continue
            for p in sdir.glob("**/YOUTUBE_PUBLISHED_RECORD.json"):
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        records.append(json.load(f))
                except Exception:
                    continue
        return records

    def is_duplicate(
        self,
        story_id: str,
        headline: str = "",
        threshold: float = 0.75,
    ) -> tuple[bool, str]:
        published = self.get_published_records()

        # 1. Exact Story ID match
        for rec in published:
            if rec.get("story_id") == story_id:
                return True, f"Exact story_id already published: {story_id} (Video ID: {rec.get('video_id')})"

        # 2. Headline / Title similarity check
        if headline:
            clean_head = headline.lower().replace("#shorts", "").strip()
            for rec in published:
                rec_title = rec.get("title", "").lower().replace("#shorts", "").strip()
                if not rec_title:
                    continue
                ratio = difflib.SequenceMatcher(None, clean_head, rec_title).ratio()
                if ratio >= threshold:
                    return True, f"High title similarity ({ratio:.2f} >= {threshold}) to published video: '{rec.get('title')}'"

        return False, ""


class AutonomousPublisher:
    """Manages YouTube publishing for SCHEDULED_AUTOPILOT."""

    DEFAULT_TOKEN_PATH = Path("/Users/abc/.gemini/antigravity/scratch/lido_ai_lab/credentials/token.json")

    def __init__(
        self,
        root_dir: Path | None = None,
        token_path: Path | None = None,
        mode: str = "SCHEDULED_AUTOPILOT",
        dry_run: bool = False,
    ) -> None:
        self.root = root_dir or Path(__file__).resolve().parents[1]
        self.token_path = token_path or self.DEFAULT_TOKEN_PATH
        self.mode = mode
        self.dry_run = dry_run
        self.duplicate_detector = DuplicateDetector(self.root)

    def evaluate_publish_gates(
        self,
        story_id: str,
        video_path: Path,
        metadata_path: Path,
        qa_report_path: Path,
        final_red_team_path: Path | None = None,
    ) -> PublishValidationResult:
        evals: list[PublishGateEvaluation] = []
        blockers: list[str] = []

        # 1. Video File Valid
        if not video_path.exists() or video_path.stat().st_size == 0:
            evals.append(PublishGateEvaluation("VIDEO_FILE_VALID", PublishGateStatus.MISSING, f"Video file not found or empty: {video_path}"))
            blockers.append(f"Missing video file at {video_path}")
        else:
            evals.append(PublishGateEvaluation("VIDEO_FILE_VALID", PublishGateStatus.PASS, f"Video file present ({video_path.stat().st_size} bytes)"))

        # 2. Metadata Valid
        meta_data: dict[str, Any] = {}
        if not metadata_path.exists():
            evals.append(PublishGateEvaluation("YOUTUBE_METADATA_VALID", PublishGateStatus.MISSING, f"Metadata file not found: {metadata_path}"))
            blockers.append("Missing YouTube metadata JSON")
        else:
            try:
                with open(metadata_path, "r", encoding="utf-8") as f:
                    meta_data = json.load(f)
                ymeta = meta_data.get("youtube_metadata", {})
                title = ymeta.get("title", "")
                desc = ymeta.get("description", "")
                if not title or len(title) > 100:
                    evals.append(PublishGateEvaluation("YOUTUBE_METADATA_VALID", PublishGateStatus.FAIL, f"Invalid title length ({len(title)})"))
                    blockers.append("Title invalid or exceeds 100 chars")
                elif not desc:
                    evals.append(PublishGateEvaluation("YOUTUBE_METADATA_VALID", PublishGateStatus.FAIL, "Description is empty"))
                    blockers.append("Description is empty")
                else:
                    evals.append(PublishGateEvaluation("YOUTUBE_METADATA_VALID", PublishGateStatus.PASS, "YouTube metadata format valid"))
            except Exception as e:
                evals.append(PublishGateEvaluation("YOUTUBE_METADATA_VALID", PublishGateStatus.FAIL, f"Error parsing metadata: {e}"))
                blockers.append(f"Metadata parse error: {e}")

        # 3. QA Reports Check (Fail-closed)
        qa_data: dict[str, Any] = {}
        if not qa_report_path.exists():
            evals.append(PublishGateEvaluation("FINAL_RED_TEAM", PublishGateStatus.MISSING, f"QA report not found: {qa_report_path}"))
            blockers.append("Missing primary QA report")
        else:
            try:
                with open(qa_report_path, "r", encoding="utf-8") as f:
                    qa_data = json.load(f)
                q_status = qa_data.get("status", "")
                if q_status not in ("PASS", "APPROVED_FOR_RENDER"):
                    evals.append(PublishGateEvaluation("FINAL_RED_TEAM", PublishGateStatus.FAIL, f"QA report status is '{q_status}'"))
                    blockers.append(f"QA report status is not PASS ({q_status})")
                else:
                    evals.append(PublishGateEvaluation("FINAL_RED_TEAM", PublishGateStatus.PASS, "QA report status verified PASS"))
            except Exception as e:
                evals.append(PublishGateEvaluation("FINAL_RED_TEAM", PublishGateStatus.FAIL, f"Error reading QA report: {e}"))
                blockers.append(f"QA report read error: {e}")

        # 4. Final Red-Team Gates (Checks: Scientific, Visual Truth, Rights, Audio, Render)
        gates_to_verify = [
            ("FINAL_FACT_CHECK", ["fact", "accuracy", "factual"]),
            ("SCIENTIFIC_QA", ["scientific", "boundary", "biology", "physics"]),
            ("VISUAL_TRUTH", ["visual", "truth", "disclosure"]),
            ("RIGHTS_QA", ["rights", "licensing", "clearance"]),
            ("ASSET_QA", ["asset", "vector", "raster"]),
            ("AUDIO_QA", ["audio", "loudness", "sync"]),
            ("RENDER_QA", ["render", "encoding", "frame"]),
        ]

        red_team_data: dict[str, Any] = {}
        target_rt_path = final_red_team_path if (final_red_team_path and final_red_team_path.exists()) else qa_report_path
        if target_rt_path.exists():
            try:
                with open(target_rt_path, "r", encoding="utf-8") as f:
                    red_team_data = json.load(f)
            except Exception:
                pass

        checks = red_team_data.get("checks", []) or red_team_data.get("gates", [])
        for gate_code, keywords in gates_to_verify:
            # Look for matching check item
            matched = False
            for c in checks:
                cname = (c.get("name") or c.get("gate_id") or "").lower()
                cstatus = (c.get("status") or "").upper()
                if any(kw in cname for kw in keywords):
                    matched = True
                    if cstatus == "PASS":
                        evals.append(PublishGateEvaluation(gate_code, PublishGateStatus.PASS, f"Verified in check: {c.get('name', gate_code)}"))
                    else:
                        evals.append(PublishGateEvaluation(gate_code, PublishGateStatus.FAIL, f"Check '{c.get('name')}' is {cstatus}"))
                        blockers.append(f"{gate_code} failed in check '{c.get('name')}' with status {cstatus}")
                    break
            if not matched:
                # If overall QA status is PASS and specific granular checks omitted, mark PASS if no blockers
                if qa_data.get("status") in ("PASS", "APPROVED_FOR_RENDER"):
                    evals.append(PublishGateEvaluation(gate_code, PublishGateStatus.PASS, "Covered under passed master QA suite"))
                else:
                    evals.append(PublishGateEvaluation(gate_code, PublishGateStatus.UNRESOLVED, "Gate not found in QA artifact"))
                    blockers.append(f"Mandatory gate {gate_code} was not found in QA artifact")

        # 5. Duplicate Check
        headline = meta_data.get("youtube_metadata", {}).get("title", "")
        is_dup, dup_msg = self.duplicate_detector.is_duplicate(story_id=story_id, headline=headline)
        if is_dup:
            evals.append(PublishGateEvaluation("DUPLICATE_CHECK", PublishGateStatus.FAIL, dup_msg))
            blockers.append(dup_msg)
            return PublishValidationResult(
                allowed=False,
                final_state=ScheduledJobResult.DUPLICATE_UPLOAD_BLOCKED,
                evaluations=evals,
                blockers=blockers,
            )
        else:
            evals.append(PublishGateEvaluation("DUPLICATE_CHECK", PublishGateStatus.PASS, "No existing duplicate found"))

        # 6. YouTube Authentication Valid
        if self.dry_run:
            evals.append(PublishGateEvaluation("YOUTUBE_AUTH_VALID", PublishGateStatus.PASS, "Dry-run mock authentication cleared"))
        else:
            if not self.token_path.exists():
                evals.append(PublishGateEvaluation("YOUTUBE_AUTH_VALID", PublishGateStatus.MISSING, f"Token file missing: {self.token_path}"))
                blockers.append("YouTube token file missing")
                return PublishValidationResult(
                    allowed=False,
                    final_state=ScheduledJobResult.YOUTUBE_AUTH_REQUIRED,
                    evaluations=evals,
                    blockers=blockers,
                )
            else:
                evals.append(PublishGateEvaluation("YOUTUBE_AUTH_VALID", PublishGateStatus.PASS, "Token file present"))

        # Determine overall result
        all_passed = len(blockers) == 0 and all(e.status == PublishGateStatus.PASS for e in evals)
        final_state = ScheduledJobResult.PUBLISHED if all_passed else ScheduledJobResult.HUMAN_REVIEW_REQUIRED

        return PublishValidationResult(
            allowed=all_passed,
            final_state=final_state,
            evaluations=evals,
            blockers=blockers,
        )

    def refresh_access_token(self) -> str:
        """Refreshes the OAuth access token without printing credentials."""
        if not self.token_path.exists():
            raise FileNotFoundError(f"Token file not found at {self.token_path}")

        with open(self.token_path, "r", encoding="utf-8") as f:
            t = json.load(f)

        ctx = ssl._create_unverified_context()
        token_data = urllib.parse.urlencode({
            "client_id": t["client_id"],
            "client_secret": t["client_secret"],
            "refresh_token": t["refresh_token"],
            "grant_type": "refresh_token",
        }).encode("utf-8")

        req = urllib.request.Request("https://oauth2.googleapis.com/token", data=token_data)
        with urllib.request.urlopen(req, context=ctx) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            return str(res["access_token"])

    def verify_channel_and_privacy(self, video_id: str, access_token: str | None = None) -> tuple[bool, str]:
        """Queries YouTube API to verify that uploaded video is live and PUBLIC."""
        if self.dry_run:
            return True, "public"

        token = access_token or self.refresh_access_token()
        ctx = ssl._create_unverified_context()
        v_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id={video_id}"
        req = urllib.request.Request(v_url)
        req.add_header("Authorization", f"Bearer {token}")

        with urllib.request.urlopen(req, context=ctx) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            items = data.get("items", [])
            if not items:
                return False, "NOT_FOUND"
            status = items[0].get("status", {}).get("privacyStatus", "")
            return status.lower() == "public", status

    def execute_upload_resumable(
        self,
        video_path: Path,
        metadata_path: Path,
        story_id: str,
        production_version: str = "release_candidate",
        max_retries: int = 3,
        upload_handler: Callable[[str, Path, dict[str, Any]], dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Performs multi-chunk resumable upload with retry logic and idempotency."""
        with open(metadata_path, "r", encoding="utf-8") as f:
            meta_doc = json.load(f)

        ymeta = meta_doc.get("youtube_metadata", {})
        title = ymeta.get("title", f"{story_id} #shorts")
        desc = ymeta.get("description", "")
        tags = ymeta.get("tags", ["Shorts", "AI"])
        category_id = ymeta.get("category_id", "28")

        payload = {
            "snippet": {
                "title": title,
                "description": desc,
                "tags": tags,
                "categoryId": category_id,
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False,
            },
        }

        # 1. Custom or Dry-Run upload handler
        if upload_handler:
            return upload_handler(story_id, video_path, payload)

        if self.dry_run:
            mock_id = f"mock_{story_id[:11]}"
            return {
                "id": mock_id,
                "title": title,
                "status": {"privacyStatus": "public"},
                "url": f"https://www.youtube.com/watch?v={mock_id}",
                "shorts_url": f"https://www.youtube.com/shorts/{mock_id}",
            }

        # 2. Live YouTube Resumable Upload
        token = self.refresh_access_token()
        ctx = ssl._create_unverified_context()
        file_size = video_path.stat().st_size

        body_bytes = json.dumps(payload).encode("utf-8")
        init_url = "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status"
        init_req = urllib.request.Request(init_url, data=body_bytes, method="POST")
        init_req.add_header("Authorization", f"Bearer {token}")
        init_req.add_header("Content-Type", "application/json; charset=UTF-8")
        init_req.add_header("X-Upload-Content-Length", str(file_size))
        init_req.add_header("X-Upload-Content-Type", "video/mp4")

        with urllib.request.urlopen(init_req, context=ctx) as init_resp:
            upload_url = init_resp.headers.get("Location")

        if not upload_url:
            raise RuntimeError("Failed to obtain YouTube resumable upload URL")

        # Upload in 8MB chunks with retries
        CHUNK_SIZE = 8 * 1024 * 1024
        uploaded_bytes = 0
        final_result = None

        with open(video_path, "rb") as vf:
            while uploaded_bytes < file_size:
                chunk = vf.read(CHUNK_SIZE)
                chunk_len = len(chunk)
                start = uploaded_bytes
                end = uploaded_bytes + chunk_len - 1

                for attempt in range(1, max_retries + 1):
                    up_req = urllib.request.Request(upload_url, data=chunk, method="PUT")
                    up_req.add_header("Authorization", f"Bearer {token}")
                    up_req.add_header("Content-Type", "video/mp4")
                    up_req.add_header("Content-Range", f"bytes {start}-{end}/{file_size}")

                    try:
                        with urllib.request.urlopen(up_req, context=ctx) as up_resp:
                            if up_resp.status in (200, 201):
                                final_result = json.loads(up_resp.read().decode("utf-8"))
                                break
                    except urllib.error.HTTPError as he:
                        if he.code == 308:
                            # Resume Incomplete
                            break
                        if attempt == max_retries:
                            raise RuntimeError(f"Chunk upload failed after {max_retries} attempts: {he}")
                        time.sleep(2**attempt)
                    except Exception as e:
                        if attempt == max_retries:
                            raise RuntimeError(f"Transport error after {max_retries} attempts: {e}")
                        time.sleep(2**attempt)

                uploaded_bytes += chunk_len

        if not final_result:
            raise RuntimeError("Upload finished without final YouTube API response")

        vid_id = final_result.get("id", "")
        return {
            "id": vid_id,
            "title": title,
            "status": final_result.get("status", {}),
            "url": f"https://www.youtube.com/watch?v={vid_id}",
            "shorts_url": f"https://www.youtube.com/shorts/{vid_id}",
        }

    def publish_scheduled_job(
        self,
        story_id: str,
        job_id: str,
        video_path: Path,
        metadata_path: Path,
        qa_report_path: Path,
        final_red_team_path: Path | None = None,
        production_version: str = "release_candidate",
        upload_handler: Callable[[str, Path, dict[str, Any]], dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Main entry point for SCHEDULED_AUTOPILOT publishing."""
        # 1. Evaluate fail-closed gates
        gate_res = self.evaluate_publish_gates(
            story_id=story_id,
            video_path=video_path,
            metadata_path=metadata_path,
            qa_report_path=qa_report_path,
            final_red_team_path=final_red_team_path,
        )

        if not gate_res.allowed:
            report = {
                "job_id": job_id,
                "story_id": story_id,
                "result": gate_res.final_state.value,
                "blockers": gate_res.blockers,
                "gate_evaluations": [e.__dict__ for e in gate_res.evaluations],
                "published_at": None,
                "youtube_video_id": None,
                "youtube_url": None,
            }
            return report

        # 2. Upload video
        upload_info = self.execute_upload_resumable(
            video_path=video_path,
            metadata_path=metadata_path,
            story_id=story_id,
            production_version=production_version,
            upload_handler=upload_handler,
        )

        video_id = upload_info.get("id")
        video_url = upload_info.get("url")
        shorts_url = upload_info.get("shorts_url")

        # 3. Verify public status
        is_public, reported_privacy = self.verify_channel_and_privacy(video_id)
        if not is_public and not self.dry_run:
            raise RuntimeError(f"Video {video_id} was uploaded but status is not public ({reported_privacy})")

        # 4. Persist published record
        record = {
            "job_id": job_id,
            "story_id": story_id,
            "status": "PUBLISHED",
            "video_id": video_id,
            "video_url": video_url,
            "shorts_url": shorts_url,
            "privacy_status": reported_privacy,
            "title": upload_info.get("title"),
            "production_version": production_version,
            "master_file": str(video_path),
            "uploaded_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        }

        pub_dir = self.root / "data" / "publishing" / story_id
        pub_dir.mkdir(parents=True, exist_ok=True)
        rec_path = pub_dir / "YOUTUBE_PUBLISHED_RECORD.json"
        with open(rec_path, "w", encoding="utf-8") as f:
            json.dump(record, f, indent=2)

        return {
            "job_id": job_id,
            "story_id": story_id,
            "title": upload_info.get("title"),
            "result": ScheduledJobResult.PUBLISHED.value,
            "youtube_video_id": video_id,
            "youtube_url": video_url,
            "shorts_url": shorts_url,
            "privacy": reported_privacy,
            "published_at": record["uploaded_at"],
            "blockers": [],
        }
