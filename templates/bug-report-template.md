# Template de Rapport de Vulnérabilité / Vulnerability Report Template

> Copier ce template pour chaque nouveau rapport. Supprimer les instructions en italique avant soumission. Voir la méthodologie complète : [`docs/10-Reporting-and-Communication`](../docs/10-Reporting-and-Communication/README.md).

---

## Titre

*[Classe de vulnérabilité] + [localisation exacte] + [impact principal]*

Exemple : `IDOR sur /api/v2/orders/{id}/invoice permettant l'accès aux factures de tout utilisateur (fuite de PII et données financières à l'échelle de la plateforme)`

## Résumé exécutif

*2-3 phrases maximum. Quoi, où, impact principal — lisible seul sans le reste du rapport.*

## Sévérité

**Sévérité :** [Critical / High / Medium / Low]
**Score CVSS 3.1 :** [X.X] — [Vecteur complet, ex: AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N]
**Justification :** *Pourquoi ce score exactement — expliciter chaque composante du vecteur.*

## Composants affectés

- **URL/Endpoint :** `https://...`
- **Paramètre(s) affecté(s) :** `...`
- **Méthode HTTP :** `GET/POST/PUT/DELETE`
- **Comptes de test utilisés :** `test-a@example.com` (rôle X), `test-b@example.com` (rôle Y)

## Étapes de reproduction

*Numérotées, exécutables telles qu'écrites, sans étape implicite. Inclure les requêtes/réponses HTTP brutes en bloc de code.*

1. ...
2. ...
3. ...

```http
GET /api/v2/orders/12345/invoice HTTP/1.1
Host: target.com
Authorization: Bearer <token-utilisateur-A>

[Réponse]
HTTP/1.1 200 OK
...
```

## Preuve visuelle

*Capture(s) d'écran ou vidéo jointe démontrant l'exploitation de bout en bout. Une vidéo est recommandée pour toute vulnérabilité multi-étapes ou multi-comptes.*

## Impact business

*Traduire le technique en risque réel pour l'entreprise : nombre d'utilisateurs concernés, sensibilité des données exposées, scénario d'attaque réaliste à l'échelle, coût estimé si applicable.*

## Scénario d'attaque réaliste

*Comment un attaquant réel exploiterait ce bug en conditions réelles — vecteur de distribution, échelle atteignable, prérequis d'accès.*

## Chaînage / Vulnérabilités liées

*Si ce bug a été découvert/amplifié en combinaison avec un autre signal, le documenter ici avec référence croisée.*

## Remédiation suggérée

*Recommandation technique concrète, pas générique — spécifique au mécanisme observé.*

## Références

*Liens vers la documentation technique pertinente (OWASP, PortSwigger, CVE si applicable).*

---

*Checklist avant soumission — voir [`docs/12-Checklists-and-CheatSheets/README.md`](../docs/12-Checklists-and-CheatSheets/README.md#checklist-avant-de-soumettre-un-rapport-universelle)*
