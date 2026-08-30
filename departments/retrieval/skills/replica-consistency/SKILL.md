---
name: replica-consistency
description: Use when a fabric service runs multiple replicas over shared state — no per-process caches of store contents without invalidation, health checks that touch the real store path, and consistency probes that compare replicas to each other and to the store.
---

# Replica Consistency

The house case: the document store held 23 documents. One replica reported 6, the
other 17, alternating as the load balancer rotated — each had cached its own list
in process memory at startup and never re-read the database. Neither was correct,
and everything reported healthy.

## Rules

- **The store is the source of truth.** A replica may cache store contents only
  with an explicit freshness mechanism — TTL, invalidation on write, or
  read-through. A cache populated once at startup is a snapshot wearing a
  cache's name.
- **Writes go to the store, then readers see them.** Any write path that updates
  a replica's memory but not the store (or vice versa) will pass every
  single-replica test and fail in production rotation.
- **Health checks exercise the store path.** A liveness probe that returns 200
  from process memory says the process is up, not that it can serve truth. At
  least one probe per service performs a real read through the same code path
  users hit.

## The consistency probe

Bypass the load balancer and ask each replica directly (port-forward or pod IP):

1. The same cheap query to every replica — e.g. document count, latest-write id.
2. Compare replicas to each other **and to the store queried directly**. All
   three agreeing is the pass; replicas agreeing with each other but not the
   store is still a fail (shared stale cache).
3. After a write: re-probe within the freshness window and confirm every replica
   sees it.

Run the probe after deploys, after scaling events, and on schedule. Save the
outputs — the alternating 6/17 bug is invisible in any single response and
obvious in a saved pair.

## When you find drift

Restarting the stale replica hides the evidence and reschedules the bug. Capture
both replicas' answers and the store's first, then fix the caching design —
the restart is the last step, not the first.
