---
name: test-forensics
description: Use when auditing an existing test suite, health check, or monitoring setup for vacuous assertions — checks that pass while measuring nothing. Run it on inherited code, vendor deliverables, and anything that "arrived with a passing suite."
---

# Test Forensics

A passing suite is a claim, not a fact. This skill audits what the suite would
actually catch. The motivating case: a project arrived with a passing suite that
asserted answers about OAuth2, AES-256-GCM, and a 15-minute SLA were non-empty.
Every one was answerable from a language model's general knowledge. **The suite
passed with the vector database switched off** — and had already been reported as
proof the system worked.

## The hunt list

Read every assertion and ask: what failure mode would this miss?

- **General-knowledge assertions.** The expected answer is producible without the
  system under test (common protocols, algorithms, round numbers). Replace with
  corpus-only facts asserted as exact strings.
- **Non-empty / non-error assertions.** `assert response` passes on an apology,
  a hallucination, or an HTML error page.
- **Status-endpoint oracles.** The test asks the system whether it is healthy and
  believes the answer. Health must be demonstrated on the real code path (a real
  query, a real write-and-read-back), not self-reported.
- **Unreachable branches.** Trace error handling for shell traps: an assignment or
  command substitution under `set -e`, a `&&` chain that short-circuits past the
  diagnostic, a `catch` that logs and continues. Prove the failure branch runs by
  forcing it once.
- **Mocks that mock the subject.** If the component being tested is replaced by a
  stub, the test exercises the stub.
- **Time and state leaks.** Tests that pass only in sequence, or that depend on
  state a previous run created, will pass in CI and fail in the field.

## Deliverable

A table: each vacuous check, the failure mode it would miss, and the replacement
assertion. Then rewrite, and prove the new suite can fail (see `negative-controls`).
Do not report the audit as done until the rewritten suite has been watched failing
against a broken system at least once.
