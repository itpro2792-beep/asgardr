---
name: device-fit
description: Use when validating a public Asgardr page on real phones — no horizontal overflow from 320 CSS px up, 44 px touch targets, safe-area padding, visible focus, reduced-motion support, keyboard-operable tabs, shrink-safe grids.
---

# Device Fit

The public works get read on phones — sometimes a folding one, sometimes on a
catwalk with gloves. These are the acceptance targets a page must meet before it
claims to fit.

## Acceptance targets

- **No page-level horizontal overflow from 320 CSS px upward.** The body never
  scrolls sideways; wide tables, ladders, and code blocks scroll inside their own
  `overflow-x: auto` containers.
- **Shrink-safe layout.** Grid and flex tracks that contain text use
  `minmax(0, 1fr)` — the default `auto` minimum is how a long token forces the
  whole page wide. Test with an unbroken 40-character string in every flexible
  region.
- **44 px touch targets** for every control, including icon buttons and tab
  strips.
- **Safe-area padding** (`env(safe-area-inset-*)`) so notches and gesture bars
  never cover content; sticky banners must not overlap the content they are
  stuck above.
- **Keyboard operability.** Tab strips take Arrow, Home, and End; every
  interactive element is reachable and shows **visible focus**.
- **Reduced motion respected.** Animations gate on
  `prefers-reduced-motion: reduce`.
- **Equal-width tabs** where a tab strip exists — labels truncate, the strip
  does not jitter.

## Verification

- Check at 320, 360, 412, and the device's folded/unfolded widths; verify
  viewport scale and DPR are what the meta viewport intends.
- A scan result applies **only to the viewport and workspace scanned** — passing
  folded says nothing about unfolded. Record which combination each artifact
  covers.
- Verification stores nothing and phones home nothing: a device-fit scanner is a
  public-surface feature and lives inside the same safety boundary as the page
  (`public-surface-review`).
- The artifact is the saved scan/screenshot set per viewport, kept with the
  release notes for the canary that shipped it.
