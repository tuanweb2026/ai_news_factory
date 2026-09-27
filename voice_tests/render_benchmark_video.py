import subprocess
import os

final_out = "voice_tests/VOICE_BENCHMARK_TEST_VIDEO.mp4"
raw_video = "voice_tests/clips/sequence_60s_raw.mp4"
master_audio = "voice_tests/master_benchmark_audio.wav"
srt_file = os.path.abspath("voice_tests/benchmark_subtitles.srt")

# Composite final video:
# Video: sequence_60s_raw.mp4
# Audio: master_benchmark_audio.wav
# Subtitles: benchmark_subtitles.srt embedded as mov_text (standard MP4 timed text subtitle track)
cmd_final = [
    "ffmpeg", "-y",
    "-i", raw_video,
    "-i", master_audio,
    "-i", srt_file,
    "-c:v", "libx264", "-preset", "medium", "-crf", "18",
    "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
    "-c:s", "mov_text", "-metadata:s:s:0", "language=eng",
    "-t", "60.0",
    final_out
]

print("Running final composite...")
subprocess.run(cmd_final, check=True)
print(f"Successfully generated {final_out}!")

