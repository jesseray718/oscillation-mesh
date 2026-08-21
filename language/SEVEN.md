# 7-Symbol Language — Oscillation Lattice

Seven glyphs. Enough to describe any node, any link, any energy flow, any observation.
Designed so a human with a stick in the dirt and a computer with a full stack can both read it.

## Glyphs (Unicode + ASCII fallback)

1. ●   NODE        (existence, presence, lowest node)
2. ─   LINK        (connection, mesh edge, absolute path)
3. ≈   ENERGY      (η, joules, useful work)
4. □   STORE       (capture, ledger, seed, version)
5. →   RETURN      (give back, gratitude, cycle close)
6. ○   OBSERVE     (sense, measure, status, heal)
7. ✧   TRANSFORM   (oscillate, rise/fall between layers, compound)

## Minimal grammar
- Sequence is left-to-right or top-to-bottom.
- ●─●          two nodes linked
- ●≈□          node stores energy
- ○●→          observe node then return
- ●✧○          node transforms under observation
- Full cycle:  ○ ● ≈ □ → ● ✧ ○

## Why seven
- Matches Seed of Life (seven circles)
- Matches the completeness cycle (work + rest)
- Small enough to carve, large enough to express the entire lattice
- Can be drawn by hand or rendered by any modern tool

## Implementation note
A future interpreter can treat these as the only tokens of a tiny language
that compiles to shell, Python, or pure physical action.
