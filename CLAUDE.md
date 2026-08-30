# CLAUDE.md — working rules for this repository

This is the public GitHub Pages repo for Asgardr (a private ten-computer
fabric) plus the Asgardr operations org (departments of Claude Code skills
under `departments/`). Everything in this repo is public.

## The gate before any push

1. `python3 scripts/check-publication-safety.py` — must exit 0. Its findings
   are reviewer-class: fix them, or stop and ask the Operator; never push
   around them.
2. If anything under `departments/` changed:
   `python3 scripts/build-org-chart.py` and commit the regenerated
   `org/index.html`. The freshness check fails the push gate otherwise.
3. After editing either script, run
   `python3 scripts/check-publication-safety.py --self-test` — the checker
   must still be able to fail.
4. In a fresh clone, run `sh scripts/install-hooks.sh` once — it wires the
   same gate in as a pre-push hook. Overrides of a blocking finding are valid
   only with an Operator entry in `LEDGER.md`.

## Hard rules for public pages

- Pages are self-contained static HTML: no external scripts, stylesheets,
  fonts, or images; no `fetch`/XHR/WebSocket/service workers; no analytics.
  Outbound `<a href>` navigation links are fine.
- Synthetic data only, labeled as such; identities use `demo-*` / `DEMO-*`.
  Never publish private hostnames, RFC1918 or CGNAT/tailnet addresses,
  serials, credentials, or anything derived from live cluster state. This
  covers transcripts and screenshots too — an agent log pasted into a public
  page is a public surface.
- `org/index.html` is generated — edit `scripts/build-org-chart.py`,
  `departments/org-manifest.json`, or the skills, never the output.
- Moved pages keep a meta-refresh **plus** a visible link to the canonical
  destination (see existing `index.html`, `garden/index.html`).
- Color schemes: support light and dark, or commit to one with every color
  explicit — never a half-theme.

## Skills conventions

- One skill per directory: `departments/<dept>/skills/<name>/SKILL.md`;
  frontmatter `name` must equal the directory name; `description` starts with
  "Use when …" and states concrete triggers.
- New skills are distilled from real Asgardr practice with an evidence
  requirement stated, not generic advice.
- A new department needs: `departments/<id>/.claude-plugin/plugin.json`, an
  entry in `.claude-plugin/marketplace.json`, an entry in
  `departments/org-manifest.json`, then a chart regeneration.
