#!/usr/bin/env python3
"""CLI Reporter for AI NEWS FACTORY.

Inspects all published records, QA reports, rendered videos,
and displays a clean status overview directly in terminal.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def get_status_badge(privacy):
    p = str(privacy).lower()
    if p == "public":
        return "\033[92m● PUBLIC\033[0m"
    elif p == "unlisted":
        return "\033[93m● UNLISTED\033[0m"
    else:
        return f"\033[90m● {str(privacy).upper()}\033[0m"

def main():
    print("\n" + "=" * 95)
    print("\033[1;36m              AI NEWS FACTORY — YOUTUBE PUBLISHING & PIPELINE REPORT                \033[0m")
    print("=" * 95)
    
    pub_dir = ROOT / "data" / "publishing"
    records = []
    
    for sdir in sorted(pub_dir.iterdir()):
        if not sdir.is_dir():
            continue
        
        rec_file = sdir / "YOUTUBE_PUBLISHED_RECORD.json"
        rep_file = sdir / "PUBLISHED_REPORT.json"
        
        info = {
            "story_id": sdir.name,
            "title": "N/A",
            "video_id": "N/A",
            "privacy": "N/A",
            "published_at": "N/A",
            "url": "N/A",
            "shorts_url": "N/A"
        }
        
        if rec_file.exists():
            try:
                with open(rec_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    info["title"] = data.get("title") or info["title"]
                    info["video_id"] = data.get("video_id") or data.get("id") or info["video_id"]
                    info["privacy"] = data.get("privacy_status") or data.get("privacy") or info["privacy"]
                    info["published_at"] = data.get("uploaded_at") or data.get("published_at") or info["published_at"]
                    info["url"] = data.get("video_url") or data.get("youtube_url") or data.get("url") or info["url"]
                    info["shorts_url"] = data.get("shorts_url") or f"https://www.youtube.com/shorts/{info['video_id']}"
            except Exception:
                pass
                
        if rep_file.exists():
            try:
                with open(rep_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if info["title"] == "N/A":
                        info["title"] = data.get("title") or info["title"]
                    if info["video_id"] == "N/A":
                        info["video_id"] = data.get("youtube_video_id") or info["video_id"]
                    if info["privacy"] == "N/A":
                        info["privacy"] = data.get("privacy") or data.get("privacy_status") or info["privacy"]
                    if info["published_at"] == "N/A":
                        info["published_at"] = data.get("published_at") or data.get("uploaded_at") or info["published_at"]
                    if info["url"] == "N/A":
                        info["url"] = data.get("youtube_url") or info["url"]
                    if info["shorts_url"] == "N/A":
                        info["shorts_url"] = data.get("shorts_url") or f"https://www.youtube.com/shorts/{info['video_id']}"
            except Exception:
                pass

        if info["video_id"] != "N/A":
            records.append(info)

    # Sort records by published_at if available
    records.sort(key=lambda r: r["published_at"], reverse=True)

    print(f"\n\033[1;32mTổng số Video đã phát hành trên @lidoailab:\033[0m \033[1m{len(records)}\033[0m\n")
    print(f"{'STT':<4} | {'Trạng Thái':<18} | {'Video ID':<13} | {'Ngày Phát Hành':<20} | {'Tiêu Đề Video'}")
    print("-" * 110)
    
    for idx, r in enumerate(records, 1):
        status = get_status_badge(r["privacy"])
        pub_time = r["published_at"][:19].replace("T", " ") if r["published_at"] != "N/A" else "N/A"
        title = r["title"][:50] + "..." if len(r["title"]) > 53 else r["title"]
        print(f"{idx:<4} | {status:<27} | {r['video_id']:<13} | {pub_time:<20} | {title}")
        print(f"     \033[90m↳ Link Shorts:\033[0m \033[4;34m{r['shorts_url']}\033[0m")
        print()

    print("=" * 95)
    print("\033[1;33mLệnh Hướng Dẫn Nhanh Cho Terminal:\033[0m")
    print("  • Tự chạy sản xuất tin tức tự động:  \033[32m./run_pipeline.sh\033[0m")
    print("  • Kiểm tra báo cáo phát hành:         \033[32m./check_report.sh\033[0m")
    print("  • Chạy kiểm tra quy chuẩn schema:     \033[32m.venv/bin/python3 src/validate_artifacts.py\033[0m")
    print("=" * 95 + "\n")

if __name__ == "__main__":
    main()
