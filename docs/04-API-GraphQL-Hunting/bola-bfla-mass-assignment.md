# BOLA, BFLA & Mass Assignment

## BOLA (Object Level)

Same as IDOR for APIs. Prioritize:

- `/users/{id}`, `/orders/{id}`, `/files/{id}`  
- Nested: `/orgs/{oid}/projects/{pid}`  
- RPC-style: `{"method":"GetInvoice","id":"..."}`  

### Amplifiers

| Amplifier | Effect |
|-----------|--------|
| Predictable IDs | Enumeration |
| Search without authZ | Bulk leak |
| Exports | Bulk leak |
| Webhooks signed with user-controlled URL | Secondary impact |

## BFLA (Function Level)

Can a lower role invoke admin functions?

- Verb changes: `DELETE` vs `GET`  
- Path variants: `/admin/` vs feature flags  
- GraphQL mutations reserved for staff  
- Internal headers (`X-Original-Role`) trusted by gateway  

## Mass assignment / excessive data exposure

**Write:** extra fields in JSON (`role`, `balance`, `verified`, `tenant_id`)  
**Read:** API returns fields UI never shows (hashes, internal flags, other users’ PII)

### Test method

1. Capture legit create/update body  
2. Add privileged fields one by one  
3. Re-fetch object; confirm server accepted  
4. Document security model violation  

## Excessive data exposure report framing

Show **specific sensitive fields** and who should not see them. Diff “intended public profile” vs raw API JSON.

## FR

BOLA = ID objet. BFLA = fonction admin. Mass assignment = champs fantômes. Excessive exposure = JSON trop bavard. Preuves un champ à la fois.
