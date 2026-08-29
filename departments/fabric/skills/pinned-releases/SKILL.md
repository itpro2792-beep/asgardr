---
name: pinned-releases
description: Use when deploying or updating any workload on the Asgardr fabric — pinned image tags with digests, a rollback target named before rollout, and model or backend swaps done as config changes, never code changes.
---

# Pinned Releases

A moving tag has no rollback target. Everything that runs on the fabric is pinned,
and every rollout knows where it would retreat to before it advances.

## Rules

- **Pin tag and digest.** `image: registry/app:v1.4.2@sha256:…`. `latest`,
  `stable`, and channel tags are banned in manifests — they can change under a
  running cluster and make "what is deployed" unanswerable.
- **Name the rollback target first.** Before applying, record the currently
  running digest. The rollout entry in the decision ledger carries both: what we
  moved to, what we would move back to.
- **Swaps are config, not code.** The model behind the gateway, the embedding
  backend, the retrieval endpoint — all selected by configuration. Changing a
  model must never require rebuilding an image. Corollary from the house history:
  verify the configured value is *used* — a fallback chain once hardcoded a model
  ahead of the configured one, and the configured model had never run.
- **One change per rollout.** An image bump and a config change in the same apply
  makes the rollback ambiguous.
- **Verify on the real path.** After rollout, exercise the service through its
  public behavior (a real query, a real page) and save the output next to the
  digest. Pod Ready is a precondition, not the proof.

## Rollback

Rollback is applying the previous pinned digest — which exists, because rule one.
After any rollback, the ledger entry for the failed rollout stays, marked
superseded, with what went wrong. A rollback that cannot be explained becomes an
incident, not a shrug.
