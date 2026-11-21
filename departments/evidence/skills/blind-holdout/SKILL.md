---
name: blind-holdout
description: Use when a score is about to justify promoting an Asgardr candidate — beating an incumbent, clearing a declared floor, re-scoring after remediation, any number the builders could have tuned toward. Freezes the question set and its pass rule in git before the system under test ever sees a question; one run, one verbatim result, pass or scar - an exposed set is never blind again.
---

# Blind Holdout

Blindness is sequence, not character: a test the builder has seen is a test the
builder can teach to, with or without meaning to. The threat is not a check that
cannot fail (`test-forensics` hunts those); it is a candidate taught to pass one.
Asgardr once accepted a candidate's self-scored all green; **it collapsed under
independent review**, and every trusted round since has committed its questions
first. Git history is the witness.

## The three commits

**1. The candidate, frozen and hashed.** Kills the moving target: a score whose
code cannot be named is not a score.

**2. The blind set, pass rule inside.** Committed before the system under test is
invoked on any question, so a test written after seeing the answers cannot happen
silently. Questions are corpus-only facts per `negative-controls`, asserted in both
directions per `grounded-answering`; expected answers are verified from raw sources
and the standard library, never the candidate, whose errors the key would inherit.
The runner proves it can fail before the round; there is no second run to debug in.

**3. The verbatim result of one run.** Pass or fail, committed unmodified — no
rescoring, no second run, no edit to the set or the threshold after seeing output.

## The leaks

- **Threshold drift.** The floor bends to meet the score. The frozen rule states
  minimum questions, a floor the runner may raise but never lower, zero wrong
  answers on positives — answered-but-incomplete is wrong; only an explicit
  refusal is a mere miss — and zero fabrications on must-refuse questions.
- **The unpaired win.** The candidate strictly beats the incumbent on the same
  questions in the same run — paired, same corpus, incumbent in an isolated
  interpreter. No score promotes without the win; a win below the floor is
  progress, recorded and held.
- **The spent set.** One run spends the set: relabel it a regression gate, never
  again blind evidence; tuning to its exposed misses is what the next fresh set
  is for. A set or result that leaks into the corpus is spent too
  (`eval-meta-isolation` owns the fence).
- **The buried failure.** A fail is committed with a pass's care: a scar receipt
  that blocks promotion mechanically and names remediation targets by reason code.
  One red among green signals is a `discrepancy-ledger` entry, kept visible.
- **The gate that fails open.** The release gate reads committed results from the
  tree: missing or unparseable input is a refusal, not a pass, and a skipped check
  states its reason or it is a hole.

## Deliverable

Three commit hashes in order; the pass rule as frozen; the single result file, its
summary quoted unmodified by `evidence-review`; for a fail, the scar receipt —
ledgered the way `restore-drill` ledgers a drill. A passed holdout mints CONFIRMED
(`claim-labeling`); a self-scored green stays PRELIMINARY, however green. A report
that cannot name its three hashes is a status color, not a result; if the set's
commit does not predate the first run, it was never a holdout.
