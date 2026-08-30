---
name: page-shipping
description: Use when creating or editing a page on the Asgardr public site — self-contained static HTML, both color schemes handled deliberately, truthful metadata, wide content scrolling in its own container, then the publication-safety gate before push.
---

# Page Shipping

Every public Asgardr page is a static, self-contained artifact: one HTML file that
carries its own styles and needs nothing from anyone else's server.

## House style

- **No external resource loads.** No CDN scripts, no web fonts, no remote images.
  System font stacks (`-apple-system, "Segoe UI", …` / `ui-monospace, Menlo, …`)
  and inline or same-directory assets only. Outbound `<a href>` navigation links
  are fine; outbound *loads* are not — the checker enforces this.
- **Color schemes are a decision.** Either support both — light tokens on
  `:root`, dark overrides under `@media (prefers-color-scheme: dark)`, as
  `private-ai/` and `ibwbench/` do — or commit to a single look with every color
  explicit, as the root page does. Never a half-theme that inherits the browser's
  defaults for some elements.
- **Truthful metadata.** `<title>`, `meta description`, and `og:` tags describe
  what the page is *now* (see `redirect-integrity` for moved pages). The
  description is a claim; Records rules apply to it.
- **Wide things scroll alone.** Tables, code blocks, and diagrams get their own
  `overflow-x: auto` container; the page body never scrolls horizontally
  (`device-fit` owns the phone acceptance targets).
- **Accessible by default.** `lang` on `<html>`, one `<h1>`, visible focus,
  honest link text, alt text on images.

## The gate

Before any push that touches HTML:

1. Run `python3 scripts/build-org-chart.py --check` if department skills changed
   (the chart page is generated; a stale one is a false public claim).
2. Run `python3 scripts/check-publication-safety.py` from the repository root.
3. Apply the `public-surface-review` checklist for anything the checker cannot
   see (meaning, provenance, operational capability).

Findings from 2 and 3 are reviewer-class: fix them or take the Operator override
path with a ledger entry. There is no third option.
