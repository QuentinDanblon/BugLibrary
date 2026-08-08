# Impact Writing

## Formula

```text
Actor with privilege P can action A on asset X belonging to victim V
resulting in consequence C at scale S.
```

## Consequence ladder (examples)

| Technical | Business translation |
|-----------|----------------------|
| Read invoice IDOR | Exposure of customer financial PII; regulatory risk |
| Admin mass assignment | Full tenant takeover; integrity loss |
| SSRF to internal | Potential access to internal admin; data breach path |
| Race double redeem | Direct financial loss per exploit |

## Avoid

- Sci-fi impact without path  
- “Could be used by nation states” filler  
- CVSS-only arguments when program uses custom tables  

## FR

Acteur + privilège + action + victime + conséquence + échelle. Traduire en risque business. Éviter la science-fiction.
