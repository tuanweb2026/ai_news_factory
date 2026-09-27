import subprocess
import os

final_out = "voice_tests/VOICE_C_RATE_TEST.mp4"
master_audio = "voice_tests/rate_tests/master_rate_test_audio.wav"
srt_file = os.path.abspath("voice_tests/rate_tests/rate_subtitles.srt")

# Create 45.0s video base from sequence_15s.mp4 (which repeats the 5 technical scenes 3.0s each)
# 3 repeats of sequence_15s.mp4 = exactly 45.0s
concat_45s_vid = "voice_tests/rate_tests/concat_vid_45s.txt"
with open(concat_45s_vid, "w") as f:
    for _ in range(3):
        f.write("file '../clips/sequence_15s.mp4'\n")

raw_video_45s = "voice_tests/rate_tests/sequence_45s_raw.mp4"
cmd_vid = [
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_45s_vid,
    "-c", "copy", raw_video_45s
]
subprocess.run(cmd_vid, check=True)
print(f"Generated {raw_video_45s}")

# Final composite:
cmd_final = [
    "ffmpeg", "-y",
    "-i", raw_video_45s,
    "-i", master_audio,
    "-i", srt_file,
    "-c:v", "libx264", "-preset", "medium", "-crf", "18",
    "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
    "-c:s", "mov_text", "-metadata:s:s:0", "language=eng",
    "-t", "45.0",
    final_out
]

print("Rendering VOICE_C_RATE_TEST.mp4...")
subprocess.run(cmd_final, check=True)
print(f"Successfully generated {final_out}!")

