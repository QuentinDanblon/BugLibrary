# Recon Philosophy / Philosophie de recon

<!-- updated: 2026-03 -->

## English

Recon exists to **feed hypotheses**, not to fill disk with subdomains.

### Hierarchy of value

1. **Authenticated application map** (what logged-in users can reach)  
2. **API surface** (objects, verbs, IDs)  
3. **Admin / internal-ish hosts still in scope**  
4. **Mobile/BFF endpoints**  
5. **Passive DNS & certificate history**  
6. **Raw brute wordlists** (lowest signal alone)  

### Passive before active

| Phase | Actions | Risk |
|-------|---------|------|
| Passive | CT logs, archives, public repos, job posts, mobile store metadata | Low |
| Soft active | Careful DNS, careful HTTP to in-scope, robots/sitemap | Medium |
| Active | Content discovery, authenticated spidering | Higher — budget it |

### Signal metrics

Track: % of assets that led to a hypothesis; % of requests with a labeled purpose.  
If you cannot name the purpose, do not send the request.

### Pro tip

“**Interesting**” is not a finding. Convert every recon note into either a hypothesis ID or a kill reason.

---

## Français

La recon nourrit des **hypothèses**, elle ne remplit pas un disque. Priorité : carte authentifiée > API > hosts admin in-scope > mobile > passif DNS > brute force aveugle. Mesurer le signal. Chaque note → hypothèse ou raison de kill.
