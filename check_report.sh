#!/usr/bin/env bash
# AI NEWS FACTORY - Check Report Shortcut
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ -f ".venv/bin/python3" ]; then
    .venv/bin/python3 scripts/cli_reporter.py
else
    python3 scripts/cli_reporter.py
fi
