---
name: node-lifecycle
description: Use when taking a fabric host down for maintenance or returning it to service (July–August 2026 k3s cordon/drain runbook preserved; five-node k3s layer retired 2026-08-11 in favor of host-native service management, recorded 2026-11-02) — prove surviving capacity before exit and prove return with artifacts rather than dashboard green.
---

# Node Lifecycle

> **Architecture & vintage note (`CONFIRMED` · recorded `2026-11-02`):** The
> five-node `k3s` orchestration layer illustrated in the commands below
> (**July–August 2026 vintage**) was **retired on `2026-08-11`** in favor of
> host-native service management (see [`LEDGER.md`](../../../../LEDGER.md),
> Discrepancy D-01). Per `source-dating` and `discrepancy-ledger`, the
> historical `k3s` drain procedure stays preserved below with its vintage
> labeled; under host-native service management, the same evidence contract
> governs every host maintenance window (verify standby/failover readiness on a
> distinct host before stopping supervised services, and prove return with a
> saved end-to-end artifact).

*Historical runbook (July–August 2026 `k3s` core vintage):* Critical services
run two replicas across core nodes and must survive a node loss. This runbook
makes each node exit and return an evidenced event, not an act of faith.

## Before touching the node

1. **Redundancy is real, now.** For every critical service: two ready replicas on
   *different* nodes (`kubectl get pods -o wide`). A second replica on the node
   you are about to drain is not redundancy.
2. **Quorum margin.** Confirm how many control-plane/etcd members exist and that
   losing this one keeps quorum. On a five-node core the math is easy — until two
   are down for different reasons.
3. **Disruption budgets.** PDBs exist for the services that need them; a drain
   that would violate one should block, and that block is a feature.

## The drain

```
kubectl cordon <node>
kubectl drain <node> --ignore-daemonsets --delete-emptydir-data --timeout=5m
```

Watch the *pods*, not the node status: every evicted pod reaches Ready on another
node. Save the before/after `get pods -o wide` output — that pair is the artifact
that redundancy worked.

## The return

1. `kubectl uncordon <node>` after maintenance.
2. Node reaches Ready and workloads actually reschedule or rebalance onto it —
   an uncordoned node that never receives a pod again is a silent capacity loss.
3. Run one end-to-end check through the real path (a scoped retrieval query, a
   page fetch) and save it.
4. Ledger entry: what was done to the node, the artifacts, anything surprising.

## Failure posture

If the drain stalls or a service loses its last replica: uncordon, let it
recover, and diagnose before retrying. A maintenance window is never a reason to
force-delete pods whose state you have not read.
