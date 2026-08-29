---
name: discrepancy-ledger
description: Use when sources contradict each other or the public record contradicts itself — flag the discrepancy openly rather than silently resolving it, track open questions to answered, and keep resolved entries visible.
---

# Discrepancy Ledger

When two sources disagree, the honest output is the disagreement. Picking the
tidier number and moving on is how public records rot. The house notebook
carries seven flagged places where the record contradicts itself — flagged is
the feature.

## Entry format

```
## D-07 — Adoption date: city site vs. meeting minutes
Source A:  …what it says, dated, linked…
Source B:  …what it says, dated, linked…
Status:    open | answered
Resolution: (when answered) which source won, on what evidence, and why
```

## Rules

- **Flag, don't smooth.** A discrepancy is published as a discrepancy. Readers
  can handle "these two official numbers disagree"; they cannot handle being
  quietly handed the wrong one.
- **Resolution requires evidence**, not seniority of source. "The PDF is newer"
  is a hypothesis; the resolution entry says what artifact settled it.
- **Answered entries stay visible.** The ledger's first answered question is a
  milestone, not deleted clutter — it shows the process works. Mark it
  `answered`, keep it.
- **Open is a working status.** Entries carry what would settle them (a FOIL
  response, a site visit, a drill), so "open" means awaiting a named artifact,
  not abandoned.

## Engineering use

The same ledger pattern covers the fabric: monitoring says the service is up,
the probe matrix says one direction is down — that is a discrepancy entry, not a
judgment call made silently in favor of the dashboard. Cross-reference the
decision ledger when a resolution changes what the fabric does.
