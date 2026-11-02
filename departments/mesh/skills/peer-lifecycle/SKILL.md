---
name: peer-lifecycle
description: Use when joining, replacing, or retiring an Asgardr mesh peer — key issuance stays with the Operator, every step leaves an artifact, and retirement is proven by the retired peer failing to connect.
---

# Peer Lifecycle

Mesh peers extend the private fabric across roles and locations (note recorded
`2026-11-02`, `CONFIRMED`: the July–August 2026 five-node `k3s` core referenced
in early mesh notes was retired on `2026-08-11` in favor of host-native service
management — see [`LEDGER.md`](../../../../LEDGER.md)). Peers come and go;
the mesh's trust model must not drift while they do.

## Joining a peer

1. **Key issuance is Tier 3** (`operator-authority`): the Operator mints the
   credential; automation may stage everything else.
2. **Least privilege from the first packet.** The peer's ACLs grant what its role
   needs — a display node does not get SSH to the core. Write the intended grants
   down before joining, then verify the effective ACLs match them.
3. **Prove the join from both ends.** A handshake or session log on the new peer
   *and* on an existing peer, saved. One-sided evidence has fooled better setups.
4. **Name it honestly.** The peer's mesh name states its role; its hardware,
   location, and recovery path go in the continuity plan's knowledge ledger.

## Replacing a peer

Bring the replacement up before the incumbent goes away when the role allows —
the mesh should never silently drop below its expected strength. The replacement
gets a *new* credential; credentials do not transfer between machines. Then retire
the old peer properly:

## Retiring a peer

1. Remove its credential and ACL entries.
2. **Negative control: the retired peer must fail.** Attempt a connection from it
   (or with its captured credential) and save the refusal. Removal without the
   failing artifact is a belief, not a retirement.
3. Wipe fabric credentials from the machine before it leaves custody.
4. Ledger entry: when, why, and the refusal artifact.

## Standing audit

The set of peers the mesh control plane lists must equal the set the continuity
plan documents — run the comparison whenever either changes. An extra entry
nobody remembers is a finding, not clutter.
