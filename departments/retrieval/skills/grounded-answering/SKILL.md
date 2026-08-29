---
name: grounded-answering
description: Use when building or tuning how the Asgardr assistant answers from documents — every claim cited to its passage, clean refusal when the corpus is silent, and grounding prompts tested in both directions so strictness never refuses a rank-1 answer.
---

# Grounded Answering

The fourth demo answer on the public page is the important one: asked for a fact
the corpus does not contain, the assistant refuses. An assistant that invents a
clearance height is worse than no assistant, because someone would act on it.
Refusing cleanly is a feature that has to be built and tested for — it is not
free.

## Required behaviors

1. **Every claim carries its citation** — document and passage. An uncited claim
   in an answer is a defect even when it happens to be true.
2. **Corpus-silent → clean refusal.** No plausible numbers, no "typically", no
   general-knowledge padding. The refusal states that the documents do not cover
   the question.
3. **Scope respected** — the answer draws only from the documents the query was
   scoped to (`scoped-retrieval` owns the enforcement and its tests).

## The strictness trap — test both directions

Grounding prompts fail in two directions, and the house has been burned by the
second:

- **Too loose:** the model answers from general knowledge. Caught by negative
  controls (absent facts must refuse).
- **Too strict:** a grounding prompt that forbade "extrapolation" so hard that
  the model refused a safety question *while the answering passage sat at
  retrieval rank 1*. Retrieval was correct; the instruction was wrong.

So the test set must assert both: absent facts refuse, AND present facts answer.
A grounding change that improves one axis is not shippable until the other axis
is re-run. When a refusal occurs, diagnose which layer refused — look at what
retrieval actually returned before touching the prompt.

## Test set construction

Corpus-only facts asserted as exact strings (asset tags, four-decimal
coefficients, named engineers), one per document region (start, middle, end),
plus the negative and scoping controls. Prompt changes go through Evidence
Review like any other change that claims to work.
