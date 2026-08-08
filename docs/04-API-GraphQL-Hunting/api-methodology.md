# API Hunting Methodology

<!-- updated: 2026-03 -->

## Why APIs dominate modern BB

UI is a partial client. Mobile, integrations, and partner APIs expose **full object models**.

## Workflow

1. Collect traffic from web + mobile + official docs  
2. Build OpenAPI-like mental model (resources, IDs, verbs)  
3. AuthZ matrix on every resource  
4. Mass assignment on create/update  
5. Pagination/filter/search edge oracles  
6. Batch & async job endpoints  
7. Webhooks & callbacks  

## Request anatomy checklist

```text
Method + path
Auth (cookie/bearer/key)
Object IDs (path/query/body/headers)
Tenant IDs
Idempotency keys
Content-Type variants
API version headers
```

## Content-Type & parser differentials

- JSON vs form vs multipart  
- Duplicate keys / JSON pollution classes  
- HTTP parameter pollution on gateways  

## Pro tip

If web UI hides a field, **API often still accepts it**. That is the mass-assignment motherlode.

## FR

L’API est le vrai produit. Matrice authZ, mass assignment, jobs async, webhooks. Si le champ est absent de l’UI, tester l’API.
