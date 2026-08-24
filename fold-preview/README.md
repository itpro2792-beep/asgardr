# Ásgarðr Fold Synthetic Phone Preview

This directory is a clean-room, non-operational public UI study. It is intentionally separate from every quarantined controller candidate.

## Safety boundary

- Synthetic browser-memory fixtures only.
- No network calls, API clients, service workers, analytics, authentication, credentials, live identifiers, audio capture, or browser permissions.
- No mutation, execution, or control capability.
- Reloading resets every interaction.
- The Content Security Policy sets `connect-src 'none'` and `worker-src 'none'`.

## First-release scope

The release contains a responsive cover HUD, an unfolded SOC study, filters, fixture rotation, queue/event views, and a local text-only Siren simulation. The manifest and icons support adding the preview to a phone home screen. Offline caching is deliberately deferred so rollback remains a normal Git revert.

## Public URL

`https://itpro2792-beep.github.io/asgardr/fold-preview/`
