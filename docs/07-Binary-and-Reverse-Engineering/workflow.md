# RE Workflow (BB)

1. **Scope confirm** for the binary  
2. **Inventory** strings, imports, URLs  
3. **Map** update, license, auth, network  
4. **Dynamic** on isolated lab VM  
5. **Hypotheses** about server trust of client  
6. **Validate on server side** — client-only checks are often accepted only with server impact  
7. **Report** with clear server-side impact  

## Lab hygiene

- Snapshots  
- No production credentials  
- No distribution of patched malware-like samples  

## FR

Inventaire → map auth/réseau → dynamique en lab → impact **côté serveur** pour le payout.
