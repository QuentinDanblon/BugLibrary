# API Versioning & Legacy Seams

## Why seams pay

New GraphQL with old REST; `/v2` with leftover `/v1`; mobile pin to old host.

## Checklist

- [ ] Enumerate version prefixes and hosts  
- [ ] Replay modern tokens against legacy  
- [ ] Compare authZ middleware parity  
- [ ] Deprecated fields still writable  
- [ ] Old docs still accurate (often more verbose)  

## Pro tip

Store mobile traffic from **previous APK/IPA versions** when legal — old clients keep old APIs alive.

## FR

Les coutures v1/v2 et mobile legacy sont des mines d’authZ incomplète.
