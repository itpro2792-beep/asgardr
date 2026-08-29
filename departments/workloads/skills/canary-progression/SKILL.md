---
name: canary-progression
description: Use when advancing a public interactive Asgardr workload through canary versions — one capability class per release, risky capabilities deliberately deferred until earned, every canary an atomic static release whose rollback is a git revert.
---

# Canary Progression

The Fold preview shipped as canary V1 → V2 → V3: first an isolated synthetic
phone study, then a broadened operations study, then a distinct RF/DAS workspace.
Each canary was a complete, revertible static release. That progression is the
house pattern for anything interactive in public.

## Rules

- **One capability class per canary.** A release adds a workspace, or a data
  domain, or an interaction model — not all three. When a canary misbehaves, the
  suspect list should have one name on it.
- **Defer capabilities until earned — and say so.** V3 deliberately deferred the
  service worker, and therefore *does not describe itself as offline-capable*.
  The deferral and the honest claim travel together: a capability you have not
  shipped is one you may not advertise. Candidates for deliberate deferral:
  service workers, persistent storage, notifications, anything requesting
  browser permissions.
- **Atomic releases, versioned assets.** Each canary is one commit-set with its
  static assets versioned together, so rollback remains a normal `git revert` —
  no migration, no cache-busting archaeology. If a rollback would need a
  procedure, the release was not atomic.
- **Acceptance targets are written before the canary ships** (`device-fit` holds
  the phone targets) and verified on the real device class, not only in a
  desktop emulator.
- **The safety boundary is re-reviewed every canary.** Each new workspace or data
  domain re-enters `public-surface-review` — V(n)'s approval does not transfer
  to V(n+1), because the surface grew.

## Promotion and retirement

A canary graduates when its acceptance targets have artifacts and a full cycle
has passed without findings. Superseded canaries follow `redirect-integrity` if
their URL was ever shared; the ledger records what each canary added and what it
deferred.
