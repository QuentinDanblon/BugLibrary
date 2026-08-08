# Recon OPSEC

## Goals

1. Stay within rate and legal bounds  
2. Avoid accidental account locks / WAF bans that burn time  
3. Separate personal identity from research identity when appropriate  
4. Never leak your recon data publicly with private details  

## Practical controls

| Control | Practice |
|---------|----------|
| Rate | Self-imposed RPS caps; backoff on 429 |
| Identity | Dedicated research browser profile / VMs |
| Credentials | Unique passwords; no password reuse with personal |
| Storage | Encrypt notes; no client data in public git |
| Collaboration | Share scope-redacted notes only |
| Cloud egress | Know what your IP reputation looks like |

## Noise anti-patterns

- Full port scans on BB web programs (often useless + noisy)  
- Megathread fuzzing login with 100k passwords (banned + useless)  
- Hitting out-of-scope third parties “because linked”  

## If you get blocked

1. Stop  
2. Review policy for guidance  
3. Reduce concurrency; switch to authenticated logic testing  
4. Do not play cat-and-mouse with WAF evasions as a goal  

## FR

Budgets de rate, identité de recherche dédiée, pas de fuites de notes, pas de brute force massif. Blocage → ralentir, pas “bypasser le WAF pour le sport”.
