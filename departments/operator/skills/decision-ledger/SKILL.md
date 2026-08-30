---
name: decision-ledger
description: Use when recording an operational decision for the Asgardr fabric — what was decided, on what evidence, what was rejected, and when to revisit. Also the required destination for reviewer-class overrides and accepted risks.
---

# Decision Ledger

Decisions decay into folklore unless written down with their evidence. The ledger
is append-only in spirit: corrections stay visible, nothing is silently rewritten.

## Entry format

```
## 2026-08-29 — Pin retrieval gateway to vX.Y.Z (digest sha256:…)
Decision:   …one sentence…
Evidence:   links/paths to the artifacts that justified it
Rejected:   the alternative(s) and why
Revisit:    the condition or date that reopens this
Status:     open | answered | superseded-by <entry>
```

## Rules

- **Evidence, not vibes.** An entry with no artifact link is a preference, not a
  decision. Preferences are allowed — labeled as such.
- **Corrections append.** When an entry proves wrong, add the correction below it
  and mark the original `superseded`. The wrong version stays readable; that is
  the point.
- **Open questions live here too.** Carry them as `open` until answered, then mark
  them `answered` with the artifact — an open ledger that never answers anything
  is a worry list.
- **Reviewer overrides land here, always.** When the Operator overrides a blocking
  finding from Evidence Review or Publication Safety, the entry records the
  finding, the override reason, and the accepted risk. No ledger entry, no
  override.
- **Accepted risks are decisions.** "We know replica consistency checks don't
  cover service X yet" belongs in the ledger with a revisit condition, not in a
  commit message.

## Where it lives

One ledger per concern, next to the thing it governs (a `LEDGER.md` in the
relevant repository or directory), findable from the fabric's index. Private
ledgers may reference private systems freely; anything quoted onto a public
surface goes through `public-surface-review` first.
