---
name: holdout-authoring
description: Use when authoring the questions, keys, and forbidden tokens for an Asgardr blind holdout set — untouched-source mining, the four must-refuse shapes, per-question pass criteria committed before the freeze. Most evaluation defects are authoring defects - a pass rule may demand a verbatim corpus string or a clean refusal, never text the system synthesizes.
---

# Holdout Authoring

Most evaluation defects are authoring defects, found only when a case fails for
the wrong reason — and `blind-holdout` runs a set exactly once, so a bad question
burns the only run. The review happens before the freeze.

## The invariants

- **Mine the untouched tail.** Inventory every question ever asked — prior sets,
  regression suites, probe scripts — and the files and fields each touched; author
  only from sources none touched. Exact-duplicate tooling is a floor, not a
  defense: it cannot see paraphrase. Fresh sourcing is the real independence.
- **Require only what the raw source contains.** Every required value is readable
  from the file with the standard library — never text the system synthesizes
  (presentation tags, derived date labels, computed counts): no disk-level
  verifier can match it. Asgardr froze this defect once — **the case was
  unwinnable** — and disclosed it in review rather than rescoring.
- **Forbidden tokens are chosen, not sprayed.** Forbid sibling-record values the
  correct answer must not contain and cross-file values proving attribution drift
  (`scoped-retrieval` has the mechanics); never a token a correct answer or a
  clean refusal may carry — a key name, a short digit string. A forbid that can
  false-fire teaches nothing.
- **Verify the key, commit the verifier.** Every expected value is re-derived by a
  pure standard-library script committed beside the frozen set, so a later reader
  re-checks the key without trusting the author. One- and two-digit values are
  weak substrings; prefer full hashes, exact decimals, distinctive identifiers.

## The four negative shapes

- **The explicit null.** A field that is null in the named document. Correct is a
  refusal that may name the null — never a value from elsewhere.
- **The absent key.** A key held by no document, asked against a real document.
- **The plausible fake.** A receipt, phase, or node that does not exist — probes
  whether resolvers substitute the nearest real thing, the most dangerous failure.
- **The isolation probe.** A fact living only in sources the system must exclude,
  asked without naming them — correct is refusal though the string is in the tree.

## The order of operations

1. Inventory every prior set, suite, and probe; reserve the untouched sources.
2. Author positives as corpus-only exact strings; `negative-controls` owns fact
   choice. Multi-field asks are deliberate: a dropped second field fails the case.
3. Author all four shapes; calibrate must-refuse strictness in both directions
   (`grounded-answering` owns the strictness trap).
4. Re-derive every key with the verifier; audit the finished set against the
   `test-forensics` hunt list.
5. Freeze last (`blind-holdout` owns the run); the set and its reserved sources
   never enter the corpus (`eval-meta-isolation` owns the fence).

The deliverable: the untouched-source inventory; the frozen set with per-question
required and forbidden rationale in a note field; the committed verifier and its
clean run. A set that cannot show its inventory measures rehearsal.
