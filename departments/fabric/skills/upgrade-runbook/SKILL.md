---
name: upgrade-runbook
description: Use when upgrading k3s, the node OS, or cluster-level components across the five-node Asgardr core — snapshot first and prove it restorable, one node at a time, artifact checks between each, written abort criteria.
---

# Upgrade Runbook

Cluster upgrades are the highest-blast-radius routine work the fabric does. The
runbook trades speed for the ability to stop.

## Before the first node

1. **Snapshot etcd and drill it.** Take the snapshot, then prove it restorable
   into a scratch datastore (see Evidence Review's `restore-drill`). An upgrade
   backed by an unverified snapshot is backed by hope.
2. **Read the release notes for removals.** API deprecations and default changes,
   checked against what the fabric actually uses (`kubectl api-resources`, the
   manifests in git). Record findings even when the answer is "none apply."
3. **Write the abort criteria.** Concrete, in advance: e.g. "any control-plane
   component not Ready within 10 minutes", "retrieval end-to-end check fails",
   "etcd alarms". Deciding what failure looks like *during* the failure is how
   upgrades limp to completion broken.
4. **Version skew.** Servers before agents; stay inside the supported skew window
   for the jump; no skipping minor versions the project says not to skip.

## The loop, per node

1. Drain via `node-lifecycle` (with its redundancy proof).
2. Upgrade this node only. 
3. Return it, and run the between-nodes artifact check: node versions
   (`kubectl get nodes`), all system pods Ready, and one end-to-end query through
   the real service path. Save the outputs.
4. Only then move to the next node. Two nodes mid-upgrade at once means a single
   additional failure removes three.

## After the last node

Full pass: versions uniform, workloads on their pinned digests, end-to-end checks
green *and reviewed as evidence* (would they fail if retrieval were down?).
Ledger entry with from-version, to-version, artifacts, and anything that deviated
from this runbook — deviations are how the runbook improves.
