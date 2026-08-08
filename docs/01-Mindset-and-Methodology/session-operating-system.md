# Session Operating System / OS de session de hunt

## Pre-flight (5 min)

- [ ] Program policy open; scope note visible  
- [ ] Accounts ready (A/B users, roles) — labeled  
- [ ] Proxy + scope prefix filters set  
- [ ] Rate limit self-budget defined  
- [ ] Hypothesis card selected (not “browse randomly”)  

## During

| Practice | Why |
|----------|-----|
| One primary hypothesis at a time | Prevents thrash |
| Annotate proxy history with H-IDs | Replay & report later |
| Prefer two-account proofs for authZ | Gold standard for IDOR |
| Snapshot interesting responses | Evidence integrity |
| Pause on unexpected production impact | Safety |

## Notes structure

```text
/program-x
  policy.md
  asm.yaml
  hypotheses/
  evidence/
  reports/
  graveyard.md
```

## Post-session (10 min)

- [ ] Update ASM deltas  
- [ ] Close or schedule hypotheses  
- [ ] Draft report skeleton if anything confirmed  
- [ ] Log noise sources to avoid tomorrow  
- [ ] Emotional checkout: tilted? rest  

## Deep work blocks

Elite default: **90-minute** focused blocks, phone away, leaderboard closed.

## FR

Pre-vol scope + comptes + budget de rate. Une hypothèse principale. Notes structurées. Post-session : ASM, cimetière, draft rapport. Blocs 90 min.
