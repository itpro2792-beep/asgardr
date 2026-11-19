---
name: holdout-authoring
description: Use when writing or reviewing the cases for an Asgardr blind holdout, before the freeze commit — require only literals that exist verbatim in the source, forbid tokens that prove a leak or fabrication, assert refusals, and never require wording the system must compose.
---

# Holdout Authoring

The house case: a holdout case was lost because its expected string was
synthesized wording, not a literal from the corpus. A correct answer phrased
differently fails such a case. A pass condition a correct answer can fail
grades phrasing.

## The pass condition

A case asserts three kinds of thing and no others. Each must fail a wrong
answer — item 2 of `evidence-review` — and must pass a correct answer in
other words, the direction this skill adds (the two-sided test in
`grounded-answering`).

- **Require a literal.** The shortest atomic fact a correct answer must
  reproduce unchanged — an asset tag, a coefficient, a `demo-*` identifier
  — never a phrase or sentence, never a string the prompt contains. "Exact
  string" in `negative-controls` and `grounded-answering` means a corpus
  literal, never answer wording; which facts qualify stays with
  `negative-controls` ("Choosing test facts"). Search the source byte for
  byte; record location and match count. Zero matches means re-cut the
  literal, not loosen the assertion; a match outside the intended passage
  does not prove which passage was retrieved. **Never require text the
  system must compose** — paraphrase, summary, the author's conclusion.
- **Forbid a token.** A string whose appearance in an answer proves a leak or
  a fabrication; record which. A token the prompt contains, or a correct
  answer could contain, is not a control — a clean refusal may quote it.
  Where no token survives the rule, the case asserts the refusal alone.
- **Assert a refusal.** As `grounded-answering` defines it, never by matching
  the refusal's sentence — that is synthesized text again. The grading rule
  — those criteria, plus any mechanical part such as forbidden tokens or no
  citation — is written into the case before the freeze, not after the run.

## The negative shapes

Negative cases come in distinct shapes. The house form uses four, and a
holdout carries each. Tag every case with its shape.

1. **Absent fact.** The absence control from `negative-controls`, as a case.
2. **Scope leak.** The leak test from `scoped-retrieval`; the out-of-scope
   value is the forbidden token.
3. **False premise.** The prompt asserts what the corpus does not say and
   carries no value for a refusal to quote. The token is a detail only
   invention could produce; where none exists, the refusal alone.
4. **Near miss.** The entity exists, the asked attribute does not. A
   sibling's value is a corpus value a correct answer may cite, so no token
   survives — the case asserts the refusal, and its grading rule names the
   failure: the sibling's value given as the asked attribute.

## The case file

Every prompt is new — compared mechanically, never from memory, against the
full prior-prompt registry before the freeze, several hundred prompts by
late rounds. Zero overlap, or the case is rewritten. The overlap report
states the comparison method and normalization, the registry size compared
against, and the result; a report without its method is not an artifact.

The artifact is the case file — each literal with location and match count,
each token with what it proves, each refusal with its grading rule, each
case with its shape — plus the saved overlap report. A literal without a
match count is a guess; a token without the thing it proves is decoration.
A case found defective after the freeze stays in the record as lost — the
correction appends (`decision-ledger`), the case is never re-graded.
Authoring ends at the freeze commit — `blind-holdout` owns the run and the
registry, `eval-meta-isolation` keeps this file out of the index.
