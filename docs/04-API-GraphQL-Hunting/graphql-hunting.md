# GraphQL Hunting

<!-- updated: 2026-03 -->

## Surface discovery

- Common paths: `/graphql`, `/api/graphql`, `/gql`, `/v1/graphql`  
- Method: usually POST; sometimes GET  
- Batch: array of operations  
- Persisted queries / APQ  

## Introspection

If enabled, map types/mutations. Impact of introspection alone is often **low** — use it as a map, not a trophy unless policy values it.

## AuthZ on GraphQL

| Risk | Test |
|------|------|
| Field-level authZ missing | Request sensitive fields as low priv |
| Node interface IDOR | `node(id:)` global IDs |
| Nested resolvers | Parent authorized, child not checked |
| Mutations | Horizontal/vertical like REST |
| Subscriptions | Channel authZ |

## Query complexity & batching

- Nested depth / alias flooding — **careful**: may be DoS; many programs ban pure DoS  
- Prefer **authZ impact** over resource exhaustion reports unless explicitly rewarded  

## Suggestions / errors as oracles

Verbose errors and `extensions` can leak field existence or internal traces — report as info disclosure with concrete risk.

## Checklist

- [ ] Map mutations with write impact  
- [ ] Test IDOR on global IDs  
- [ ] Cross-tenant on org-scoped types  
- [ ] Batch mixed auth operations  
- [ ] File upload mutations  
- [ ] Admin-only types reachable  

## Pro tip

GraphQL **aliases** can sometimes bypass naive per-operation rate limits — use gently and only to demonstrate authZ issues, not to melt APIs.

## FR

Introspection = carte, pas trophy. AuthZ par champ et par `node(id)`. Éviter DoS pur. Nested resolvers = bugs fréquents.
