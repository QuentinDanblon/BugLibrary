# Injection & XSS (Modern Framing)

## Principles

- Prefer **sink-driven** testing over blind payload spam  
- Understand context (HTML, attr, JS, URL, SQL, LDAP, template)  
- Many programs want **impact** (session, data) not alert(1) alone  

## XSS classes still relevant

| Class | Notes |
|-------|-------|
| Reflected | Filters, encoding, CSP |
| Stored | Multi-user impact higher |
| DOM | `postMessage`, `location`, client routers |
| Mutation / mXSS | Sanitizer edge cases |
| PDF/HTML exporters | Server render sinks |

### CSP & modern mitigations

Document CSP presence honestly. Bypass research is advanced; do not claim critical without workable impact under real CSP.

## Server-side injection classes

| Class | When to prioritize |
|-------|--------------------|
| SQL/NoSQL | Search, filters, sort params, raw report builders |
| Command | Rare in pure SaaS; file converters, admin tools |
| SSTI | Email templates, PDF names, error pages |
| LDAP | Enterprise SSO-adjacent apps |
| Header injection | CrLF → cache/response splitting (rare modern) |

## Testing hygiene

- Use canary strings unique to you  
- Avoid destructive payloads (`DROP`, fork bombs)  
- For SQLi: prefer boolean/time only when necessary and gentle  

## Pro tip

**Export/render pipelines** (HTML→PDF, markdown→email) are higher EV than homepage search boxes on mature targets.

## FR

Tester par sinks, pas par spam. XSS avec impact réel. Injections serveur ciblées (search, export, templates). Payloads non destructifs.
