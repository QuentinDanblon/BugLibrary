# Business Logic Vulnerabilities — Race Conditions, Workflow Abuse

## Contexte

C'est la catégorie où l'expertise humaine (ou d'un agent IA bien orchestré comprenant le domaine métier) surpasse totalement les scanners automatiques. Sévérité souvent Haute-Critique car l'impact est directement financier ou touche l'intégrité du système. Fréquent dans : e-commerce, fintech, plateformes SaaS avec quotas/crédits, systèmes de réservation, programmes de fidélité/référencement.

## Race Conditions (2024-2026 — catégorie en forte croissance)

### Contexte technique

Une race condition exploite l'absence de verrouillage atomique entre la **vérification** d'un état et son **utilisation** (TOCTOU). Devenu un vecteur majeur depuis la popularisation de Turbo Intruder et HTTP/2 single-packet attack (recherche PortSwigger/James Kettle).

### Comment tester

```
1. Identifier les opérations avec vérification d'état :
   - Utilisation d'un coupon/code promo (vérif "non utilisé" puis "marquer utilisé")
   - Retrait/transfert d'argent (vérif solde puis débit)
   - Inscription à un événement à places limitées
   - Application d'un crédit de parrainage
   - Vote/like unique par utilisateur
   - Changement de mot de passe / d'email en parallèle avec une action sensible

2. Envoyer un grand nombre de requêtes IDENTIQUES en parallèle,
   avec un timing le plus synchronisé possible.
```

**Technique HTTP/2 Single-Packet Attack (la plus fiable en 2024-2026) :**

```python
# Via Turbo Intruder (extension Burp) — template "race-single-packet-attack.py"
# Envoie toutes les requêtes dans un seul paquet TCP (HTTP/2 multiplexing)
# pour éliminer la variance réseau et maximiser la fenêtre de race

engine = RequestEngine(endpoint=target,
                        concurrentConnections=1,
                        engine=Engine.BURP2)

for i in range(20):
    engine.queue(target.req, gate='race1')

engine.openGate('race1')
engine.complete(timeout=60)
```

> 💡 **Pro tip d'élite :** La technique "single-packet attack" de James Kettle (PortSwigger) élimine la variance de latence réseau en envoyant les N requêtes dans un seul paquet TCP via HTTP/2, laissant le serveur les traiter quasi simultanément. C'est aujourd'hui LA méthode de référence — beaucoup plus fiable que l'ancien "30 threads en parallèle avec `requests`".

**Scénarios d'exploitation classiques :**

| Scénario | Résultat exploité |
|---|---|
| Application d'un coupon de réduction 10x en parallèle | Réduction cumulée x10, ou solde négatif |
| Retrait d'argent en parallèle sur un solde limite | Retrait de plus que le solde disponible |
| Inscription à un événement à 1 place restante, 10 requêtes parallèles | Sur-réservation |
| Like/vote en parallèle sur un système "1 par utilisateur" | Comptage multiplié |
| Changement d'email + validation de reset password simultané | Prise de compte via race sur la fenêtre de validation |
| Multi-usage d'un code de parrainage à usage unique | Crédits multipliés |

### Sous-catégorie : Limit Overrun / Time-of-Check-Time-of-Use sur fichiers

Upload de fichier avec scan antivirus asynchrone → accès au fichier possible pendant la fenêtre entre l'upload et la fin du scan (race pour accéder à un fichier malveillant avant qu'il ne soit supprimé/bloqué).

## Workflow / State Machine Bypass

```
1. Cartographier le workflow attendu (ex: panier → paiement → confirmation → livraison)
2. Identifier les étapes qui dépendent d'un état côté serveur transmis au client
   (souvent un statut dans une requête, pas re-vérifié à chaque étape suivante)
3. Sauter des étapes en appelant directement l'endpoint de l'étape N+2 sans passer par N+1
4. Revenir en arrière dans le workflow après une étape "irréversible" côté métier
```

**Exemples concrets :**
- Appeler directement `/api/order/confirm` sans jamais avoir appelé `/api/order/pay` (si la confirmation ne re-vérifie pas le statut de paiement côté serveur).
- Modifier le prix côté client puis soumettre directement à l'étape de confirmation si le prix n'est pas recalculé serveur-side à chaque étape.
- Manipuler la quantité négative dans un panier (`quantity: -5`) pour créer un solde de remboursement/crédit anormal.
- Appliquer un discount deux fois en rejouant une requête de "apply coupon" après le calcul du total.

## Abus financier / de quotas — patterns fréquents

| Pattern | Comment tester |
|---|---|
| Manipulation de prix côté client | Intercepter et modifier le prix/montant dans la requête avant soumission — vérifier si le serveur recalcule ou fait confiance au client |
| Devise/unité manipulée | Changer la devise pour profiter d'un taux de conversion mal appliqué |
| Quantité négative ou à virgule flottante sur un champ entier attendu | `quantity: -1`, `quantity: 0.5` sur un système de facturation |
| Rounding/précision exploitée | Micro-transactions répétées exploitant un arrondi favorable (ex: 0.001 non facturé × 100000) |
| Webhook de paiement rejouable | Rejouer un webhook "paiement confirmé" pour créditer un compte plusieurs fois |
| Idempotency key absente/mal implémentée | Rejouer une requête de transfert sans clé d'idempotence → duplication |

> 💡 **Pro tip :** Sur toute plateforme avec des "crédits"/"points"/"tokens" internes (pas juste de l'argent réel), l'abus de logique est souvent moins surveillé qu'un vrai flux financier — mais reste presque toujours en scope et payé, car il représente une perte réelle pour l'entreprise (crédits = coût réel de service).

## Comment confirmer l'impact

- Vidéo/capture montrant la séquence exacte de requêtes (timestamps) et l'état final anormal (solde, quota, statut).
- Chiffrer l'impact potentiel si généralisé (ex: "un attaquant répétant cette race 100x obtiendrait X$ de crédit gratuit — extrapolation à l'échelle de la plateforme").
- Toujours tester sur un compte de test avec des montants/quantités minimales.

## Remédiation

- Verrous atomiques (transactions DB avec isolation appropriée, verrous distribués type Redis `SETNX`) sur toute opération critique.
- Idempotency keys obligatoires sur les opérations financières.
- Re-validation serveur de CHAQUE étape d'un workflow, jamais de confiance dans l'état transmis par le client.

## Références

- PortSwigger Research — "Smashing the state machine" (James Kettle, race conditions)
- PortSwigger Web Security Academy — Race conditions, Business logic vulnerabilities
- OWASP Business Logic Testing Guide
