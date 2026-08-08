# Access Control & IDOR / BOLA

<!-- updated: 2026-03 -->

## Mental model

Every request that includes an **object identifier** is a potential BOLA until proven otherwise.

Identifiers: numeric IDs, UUIDs, slugs, emails, filenames, share tokens, job IDs, invoice numbers.

## Test matrix (minimum)

| Actor | Action | Object owner | Expected |
|-------|--------|--------------|----------|
| userA | read | userB object | deny |
| userA | update | userB object | deny |
| userA | delete | userB object | deny |
| userA | list | filter bypass | only A |
| member | admin action | org | deny |
| tenant1 | read | tenant2 | deny |

## Methodology

1. Capture a legitimate request with ID  
2. Swap ID to another you own (control)  
3. Swap to victim-owned ID (same role)  
4. Retry with lower privilege session  
5. Retry with alternate API version / mobile endpoint  
6. Retry on **export, preview, thumbnail, pdf, websocket** siblings  

## Hidden siblings (elite)

| Primary | Sibling often weaker |
|---------|----------------------|
| `GET /items/{id}` | `GET /items/{id}/export` |
| REST detail | GraphQL node query |
| JSON API | CSV report job |
| App domain | Legacy `api-v1` host |
| Direct object | Search that returns full objects |

## Vertical privilege

- Parameter pollution: `role`, `isAdmin`, `plan`, `permissions[]`  
- Hidden admin routes found in JS  
- Feature flags forced client-side only  

## Impact framing for reports

Not “IDOR on endpoint X” alone — state:

- Data classification (PII, secrets, financial)  
- Cross-user vs cross-tenant  
- Write vs read  
- Scalability (mass enumeration practical?)  

## Pro tips

- UUID does **not** mean safe — authZ still required  
- Batch endpoints multiply impact  
- Change **one variable at a time** for clean repro  

## FR

Tout ID d’objet = BOLA potentiel. Matrice multi-comptes. Tester les siblings export/GraphQL/legacy. Impact = type de données + croisement tenant + écriture.
