# Hypothesis-Driven Hunting

<!-- updated: 2026-03 -->

## Definition

A **hypothesis** is a falsifiable statement about system behavior under a trust assumption.

> Bad: “I’ll look for XSS.”  
> Good: “If `noteId` is only authorized by obscurity, user A can read user B’s note via `GET /api/notes/{id}` with A’s session.”

## Template

```markdown
### H-YYYYMMDD-###
Asset: ...
Trust boundary: (e.g. user → user, tenant → tenant, user → admin)
Claim: ...
Predicted evidence: (status codes, body fields, timing, error)
Test plan: (steps, accounts needed)
Risk controls: (rate, data minimization)
Status: open | confirmed | killed | blocked-by-scope
Notes: ...
```

## Generating hypotheses (sources)

1. **Access control matrix** — roles × objects × actions  
2. **State machines** — order of steps (pay → fulfill, invite → accept)  
3. **Multi-tenant IDs** — UUID vs sequential; leakage in exports  
4. **Feature flags / beta hosts** — weaker auth on staging-like prod  
5. **Diffs** — what changed in last release notes / JS bundles  
6. **Error oracles** — verbose errors, GraphQL extensions  
7. **Trust of secondary channels** — email links, webhooks, mobile deep links  

## Ranking (Expected Value)

\[
EV \approx P(\text{exists}) \times \text{Impact} \times P(\text{accept}) \big/ \text{Cost}
\]

| Factor | High score signals |
|--------|--------------------|
| P(exists) | New feature, complex authZ, IDOR-prone patterns |
| Impact | Auth bypass, cross-tenant, RCE-class, PII mass |
| P(accept) | Clear repro, in-scope, not “best practice” nits |
| Cost | Accounts ready, no heavy reverse, low rate risk |

## Kill criteria (stop testing)

- Out of scope explicitly  
- Mitigations proven (same-origin, binding tokens, etc.)  
- Cost exceeds EV by 5× without new signal  
- Safe harbor risk rising (noisy, production impact)  

## Session example (short)

1. Map `POST /teams/{id}/invites`  
2. H1: invite token not bound to email  
3. H2: role escalation via `role=admin` mass assignment  
4. H3: list invites across orgs via IDOR  
5. Test H2 first (often highest EV on SaaS)  

## Pro tip

Write hypotheses **before** opening Burp’s active scan. Scanning is for residual coverage after thinking.

## FR

Une hypothèse est une affirmation **falsifiable** sur un comportement sous une frontière de confiance. Classer par espérance de valeur. Tuer vite les pistes mortes. Documenter le cimetière d’hypothèses.
