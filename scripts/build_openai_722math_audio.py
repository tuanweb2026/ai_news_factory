import json
from pathlib import Path
from src.render.audio import AudioEngine
from src.render.subtitles import SubtitleEngine

def main():
    story_dir = Path("data/rendered/openai-publishes-722-mathematical-proofs-github-2026")
    audio_dir = story_dir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    
    script_path = Path("data/scripts/SCRIPT_openai-publishes-722-mathematical-proofs-github-2026.json")
    with open(script_path, "r", encoding="utf-8") as f:
        script_data = json.load(f)
        
    print("Generating audio via AudioEngine...")
    audio_engine = AudioEngine()
    master_wav, timing_manifest = audio_engine.build_voice_track(script_data, audio_dir, lang="en")
    print(f"Master voice generated: {master_wav}")
    
    print("Generating subtitles via SubtitleEngine...")
    sub_engine = SubtitleEngine()
    sub_dir = story_dir / "subtitles"
    subs = sub_engine.generate_all(script_data, sub_dir, lang="en")
    print(f"Subtitles generated: {subs}")

if __name__ == "__main__":
    main()
