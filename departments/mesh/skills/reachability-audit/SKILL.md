---
name: reachability-audit
description: Use when verifying connectivity across the Asgardr mesh — a full peer-to-peer probe matrix at the service level, read from saved artifacts with current timestamps, never from a dashboard's green dot.
---

# Reachability Audit

A mesh dashboard shows what the control plane believes. The audit shows what the
packets do.

## The probe matrix

For the five peers (and the core as a sixth endpoint where relevant), probe every
directed pair — reachability is not symmetric, and the asymmetric failures are
the interesting ones.

- **Probe at the service level**, not just ICMP. A peer that answers ping but
  fails the service probe (SSH, HTTP on the actual port, a retrieval query) is
  *down* for every purpose that matters. Ping-only green is the mesh's version of
  a vacuous test.
- **Save the matrix as an artifact**: source, destination, probe type, result,
  latency, timestamp. The saved matrix — not the memory of running it — is what
  the audit produces.
- **Check the timestamps.** An artifact from last month proves last month.
  Staleness of the evidence is itself a finding.

## Reading the results

- **Baseline the latencies.** Keep the previous matrix; a path that doubled its
  latency while staying "up" is drifting toward a failure and worth a ledger note.
- **Direct vs. relayed.** If the mesh can relay traffic, mark which paths went
  direct — a peer that silently fell back to relay works today and fails when the
  relay does.
- **One failing direction** of a pair is a real finding even when the reverse
  works; do not average it away.

## Cadence and negative control

Run the audit on schedule and after any mesh change (join, retirement, rotation,
ACL edit). The audit's own negative control: probe one endpoint that must be
unreachable (a retired peer, a blocked port). If the forbidden probe succeeds,
either the ACLs or the audit is broken — both are findings.
