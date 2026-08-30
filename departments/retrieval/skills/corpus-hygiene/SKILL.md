---
name: corpus-hygiene
description: Use when adding, chunking, or re-embedding documents in the Asgardr knowledge fabric — chunk sizing, indexing vs querying task prefixes, scoping payloads, and re-embedding on model change decide both retrieval quality and the privacy boundary.
---

# Corpus Hygiene

Retrieval quality is decided at ingestion time. A corpus assembled carelessly
answers carelessly, and no prompt downstream can fix it.

## Chunking

- House baseline: recursive split, **~750 characters with 100 overlap**. A 21 KB
  document becomes ~38 chunks with exact retrieval from the middle and the end —
  verify that claim per corpus, don't inherit it: after ingesting, query for a
  fact from a document's middle and from its last paragraph.
- Respect structure where the splitter allows: breaking mid-table or mid-clause
  produces chunks that embed poorly and cite worse.

## Embedding

- **Task prefixes differ for indexing and querying** when the model supports
  them; using one prefix for both measurably degrades retrieval. Record which
  prefixes the corpus was indexed with.
- **Embeddings do not mix across models.** A model change (or version change)
  means re-embedding the whole corpus into a new collection and cutting over —
  never mixing vectors from two models in one collection. The old collection is
  the rollback target until the new one is verified.

## Payloads

Every point carries the payload that scoping depends on: document identity at
minimum, plus whatever the privacy boundary filters on. A chunk without scoping
payload is unscopable forever — see `scoped-retrieval` for why that is the
product's load-bearing wall.

## Corpus versioning

- Record per ingestion: source documents, chunk parameters, embedding model and
  prefixes, point counts. "The corpus" is a version, not a place.
- Deduplicate before embedding; near-duplicate chunks crowd the top-k with one
  document's voice.
- After any ingestion, run the retrieval test set — including the negative
  controls (a fact the corpus does not contain must still draw a refusal).
