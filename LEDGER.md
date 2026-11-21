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

## 2026-11-21 — Harden the publication gate after an adversarial review of PR #6

- **Decision:** Rewrite the CSP rule and the reporting path of
  [`scripts/check-publication-safety.py`](scripts/check-publication-safety.py).
  The policy is found the way a browser finds it: a real
  `<meta http-equiv="Content-Security-Policy">` in `<head>`, before any script,
  style, link or base. Report-Only, commented-out, templated and body-placed
  declarations do not count. The policy is parsed as CSP3 parses it and its
  sources are allow-listed instead of block-listed. Findings name file, line,
  column, category and length only: no matched text, no surrounding line, no
  digest. Every file is scanned in several decodings (UTF-8, BOM-marked or
  NUL-patterned UTF-16/32, NUL-stripped, entity-decoded pages), every pattern is
  bounded so long lines stay linear, and the self-test gains a fixture per
  evasion.
- **Evidence:** Two independent reviewers reproduced 14 defects in the first
  version (`505e209`), among them twelve CSP declarations Chromium ignores but
  the gate accepted; scheme-less hosts, `*:*`, `&#42;`, a shadowed `default-src`
  and `'strict-dynamic'` accepted as strict; source lines carrying addresses and
  keys still printed by the load and network findings; the printed `sha256`
  prefix of a private address reversed by brute force in 7–8 s; and a 181 KB
  single-line stylesheet taking 32 s. After the rewrite the self-test passes
  (81 findings on bad fixtures, 0 on clean ones), 41 of 43 mutants are killed
  (the 2 survivors are equivalent: a check another guard fully covers, and a
  speed-only shortcut), and the long-line control takes under 1 s yet fails
  (37.9 s, 149.6 s) when either pattern bound is removed.
- **Rejected:** Hash-only style sources (`'sha256-…'` per `<style>` block):
  tighter on paper, but every edit would need a recomputed hash or the page
  silently loses its styles. `'unsafe-inline'` for styles on script-free pages
  is the house policy. Also rejected: printing a digest for correlation, since
  a low-entropy value's digest is itself a publication.
- **Revisit:** When a page needs something outside the allow-list (a font, a
  frame, a host): extend the allow-list here with the reason, never per page.
- **Status:** answered

## 2026-11-21 — Open: is the private-ai sample corpus synthetic?

- **Question:** The [`private-ai/`](private-ai/) case study shows answers drawn
  from a sample corpus about a venue named "Meridian Arena". Is that corpus
  synthetic, and are its figures and documents free of real client or site data?
- **Why it matters:** The rule is synthetic data only, labeled as such. If the
  corpus is synthetic, the page needs a label in place (and a `demo-*` venue
  name when the demo is next regenerated, or a recorded accepted risk for
  keeping the name). If it is not, the page needs removal, not a label.
- **Evidence so far:** The venue name appears in no other file of this
  repository; the commit that created the page (`7cf7e9a`) describes "four real
  question-and-answer exchanges"; an external review called the corpus
  synthetic without citing a source. A synthetic label was drafted in PR #6 and
  withdrawn, because nothing in the repository supports it.
- **Owner:** Operator. **Settled by:** the corpus generator and seed, or the
  Operator's statement.
- **Status:** open
