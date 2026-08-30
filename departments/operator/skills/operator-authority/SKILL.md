---
name: operator-authority
description: Use when deciding whether an action on the Asgardr fabric may proceed autonomously, must be logged and reversible, or belongs to the Operator alone — cluster state changes, new controllers, credential issuance, public exposure, deletions.
---

# Operator Authority

Asgardr runs on evidence-led human authority: agents and automation do real work,
but the shape of that work — and every irreversible edge of it — belongs to the
Operator.

## The three tiers

**Tier 1 — Autonomous.** Proceed without asking. Read-only inspection, synthetic
work, analysis, drafting, and changes fully reversible by `git revert` in a
repository the agent was pointed at. Leave artifacts of what was done.

**Tier 2 — Gated by evidence.** Proceed, but only with a named rollback target and
a ledger entry. Deployments of pinned releases, node drains with proven redundancy,
corpus updates, credential *rotation* (not issuance). If the rollback target cannot
be named, the action is not Tier 2.

**Tier 3 — Operator only.** Do not proceed; prepare the change and present it.
- Issuing new credentials or widening any access.
- Exposing a new surface publicly, or adding any live connection to a public one.
- Deleting data, collections, snapshots, or history.
- Promoting a quarantined controller candidate (below).
- Anything whose reversal path you cannot describe.

## Quarantine

New controllers — anything that can *act* on the fabric rather than observe it —
start in quarantine: isolated from live systems, fed synthetic fixtures, and kept
deliberately separate from public surfaces. A candidate leaves quarantine only by
the Operator's decision, recorded in the ledger with the evidence that earned it.
Public UI studies are built clean-room from quarantined candidates, never wired to
them.

## When unsure

Unsure means Tier 3. The cost of asking is minutes; the cost of a wrong Tier 1
guess on a ten-machine fabric is the weekend. An agent that escalates a borderline
call with its evidence attached is doing the job, not failing it.
