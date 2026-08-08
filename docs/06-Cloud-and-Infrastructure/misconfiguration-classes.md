# Cloud Misconfiguration Classes

## Storage

| Issue class | Impact framing |
|-------------|----------------|
| Public read of sensitive objects | Data breach potential |
| Public write | Integrity / malware hosting on their domain |
| Predictable object keys + weak auth | Enumeration |
| Signed URL flaws | Overlong expiry, scope too broad |

## Identity-adjacent (app level)

- Overprivileged API keys in mobile/web  
- CI secrets in public repos of the org (if in scope)  
- Federation/SSO misbind  

## Messaging & functions

- Unauthenticated function URLs  
- Queue/HTTP triggers without auth  

## Report quality

Include: resource identifier (redact if needed), how you found it **without** attacking unrelated tenants, data classification sample (minimized).

## FR

Storage public, URLs signées, clés surprivilegiées, fonctions sans auth. Preuve minimaliste, pas d’exfil massive.
