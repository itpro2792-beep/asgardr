# Asgardr Public-Site Decision Ledger

The decision ledger for everything this repository governs: the public pages
and the operations org. Kept per the org's own
[`decision-ledger`](departments/operator/skills/decision-ledger/SKILL.md) skill:
entries carry their evidence, corrections append rather than rewrite, and
reviewer-class overrides are not valid unless recorded here. The private
fabric keeps its own ledger beside the systems it governs; nothing in this
file references live cluster state.

---

## 2026-08-30 — Adopt the operations org (PR #2)

- **Decision:** Structure Asgardr's operational doctrine as an installable
  skill org — 8 departments, 27 skills, 2 reviewer-class — patterned after
  cbrock84/headcount (MIT), with reviewer findings enforced mechanically
  (`scripts/check-publication-safety.py` + CI) rather than by prose.
- **Evidence:** [PR #2](https://github.com/itpro2792-beep/asgardr/pull/2),
  merged as `3570f03`; CI green on every head; checker self-test passing with
  seeded-bad fixtures; independent reproduction on a second OS by the
  workstation agent (self-test PASS, scan clean, chart current).
- **Rejected:** Installing headcount's corporate departments wholesale — the
  pattern transfers, the content does not. Also rejected: prose-only reviewer
  authority, which cannot block anything.
- **Revisit:** After a month of real use — prune skills that never trigger,
  split ones doing double duty.
- **Status:** answered

## 2026-08-30 — Harden the scanner twice, same day (5492d01, 18bca0d)

- **Decision:** Extend the private-address rule to the CGNAT block (100.64/10)
  after a partner-agent transcript surfaced a tailnet-style address; rewrite
  resource-load rules as whole-text passes after adversarial testing evaded the
  line-based scanner three ways (multi-line tag, unquoted attribute,
  protocol-relative URL).
- **Evidence:** Before/after artifacts in the commit messages — 0/3 evasions
  caught before, 3/3 after; self-test extended to pin both (now 12 findings on
  seeded-bad fixtures, and it fails if either private-address range or any
  evasion category stops firing). Notably, the checker blocked its own
  hardening commit over a dotted-quad example in a comment.
- **Revisit:** On any real page adding inline scripts or new asset types.
- **Status:** answered

## 2026-08-30 — Accepted risk: credential and address rules are line-based

- **Decision:** The secret-pattern and private-address rules scan per line.
  A credential deliberately split across lines, or assembled at runtime, would
  evade them. Accepted: tokens do not naturally split, the load rules (the
  channel such a trick would feed) are whole-text, and `secret-hygiene` review
  covers intent that regex cannot.
- **Revisit:** Immediately, if any split or assembled credential is ever found
  in a public artifact.
- **Status:** open (accepted risk)

## 2026-08-30 — Accepted risk: org chart commits to the dark garden theme

- **Decision:** `org/index.html` ships single-theme (night pine, explicit
  colors, `color-scheme: dark`) matching the garden's root-page identity,
  rather than dual light/dark.
- **Rejected:** A light variant nobody designed — the half-theme failure mode
  CLAUDE.md forbids.
- **Revisit:** If the garden portal itself adopts a light mode.
- **Status:** open (accepted risk)

## 2026-08-30 — Open: first live restore drill

- **Decision pending:** Run `restore-drill` against the fabric's real backups
  (vector collections and the cluster datastore): snapshot → restore into
  scratch → query a corpus-only fact → record the artifact here and in the
  private ledger.
- **Owner:** The Operator, with the workstation agent.
- **Settles it:** The saved drill artifact, per the skill.
- **Status:** open

## 2026-08-30 — Open: garden portal links the org chart

- **Decision pending:** The canonical portal (hosted outside this repository)
  should link `…/asgardr/org/`, described honestly: generated from the
  repository tree, no live cluster access.
- **Owner:** The Operator, with the workstation agent (`public-surface-review`
  checklist applies manually — the checker cannot see that host).
- **Status:** open
