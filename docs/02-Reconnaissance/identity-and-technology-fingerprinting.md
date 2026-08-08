# Identity & Technology Fingerprinting

## Auth scheme inventory

| Scheme | Look for | Hypotheses seed |
|--------|----------|-----------------|
| Session cookies | flags, fixation, CSRF pairing | session issues, CSRF |
| JWT (SPA) | alg, kid, claims, storage | claim tampering classes, XSS→token |
| OAuth/OIDC | redirect_uri, state, PKCE | redirect, token leak |
| API keys | header vs query, rotation | leakage, overbroad key |
| mTLS / device | mobile pinning | bypass only if in scope & allowed |
| Magic links | token entropy, bind to purpose | token reuse, fixation |

## Stack notes (why they matter)

| Observation | Hunting implication |
|-------------|---------------------|
| Multi-tenant SaaS | Cross-tenant IDOR priority |
| GraphQL gateway | Batching, field authZ, deferred |
| Serverless APIs | Inconsistent auth middleware |
| Legacy + new | AuthZ gaps at seams |
| WAF present | Soften rate; logic bugs still exist |

## Header & behavior fingerprint (safe)

Document: server headers, error shapes, rate-limit headers, request-id correlation. Use for **mapping**, not for DoS.

## FR

Inventorier schémas d’auth et en dériver des classes d’hypothèses. Les coutures legacy/new et multi-tenant sont prioritaires.
