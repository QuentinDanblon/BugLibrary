# Authorization Checklist

## Horizontal

- [ ] Swap object IDs between same-role users
- [ ] List endpoints filter bypass
- [ ] Search returns other users’ objects
- [ ] Export/print/PDF siblings
- [ ] Async job status/result IDs
- [ ] WebSocket/channel subscriptions
- [ ] GraphQL `node(id:)` / aliases

## Vertical

- [ ] Admin routes as user
- [ ] Mass-assign role/plan/permissions
- [ ] Feature-flag forced client-side only
- [ ] Impersonation endpoints
- [ ] Staff GraphQL mutations

## Tenant

- [ ] Cross-tenant read/write
- [ ] Tenant ID in body trusted blindly
- [ ] Shared resources leakage

## FR

Horizontal, vertical, tenant — siblings export/jobs/GraphQL inclus.
