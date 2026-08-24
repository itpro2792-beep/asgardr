# Ásgarðr Fold Synthetic Phone Preview

This directory is a clean-room, non-operational public UI study. It is intentionally separate from every quarantined controller candidate.

## Safety boundary

- Synthetic browser-memory fixtures only.
- After the same-origin static page assets load, the app makes no API, telemetry, live-data, or background connections.
- No service workers, analytics, authentication, credentials, live identifiers, audio capture, or browser permissions.
- No mutation, execution, or control capability.
- Reloading resets every interaction.
- The Content Security Policy sets `connect-src 'none'` and `worker-src 'none'`.

## Canary V3 scope

The release adds a distinct RF/DAS workspace alongside the operations study. Three coherent cross-domain scenarios rotate together across a cover HUD, RF scorecard, signal-path ladder, remote-unit matrix, fixed trend table, finding inbox, cluster services, queue/events, inspectors, and deterministic text-only Siren explanations.

All RF values are generated samples and are explicitly not design, commissioning, acceptance, test-equipment, alarm, or live telemetry data. They use fictional `demo-*` and `DEMO-*` identities only. There are no tune, transmit, acknowledge, restart, or other operational actions.

The manifest and icons support adding the preview to a phone home screen. A service worker remains deliberately deferred, so this release is not described as offline-capable and rollback remains a normal Git revert.

## Physical Fold acceptance targets

- No page-level horizontal overflow from 320 CSS px upward.
- Equal-width job tabs with Arrow, Home, and End keyboard behavior.
- A shrink-safe Siren query row using `minmax(0, 1fr)`.
- Sticky safety disclosure, safe-area padding, 44 px controls, visible focus, and reduced-motion support.
- The built-in device-fit scanner checks visible overflow rails, clipped controls, 44 px targets, viewport scale/DPR, and sticky-banner overlap. It stores nothing and each result applies only to the scanned viewport/workspace.

## Public URL

`https://itpro2792-beep.github.io/asgardr/fold-preview/`
