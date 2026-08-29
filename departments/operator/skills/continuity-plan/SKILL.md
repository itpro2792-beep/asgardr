---
name: continuity-plan
description: Use when assessing single-operator risk for the Asgardr fabric — what runs unattended, what only the Operator knows, and whether the cluster could be cold-started from written artifacts alone. The homelab translation of succession planning and workforce risk.
---

# Continuity Plan

A ten-computer fabric with one operator has a bus factor of one. Corporate orgs
run succession planning for this; Asgardr runs a continuity plan.

## The nap test

The fabric must keep doing its job with no operator input: nothing requires
interactive approval to stay up, certificates and credentials do not expire
mid-nap, storage does not fill silently, and a single node loss reschedules
without a human. Verify each of these from artifacts, on a schedule — the test is
"what broke while nobody watched," and the answer should be in logs, not in
surprises.

## The knowledge ledger

List everything that exists only in the Operator's head, then either write it
down or accept the risk explicitly in the decision ledger. The usual suspects:

- Disk-encryption and password-manager recovery paths.
- Which physical machine is which, and what breaks if each one dies.
- The order things must come up in after a full power loss.
- Where the backups live and how the restore drill runs (see `restore-drill`).
- Which external accounts (DNS, tunnel, registry) the fabric depends on and how
  to reach them.

## The cold-start drill

The continuity artifact is a runbook that a competent stranger could follow to
bring the fabric from powered-off to serving. Like backups, an unrehearsed
runbook is of unknown provenance: walk it periodically — ideally on the next
planned full shutdown — and correct it where reality disagrees. Every correction
stays visible.

## Time-away posture

Before any planned absence: verify the nap test recently passed, confirm nothing
expires during the window, decide what automation may do alone (per
`operator-authority`, nothing Tier 3), and leave the fabric a way to fail safe —
degraded and honest beats up and lying.
