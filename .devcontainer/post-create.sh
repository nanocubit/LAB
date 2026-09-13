#!/usr/bin/env bash
set -euo pipefail
if [ -f lab_sdk/pyproject.toml ]; then
  cd lab_sdk
  uv sync --extra dev || python -m pip install -e '.[dev]'
fi
