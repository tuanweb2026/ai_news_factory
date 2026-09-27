import subprocess
import os

# We will create exactly 15.00s for each candidate:
# Candidate A: 0.00s to 15.00s
# Candidate B: 15.00s to 30.00s
# Candidate C: 30.00s to 45.00s
# Candidate D: 45.00s to 60.00s
#
# To ensure natural audio without awkward mid-sentence cutoffs, we extract the first 14.5s of each candidate,
# add a smooth 0.3s fade-out ending at 14.8s, and pad with silence to exactly 15.00s.
#
# Let's test ffmpeg filters for each candidate chunk:

os.makedirs("voice_tests/audio_segments", exist_ok=True)

candidates = [
    ("candidate-a", "voice_tests/voice_samples/candidate-a.wav"),
    ("candidate-b", "voice_tests/voice_samples/candidate-b.wav"),
    ("candidate-c", "voice_tests/voice_samples/candidate-c.wav"),
    ("candidate-d", "voice_tests/voice_samples/candidate-d.wav"),
]

for name, path in candidates:
    out_path = f"voice_tests/audio_segments/{name}_15s.wav"
    # Extract 0 to 14.7s with afade out at 14.4s (0.3s duration), then apad to 15.0s
    cmd = [
        "ffmpeg", "-y", "-i", path,
        "-af", "atrim=0:14.7,afade=t=out:st=14.4:d=0.3,apad=whole_dur=15.0",
        "-ar", "48000", "-ac", "2",
        out_path
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Created {out_path}")

# Now concatenate the four 15s segments to create speech_60s.wav (total 60.00s)
concat_list = "voice_tests/audio_segments/concat.txt"
with open(concat_list, "w") as f:
    for name, _ in candidates:
        f.write(f"file '{name}_15s.wav'\n")

cmd_concat = [
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list,
    "-c", "copy", "voice_tests/speech_60s.wav"
]
subprocess.run(cmd_concat, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("Created voice_tests/speech_60s.wav")

# Generate ambient background drone (low-level sine/drone at -24 dB or gentle synth bed)
# 60 seconds duration
drone_wav = "voice_tests/ambient_drone_60s.wav"
cmd_drone = [
    "ffmpeg", "-y", "-f", "lavfi",
    "-i", "anoisesrc=d=60:c=pink:r=48000:a=0.015,lowpass=f=250,volume=-24dB",
    "-ar", "48000", "-ac", "2",
    drone_wav
]
subprocess.run(cmd_drone, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("Created voice_tests/ambient_drone_60s.wav")

# Mix speech and drone with exact normalization
master_wav = "voice_tests/master_benchmark_audio.wav"
cmd_mix = [
    "ffmpeg", "-y",
    "-i", "voice_tests/speech_60s.wav",
    "-i", drone_wav,
    "-filter_complex", "[0:a][1:a]amix=inputs=2:duration=first:dropout_transition=0,loudnorm=I=-16:LRA=11:TP=-1.5[aout]",
    "-map", "[aout]",
    "-ar", "48000", "-ac", "2",
    master_wav
]
subprocess.run(cmd_mix, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("Created master_benchmark_audio.wav")

