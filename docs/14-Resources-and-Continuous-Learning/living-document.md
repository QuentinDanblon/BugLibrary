# Living Document — Maintenance

<!-- updated: 2026-03 -->

## English

BugLibrary is a **living document**: intentionally never “finished.” Security practice drifts; stale advice harms hunters.

### Maintenance principles

1. **Date major technique pages** with `<!-- updated: YYYY-MM -->`  
2. **Prefer PRs over silent rewrites** — reviewable history  
3. **Deprecate explicitly** — don’t leave contradictory pages  
4. **Signal > completeness** — delete low-value fluff  
5. **Safety review** on every offensive-leaning change  

### Cadence (recommended)

| Cadence | Action |
|---------|--------|
| Weekly | Personal notes → candidate PRs |
| Monthly | Section owners skim for staleness |
| Quarterly | AI agents doc + tooling categories refresh |
| On incident | Emergency ethics/OPSEC notes |

### Change types

| Type | Example |
|------|---------|
| Additive | New checklist item for GraphQL subscriptions |
| Corrective | IMDS guidance updated for provider hardening |
| Deprecation | Remove obsolete tool flag advice |
| Structural | Split oversized page |

### Review checklist for maintainers

- [ ] Still authorized-testing framed?  
- [ ] Any weaponized payload introduced? → reject  
- [ ] Cross-links valid?  
- [ ] FR/EN parity for user-facing major guides?  
- [ ] Update root README index if structure changed  

### Ownership model

- Default: repository maintainers  
- Community: PRs per CONTRIBUTING  
- AI-generated PRs must be human-reviewed end-to-end  

### Metrics of health

- Days since last meaningful docs commit  
- Open “stale” issues count  
- Hunter feedback: “I used X and it failed because…”  

## Français

Document vivant : dater, PR, déprécier explicitement, sécurité d’abord. Cadence hebdo/mensuelle/trimestrielle. Toute contribution IA relue par un humain.

### Processus de contribution au living document

1. Ouvrir une issue “stale: <page>”  
2. PR avec justification  
3. Checklist maintainer  
4. Merge + note dans changelog personnel optionnel  

---

**If you only maintain one habit: update the pages you actually hunt with.**
