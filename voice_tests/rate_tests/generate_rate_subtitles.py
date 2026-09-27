# Subtitles for the 3 sections:
# 00-15s: ARIA / 165 WPM
# 15-30s: ARIA / 170 WPM
# 30-45s: ARIA / 175 WPM

def format_timestamp_srt(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int(round((seconds - int(seconds)) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

sections = [
    {
        "offset": 0.0,
        "label": "ARIA / 165 WPM",
        "sublabel": "Cadence: Natural Explainer • +26% Rate",
    },
    {
        "offset": 15.0,
        "label": "ARIA / 170 WPM",
        "sublabel": "Cadence: Broadcast Pace • +30% Rate",
    },
    {
        "offset": 30.0,
        "label": "ARIA / 175 WPM",
        "sublabel": "Cadence: Rapid Energy • +34% Rate",
    },
]

phrases = [
    (0.0, 4.8, "Artificial intelligence is moving faster than most teams can track."),
    (4.8, 9.6, "Every week brings new models, benchmarks, and autonomous agents."),
    (9.6, 14.7, "The real bottleneck is no longer raw compute."),
]

srt_lines = []
counter = 1

for sec in sections:
    base = sec["offset"]
    for p_start, p_end, text in phrases:
        s_start = base + p_start
        s_end = base + p_end
        srt_lines.append(str(counter))
        srt_lines.append(f"{format_timestamp_srt(s_start)} --> {format_timestamp_srt(s_end)}")
        srt_lines.append(f"[{sec['label']} | {sec['sublabel']}]\n{text}\n")
        counter += 1

with open("voice_tests/rate_tests/rate_subtitles.srt", "w") as f:
    f.write("\n".join(srt_lines))

print("Created voice_tests/rate_tests/rate_subtitles.srt")
