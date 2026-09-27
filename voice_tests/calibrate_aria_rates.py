import asyncio
import os
import subprocess
import wave

test_script = (
    "Artificial intelligence is moving faster than most teams can track. "
    "Every week brings new models, new reasoning benchmarks, and new autonomous agents. "
    "The real bottleneck is no longer raw compute. "
    "It is whether your systems can make fast, reliable decisions under uncertainty. "
    "Watch how this architecture adapts in real time."
)
# Note: word count is 50 words! Let's check:
words = test_script.split()
word_count = len(words)
print(f"Exact word count in script: {word_count}")

# 50 words:
# For 165 WPM: Target duration = (50 / 165) * 60 = 18.18s
# For 170 WPM: Target duration = (50 / 170) * 60 = 17.65s
# For 175 WPM: Target duration = (50 / 175) * 60 = 17.14s

# From our previous run:
# Rate +26% -> 18.19s -> WPM = (50 / 18.19) * 60 = 164.9 WPM (~165 WPM!)
# Let's test +29%, +30%, +31%, +32%, +33%, +34%, +35% to find exact 170 WPM and 175 WPM

rates_to_try = ["+26%", "+29%", "+30%", "+31%", "+32%", "+33%", "+34%", "+35%", "+36%"]

async def synthesize(rate_str):
    out_mp3 = f"voice_tests/rate_tests/aria_{rate_str.replace('+', 'plus').replace('%', 'pct')}.mp3"
    cmd = [
        ".venv/bin/edge-tts",
        "--voice", "en-US-AriaNeural",
        "--rate", rate_str,
        "--text", test_script,
        "--write-media", out_mp3
    ]
    proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    await proc.communicate()
    wav_path = out_mp3.replace(".mp3", ".wav")
    subprocess.run(["ffmpeg", "-y", "-i", out_mp3, "-ar", "48000", "-ac", "2", wav_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with wave.open(wav_path, "rb") as w:
        dur = w.getnframes() / float(w.getframerate())
    wpm = (word_count / dur) * 60.0
    return rate_str, dur, wpm, wav_path

async def main():
    for r in rates_to_try:
        rate_str, dur, wpm, wav_path = await synthesize(r)
        print(f"Rate: {rate_str} -> Duration: {dur:.2f}s -> WPM: {wpm:.2f}")

asyncio.run(main())
