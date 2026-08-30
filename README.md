# Asgardr — public garden repository

This is the GitHub Pages home for the public surfaces of **Asgardr**: a
ten-computer, local-first intelligence and knowledge fabric — a five-node k3s
core, five mesh peers, and one evidence-led operator. The canonical public guide
lives at the [Asgardr garden portal](https://asgardr-public-garden.itpro27.chatgpt.site/);
this repository hosts the static pages and the **Asgardr operations org**.

Everything here is public-safe by construction: synthetic data only, no live
cluster access, no telemetry, no operator controls. A mechanical checker
enforces that boundary (below).

## Pages

| Path | What it is |
| --- | --- |
| [`/org/`](https://itpro2792-beep.github.io/asgardr/org/) | **The operations org chart** — generated from this repository tree |
| [`/private-ai/`](https://itpro2792-beep.github.io/asgardr/private-ai/) | Case study: self-hosted, cited document Q&A on the fabric |
| [`/ibwbench/`](https://itpro2792-beep.github.io/asgardr/ibwbench/) | An in-building wireless / DAS reasoning benchmark for LLMs |
| [`/fold-preview/`](https://itpro2792-beep.github.io/asgardr/fold-preview/) | Synthetic phone UI study (canary V3), clean-room and non-operational |
| [`/amsterdam/`](https://itpro2792-beep.github.io/asgardr/amsterdam/) | Civic notebook for Amsterdam, NY — every claim labeled and dated |
| `/`, `/garden/…` | Redirects to the canonical garden portal |

## The Asgardr operations org

An agent organization for running the fabric, structured as departments of
Claude Code skills. **8 departments · 27 skills · 2 reviewer-class.** Every
department installs independently, so each of the ten machines carries only the
departments its role needs:

```
/plugin marketplace add itpro2792-beep/asgardr
/plugin install fabric@asgardr            # the k3s core machine
/plugin install evidence@asgardr          # everywhere work gets verified
/plugin install publication-safety@asgardr # wherever public pages are edited
```

| Department | Class | Holds |
| --- | --- | --- |
| `evidence` | **reviewer** | Evidence review, negative controls, test forensics, restore drills |
| `publication-safety` | **reviewer** | Public-surface review, synthetic fixtures, secret hygiene, redirect integrity |
| `operator` | line | Authority tiers, continuity planning, the decision ledger |
| `fabric` | line | Node lifecycle, pinned releases, upgrade runbooks |
| `mesh` | line | Peer lifecycle, key rotation, reachability audits |
| `retrieval` | line | Corpus hygiene, grounded answering, scoped retrieval, replica consistency |
| `workloads` | line | Page shipping, canary progression, device fit |
| `records` | line | Claim labeling, discrepancy ledgers, source dating |

The skills are not generic runbooks: each one is distilled from Asgardr's own
published operating history — the test suite that passed with the vector
database off, the replicas that disagreed about how many documents existed, the
backup doctrine ("a backup that has never been restored is a file of unknown
provenance"), the synthetic-only canary boundary, the civic notebook's
claim-labeling rules.

### Reviewer-class, and why it is mechanical

The two reviewer departments report to the Operator, not into the functions they
review, and **their blocking findings are not overrulable by the department
under review** — only the Operator may override, recorded in the decision
ledger. Prose can't enforce that, so this repository does:

```
python3 scripts/check-publication-safety.py --self-test   # prove the checker can fail
python3 scripts/check-publication-safety.py               # scan the whole repo
python3 scripts/build-org-chart.py --check                # chart must match the tree
```

The checker blocks external resource loads, network APIs in page code,
credential-shaped strings, private-fabric identifiers, and a stale generated
chart. Its `--self-test` seeds a known-bad fixture and asserts every rule
fires — a scanner that has never caught anything is indistinguishable from a
scanner that cannot.

Install the same gate as a local pre-push hook in any clone, one command:

```
sh scripts/install-hooks.sh
```

Decisions, accepted risks, and reviewer overrides for this repository are
recorded in [`LEDGER.md`](LEDGER.md) — the org's `decision-ledger` skill,
practiced on the org itself.

### Regenerating the chart

[`org/index.html`](org/index.html) is generated — never hand-edit it:

```
python3 scripts/build-org-chart.py
```

## Relation to headcount

The org pattern follows [cbrock84/headcount](https://github.com/cbrock84/headcount)
(MIT) — an agent organization structured as a company: independently installable
departments, a reviewer class reporting to the top, and a chart generated from
the repository tree. Asgardr adapts it: departments shaped like a fabric rather
than a firm, reviewer findings enforced by a script and a self-test rather than
by prose, and skills distilled from lived operational evidence rather than
general practice. Gaps and improvements travel well in both directions.
