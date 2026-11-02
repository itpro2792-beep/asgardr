# Asgardr Public-Site Decision & Discrepancy Ledger

The decision and discrepancy ledger for everything this repository governs: the
public pages and the operations org. Kept per the org's own
[`decision-ledger`](departments/operator/skills/decision-ledger/SKILL.md) and
[`discrepancy-ledger`](departments/records/skills/discrepancy-ledger/SKILL.md)
skills: entries carry their evidence, contradictions in the public record are
flagged openly rather than smoothed over, corrections append rather than
rewrite, and reviewer-class overrides are not valid unless recorded here. The
private fabric keeps its own ledger beside the systems it governs; nothing in
this file references live cluster state.

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

## 2026-11-02 — Discrepancy D-01: July–August 2026 k3s core framing vs. 2026-08-11 retirement

- **Source A:** July–August 2026 public surfaces in this repository —
  [`index.html`](index.html), [`garden/written/index.html`](garden/written/index.html),
  [`private-ai/index.html`](private-ai/index.html), [`README.md`](README.md),
  [`departments/org-manifest.json`](departments/org-manifest.json), and
  [`departments/fabric/`](departments/fabric/) (published through PR #2,
  `3570f03`, merged `2026-08-30`) — described the fabric in the present tense
  as running a five-node `k3s` Kubernetes core (and an earlier cluster-count
  phrasing in the July–August 2026 `private-ai/` case study footer).
- **Source B:** **CONFIRMED** architecture transition (`2026-08-11`): the
  five-node `k3s` Kubernetes orchestration layer was retired on `2026-08-11` in
  favor of host-native service management across the private fabric. Late-August
  2026 public commits (`2506f08`, `2026-08-29`) carried forward the July–August
  2026 `k3s` description without recording the `2026-08-11` transition.
- **Status:** answered
- **Resolution:** Flagged and dated across all affected public pages,
  [`README.md`](README.md), [`departments/org-manifest.json`](departments/org-manifest.json),
  [`org/index.html`](org/index.html), and [`departments/fabric/`](departments/fabric/)
  on `2026-11-02` per [`discrepancy-ledger`](departments/records/skills/discrepancy-ledger/SKILL.md)
  and [`source-dating`](departments/records/skills/source-dating/SKILL.md).
  Present-tense claims now state host-native service management without
  publishing live machine counts or private topology; historical `k3s` pages
  and runbooks stay visible with their **July–August 2026 vintage** labeled
  rather than silently rewritten.

## 2026-11-02 — Preserve July–August 2026 k3s runbooks with vintage labels after 2026-08-11 retirement

- **Decision:** Keep the July–August 2026 `k3s` runbooks in
  [`departments/fabric/`](departments/fabric/) (`node-lifecycle`,
  `pinned-releases`, `upgrade-runbook`) and the [`private-ai/`](private-ai/)
  case study intact, explicitly labeled with their **July–August 2026 vintage**
  and a dated **2026-08-11** retirement / host-native transition note, and
  replace the hardcoded machine-count stat in [`scripts/build-org-chart.py`](scripts/build-org-chart.py)
  with the tree-derived line-department count so every figure on
  [`org/index.html`](org/index.html) is derived solely from the repository tree.
- **Evidence:** Discrepancy D-01 audit (`2026-11-02`) across tracked files in
  this repository; `python3 scripts/check-publication-safety.py` and
  `python3 scripts/build-org-chart.py --check` passing on the updated tree.
- **Rejected:** Silently deleting `k3s` from historical pages and skills as if
  it had never existed (violates [`source-dating`](departments/records/skills/source-dating/SKILL.md)
  rule 4: corrections stay visible), or publishing live hostnames, addresses,
  ports, or current machine counts (violates
  [`public-surface-review`](departments/publication-safety/skills/public-surface-review/SKILL.md)).
- **Revisit:** When standalone host-native service-supervision runbooks are
  distilled as companion skills alongside the July–August 2026 `k3s` runbooks.
- **Status:** answered
