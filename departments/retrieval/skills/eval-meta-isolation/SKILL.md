---
name: eval-meta-isolation
description: Use when evaluation material (prompts, expected answers, audit notes, prior holdouts) sits near a corpus the Asgardr fabric ingests — exclude by default, admit sources by name, probe isolation once per chunk shape, and keep the probe that was not enough as a scar.
---

# Eval Meta Isolation

The house case: evaluation material sat near the corpus behind an exclusion
flag applied on one chunking path only. A paragraph-shaped probe reported
isolation while table-row chunks of the same material sat in the index.

## The boundary

- **Eval-meta is never corpus.** Ingested prompts, expected answers, audit
  notes, and prior holdouts are an answer key the system retrieves (see
  `test-forensics`). `blind-holdout` and `holdout-authoring` own that material.
- **Exclude by default, admit by name.** A committed allowlist names every
  source that may enter the index; a denylist covers only what was remembered.

## The probes

1. **List the chunk shapes.** Save what the pipeline actually produces —
   paragraph, table row, heading, list item, code block — per chunking path.
2. **Plant one marker per shape.** A probe fixture beside the evaluation
   material, under the same exclusion, carries one minted `DEMO-*` marker per
   shape. Frozen holdouts are never edited (`blind-holdout` owns the freeze).
3. **Probe every shape, both ways.** Save both outputs — the marker absent
   from the store queried directly (`replica-consistency`), and the real answer
   path refusing, fixture uncited (the absence control in `negative-controls`).
4. **Prove each probe can fail.** In a scratch collection, admit the fixture
   by name, ingest, and save every probe finding its marker (the self-test
   rule in `negative-controls`). Drop it; the serving index stays sealed.
5. **Check the built index.** Diff the source identities on the points in the
   store against the allowlist; save the diff. The ingestion record
   (`corpus-hygiene`) is the claim; the store is the artifact. Ledger entry
   names the allowlist version, shape list, per-shape artifacts, and scars.

## Scars and re-probes

- **Keep the scar.** The probe that passed while the leak existed stays in
  the suite beside its replacements (`blind-holdout` owns scar receipts).
- **Re-probe every shape** on any change to the allowlist, the exclusion code,
  a chunking path or shape, the evaluation material, a re-ingestion into a new
  collection, or any `scoped-retrieval` re-run trigger.
- **Any leak is a blocking finding** under Evidence Review. Fix every chunking
  path, then re-probe every shape — a pass covers one shape (`restore-drill`).
