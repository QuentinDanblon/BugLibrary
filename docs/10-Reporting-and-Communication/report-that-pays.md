# Reports That Pay

<!-- updated: 2026-03 -->

## English

Triage has minutes, not hours. Optimize for **fast correct understanding**.

### Ideal structure

1. **Title** — type + object + impact hint  
2. **Summary** — 3–5 lines: who can do what to whom  
3. **Severity rationale** — program scale language  
4. **Steps to reproduce** — numbered, copy-pasteable, dual accounts if authZ  
5. **Evidence** — redacted screenshots, response snippets  
6. **Impact** — business worst reasonable case  
7. **Remediation** — concrete fix direction  
8. **Appendix** — HTTP requests (sanitized)  

### Title examples

| Weak | Strong |
|------|--------|
| IDOR on API | BOLA: any user can read other users’ invoices via `GET /api/invoices/{id}` |
| XSS | Stored XSS in project description leads to session takeover of org admins |

### Reproduction quality bar

- Fresh private window steps  
- Exact roles/accounts labeled `Attacker` / `Victim`  
- No “click around until”  
- Include expected vs actual  

### Attachments

- Prefer text requests over opaque videos when possible  
- Videos for multi-step UI only  
- Never attach live session tokens  

### Use the template

→ [`../../templates/bug-report-template.md`](../../templates/bug-report-template.md)

## FR

Titre précis, résumé qui/quoi/à qui, steps dual-compte, impact business, remediation claire, tokens absents des pièces jointes.
