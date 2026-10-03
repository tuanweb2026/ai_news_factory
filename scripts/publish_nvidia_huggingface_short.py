#!/usr/bin/env python3
"""Publish NVIDIA Hugging Face Short to YouTube @lidoailab
under SCHEDULED_AUTOPILOT mode.
"""

import json
from pathlib import Path
from src.publisher import AutonomousPublisher

def main():
    story_id = "nvidia-acquires-hugging-face-12-9b-2026"
    job_id = "job-20261004-0655-nvidia-hf"
    
    video_path = Path(f"data/rendered/{story_id}/video/NVIDIA_HUGGINGFACE_SHORT.mp4")
    metadata_path = Path(f"data/publishing/{story_id}/METADATA_{story_id}.json")
    qa_report_path = Path(f"data/qa/QA_REPORT_{story_id}.json")
    
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
