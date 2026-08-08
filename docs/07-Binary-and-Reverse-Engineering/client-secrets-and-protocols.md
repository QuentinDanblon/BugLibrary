# Client Secrets & Custom Protocols

## Secret classes

| Finding | Typical severity driver |
|---------|-------------------------|
| Third-party API key in binary | Key privileges + abuse potential |
| Shared HMAC for all clients | Forgery of requests |
| Private keys | Critical if production |
| Obfuscated but identical crypto | Show practical forgery |

## Protocol analysis tips

- Diff legit vs modified messages  
- Check whether server re-validates client assertions  
- Replay, reorder, privilege fields  

## FR

Clés embarquées : juger par privilège. Protocoles : le serveur revalide-t-il ? Forgery pratique > obfuscation contournée.
