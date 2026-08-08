# 05 — Mobile Hunting (Android & iOS)

## Contexte

Le mobile reste une surface sous-testée par rapport au web (barrière d'outillage perçue), donc **moins de duplicates**. La majorité des bugs mobiles à fort payout se trouvent en réalité côté **API backend** consommée par l'app, découverte via interception de trafic mobile.

## Setup d'interception

```
Android :
1. Émulateur (Genymotion/AVD rooté) ou device physique rooté (pour bypass SSL pinning si nécessaire).
2. Proxy Burp/mitmproxy configuré, certificat CA installé dans le store système (pas juste utilisateur, sur Android 7+ les apps ignorent le store utilisateur par défaut).
3. Frida pour bypass SSL pinning : frida-server sur device + script frida-multiple-unpinning.

iOS :
1. Device jailbreaké (ou outil de patch IPA sans jailbreak type "Sideloadly + objection").
2. Burp/mitmproxy + certificat CA installé + trust configuré.
3. Objection ou Frida pour bypass SSL pinning et détection d'anti-debug.
```

```bash
# Bypass SSL pinning générique avec Frida (Android/iOS)
frida -U -f com.target.app -l frida-script-ssl-pinning-bypass.js --no-pause

# Objection (patch d'app + bypass intégré, plus simple à démarrer)
objection -g com.target.app explore
android sslpinning disable
```

> 💡 **Pro tip :** Beaucoup d'apps 2024-2026 utilisent du pinning basé sur des libs custom (OkHttp CertificatePinner, TrustKit) plutôt que le pinning système — les scripts Frida génériques "universal SSL unpinning" doivent souvent être adaptés à la lib spécifique détectée par reverse.

## Reverse Engineering Android (APK)

```bash
# Décompilation
apktool d app.apk -o app_decompiled/
jadx-gui app.apk   # décompilation Java plus lisible pour l'analyse manuelle

# Recherche de secrets/endpoints en dur
grep -rE "(api[_-]?key|secret|token|https?://)" app_decompiled/ --include=*.smali --include=*.xml

# Analyse du manifest pour surface exportée
cat app_decompiled/AndroidManifest.xml | grep -A3 "exported=\"true\""
```

**Signaux à chercher dans le code décompilé :**
- Clés d'API/secrets hardcodés (Firebase, AWS, Stripe, Google Maps).
- Endpoints internes/de debug (`/internal/`, `/debug/`, `api-staging.`).
- Logique de vérification côté client (bypassable) vs. côté serveur (root detection, jailbreak detection, licence/paiement vérifiés uniquement côté client).
- Deep links / Intent filters mal validés (voir ci-dessous).

## Vulnérabilités spécifiques Android

| Vulnérabilité | Description |
|---|---|
| **Exported Components** | `Activity`/`Service`/`BroadcastReceiver`/`ContentProvider` avec `exported="true"` sans permission — accessibles par n'importe quelle app tierce installée |
| **Intent Redirection / Injection** | Une Activity exportée relaie un Intent contrôlé par l'attaquant vers un composant interne sensible |
| **Insecure WebView** | `setJavaScriptEnabled(true)` + `addJavascriptInterface` exposant des méthodes natives à du JS non fiable chargé dans la WebView |
| **Path Traversal via ContentProvider** | ContentProvider exporté acceptant un chemin de fichier non sanitizé |
| **Insecure local storage** | Données sensibles en `SharedPreferences` non chiffrées, ou en clair dans une base SQLite locale accessible (root/backup) |
| **Backup non sécurisé** | `android:allowBackup="true"` permettant l'extraction de données via `adb backup` sur device non rooté |
| **Deep Link Hijacking** | Deep link (`myapp://action?param=`) traité sans validation d'origine → injection de paramètres malveillants (redirection, XSS dans WebView, actions non désirées) |
| **Root/Jailbreak detection bypass** | Souvent contournable avec Frida/Magisk Hide — signal utile mais rarement une vuln primée seule, sauf si elle protège un contrôle de sécurité critique côté client (vérif de paiement, DRM) |

## Vulnérabilités spécifiques iOS

| Vulnérabilité | Description |
|---|---|
| **Insecure Keychain usage** | Données sensibles stockées avec un niveau d'accessibilité trop permissif (`kSecAttrAccessibleAlways`) |
| **URL Scheme Hijacking** | Custom URL scheme non validé, exploitable par une app malveillante enregistrant le même scheme |
| **Universal Links mal validés** | Absence de validation du fichier `apple-app-site-association`, ou logique de traitement du lien vulnérable côté app |
| **Pasteboard leakage** | Données sensibles copiées dans le presse-papiers universel accessible par d'autres apps |
| **Absence d'ATS (App Transport Security) strict** | Exceptions ATS trop larges autorisant du trafic non-TLS ou TLS faible |
| **Local Data Protection insuffisante** | Fichiers stockés sans `NSFileProtectionComplete`, extractibles si device compromis/perdu |

## Focus prioritaire : l'API backend derrière l'app

> 💡 **Pro tip d'élite le plus rentable en mobile :** Passe 80% de ton temps sur l'API backend révélée par l'interception de trafic, pas sur le binaire lui-même. Les apps mobiles exposent très souvent des endpoints **absents de la version web** (endpoints "legacy", "internal", ou pensés "cachés" car non liés dans une UI web) — c'est une extension directe de la surface d'attaque documentée en [`04-API-GraphQL-Hunting`](../04-API-GraphQL-Hunting/README.md) et [`03-Web-Application-Hunting`](../03-Web-Application-Hunting/README.md).

Checklist spécifique à l'API mobile :
- Les contrôles d'autorisation présents côté web sont-ils **répliqués côté mobile** (souvent implémentés en double, avec des oublis) ?
- Le mobile utilise-t-il une version d'API antérieure moins sécurisée pour compatibilité descendante ?
- Les tokens/clés API embarqués dans l'app sont-ils partagés entre tous les utilisateurs (clé statique plutôt que par-utilisateur) ?

## Comment confirmer l'impact

- Capture d'écran/vidéo de l'exploitation d'un composant exporté depuis une app tierce de test (ADB `am start` pour simuler l'attaque).
- Pour l'API backend : mêmes standards de preuve que pour le web (voir sections 03/04).
- Toujours préciser la version exacte de l'app/OS testée dans le rapport (comportement souvent version-dépendant).

## Références

- OWASP Mobile Application Security Testing Guide (MASTG) & MASVS
- `objection`, `frida`, `jadx`, `apktool`, `mobsf` (Mobile Security Framework)
- HackTricks — Android/iOS Pentesting sections
