import subprocess
import json
import wave
import re

variants = [
    {
        "id": "variant-a",
        "label": "ARIA / 165 WPM",
        "wpm_target": 165,
        "rate": "+26%",
        "ssml_rate": "+26.0%",
        "mp3": "voice_tests/rate_tests/aria_plus26pct.mp3",
        "raw_wav": "voice_tests/rate_tests/aria_plus26pct.wav",
        "norm_wav": "voice_tests/rate_tests/final_variants/aria_165wpm_norm.wav",
        "section_wav": "voice_tests/rate_tests/final_variants/aria_165wpm_15s.wav"
    },
    {
        "id": "variant-b",
        "label": "ARIA / 170 WPM",
        "wpm_target": 170,
        "rate": "+30%",
        "ssml_rate": "+30.0%",
        "mp3": "voice_tests/rate_tests/aria_plus30pct.mp3",
        "raw_wav": "voice_tests/rate_tests/aria_plus30pct.wav",
        "norm_wav": "voice_tests/rate_tests/final_variants/aria_170wpm_norm.wav",
        "section_wav": "voice_tests/rate_tests/final_variants/aria_170wpm_15s.wav"
    },
    {
        "id": "variant-c",
        "label": "ARIA / 175 WPM",
        "wpm_target": 175,
        "rate": "+34%",
        "ssml_rate": "+33.7%", # +34% gives 175.32 WPM
        "mp3": "voice_tests/rate_tests/aria_plus34pct.mp3",
        "raw_wav": "voice_tests/rate_tests/aria_plus34pct.wav",
        "norm_wav": "voice_tests/rate_tests/final_variants/aria_175wpm_norm.wav",
        "section_wav": "voice_tests/rate_tests/final_variants/aria_175wpm_15s.wav"
    }
]

def analyze_ebur128(wav_path):
    cmd = ["ffmpeg", "-i", wav_path, "-af", "ebur128=framelog=quiet", "-f", "null", "-"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    out = res.stderr
    
    i_match = re.search(r"Integrated loudness:\s+I:\s+([-0-9.]+)\s+LUFS", out)
    tp_match = re.search(r"True peak:\s+Peak:\s+([-0-9.]+)\s+dBFS", out)
    lra_match = re.search(r"Loudness range:\s+LRA:\s+([-0-9.]+)\s+LU", out)
    
    return {
        "lufs": float(i_match.group(1)) if i_match else None,
        "tp": float(tp_match.group(1)) if tp_match else None,
        "lra": float(lra_match.group(1)) if lra_match else None,
    }

results = []

for v in variants:
    # 1. Normalize full speech to -16 LUFS
    cmd_norm = [
        "ffmpeg", "-y", "-i", v["raw_wav"],
        "-af", "loudnorm=I=-16:LRA=11:TP=-1.5",
        "-ar", "48000", "-ac", "2",
        v["norm_wav"]
    ]
    subprocess.run(cmd_norm, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Measure full normalized speech
    with wave.open(v["norm_wav"], "rb") as w:
        frames = w.getnframes()
        dur = frames / float(w.getframerate())
    
    metrics = analyze_ebur128(v["norm_wav"])
    exact_wpm = (50 / dur) * 60.0
    
    # 2. Prepare 15.0s section for comparison video
    # 0 to 14.7s with gentle fade out at 14.4s, padded to exactly 15.0s
    cmd_sec = [
        "ffmpeg", "-y", "-i", v["norm_wav"],
        "-af", "atrim=0:14.7,afade=t=out:st=14.4:d=0.3,apad=whole_dur=15.0",
        "-ar", "48000", "-ac", "2",
        v["section_wav"]
    ]
    subprocess.run(cmd_sec, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    sec_metrics = analyze_ebur128(v["section_wav"])
    
    v_info = {
        "variant": v["id"],
        "label": v["label"],
        "wpm_target": v["wpm_target"],
        "wpm_actual": round(exact_wpm, 2),
        "rate_param": v["rate"],
        "full_duration_s": round(dur, 3),
        "integrated_loudness_lufs": metrics["lufs"],
        "true_peak_dbtp": metrics["tp"],
        "lra": metrics["lra"],
        "section_15s_loudness_lufs": sec_metrics["lufs"],
        "full_wav": v["norm_wav"],
        "section_wav": v["section_wav"]
    }
    results.append(v_info)
    print(f"Processed {v['label']}: Actual WPM={exact_wpm:.2f}, Dur={dur:.2f}s, LUFS={metrics['lufs']}")

with open("voice_tests/rate_tests/variant_measurements.json", "w") as f:
    json.dump(results, f, indent=2)

print("Saved voice_tests/rate_tests/variant_measurements.json")
