# Recon Template / Template de reconnaissance

**Program:**  
**Date:**  
**Hunter / Agent run ID:**  
**Policy version / URL:**  

---

## Scope pack

### In scope

| Asset | Type | Notes |
|-------|------|-------|
| | domain / app / IP | |

### Out of scope / exclusions

| Asset | Reason |
|-------|--------|
| | |

### Rate & automation rules

```
max_rps:
automation_allowed:
special_notes:
```

---

## Identity matrix

| Account label | Role | Org/Tenant | MFA | Notes |
|---------------|------|------------|-----|-------|
| Attacker-A | | | | |
| Victim-B | | | | |
| LowPriv-C | | | | |

---

## Asset inventory (ASM)

| ID | Host/App | Auth | Stack notes | Last seen | Status (in/unclear/out) |
|----|----------|------|-------------|-----------|-------------------------|
| | | | | | |

---

## Trust boundaries

| From | To | Risk theme |
|------|-----|------------|
| user | user | horizontal |
| member | admin | vertical |
| tenant1 | tenant2 | isolation |

---

## Entry points (sample)

| Method | Path / Operation | Auth | Object IDs | Notes |
|--------|------------------|------|------------|-------|
| | | | | |

---

## Tech fingerprint

- Auth schemes:  
- API styles:  
- WAF/CDN:  
- Mobile apps:  
- Interesting headers:  

---

## Deltas since last session

| Change | Source | Hypothesis IDs |
|--------|--------|----------------|
| | | |

---

## Hypothesis backlog (top)

| ID | Claim | EV 1–5 | Status |
|----|-------|--------|--------|
| H- | | | open |

---

## Noise / do-not-repeat

-  

---

## OPSEC notes

- IP/profile used:  
- Rate incidents:  
- Blocks:  

---

## Sign-off

- [ ] No unclear assets tested  
- [ ] Budgets respected  
- [ ] Secrets not stored in plain git  
