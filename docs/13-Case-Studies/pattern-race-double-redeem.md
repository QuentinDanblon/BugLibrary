# Pattern: Double Redeem Race

## Story (composite)

Promo code “once per account” enforced with read-check-then-write without transaction/lock. Parallel requests both succeed.

## Hunt method

5–20 parallel redeem requests; observe multiple credits.

## Lessons

- Invariants need atomic server enforcement  
- Start low concurrency  
- Financial impact is easy to explain to triage  

## FR

Invariant “une fois” sans atomicité → course. Impact financier clair pour le triage.
