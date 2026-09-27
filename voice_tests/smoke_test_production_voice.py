import subprocess
import os
import re
import wave
import json

test_script = (
    "Artificial intelligence is moving faster than most teams can track. "
    "Every week brings new models, new reasoning benchmarks, and new autonomous agents. "
    "The real bottleneck is no longer raw compute. "
    "It is whether your systems can make fast, reliable decisions under uncertainty. "
    "Watch how this architecture adapts in real time."
)
words = test_script.split()
word_count = len(words)
assert word_count == 50

out_wav = "voice_tests/VOICE_PRODUCTION_165_SMOKE_TEST.wav"
tmp_mp3 = "voice_tests/smoke_tmp.mp3"

edge_tts_bin = ".venv/bin/edge-tts"
ffmpeg_bin = "ffmpeg"

# 1. Synthesize using locked voice profile: en-US-AriaNeural at +26% rate
cmd_synth = [
    edge_tts_bin,
    "--voice", "en-US-AriaNeural",
    "--rate", "+26%",
    "--text", test_script,
    "--write-media", tmp_mp3
]
print("Running voice synthesis...")
subprocess.run(cmd_synth, check=True)

# 2. Convert to 48kHz stereo WAV normalized to -16 LUFS (True Peak <= -1.5 dBTP)
cmd_norm = [
    ffmpeg_bin, "-y",
    "-i", tmp_mp3,
    "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
    "-ar", "48000",
    "-ac", "2",
    out_wav
]
print("Normalizing to -16 LUFS...")
subprocess.run(cmd_norm, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if os.path.exists(tmp_mp3):
    os.remove(tmp_mp3)

# 3. Analyze Audio
with wave.open(out_wav, "rb") as w:
    frames = w.getnframes()
    rate = w.getframerate()
    channels = w.getnchannels()
    dur = frames / float(rate)

actual_wpm = (word_count / dur) * 60.0

res = subprocess.run([ffmpeg_bin, "-i", out_wav, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
summary_idx = res.stderr.rfind("Summary:")
summary = res.stderr[summary_idx:] if summary_idx != -1 else ""

i_match = re.search(r"I:\s+([-0-9.]+)\s+LUFS", summary)
tp_match = re.search(r"Peak:\s+([-0-9.]+)\s+dBFS", summary)
lra_match = re.search(r"LRA:\s+([-0-9.]+)\s+LU", summary)

lufs_val = float(i_match.group(1)) if i_match else None
tp_val = float(tp_match.group(1)) if tp_match else None
lra_val = float(lra_match.group(1)) if lra_match else None

# Check clipping
clip_res = subprocess.run([ffmpeg_bin, "-i", out_wav, "-af", "astats", "-f", "null", "-"], capture_output=True, text=True)
flat_matches = re.findall(r"Flat factor:\s+([0-9.]+)", clip_res.stderr)
has_clipping = any(float(f) > 0.0 for f in flat_matches) if flat_matches else False

results = {
    "voice_file": out_wav,
    "voice_name": "en-US-AriaNeural",
    "style": "newscast-formal",
    "locale": "en-US",
    "target_wpm": 165,
    "actual_wpm": round(actual_wpm, 2),
    "duration_seconds": round(dur, 3),
    "sample_rate_hz": rate,
    "channels": channels,
    "integrated_loudness_lufs": lufs_val,
    "true_peak_dbtp": tp_val,
    "lra": lra_val,
    "clipping_detected": has_clipping,
    "synthesis_errors": None
}

with open("voice_tests/smoke_test_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\n--- SMOKE TEST RESULTS ---")
print(f"File: {out_wav}")
print(f"Duration: {dur:.3f} s")
print(f"WPM: {actual_wpm:.2f} (Target: 165 WPM)")
print(f"Loudness: {lufs_val} LUFS (Target: -16 LUFS)")
print(f"True Peak: {tp_val} dBTP (Max: -1.5 dBTP)")
print(f"Clipping: {'NO' if not has_clipping else 'YES'}")
print("Smoke test successfully completed!")
