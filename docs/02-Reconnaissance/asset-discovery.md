# Asset Discovery

## Inputs

- Program scope list (domains, apps, CIDRs if any, wildcards)  
- Explicit exclusions and third-party notes  
- Brand names, legal entities, acquisitions  

## Techniques (authorized, in-scope framing)

### DNS & certificate transparency

- Collect names from CT logs for in-scope roots  
- Resolve carefully; record CNAMEs (SaaS vs origin)  
- Flag third-party CNAMEs as **often out of scope** unless listed  

### Historical & OSINT

- Public archives of in-scope hosts (respect robots/ToS of sources)  
- Engineering blogs, status pages, changelogs  
- Mobile package names → API hosts in config (see Mobile section)  
- GitHub/org search for **public** leaks of endpoints (never use leaked secrets to access systems)  

### Acquisitions & brand expansion

Elite edge: acquired products keep separate auth and weaker isolation.

Checklist:

- [ ] Recent M&A press → new host patterns  
- [ ] Job postings mentioning internal tools names  
- [ ] Parallel product lines under same wildcard  

### Cloud storage & public buckets (class)

Only test assets clearly in scope. Look for **naming patterns** tied to the program’s disclosed cloud presence — do not mass-scan the entire cloud provider.

## Output quality bar

Each asset record:

```text
host | in-scope? | owner guess | auth surface | notes | last_seen
```

## Pro tips

- Prefer **origin** over CDN edge when both in scope — logic lives at origin  
- Staging names in prod wildcards are high EV **if in scope**  
- Screenshot marketing sites; spend time on apps with login  

## FR

Découverte = inventaire **scopé**. CT + OSINT + acquisitions. CNAME tiers souvent hors scope. Chaque asset : statut scope, surface auth, last_seen.
