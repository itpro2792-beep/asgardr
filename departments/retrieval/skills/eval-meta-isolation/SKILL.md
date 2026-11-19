---
name: eval-meta-isolation
description: Use when deciding what an Asgardr retrieval corpus may ingest, or auditing one whose scores rise without a visible cause — review write-ups, scorecards, evaluation commentary, frozen holdout sets, transcripts and ledger entries that quote expected answers. Eval-meta is excluded by default and admitted only by name - a system that can quote its own report card is self-grading, not retrieving.
---

# Eval-Meta Isolation

Review write-ups, scorecards, evaluation commentary, frozen question sets,
pass/fail records, and transcripts or ledger entries that quote expected
answers are eval-meta: documents about the system's quality. Served by
default, they answer a quality question from the report card and a blind
question from the answer key. Both leaks are silent: **scores go up.**

## The invariants

- **Exclude by default, admit by name.** Eval-meta is never retrieved unless
  the question names the exact file: a reviewer asking what a named review
  says is served; a general question never is. An answer that cites its own
  scorecard is correctly cited (`grounded-answering`) and still self-grading.
- **Classify by name pattern and by content.** Known filename prefixes catch
  the review documents; content markers ("blind set", "holdout", scores)
  catch what drifts in under other names. New reviews appear every round —
  the newest review is always the likeliest leak.
- **Every chunk shape inherits the flag.** Asgardr once leaked a review
  through **table-row chunks while paragraph chunks of the same document were
  correctly excluded** — the flag rode one chunker code path and not the
  other. Classify at the document level; assert inheritance structurally.
- **Exclusion lives at the store.** Retrieving broadly and discarding
  eval-meta downstream is not isolation — the content already reached the
  application (`scoped-retrieval` owns that argument at the privacy boundary).
- **Holdout material lives outside ingested paths.** A frozen set or verbatim
  result in an indexed tree spends the blind before its one run
  (`blind-holdout`); review findings are filed outside the corpus the same way
  (`evidence-review`). A ledger entry that quotes an answer is eval-meta too.

## The order of operations

1. Classify before ingesting; record the rule and its verdicts in the
   per-ingestion source record (`corpus-hygiene` owns the record).
2. Ingest with the exclusion flag asserted on every chunk, whatever its shape.
3. Probe blind, per chunk shape: a paragraph fact, a table-row fact, a heading
   fact, each living only in eval-meta, asked without naming the file; each
   must refuse — the absence control turned inward (`negative-controls`).
4. Re-probe forever: every future blind set carries at least one isolation
   probe (`holdout-authoring`, the fourth negative shape). Isolation verified
   once and never probed again is isolation you have, at best, historically.

## Deliverable

The document-level classification rule, name patterns and content markers
both; a refusal transcript per chunk shape; after any leak, the regression
case pinned and keyed to the chunk shape that leaked. Do not report isolation
as done until every chunk-shape probe has been watched refusing — a rising
score is evidence of nothing but change.
