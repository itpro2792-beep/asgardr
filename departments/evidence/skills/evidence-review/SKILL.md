---
name: evidence-review
description: Use when any Asgardr change claims to work — before merging, deploying, reporting success, or marking a task done. Reviews the evidence behind the claim, not the status color. Reviewer-class - blocking findings are not overrulable by the department under review.
---

# Evidence Review

This is a reviewer-class skill. It reports to the Operator, not into the department
whose work it reviews. A blocking finding raised here can be overridden only by the
Operator, and the override must be recorded in the decision ledger with a reason.

## The doctrine

Green is not evidence. The artifact is. A check whose passing condition is also
satisfied by the failure mode is decoration.

Asgardr's own history supplies the canonical failures. Each one reported healthy:

- A test suite passed with the vector database switched off — every assertion was
  answerable from a language model's general knowledge, so it measured nothing.
- A diagnostic branch was unreachable because a shell assignment under `set -e`
  aborted before it — the suite could not report a dead endpoint.
- Two replicas each cached their own document list in process memory. The store held
  23 documents; one replica said 6, the other 17, alternating with the load balancer.
- A fallback chain hardcoded a model ahead of the configured one, so the configured
  model had never once been used.

## Review checklist

Work through every item. Any "no" is a finding; findings that hide a failure mode
are blocking.

1. **What artifact proves the claim?** A status field, dashboard color, or "tests
   pass" is not an artifact. Acceptable artifacts: command output showing the
   specific behavior, a log line from the real code path, a diff of real state,
   a saved probe result.
2. **Would this check still pass in the failure mode?** Simulate it mentally or
   actually: turn the dependency off, point at a dead endpoint, empty the corpus.
   If the check still passes, it is decoration — blocking finding.
3. **Is there a negative control?** Something that must fail, refused, or be absent.
   See the `negative-controls` skill. A suite with only positive cases is incomplete.
4. **Is the failure path proven?** Point the check at an unreachable target once and
   confirm it reports the failure and exits non-zero.
5. **Is the claim scoped and dated?** "Works" is not a claim. "Restored snapshot
   2026-08-29 into a scratch collection and retrieved asset tag X" is.

## Output format

Report findings as a list, most severe first:

- `BLOCKING` — the claim's evidence would also be produced by the failure mode.
- `FINDING` — evidence is weak, undated, or secondhand; the claim may still be true.
- `PASS` — artifact reviewed and it demonstrates the specific behavior claimed.

Never soften a blocking finding into advice. The department under review does not
get to negotiate it away; that path runs through the Operator and the ledger.
