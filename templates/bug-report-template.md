# Bug Report Template / Template de rapport

> Maximize triage speed and payout clarity. Redact secrets. Authorized programs only.  
> Maximiser la vitesse de triage et la clarté d’impact. Rédiger les secrets.

---

## Title / Titre

```
[TYPE] <short object> — <impact hint>
```

**Example:** `[BOLA] Invoice PDF API — any authenticated user can read other users’ invoices`

---

## Summary / Résumé

<!-- 3–5 lines: who can do what to whom -->

- **Actor:**  
- **Action:**  
- **Victim asset:**  
- **Result:**  

---

## Severity rationale / Justification de sévérité

| Factor | Assessment |
|--------|------------|
| Confidentiality | |
| Integrity | |
| Availability | |
| Privileges required | |
| User interaction | |
| Scope (single user / tenant / system) | |
| Program scale mapping | |

---

## Affected assets / Assets affectés

| Asset | Environment | In-scope ref |
|-------|-------------|--------------|
| | Production / … | Policy line / URL |

---

## Preconditions / Prérequis

- Accounts: `Attacker` (role …), `Victim` (role …)  
- Feature flags / plan tier:  
- Other:  

---

## Steps to reproduce / Étapes de reproduction

1.  
2.  
3.  
4.  

**Expected:**  
**Actual:**  

---

## Proof of Concept / Preuve de concept

### HTTP (sanitized)

```http
GET /api/example HTTP/1.1
Host: in-scope.example
Authorization: Bearer <REDACTED>
```

### Response (sanitized excerpt)

```http
HTTP/1.1 200 OK
...
```

### Screenshots

<!-- attach; blur tokens -->

---

## Impact / Impact

Business-oriented paragraph: data types, cross-user/tenant, financial, regulatory, abuse scenario at reasonable scale.

---

## Remediation / Remédiation

1. Enforce server-side authorization on object/function  
2. Add regression tests for dual-account access  
3. Audit sibling endpoints (export, preview, jobs)  
4. …  

---

## Related endpoints / Endpoints liés

| Method | Path | Notes |
|--------|------|-------|
| | | |

---

## Timeline / Chronologie (optional)

| Date | Event |
|------|-------|
| | Discovered |
| | Reported |

---

## Notes for triage

- Data minimized: yes/no  
- Duplicate search performed: yes/no  
- Contact preference:  

---

### Reporter checklist before submit

- [ ] Scope confirmed  
- [ ] Tokens redacted  
- [ ] Dual-account clear for authZ  
- [ ] Impact not inflated  
- [ ] Steps cold-repro OK  
