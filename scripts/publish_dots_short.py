#!/usr/bin/env python3
"""Publish OpenAI DevDay Dots & GPT-6.1 Sol Short to YouTube @lidoailab
under SCHEDULED_AUTOPILOT mode.
"""

import json
from pathlib import Path
from src.publisher import AutonomousPublisher

def main():
    story_id = "openai-devday-dots-persistent-agents-gpt61-sol-2026"
    job_id = "job-20260930-0730-dots"
    
    video_path = Path("data/rendered/openai-devday-dots-persistent-agents-gpt61-sol-2026/video/DOTS_SHORT.mp4")
    metadata_path = Path("data/publishing/openai-devday-dots-persistent-agents-gpt61-sol-2026/METADATA_openai-devday-dots-persistent-agents-gpt61-sol-2026.json")
    qa_report_path = Path("data/qa/OPENAI_DOTS_RED_TEAM_QA_20260930.json")
    
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
    
    # Save report
    out_report = Path(f"data/publishing/{story_id}/PUBLISHED_REPORT.json")
    with open(out_report, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"Report saved to {out_report}")

if __name__ == "__main__":
    main()
