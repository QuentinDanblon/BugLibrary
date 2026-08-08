# Differential & Continuous Recon

<!-- updated: 2026-03 -->

## Why delta wins

Static mega-recon is commoditized. Programs ship features weekly. **Your edge is noticing change.**

## What to version

| Artifact | Cadence |
|----------|---------|
| Host list | Daily/weekly |
| TLS cert set | Weekly |
| JS bundle hashes | Per hunt session |
| OpenAPI / GraphQL schema snapshot | When available |
| Mobile app version | On store updates |
| Program policy text | On every login to platform |

## Diff-driven hunting workflow

```text
1. Pull latest artifacts
2. Diff → changelog of surface
3. For each new endpoint/type/host:
     create ≥1 hypothesis
4. Rank EV; test same day if high
5. Archive snapshots
```

## Automation shape (safe)

Continuous recon bots must:

- Respect robots/rate  
- Only touch in-scope hosts  
- Alert on **delta**, not raw volume  
- Never auto-exploit  

See `docs/09-Automation-and-Tooling`.

## Pro tip

Subscribe to the target’s status page and changelog. Many “new” admin APIs ship with incomplete authZ in week one.

## FR

L’avantage est le **delta**. Versionner hosts, JS, schémas, policy. Chaque nouveauté → hypothèse le jour même.
