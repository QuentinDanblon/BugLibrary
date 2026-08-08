# Mobile Hunting Methodology

<!-- updated: 2026-03 -->

## Reality check

Most “mobile bugs” that pay are **API authZ bugs** discovered via mobile clients. Local storage issues matter when they store secrets or enable easy ATO.

## Path

1. Confirm app is in scope  
2. Static map: endpoints, keys, feature flags  
3. Dynamic traffic through proxy (if allowed)  
4. AuthZ testing on revealed APIs  
5. Local storage / WebView / deep links  
6. Report with device context + API proof  

## Platform notes

| Platform | High-signal areas |
|----------|-------------------|
| Android | Exported components, WebView, deep links, backup flags |
| iOS | Keychain usage, ATS exceptions, URL schemes, WebViews |

## Certificate pinning

- Many programs allow bypass on **your** test device for traffic analysis  
- Document method at high level; do not distribute cracked apps  
- If pinning bypass is out of policy, use official debug builds if provided  

## FR

Le mobile sert surtout à **révéler l’API**. Static map → traffic → authZ. Pinning : selon policy, sur votre device de test.
