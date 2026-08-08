# Pattern: Cross-Tenant BOLA

## Story (fictional composite)

SaaS “OrgNotes” isolates notes per organization. `GET /api/notes/{noteId}` authorized only by session login, not by org membership check.

## Why it existed

- Note IDs global UUID → false sense of security  
- Middleware checked `isAuthenticated` only  
- UI never linked cross-org so QA missed it  

## Discovery path

1. Two orgs, two users  
2. Create note in Org B  
3. As Org A user, request B’s `noteId`  
4. 200 + content  

## Impact framing

Cross-tenant confidentiality break — often Critical/High depending on data.

## Fix direction

Server-side authZ: `note.org_id == session.org_id` (or membership). Centralize policy.

## Lessons

- UUID ≠ authZ  
- Always dual-tenant accounts  
- Test API directly, not only UI  

## FR

UUID rassurant mais insuffisant. Deux tenants obligatoires. AuthZ serveur centralisée.
