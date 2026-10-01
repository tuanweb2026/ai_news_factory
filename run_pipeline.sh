#!/usr/bin/env bash
# AI NEWS FACTORY - Run Pipeline Shortcut
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ -f ".venv/bin/python3" ]; then
    PYTHON_BIN=".venv/bin/python3"
else
    PYTHON_BIN="python3"
fi

PYTHONPATH=. "$PYTHON_BIN" run_pipeline.py "$@"
