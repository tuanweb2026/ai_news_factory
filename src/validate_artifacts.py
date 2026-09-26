#!/usr/bin/env python3
"""Artifact and project validator for AI NEWS FACTORY."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    ROOT / "AI_NEWS_FACTORY_RULES.md",
    ROOT / "AI_NEWS_VISUAL_STYLE_BIBLE_v1.0.md",
    ROOT / "START_HERE.md",
    ROOT / "RUNBOOK.md",
    ROOT / "config" / "factory.yaml",
]

REQUIRED_DIRS = [
    ROOT / "data" / "inbox",
    ROOT / "data" / "verified",
    ROOT / "data" / "scripts",
    ROOT / "data" / "visuals",
    ROOT / "data" / "qa",
    ROOT / "data" / "rendered",
]

SCHEMA_MAP = {
    "inbox": ROOT / "schemas" / "news_candidates.schema.json",
    "verified": ROOT / "schemas" / "verified_news.schema.json",
    "scripts": ROOT / "schemas" / "script.schema.json",
    "visuals": ROOT / "schemas" / "visual_plan.schema.json",
    "qa": ROOT / "schemas" / "qa_report.schema.json",
}

def validate_structure() -> bool:
    all_ok = True
    print("[1/3] Checking core factory files...")
    for f in REQUIRED_FILES:
        if not f.exists():
            print(f"  ❌ Missing file: {f.relative_to(ROOT)}")
            all_ok = False
        else:
            print(f"  ✅ {f.relative_to(ROOT)}")

    print("\n[2/3] Checking data directories...")
    for d in REQUIRED_DIRS:
        if not d.exists():
            print(f"  ⚠️  Directory missing, creating: {d.relative_to(ROOT)}")
            d.mkdir(parents=True, exist_ok=True)
        print(f"  ✅ {d.relative_to(ROOT)}")

    return all_ok

def validate_schemas() -> bool:
    print("\n[3/3] Validating JSON schemas and existing artifacts...")
    try:
        import jsonschema
    except ImportError:
        print("  ℹ️  'jsonschema' package not installed. Skipping deep schema validation.")
        print("     To enable, install dependencies with: pip install -r requirements.txt")
        return True

    all_valid = True
    # Validate sample inbox file if present
    sample_inbox = ROOT / "data" / "inbox" / "NEWS_CANDIDATES.sample.json"
    if sample_inbox.exists():
        schema_file = SCHEMA_MAP["inbox"]
        if schema_file.exists():
            try:
                with open(schema_file, "r", encoding="utf-8") as sf:
                    schema_data = json.load(sf)
                with open(sample_inbox, "r", encoding="utf-8") as df:
                    sample_data = json.load(df)
                jsonschema.validate(instance=sample_data, schema=schema_data)
                print(f"  ✅ {sample_inbox.relative_to(ROOT)} conforms to {schema_file.name}")
            except Exception as e:
                print(f"  ❌ Validation error in {sample_inbox.name}: {e}")
                all_valid = False

    # Check other artifacts in data/
    for subfolder, schema_path in SCHEMA_MAP.items():
        folder_path = ROOT / "data" / subfolder
        if not folder_path.exists() or not schema_path.exists():
            continue
        with open(schema_path, "r", encoding="utf-8") as sf:
            schema = json.load(sf)
        for json_file in folder_path.glob("*.json"):
            if json_file.name.endswith(".sample.json"):
                continue
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    instance = json.load(f)
                jsonschema.validate(instance=instance, schema=schema)
                print(f"  ✅ {json_file.relative_to(ROOT)} matches {schema_path.name}")
            except Exception as e:
                print(f"  ❌ {json_file.relative_to(ROOT)} failed validation: {e}")
                all_valid = False

    return all_valid

def main():
    struct_ok = validate_structure()
    schema_ok = validate_schemas()
    if struct_ok and schema_ok:
        print("\n🎉 Factory validation PASSED.")
        sys.exit(0)
    else:
        print("\n❌ Factory validation FAILED.")
        sys.exit(1)

if __name__ == "__main__":
    main()
