#!/bin/sh
# One-command gate install for any clone of this repository:
#   sh scripts/install-hooks.sh
# Points git at the versioned .githooks directory, so every push runs the
# publication-safety scan (and the org-chart freshness check) locally, before
# CI ever sees it. Works in Git Bash on Windows and any POSIX shell.
set -e
cd "$(git rev-parse --show-toplevel)"
chmod +x .githooks/pre-push 2>/dev/null || true
# Absolute path so linked worktrees (whose checkouts may lack .githooks/)
# still run this clone's hooks instead of silently running none. Re-run this
# script if the repository directory ever moves.
git config core.hooksPath "$(pwd)/.githooks"
echo "[install-hooks] core.hooksPath -> $(pwd)/.githooks"
echo "[install-hooks] pre-push now scans every pushed commit with scripts/check-publication-safety.py"
