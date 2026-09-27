import subprocess

# Concatenate the three 15.0s sections:
# Section 1 (00–15s): ARIA / 165 WPM
# Section 2 (15–30s): ARIA / 170 WPM
# Section 3 (30–45s): ARIA / 175 WPM
concat_list = "voice_tests/rate_tests/concat_45s.txt"
with open(concat_list, "w") as f:
    f.write("file 'final_variants/aria_165wpm_15s.wav'\n")
    f.write("file 'final_variants/aria_170wpm_15s.wav'\n")
    f.write("file 'final_variants/aria_175wpm_15s.wav'\n")

cmd_concat = [
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list,
    "-c", "copy", "voice_tests/rate_tests/speech_45s.wav"
]
subprocess.run(cmd_concat, check=True)
print("Created voice_tests/rate_tests/speech_45s.wav")

# Generate continuous ambient tech drone for 45 seconds at -24 dB
drone_wav = "voice_tests/rate_tests/ambient_drone_45s.wav"
cmd_drone = [
    "ffmpeg", "-y", "-f", "lavfi",
    "-i", "anoisesrc=d=45:c=pink:r=48000:a=0.015,lowpass=f=250,volume=-24dB",
    "-ar", "48000", "-ac", "2",
    drone_wav
]
subprocess.run(cmd_drone, check=True)
print("Created voice_tests/rate_tests/ambient_drone_45s.wav")

# Mix speech and drone, normalise to -16 LUFS
master_wav = "voice_tests/rate_tests/master_rate_test_audio.wav"
cmd_mix = [
    "ffmpeg", "-y",
    "-i", "voice_tests/rate_tests/speech_45s.wav",
    "-i", drone_wav,
    "-filter_complex", "[0:a][1:a]amix=inputs=2:duration=first:dropout_transition=0,loudnorm=I=-16:LRA=11:TP=-1.5[aout]",
    "-map", "[aout]",
    "-ar", "48000", "-ac", "2",
    master_wav
]
subprocess.run(cmd_mix, check=True)
print("Created master_rate_test_audio.wav")

