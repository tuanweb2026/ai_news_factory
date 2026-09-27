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
word_count = len(test_script.split())

# We want 3 variants:
# Target A: 165 WPM -> target duration = (65 / 165) * 60 = 23.636s
# Target B: 170 WPM -> target duration = (65 / 170) * 60 = 22.941s
# Target C: 175 WPM -> target duration = (65 / 175) * 60 = 22.285s

# Let's test a range of rates to find the exact rate strings for 165, 170, and 175 WPM:
rates_to_try = ["+16%", "+18%", "+19%", "+20%", "+21%", "+22%", "+23%", "+24%", "+25%", "+26%", "+27%", "+28%"]

async def synthesize_sample(rate_str, out_path):
    cmd = [
        ".venv/bin/edge-tts",
        "--voice", "en-US-AriaNeural",
        "--rate", rate_str,
        "--text", test_script,
        "--write-media", out_path
    ]
    proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    await proc.communicate()

def get_duration_and_wpm(mp3_path):
    # Convert to wav and measure
    wav_path = mp3_path.replace(".mp3", ".wav")
    subprocess.run(["ffmpeg", "-y", "-i", mp3_path, "-ar", "48000", "-ac", "2", wav_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with wave.open(wav_path, "rb") as w:
        frames = w.getnframes()
        rate = w.getframerate()
        dur = frames / float(rate)
    wpm = (word_count / dur) * 60.0
    return dur, wpm, wav_path

async def main():
    results = []
    for r in rates_to_try:
        mp3 = f"voice_tests/rate_tests/aria_{r.replace('+', 'plus').replace('%', 'pct')}.mp3"
        await synthesize_sample(r, mp3)
        dur, wpm, wav = get_duration_and_wpm(mp3)
        results.append((r, dur, wpm, wav))
        print(f"Rate: {r} -> Duration: {dur:.2f}s -> WPM: {wpm:.1f}")

asyncio.run(main())
