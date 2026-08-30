---
name: scoped-retrieval
description: Use when queries must be restricted to a subset of documents in the Asgardr knowledge fabric — payload filtering at the database is the privacy boundary the product rests on, and it is proven with cross-document leak tests.
---

# Scoped Retrieval

Scoping is not a convenience feature. For a corpus of contracts, surveys, and
safety procedures, "this query may only see these documents" is the privacy
boundary the whole product rests on. Treat changes to it accordingly.

## Enforcement rules

- **Filter at the database.** The scope is a payload filter applied by the vector
  store in the search itself. Post-filtering in application code — retrieve
  broadly, discard out-of-scope hits — is not scoping: the out-of-scope content
  already reached the application and can leak through logs, errors, or a bug.
- **Scope is part of the query contract.** The scope used is logged with every
  answer, so any answer can later be audited against what it was allowed to see.
- **Deny by default.** A query with a malformed or empty scope fails closed —
  it does not fall back to searching everything.
- **Scoping payload is mandatory at ingestion** (see `corpus-hygiene`); a chunk
  that lacks it can never be safely served.

## The leak test

The scoping control from `negative-controls`, made specific:

1. Pick a fact that exists only in document A (an exact string).
2. Query for that fact with the scope restricted to document B.
3. Assert **both**: A's value does not appear in the answer, and A is not cited.
4. Run the reverse pair too, and one pair per scoping dimension the system
   supports (per-document, per-collection, per-tag).

Run the leak test on every change to: the filter construction code, the payload
schema, the vector-store version, or the collection layout. Any leak is a
blocking finding under Evidence Review — there is no small amount of crossing a
privacy boundary.
