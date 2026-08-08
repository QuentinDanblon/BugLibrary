# Rate Limit & Business Abuse (Non-DoS)

## In-scope abuse cases (often rewarded)

| Case | Example impact |
|------|----------------|
| Auth brute without lockout | Account takeover practicality |
| Coupon / invite farming | Financial loss |
| SMS/email flooding **to your own** sinks | Cost abuse (careful with third parties) |
| Trial / credit abuse | Revenue loss |
| API quota bypass | Cost / fair use |

## Out / risky

- Volumetric DoS  
- Hitting third-party inboxes you do not own  
- “I sent 1M requests” without business impact  

## How to report rate issues

Show **security impact** (ATO practical, bypass MFA spam on your account, financial), not mere missing 429.

## FR

Abus métier ≠ DoS volumétrique. Montrer impact sécurité/financier. Jamais spammer des tiers.
