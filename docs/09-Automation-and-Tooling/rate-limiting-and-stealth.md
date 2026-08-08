# Rate Limiting & Detection Avoidance (Ethical)

## Goal

Stay effective and polite — **not** “become invisible to commit crimes”.

## Controls

| Control | Guidance |
|---------|----------|
| RPS/concurrency | Start low; honor 429/`Retry-After` |
| Jitter | Avoid perfect bots when not needed |
| Time windows | Business hours for heavy authenticated tests if policy prefers |
| Account health | Stop on CAPTCHA storms / lock warnings |
| Fingerprints | Dedicated research profiles; don’t burn personal bank logins |

## What not to do

- WAF evasion as sport  
- Distributed residential proxy attacks on BB targets  
- Intentional log flooding  

## FR

Politesse opérationnelle : bas RPS, respect 429, comptes sains. Pas de réseaux de proxies pour “bypass WAF”.
