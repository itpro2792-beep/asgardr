---
name: redirect-integrity
description: Use when moving, retiring, or re-homing a public Asgardr page — old URLs keep working, redirects carry a visible link and an honest description of the destination, and page metadata stays truthful.
---

# Redirect Integrity

Asgardr's public home has moved before and will move again. The house pattern keeps
every URL that was ever shared alive and honest.

## The moved-page pattern

A page that has moved is replaced by a small static page that:

1. Keeps a **meta refresh** (~1 second) to the canonical destination.
2. Shows a **visible link** to the same destination — the refresh is a convenience,
   the link is the guarantee (readers with refresh disabled, crawlers, and anyone
   who hits Back).
3. States **in one or two sentences what is at the destination now** — including
   the safety posture where relevant ("synthetic-only, no live cluster access, no
   operator controls"), so the redirect page itself never oversells.
4. Updates its `<title>`, `meta description`, and `og:` tags to describe the
   current state, not the page that used to be here.

## Checks before shipping a move

- The canonical destination actually serves (fetch it once; save the status).
- Every internal link that pointed at the old page is updated or intentionally
  left to ride the redirect — decided, not defaulted.
- The old URL is never deleted. Retired content gets a redirect page explaining
  where the current material lives; nothing 404s that once worked.
- The redirect page passes `public-surface-review` like any other page — it is a
  public surface.

## Anti-patterns

- Silent JavaScript-only redirects (fail with scripts off; invisible to review).
- Redirect chains — always point at the final canonical URL.
- Descriptions that still advertise the old content ("interactive garden" for a
  page that now hosts a field guide).
