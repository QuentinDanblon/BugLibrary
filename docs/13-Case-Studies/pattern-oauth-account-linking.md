# Pattern: OAuth Account Linking ATO

## Story (composite)

App allows “Login with IdP” and “Link identity” without requiring proof on the already-logged-in victim session under certain race/order conditions — or links by email without verifying ownership on one path.

## Hunt signals

- Multiple identity providers  
- “Connect social” in settings  
- Email change + OAuth order edge cases  

## Impact

Account takeover of victim if attacker can force link.

## Lessons

- Identity linking is authN-critical  
- Every link path needs strong step-up  
- Report with exact order of operations  

## FR

Le linking d’identité = surface ATO. Chaque chemin doit prouver la possession.
