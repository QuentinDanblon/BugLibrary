# Content & Endpoint Discovery

## Authenticated > unauthenticated

On modern apps, **most value is behind login**. Spider with test accounts; map multi-role differences.

## JavaScript & SPA archaeology

1. Download main bundles for in-scope apps  
2. Extract route tables, feature flags, API base URLs, hidden admin paths  
3. Diff bundles across versions (store hashes)  
4. Hunt for hardcoded keys **only to report exposure** — do not abuse third-party quotas  

### Patterns that pay

- `/internal/`, `/staff/`, `/impersonate`, `/export`  
- GraphQL paths beyond `/graphql` (`/api/gql`, versioned)  
- Forgotten REST next to new GraphQL  

## Wordlists (disciplined use)

- Custom lists from the app’s own language (entity names from UI)  
- Avoid megabyte generic lists at full concurrency — OPSEC + ban risk  
- Time-box; stop when entropy of new finds drops  

## API schema sources

- OpenAPI/Swagger if exposed (report exposure if sensitive)  
- GraphQL introspection (if enabled — often intentional on some APIs; judge impact)  
- Mobile apps and browser HAR of normal use (best source)  

## Parameter mining

From traffic:

- Body fields not in UI  
- Hidden headers (`X-Org-Id`, `X-User-Id`, `X-Account-Id`)  
- Batch endpoints (`/batch`, `/bulk`, GraphQL multi-query)  

## Pro tip

Build an **endpoint × role** matrix early. That single artifact drives BOLA/BFLA testing.

## FR

Découverte authentifiée prioritaire. Archéologie JS. Wordlists custom et time-boxées. Matrice endpoint × rôle = artefact d’or.
