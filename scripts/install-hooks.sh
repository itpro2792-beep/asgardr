#!/bin/sh
# One-command gate install for any clone of this repository:
#   sh scripts/install-hooks.sh
# Points git at the versioned .githooks directory, so every push runs the
# publication-safety scan (and the org-chart freshness check) locally, before
# CI ever sees it. Works in Git Bash on Windows and any POSIX shell.
set -e
cd "$(git rev-parse --show-toplevel)"
chmod +x .githooks/pre-push 2>/dev/null || true
git config core.hooksPath .githooks
echo "[install-hooks] core.hooksPath -> .githooks"
echo "[install-hooks] pre-push now runs scripts/check-publication-safety.py"
