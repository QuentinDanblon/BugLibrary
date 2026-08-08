# Client-Side & SPA Hunting

## Focus areas

| Area | Classes |
|------|---------|
| `postMessage` | Origin checks missing/weak |
| DOM sinks | `innerHTML`, `eval`-like patterns in bundles |
| Open redirect | OAuth, magic links, `next=` params |
| Prototype pollution | Client gadgets → XSS/gadget chains (advanced) |
| Local storage tokens | XSS impact amplifier |
| Service workers | Cache poisoning classes (rare, careful) |
| WebSockets | AuthZ on subscribe channels |

## postMessage checklist

- [ ] Listener exists  
- [ ] `event.origin` allowlist strict  
- [ ] Data validated before DOM/sink use  
- [ ] Opener/`window.name` flows reviewed  

## SPA routing

Client-only route guards are **not** security — always retest API.

## Pro tip

When you find XSS in a mature SPA, immediately map **token storage** and **powerful postMessage** handlers for impact upgrade.

## FR

postMessage, sinks DOM, redirects, tokens en storage, WebSocket authZ. Les guards de routes SPA ne sont pas une authZ serveur.
