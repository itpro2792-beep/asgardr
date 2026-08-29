---
name: negative-controls
description: Use when designing tests or health checks for any Asgardr system — retrieval, mesh, backups, publishing, checkers themselves. Adds the cases that must fail - absent facts refuse, out-of-scope stays out, dead endpoints error, and every checker proves it can fail.
---

# Negative Controls

A suite of only positive cases cannot distinguish a working system from a confident
one. Every Asgardr test suite carries controls that must fail correctly.

## The three canonical controls

**1. The absence control.** Ask the system for something it cannot know — a fact no
document contains, a peer that does not exist, a backup from a date never taken.
The correct answer is a clean refusal or explicit error, never a plausible value.
A document assistant that invents a parking-garage clearance height is worse than
no assistant, because someone would act on it.

**2. The scoping control.** Ask for A's fact while restricted to B. Document A's
value must not appear and A must not be cited. A mesh probe scoped to one peer must
not report another's latency. Scope violations are silent by nature — only this
control surfaces them.

**3. The failure control.** Point the check at a dead endpoint once and confirm it
reports the failure and exits non-zero. Asgardr once shipped a suite whose entire
diagnostic branch was unreachable (a shell assignment under `set -e`); it could
pass but could not fail. That defect is invisible without this control.

## The self-test rule for checkers

Any automated checker (linter, scanner, validator) must include a self-test mode
that seeds a known-bad fixture and asserts the checker flags it. A scanner that has
never caught anything is indistinguishable from a scanner that cannot.
`scripts/check-publication-safety.py --self-test` in this repository is the house
example.

## Choosing test facts

Use facts that exist in no training corpus and no default configuration: an asset
tag, a path-loss coefficient to four decimal places, a named engineer, a `demo-*`
identifier you minted. Assert the exact string. Facts answerable from general
knowledge (OAuth2, AES-256, common SLA numbers) prove nothing about the system —
see `test-forensics`.
