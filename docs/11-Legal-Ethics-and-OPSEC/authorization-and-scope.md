# Authorization & Scope Mastery

<!-- updated: 2026-03 -->

## English

### Hierarchy of truth

1. Local law  
2. Written program policy / RoE  
3. Platform terms  
4. Your assumptions ← **never highest**  

### Scope parsing checklist

- [ ] In-scope assets listed  
- [ ] Explicit out-of-scope  
- [ ] Wildcards interpreted carefully  
- [ ] Third-party services policy  
- [ ] Rate limits / automation rules  
- [ ] Credential rules / no DoS / no spam  
- [ ] Data exfil limits  
- [ ] Safe harbor conditions  
- [ ] Reward eligibility (duplicates, known issues)  

### Grey areas

If asset ownership unclear: **do not test**. Ask via platform support or mark as question in report only if passive finding.

### Multi-program collisions

Same asset on two programs: follow both policies; stricter wins.

## FR

Loi > policy écrite > ToS plateforme > hypothèses. Zone grise = ne pas tester. Le plus strict gagne.
