---
name: public-surface-review
description: Use before anything ships to a public Asgardr surface — GitHub Pages, the garden portal, screenshots, posts, demos. Enforces the synthetic-only boundary between the private fabric and the public web. Reviewer-class - blocking findings are not overrulable by the department under review.
---

# Public Surface Review

This is a reviewer-class skill. It reports to the Operator, not into the department
whose page is under review. A blocking finding can be overridden only by the
Operator, recorded in the decision ledger.

## The boundary

Public surfaces are synthetic-only. They describe the fabric; they never reach into
it. The public garden's own words: no live cluster access, no private telemetry,
no operator controls.

## Review checklist

Any "no" is a finding. Items marked ⛔ are blocking.

1. ⛔ **No live connections.** After the same-origin static assets load, the page
   makes no API, telemetry, live-data, or background connections. Interactive pages
   declare it: CSP `connect-src 'none'` and `worker-src 'none'`.
2. ⛔ **No operational capability.** No tune, transmit, acknowledge, restart, or
   any action that could reach a real system — not even behind a "demo" flag.
3. ⛔ **No real identifiers.** No private hostnames, internal IPs, serials, MACs,
   real venue or client names, credentials, or filesystem paths from the fabric.
   Synthetic identities are `demo-*` / `DEMO-*` (see `synthetic-fixtures`).
4. ⛔ **No secrets.** Run `scripts/check-publication-safety.py` from the repository
   root; its findings are this department's findings and carry the same authority.
5. **Fictional data labeled fictional.** Generated values are stated to be samples —
   explicitly not design, commissioning, acceptance, test-equipment, alarm, or live
   telemetry data.
6. **Reload resets everything.** No service workers, analytics, authentication,
   audio capture, or browser permissions; no state that outlives the tab unless the
   page's README declares and justifies it.
7. **Provenance is honest.** Content derived from the repository tree (like the
   generated org chart) is publishable. Content derived from live cluster state is
   not, however aggregated.
8. **The safety disclosure is visible** on interactive pages, and the page's meta
   description tells the truth about what the page is.

## Scope

"Public surface" includes screenshots and copy-pastes: a terminal screenshot with a
real internal hostname fails item 3 exactly as a web page would. Review what will
actually be visible, not what the author intended to show.
