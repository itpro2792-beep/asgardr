---
name: key-rotation
description: Use when rotating mesh or service credentials on the Asgardr fabric — issue, cut over, revoke, then prove the rotation by attempting the old credential and saving its refusal. Rotation is proven when the old key fails, not when the new one works.
---

# Key Rotation

The new key working proves the new key works. It says nothing about whether the
old one died. Rotation is complete only when the old credential demonstrably
fails.

## The sequence

1. **Issue** the new credential (Tier 3 if it widens access; routine rotation of
   an existing grant is Tier 2 with a ledger entry).
2. **Cut over** the consumers. Prefer overlap windows where the system supports
   them — a mesh with half its peers cut over and half stranded is worse than
   either state.
3. **Revoke** the old credential at the control plane.
4. **Negative control.** Attempt the old credential against a real endpoint.
   Expect and save the refusal — timestamped, from the actual system. This
   artifact is the rotation's proof; without it, step 3 is a checkbox.
5. **Sweep for stragglers.** Grep manifests, env files, and running pods for the
   old credential's fingerprint; a consumer still holding it will fail later, at
   a worse time.
6. **Ledger entry**: what rotated, the window, the refusal artifact.

## Cadence

- Scheduled rotation for long-lived credentials — pick a cadence and record it;
  an unrotated credential's age is an accepted risk and belongs in the ledger.
- Immediate rotation on any exposure (see `secret-hygiene`, which owns the
  exposure-response details) and on any peer retirement (`peer-lifecycle`).
- Expiring credentials beat revocable ones where the tooling allows: expiry is
  rotation that happens even when nobody remembers.
