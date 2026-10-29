#!/usr/bin/env bash
# Build the "Presenting, Calm" guide site from docs/ into site/.
set -euo pipefail
cd "$(dirname "$0")"
exec python3 build.py "$@"
