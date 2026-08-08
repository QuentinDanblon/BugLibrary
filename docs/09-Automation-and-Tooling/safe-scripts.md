# Safe Scripts Policy

Scripts in this repository (`/scripts`) must:

1. Be non-weaponized (no exploit payloads, no shells)  
2. Default to dry-run / local file processing when possible  
3. Require explicit in-scope allowlists for any network I/O  
4. Log actions clearly  
5. Include a header comment: purpose, safety notes  

See examples under `/scripts`.

## FR

Scripts : pas d’exploits, dry-run par défaut, allowlist, logs, en-tête de sécurité.
