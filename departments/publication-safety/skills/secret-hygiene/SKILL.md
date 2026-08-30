---
name: secret-hygiene
description: Use when handling credentials anywhere in Asgardr — application code, container images, manifests, git history, public pages. No literal defaults; secret references only; built images must grep clean; exposure means rotation proven by the old secret failing.
---

# Secret Hygiene

The house case: an API key sat as a literal default in application source — and in
the built container image. It reported "credential managed." Both claims were
false, and only reading the artifacts found it.

## Rules

- **No literal secrets as code defaults.** Not in source, not as a "fallback",
  not commented out. A default credential is a credential you shipped.
- **Reference, don't embed.** Kubernetes Secret references and environment
  injection at deploy time. The manifest names the secret; the value lives in the
  secret store only.
- **The built image is the artifact.** Grepping source is not enough — build the
  image and grep the layers (`docker save` / `crane export`, or run the container
  and grep the filesystem). "The running image now greps clean" is the standard.
- **Git history counts.** A secret removed by a later commit is still published.
  If it ever landed in a pushed commit, treat it as exposed.
- **Public pages get scanned.** `scripts/check-publication-safety.py` runs the
  pattern scan over every file in the Pages repository and must pass before push.

## On exposure

1. Rotate immediately — issue the new credential, cut services over.
2. Revoke the old one.
3. **Prove the revocation**: attempt the old credential and save the refusal as an
   artifact. Rotation is proven when the old secret fails, not when the new one
   works (same doctrine as mesh `key-rotation`).
4. Record the exposure window and the artifact in the decision ledger.
5. Fix the path it leaked through, or it will leak again.
