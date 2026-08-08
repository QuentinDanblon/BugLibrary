# Attack Surface Mapping (ASM)

<!-- updated: 2026-03 -->

## Goal

Produce a **living graph** of in-scope assets, entry points, identities, and trust boundaries — not a raw subdomain dump.

## Layers

| Layer | Examples | Questions |
|-------|----------|-----------|
| **DNS / Host** | apex, wildcards, CDN, third-parties | Who terminates TLS? What is in scope? |
| **Application** | web apps, SPAs, mobile BFF, admin | Auth model? Tenancy? |
| **API** | REST, GraphQL, gRPC-web, webhooks | Object IDs? Versioning? |
| **Identity** | SSO, OAuth, magic links, API keys | Token lifetime? Binding? |
| **Data** | exports, uploads, search, logs | PII? Cross-tenant paths? |
| **Automation edges** | CI hooks, email, SMS, queue workers | SSRF/injection into processors? |
| **Cloud-adjacent** | storage URLs, metadata (if in scope) | Misconfig classes? |

## Minimal ASM artifact

```yaml
program: example-bb
updated: 2026-03-01
assets:
  - id: web-app
    hosts: [app.example.com]
    auth: session+cookie
    roles: [user, admin]
    notes: multi-tenant org model
  - id: api
    hosts: [api.example.com]
    style: REST+JSON
    auth: Bearer JWT
entry_points:
  - method: GET
    path: /api/v1/orgs/{orgId}/members
    authz: org member
trust_boundaries:
  - from: userA
    to: userB
    risk: horizontal IDOR
  - from: member
    to: admin
    risk: vertical privilege
out_of_scope_reminders:
  - "*.marketing-cdn.example"
  - third-party Zendesk
```

## Process (repeatable)

1. **Ingest scope** — domains, apps, wildcards, exclusions  
2. **Enumerate carefully** — respect rate limits; prefer passive first  
3. **Fingerprint** — stacks, WAF, auth schemes  
4. **Build identity matrix** — accounts you can legally create  
5. **Map sensitive actions** — money, admin, export, delete, invite  
6. **Diff** — weekly ASM delta is where fresh bugs live  
7. **Feed hypotheses** — each new edge → ≥1 hypothesis  

## Differential recon (2024–2026 essential)

Elite hunters win on **delta**, not first-day dump:

- New subdomains / hosts  
- New JS routes and GraphQL types  
- New mobile app versions → new API  
- Acquisitions folded into wildcard  

## Pro tips

- Tag every asset: `in-scope | unclear | out` — never test `unclear`  
- Third-party SaaS linked from the product is often **out** unless listed  
- Store ASM in your notes system; the repo `templates/recon-template.md` is the scaffold  

## FR

L’ASM n’est pas une liste de sous-domaines : c’est un **graphe de confiance**. Prioriser les deltas. Chaque nouvelle arête génère des hypothèses. Ne jamais tester un asset `unclear`.
