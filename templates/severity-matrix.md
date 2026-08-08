# Privilege / AuthZ Matrix Template

| Endpoint / Action | Anon | User | User (other’s object) | Admin | Notes |
|-------------------|------|------|----------------------|-------|-------|
| GET /api/me | | | | | |
| GET /api/items/{id} | | | | | |
| PUT /api/items/{id} | | | | | |
| DELETE /api/items/{id} | | | | | |
| POST /api/admin/... | | | | | |
| Export job download | | | | | |

**Legend:** `Y` allow expected · `N` deny expected · `?` untested · `BUG` actual unexpected allow

## Test log

| Cell | Result | Evidence |
|------|--------|----------|
| | | |
