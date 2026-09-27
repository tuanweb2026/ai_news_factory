# Generate SRT and ASS subtitles for the 60-second video
# Format:
# 00:00 - 00:15: Candidate A (en-GB-RyanNeural)
# 00:15 - 00:30: Candidate B (en-GB-SoniaNeural)
# 00:30 - 00:45: Candidate C (en-US-AriaNeural)
# 00:45 - 01:00: Candidate D (en-US-ChristopherNeural)

def format_timestamp_srt(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int(round((seconds - int(seconds)) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def format_timestamp_ass(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int(round((seconds - int(seconds)) * 100))
    return f"{h:01d}:{m:02d}:{s:02d}.{cs:02d}"

sections = [
    {
        "offset": 0.0,
        "voice": "VOICE A: en-GB-RyanNeural",
        "style": "British Neural • Technology News",
    },
    {
        "offset": 15.0,
        "voice": "VOICE B: en-GB-SoniaNeural",
        "style": "British Neural • Broadcast Explainer",
    },
    {
        "offset": 30.0,
        "voice": "VOICE C: en-US-AriaNeural",
        "style": "US Neural • Newscast Professional",
    },
    {
        "offset": 45.0,
        "voice": "VOICE D: en-US-ChristopherNeural",
        "style": "US Neural • Broadcast Authority",
    },
]

# Each 15s section has three narration phrases corresponding to the first 14.5s:
# 1. 0.0 - 5.0: "Artificial intelligence is moving faster than most teams can track."
# 2. 5.0 - 10.0: "Every week brings new models, new reasoning benchmarks, and new autonomous agents."
# 3. 10.0 - 14.5: "The real bottleneck is no longer raw compute."

phrases = [
    (0.0, 5.0, "Artificial intelligence is moving faster than most teams can track."),
    (5.0, 10.0, "Every week brings new models, benchmarks, and autonomous agents."),
    (10.0, 14.7, "The real bottleneck is no longer raw compute."),
]

srt_lines = []
counter = 1

for sec in sections:
    base = sec["offset"]
    # Header label display for the candidate throughout the section
    for p_start, p_end, text in phrases:
        s_start = base + p_start
        s_end = base + p_end
        srt_lines.append(str(counter))
        srt_lines.append(f"{format_timestamp_srt(s_start)} --> {format_timestamp_srt(s_end)}")
        srt_lines.append(f"[{sec['voice']} | {sec['style']}]\n{text}\n")
        counter += 1

with open("voice_tests/benchmark_subtitles.srt", "w") as f:
    f.write("\n".join(srt_lines))

print("Created voice_tests/benchmark_subtitles.srt")

# Also create ASS format with high quality styling
ass_content = """[Script Info]
Title: AI News Factory Voice Benchmark
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: None
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: VoiceTag,Arial,42,&H004DEBFF,&H000000FF,&H00070A0F,&H80000000,-1,0,0,0,100,100,1,0,1,3,0,8,60,60,250,1
Style: SubtitleText,Arial,48,&H00FFFFFF,&H000000FF,&H00070A0F,&H80000000,-1,0,0,0,100,100,1,0,1,3,0,2,80,80,340,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

for sec in sections:
    base = sec["offset"]
    tag_start = format_timestamp_ass(base)
    tag_end = format_timestamp_ass(base + 14.8)
    tag_text = f"\\b1[{sec['voice']}]\\b0\\N{sec['style']}"
    ass_content += f"Dialogue: 0,{tag_start},{tag_end},VoiceTag,,0,0,0,,{tag_text}\n"

    for p_start, p_end, text in phrases:
        t_start = format_timestamp_ass(base + p_start)
        t_end = format_timestamp_ass(base + p_end)
        ass_content += f"Dialogue: 0,{t_start},{t_end},SubtitleText,,0,0,0,,{text}\n"

with open("voice_tests/benchmark_subtitles.ass", "w") as f:
    f.write(ass_content)

print("Created voice_tests/benchmark_subtitles.ass")
