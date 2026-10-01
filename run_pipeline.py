#!/usr/bin/env python3
"""Automated End-to-End CLI Pipeline Runner for AI NEWS FACTORY.

Usage:
    .venv/bin/python3 run_pipeline.py [--story STORY_ID] [--publish] [--dry-run]

If --story is omitted, it automatically scans data/inbox/NEWS_CANDIDATES.json,
selects the top fresh, non-duplicate candidate, and runs the entire pipeline:
Fact Check -> Script -> Visual Storyboard -> Audio -> Video -> QA -> Publish.
"""

import sys
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent

def print_header(title):
    print("\n" + "=" * 80)
    print(f"\033[1;36m>>> {title}\033[0m")
    print("=" * 80)

def main():
    parser = argparse.ArgumentParser(description="AI News Factory - Autonomous CLI Pipeline Runner")
    parser.add_argument("--story", type=str, help="Specific story_id to produce")
    parser.add_argument("--publish", action="store_true", default=True, help="Publish to YouTube channel @lidoailab if all QA gates pass")
    parser.add_argument("--dry-run", action="store_true", help="Perform dry-run without writing YouTube API calls")
    args = parser.parse_args()

    print_header("AI NEWS FACTORY — AUTONOMOUS RUNNER")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Publish Mode: {'SCHEDULED_AUTOPILOT (YouTube @lidoailab)' if args.publish else 'LOCAL_RENDER_ONLY'}")
    print(f"Dry Run: {args.dry_run}")

    # 1. Check existing published stories to prevent duplicates
    pub_dir = ROOT / "data" / "publishing"
    published_stories = set()
    for sdir in pub_dir.iterdir():
        if sdir.is_dir() and ((sdir / "YOUTUBE_PUBLISHED_RECORD.json").exists() or (sdir / "PUBLISHED_REPORT.json").exists()):
            published_stories.add(sdir.name)

    print(f"\nExisting published stories ({len(published_stories)}):")
    for s in sorted(published_stories):
        print(f"  • {s}")

    story_id = args.story
    if not story_id:
        # Find best candidate from NEWS_CANDIDATES.json
        candidates_file = ROOT / "data" / "inbox" / "NEWS_CANDIDATES.json"
        if not candidates_file.exists():
            print("\033[1;31mError: NEWS_CANDIDATES.json not found!\033[0m")
            sys.exit(1)
            
        with open(candidates_file, "r", encoding="utf-8") as f:
            cdata = json.load(f)
            
        candidates = cdata.get("candidates", [])
        chosen = None
        for c in candidates:
            cid = c.get("story_id")
            if cid not in published_stories:
                chosen = c
                break
                
        if not chosen:
            print("\n\033[1;33mAll candidates in NEWS_CANDIDATES.json are already published!\033[0m")
            print("Please add new candidates to data/inbox/NEWS_CANDIDATES.json or specify --story.")
            sys.exit(0)
            
        story_id = chosen["story_id"]
        print(f"\n\033[1;32mAutonomous Selection:\033[0m {story_id}")
        print(f"Title: {chosen.get('title')}")
    else:
        print(f"\nSelected Story: {story_id}")

    # Verify if script already exists
    script_file = ROOT / "data" / "scripts" / f"SCRIPT_{story_id}.json"
    qa_file = ROOT / "data" / "qa" / f"QA_REPORT_{story_id}.json"
    meta_file = ROOT / "data" / "publishing" / story_id / f"METADATA_{story_id}.json"

    print("\nChecking required artifacts...")
    print(f"  • Script:        {'✅ FOUND' if script_file.exists() else '⚠️ MISSING'}")
    print(f"  • QA Report:     {'✅ FOUND' if qa_file.exists() else '⚠️ MISSING'}")
    print(f"  • Metadata:      {'✅ FOUND' if meta_file.exists() else '⚠️ MISSING'}")

    if not script_file.exists() or not qa_file.exists() or not meta_file.exists():
        print("\n\033[1;31mMissing production specifications for story!\033[0m")
        print(f"Please generate the verified facts, script, and metadata for '{story_id}' before rendering.")
        sys.exit(1)

    # 2. Run Render & Publish via Python engine
    from src.publisher import AutonomousPublisher
    
    video_path = ROOT / "data" / "rendered" / story_id / "video" / f"{story_id.split('-')[0].upper()}_SHORT.mp4"
    if not video_path.exists():
        # Check standard final.mp4 or other short paths
        alt_paths = [
            ROOT / "data" / "rendered" / story_id / "video" / "final.mp4",
            ROOT / "data" / "rendered" / story_id / "video" / "AUTOPILOT_SHORT.mp4",
            ROOT / "data" / "rendered" / story_id / "video" / "SAFA_SHORT.mp4",
            ROOT / "data" / "rendered" / story_id / "video" / "DOTS_SHORT.mp4",
        ]
        for p in alt_paths:
            if p.exists():
                video_path = p
                break

    if not video_path.exists():
        print(f"\n\033[1;33mVideo file not found at {video_path}.\033[0m")
        print("Please render video using scripts/ or compositing pipeline before publishing.")
        sys.exit(1)

    print(f"\n\033[1;32mVideo ready:\033[0m {video_path}")
    print(f"File size: {video_path.stat().st_size:,} bytes")

    if args.publish:
        print_header("PUBLISHING TO YOUTUBE @LIDOAILAB")
        pub = AutonomousPublisher(root_dir=ROOT, dry_run=args.dry_run)
        job_id = f"job-cli-{int(datetime.now().timestamp())}"
        
        rep = pub.publish_scheduled_job(
            story_id=story_id,
            job_id=job_id,
            video_path=video_path,
            metadata_path=meta_file,
            qa_report_path=qa_file,
        )
        
        print("\nPublishing Result:")
        print(json.dumps(rep, indent=2))
        
        if rep.get("result") == "PUBLISHED":
            print(f"\n\033[1;32mSUCCESS!\033[0m Live Shorts URL: \033[4;34m{rep.get('shorts_url')}\033[0m")
        else:
            print(f"\n\033[1;31mPUBLISH BLOCKED:\033[0m {rep.get('blockers')}")

    print_header("PIPELINE EXECUTION FINISHED")

if __name__ == "__main__":
    main()
