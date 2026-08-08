# File Upload & SSRF Classes

## Upload checklist

- [ ] Type validation: extension vs content vs MIME  
- [ ] Path/name control  
- [ ] Overwrite / traversal classes  
- [ ] AuthZ on download URLs  
- [ ] Processing pipeline (image magick, antivirus, transcode) — injection into processors  
- [ ] XSS via served content-type  

Upload bugs often become **stored XSS** or **RCE-class** only on specific stacks — report truthfully.

## SSRF classes (high value when in scope)

| Sink type | Examples |
|-----------|----------|
| URL fetch | webhooks, link unfurl, import-from-URL |
| Document converters | HTML/PDF fetch resources |
| Cloud metadata | Only relevant if infrastructure allows; many clouds block IMDS — still report carefully if reachable |
| Internal ports | Scan gently if allowed; avoid aggressive port storms |

### Safe SSRF proof pattern

1. Prove server requests an endpoint **you control** (collaborator / interact)  
2. Show impact path without harming third parties  
3. If internal access claimed, use **minimal** non-destructive evidence  

## Out of scope traps

- Attacking random third-party websites via the target’s fetcher  
- Using SSRF to mine crypto or spam  

## FR

Uploads : validation, authZ download, pipelines. SSRF : webhooks, unfurl, import URL. Preuve via endpoint contrôlé. Pas d’abus tiers.
