---
name: blind-holdout
description: Use when running or auditing a blind holdout of an Asgardr retrieval or answering change before apply — freeze prompts, expectations and thresholds first, run once, keep the raw run and every scar, count a missing gate as FAIL. The author's own pass is not independent.
---

# Blind Holdout

A pass graded by the hands that wrote the fix is a claim, not a measurement.
The house case: a remediation's author ran the twelve-gate battery on a fresh
holdout and every gate passed. The pass was real, and nothing in the table
showed it was not independent — apply waited for a different reviewer's round.

The retrieval test set `corpus-hygiene` runs after every ingestion is a
regression set, rerun at will; a blind holdout is spent by its one run. Case
design is `holdout-authoring`; index isolation is `eval-meta-isolation`.

## The three commits

1. **Freeze.** Commit the prompts, expected outcomes and gate thresholds
   *before* the system under test runs, with their digest.
2. **Run once.** One run on the real path, committed raw and unedited, with
   its start time and its input's digest. A holdout rerun until it passes is
   a search, not a measurement: a failure is root-caused and fixed, then
   meets a new holdout in a new round (the `restore-drill` pattern). An
   errored run is still the run; a rerun is the Operator's call, ledgered.
3. **Verdict.** The full gate table — each gate `PASS` or `FAIL`, the round
   `PASS` only if all pass — and any remediation. Diagnosis starts here,
   after the raw run is on record (`grounded-answering` owns how).

## Rules

- **Fail closed.** A missing, unparseable or errored gate is `FAIL`. Apply is
  blocked unless every gate passes in an independent round; who may apply is
  `operator-authority`. The runner proves it can fail (`negative-controls`).
- **Scars stay.** A failed gate keeps its own identifier (`DEMO-SCAR-03`) in
  the record permanently — a receipt of the round it failed in, never
  re-graded, never counted toward a later pass. The fix adds a new gate with
  a new identifier to later batteries; it does not erase the failure.
- **Fresh every round.** Each holdout has zero overlap with the registry of
  prior prompts, checked mechanically before the freeze, not from memory;
  writing such cases is `holdout-authoring`. The overlap report states its
  match rule (normalized exact match at minimum) and the digest it checked. A
  used holdout joins it, kept out of the index (`eval-meta-isolation`).
- **The author does not grade.** A pass produced by the remediation's author
  is `PRELIMINARY` (`claim-labeling`) and does not unblock apply. Apply needs
  an all-pass round run by a different reviewer on their own fresh holdout.

## What the reviewer audits

The chain of custody, from history rather than the summary: three digests
match — the freeze, the overlap report's, the run's input — and the freeze
commit precedes the run commit. Commit order proves the order of commits, not
of events, so the freeze must also have been pushed before the run's recorded
start time. A broken chain — freeze after run, digests differ, edited output,
a gate absent from the table, the author as sole grader — lets a failing
system produce the pass: `BLOCKING` in `evidence-review` vocabulary. Any other
missing artifact is a `FINDING`. The verdict and any override go to
`decision-ledger`. A pass without the chain is a status field.
