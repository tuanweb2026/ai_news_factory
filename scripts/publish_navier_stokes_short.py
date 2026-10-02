#!/usr/bin/env python3
"""Publish OpenAI Navier-Stokes Millennium Problem Short to YouTube @lidoailab
under SCHEDULED_AUTOPILOT mode.
"""

import json
from pathlib import Path
from src.publisher import AutonomousPublisher

def main():
    story_id = "openai-navier-stokes-millennium-problem-proof-2026"
    job_id = "job-20261002-1115-navier-stokes"
    
    video_path = Path("data/rendered/openai-navier-stokes-millennium-problem-proof-2026/video/NAVIER_STOKES_SHORT.mp4")
    metadata_path = Path("data/publishing/openai-navier-stokes-millennium-problem-proof-2026/METADATA_openai-navier-stokes-millennium-problem-proof-2026.json")
    qa_report_path = Path("data/qa/NAVIER_STOKES_RED_TEAM_QA_20261002.json")
    
    print("Initializing AutonomousPublisher...")
    publisher = AutonomousPublisher()
    
    print(f"Executing scheduled job for {story_id}...")
    report = publisher.publish_scheduled_job(
        story_id=story_id,
        job_id=job_id,
        video_path=video_path,
        metadata_path=metadata_path,
        qa_report_path=qa_report_path,
    )
    
    print("Publishing Report:")
    print(json.dumps(report, indent=2))
    
    out_report = Path(f"data/publishing/{story_id}/PUBLISHED_REPORT.json")
    with open(out_report, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"Report saved to {out_report}")

if __name__ == "__main__":
    main()
