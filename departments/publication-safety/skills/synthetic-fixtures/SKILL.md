---
name: synthetic-fixtures
description: Use when creating demo data, sample corpora, or interactive fixtures for a public Asgardr surface — coherent and believable, explicitly fictional, deterministic where possible, and never derived from live values.
---

# Synthetic Fixtures

Public demos run on invented data that teaches the real shape of the system without
leaking a single real value.

## House rules

- **Identities are `demo-*` / `DEMO-*`.** Every asset tag, node name, venue, unit,
  and person in a fixture uses the prefix or an obviously fictional name. Nothing
  that could be mistaken for — or collide with — a real identifier.
- **Labeled fictional, in place.** The surface states that values are generated
  samples and explicitly not design, commissioning, acceptance, test-equipment,
  alarm, or live telemetry data. The label lives next to the data, not only in a
  README.
- **Coherent across the surface.** Fixtures rotate as whole scenarios: if the
  scorecard says a remote unit is degraded, the finding inbox, trend table, and
  ladder agree. Incoherent demo data teaches users to ignore the interface.
- **Deterministic when possible.** Seeded generation makes review reproducible —
  a reviewer can regenerate the fixture and diff it. Randomness at page load is
  acceptable only for cosmetic variation.
- **Not down-sampled reality.** Anonymizing, aggregating, or perturbing live data
  does not make it synthetic. Fixtures are constructed, or they don't ship. When a
  real document inspires a fixture, rewrite the facts (names, values, dates), not
  just the labels.

## Building a fixture set

1. List what the surface must demonstrate (states, edge cases, an unhealthy case —
   demos that only show health are advertisements).
2. Invent a small world: 3–5 named `demo-*` entities with stable relationships.
3. Generate values inside plausible engineering ranges, seeded.
4. Have someone who knows the real system confirm nothing reads as real.
5. Record the seed and generator alongside the fixture.
