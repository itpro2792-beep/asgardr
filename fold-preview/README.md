# Ásgarðr Fold Synthetic Phone Preview

This directory is a clean-room, non-operational public UI study. It is intentionally separate from every quarantined controller candidate.

## Safety boundary

- Synthetic browser-memory fixtures only.
- After the same-origin static page assets load, the app makes no API, telemetry, live-data, or background connections.
- No service workers, analytics, authentication, credentials, live identifiers, audio capture, or browser permissions.
- No mutation, execution, or control capability.
- Reloading resets every interaction.
- The Content Security Policy sets `connect-src 'none'` and `worker-src 'none'`.

## Canary V2 scope

The release contains a responsive cover HUD, an unfolded SOC study, three coherent fixture scenarios, service and job inspectors, filters, queue/event views, an ephemeral activity trail, a local device-fit scanner, and a deterministic text-only Siren simulation.

The manifest and icons support adding the preview to a phone home screen. A service worker remains deliberately deferred, so this release is not described as offline-capable and rollback remains a normal Git revert.

## Physical Fold acceptance targets

- No page-level horizontal overflow from 320 CSS px upward.
- Equal-width job tabs with Arrow, Home, and End keyboard behavior.
- A shrink-safe Siren query row using `minmax(0, 1fr)`.
- Sticky safety disclosure, safe-area padding, 44 px controls, visible focus, and reduced-motion support.
- The built-in device-fit scanner checks only visible layout dimensions and stores nothing.

## Public URL

`https://itpro2792-beep.github.io/asgardr/fold-preview/`
