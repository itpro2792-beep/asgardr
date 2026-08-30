---
name: restore-drill
description: Use when validating any Asgardr backup — vector collections, etcd snapshots, config repos, volumes. A backup that has never been restored is a file of unknown provenance; this drill proves it by restoring and querying the restored copy.
---

# Restore Drill

A backup that has never been restored is a file of unknown provenance. The drill
turns "we have backups" into an artifact.

## The drill

1. **Snapshot** through the system's own mechanism (Qdrant snapshot, `etcd`
   snapshot, `git bundle`, volume snapshot). Record the command, timestamp, and
   size.
2. **Restore into scratch** — a scratch collection, namespace, or directory.
   Never restore over the live system to test the backup.
3. **Query the restored copy** for a corpus-only fact (an asset tag, a specific
   key, a named record) and compare against the live system's answer. For etcd,
   bring up a throwaway datastore from the snapshot and list a known resource.
4. **Record the artifact** — the query, both answers, the date — in the decision
   ledger. "Backup verified" with no artifact is a status field, not evidence.
5. **Tear down the scratch copy** and confirm the live system was untouched.

## Cadence and coverage

- Run the drill on schedule, not only after incidents; a drill that exists but
  never runs decays into the thing it was built to prevent.
- Every distinct backup mechanism gets its own drill — a proven Qdrant restore
  says nothing about etcd.
- After any backup-tooling upgrade, the next drill is due immediately.

## Failure handling

A failed restore is a sev-now finding on the *backup*, not on the drill. Do not
re-snapshot and call it fixed: root-cause why the previous artifact was
unrestorable, then fix the mechanism, then drill again. The negative control
applies here too — a drill pointed at a deliberately corrupted snapshot must
fail loudly, or the drill itself is decoration.
