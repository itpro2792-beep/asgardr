---
name: node-lifecycle
description: Use when taking a k3s core node down for maintenance or returning it to the Asgardr fabric — cordon, drain, prove the workloads survived, and prove the return with artifacts rather than dashboard green.
---

# Node Lifecycle

Five core nodes; critical services run two replicas and must survive a node loss.
This runbook makes each node exit and return an evidenced event, not an act of
faith.

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
