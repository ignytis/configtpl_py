#!/usr/bin/env bash

# -x flag is set to help the LLM with diagnostics
set -xeo pipefail

echo "Running unit tests..."
pytest ./tests/unit

echo "Running functional tests..."
./tests/functional/run.py

echo "Running ruff check..."
./.venv/bin/ruff check