import json

candidates = [
    {
        "id": "candidate-a",
        "voice": "en-GB-RyanNeural",
        "display_name": "Ryan (British Neural)",
        "accent": "British (en-GB)",
        "gender": "Male",
        "style_persona": "British Technology News / Authoritative",
        "rate": "+4%",
        "full_sample_duration_s": 26.35,
        "section_timestamp": "00:00 - 00:15",
        "wpm": 148.0,
        "silence_ratio": 0.18,
        "pause_count": 5,
        "integrated_loudness_lufs": -16.54,
        "true_peak_dbtp": -4.51,
        "voice_clarity": "High",
        "broadcast_authority": "Very High",
        "pacing_cadence": "Crisp, steady, natural cadence for dense technical explanations",
        "emotional_tone": "Analytical, serious, trustworthy tech broadcaster",
        "best_fit_use_case": "Technical architecture deep-dives, hardware announcements, enterprise AI benchmarks"
    },
    {
        "id": "candidate-b",
        "voice": "en-GB-SoniaNeural",
        "display_name": "Sonia (British Neural)",
        "accent": "British (en-GB)",
        "gender": "Female",
        "style_persona": "British Broadcast Explainer / Clear",
        "rate": "+4%",
        "full_sample_duration_s": 26.04,
        "section_timestamp": "00:15 - 00:30",
        "wpm": 149.8,
        "silence_ratio": 0.11,
        "pause_count": 7,
        "integrated_loudness_lufs": -16.85,
        "true_peak_dbtp": -4.51,
        "voice_clarity": "Very High",
        "broadcast_authority": "High",
        "pacing_cadence": "Fast, articulate, tight pauses with high continuous verbal energy",
        "emotional_tone": "Engaging, crisp, documentary narrator",
        "best_fit_use_case": "Fast-paced algorithmic explainers, research papers, visual breakdown Shorts"
    },
    {
        "id": "candidate-c",
        "voice": "en-US-AriaNeural",
        "display_name": "Aria (US Neural)",
        "accent": "US (en-US)",
        "gender": "Female",
        "style_persona": "Newscast Professional / Confident",
        "rate": "+3%",
        "full_sample_duration_s": 27.48,
        "section_timestamp": "00:30 - 00:45",
        "wpm": 141.9,
        "silence_ratio": 0.18,
        "pause_count": 6,
        "integrated_loudness_lufs": -16.44,
        "true_peak_dbtp": -4.50,
        "voice_clarity": "High",
        "broadcast_authority": "High",
        "pacing_cadence": "Polished newsroom cadence, expressive inflection, deliberate emphasis",
        "emotional_tone": "Energetic, modern American tech news correspondent",
        "best_fit_use_case": "Breaking AI industry news, product launches, consumer-facing agent announcements"
    },
    {
        "id": "candidate-d",
        "voice": "en-US-ChristopherNeural",
        "display_name": "Christopher (US Neural)",
        "accent": "US (en-US)",
        "gender": "Male",
        "style_persona": "Broadcast Authority / Analytical",
        "rate": "+3%",
        "full_sample_duration_s": 27.55,
        "section_timestamp": "00:45 - 01:00",
        "wpm": 141.6,
        "silence_ratio": 0.20,
        "pause_count": 7,
        "integrated_loudness_lufs": -16.58,
        "true_peak_dbtp": -4.51,
        "voice_clarity": "Very High",
        "broadcast_authority": "Very High",
        "pacing_cadence": "Deep resonant timbre, authoritative metric pacing, clear word separation",
        "emotional_tone": "Grounded, objective, commanding technical anchor",
        "best_fit_use_case": "Semiconductor breakthroughs, frontier AI models, strategic infrastructure news"
    }
]

benchmark_data = {
    "benchmark_version": "1.0.0",
    "generated_at": "2026-09-27T11:16:00+07:00",
    "video_path": "voice_tests/VOICE_BENCHMARK_TEST_VIDEO.mp4",
    "audio_mix_path": "voice_tests/master_benchmark_audio.wav",
    "subtitles_path": "voice_tests/benchmark_subtitles.srt",
    "video_specs": {
        "dimensions": "1080x1920",
        "aspect_ratio": "9:16",
        "fps": 30,
        "duration_seconds": 60.0,
        "video_codec": "H.264 (avc1)",
        "audio_codec": "AAC-LC (stereo, 48kHz, 192 kbps)",
        "subtitle_stream": "mov_text (embedded)",
        "loudness_master_lufs": -16.1,
        "loudness_range_lra": 2.3
    },
    "catalog_availability_note": {
        "dragon_hd_status": "DragonHD models (en-GB-Ollie:DragonHDLatestNeural, en-GB-Ada:DragonHDLatestNeural) are restricted enterprise private endpoint models. Standard Azure Edge catalog does not expose raw custom styles outside of dedicated endpoints.",
        "evaluated_pool": "4 top-tier broadcast/narration Neural voices across British and American English."
    },
    "candidates": candidates
}

with open("voice_tests/VOICE_BENCHMARK_RESULTS.json", "w") as f:
    json.dump(benchmark_data, f, indent=2)

print("Saved voice_tests/VOICE_BENCHMARK_RESULTS.json")
