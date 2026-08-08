# Race Conditions

<!-- updated: 2026-03 -->

## Where races hide

- Coupon redeem, referral bonuses  
- Inventory / seat limits  
- “Use once” tokens  
- Balance transfers  
- Like/vote uniqueness  
- Parallel invite accepts  

## Method

1. Identify **limit or single-use** invariant  
2. Capture legitimate request  
3. Fire N parallel requests (start small: 5–20)  
4. Observe invariant break  
5. Increase only if needed and safe  

## Tooling note

Use concurrent request features in proxies or simple async scripts **you write for your accounts**. Do not publish stress-test malware.

## Limit-overrun reporting

Show financial or integrity impact with timestamps and IDs.

## FR

Invariants “une seule fois” / limites. Paralléliser doucement sur **vos** comptes. Prouver la rupture d’invariant.
