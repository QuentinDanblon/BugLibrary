# 13 — Case Studies

## Objectif de cette section

Études de cas généralisées/anonymisées illustrant la méthodologie de chaînage et de hunting piloté par hypothèses. Ces cas sont des **compositions pédagogiques inspirées de patterns réels et publics** (write-ups connus de la communauté, disclosures publiques agrégées) — pas des rapports d'un programme spécifique nommé, sauf lorsque l'information est déjà en disclosure publique confirmée.

> 💡 Pour des études de cas réelles avec noms de programmes, consulte la Hacktivity publique de HackerOne et les write-ups référencés dans [`14-Resources-and-Continuous-Learning`](../14-Resources-and-Continuous-Learning/README.md).

## Cas 1 — De l'IDOR mineure à la prise de compte de masse

**Observation initiale :** Un endpoint `/api/v1/notifications/{id}/mark-read` accepte un ID numérique séquentiel et ne retourne qu'un `200 OK` générique, sans donnée sensible visible dans la réponse — semble low-impact à première vue.

**Hypothèse formulée :** Si l'endpoint ne vérifie pas l'appartenance de la notification à l'utilisateur courant pour une action d'écriture simple, il est probable que les endpoints de LECTURE de notifications (`GET /api/v1/notifications/{id}`) souffrent du même défaut de contrôle — et les notifications contiennent souvent des données sensibles en clair (liens de reset password, codes de vérification, contenu de messages privés).

**Test :** Requête `GET /api/v1/notifications/{id}` avec le token de l'utilisateur A et un ID appartenant à l'utilisateur B, itéré sur une plage d'IDs.

**Résultat :** Confirmation — les notifications de type "reset password" contenaient le lien complet avec token en clair, accessible pour n'importe quel ID en itérant simplement la séquence numérique.

**Impact final :** Chaîné avec l'absence de rate limiting sur cet endpoint de lecture → capacité à extraire en masse les tokens de reset password valides de tous les comptes récents, permettant une prise de compte à grande échelle. **Passé de "IDOR sans donnée visible = probablement low" à "Critical — account takeover de masse".**

**Leçon méthodologique :** Ne jamais juger l'impact d'un défaut de contrôle d'accès uniquement sur l'endpoint testé initialement — toujours vérifier les endpoints voisins de la même ressource (lecture vs écriture, liste vs objet unique).

---

## Cas 2 — Race condition sur un système de crédits de parrainage

**Observation initiale :** Un endpoint `POST /api/referral/apply` applique un crédit de bienvenue lors de l'utilisation d'un code de parrainage, avec un message "ce code a déjà été utilisé" en cas de deuxième tentative — semble correctement protégé contre la réutilisation.

**Hypothèse formulée :** La vérification "code déjà utilisé" est probablement effectuée par une lecture en base suivie d'une écriture séparée (pattern classique non-atomique), sans verrou transactionnel — vulnérable à une race condition si plusieurs requêtes arrivent avant que la première écriture ne soit committée.

**Test :** Envoi de 20 requêtes identiques via la technique HTTP/2 single-packet attack (Turbo Intruder) avec le même code de parrainage valide sur un compte de test neuf.

**Résultat :** 7 des 20 requêtes ont retourné un succès avec crédit appliqué, au lieu d'une seule — confirmation de l'absence de verrou atomique.

**Impact final :** Un attaquant répétant l'opération à plus grande échelle (plus de requêtes en parallèle, plusieurs comptes) pourrait générer un volume de crédits frauduleux significatif — **impact financier direct chiffrable**, sévérité Haute.

**Leçon méthodologique :** Tout mécanisme "vérifier puis agir" affichant un message d'erreur de type "déjà fait/déjà utilisé" est un candidat systématique au test de race condition, indépendamment de la robustesse apparente du message d'erreur en usage séquentiel normal.

---

## Cas 3 — SSRF via générateur de PDF, escaladé en accès infra cloud

**Observation initiale :** Une fonctionnalité "exporter en PDF" génère un PDF depuis une page HTML interne, incluant un logo dont l'URL peut être personnalisée par l'utilisateur dans les paramètres de compte.

**Hypothèse formulée :** Le moteur de génération PDF (probable headless Chrome/Puppeteer d'après les en-têtes de réponse observés) effectue vraisemblablement une requête serveur pour charger l'image du logo depuis l'URL fournie — candidat SSRF classique.

**Test :** Configuration de l'URL de logo vers un serveur contrôlé pour confirmer la requête sortante, puis test vers `http://169.254.169.254/latest/meta-data/iam/security-credentials/`.

**Résultat :** Le PDF généré contenait, au lieu d'une image, le texte brut de la réponse HTTP du endpoint metadata (car ce n'était pas une image valide, le moteur avait affiché le contenu texte brut par erreur de fallback) — révélant le nom du rôle IAM attaché à l'instance.

**Impact final :** Accès démontré aux credentials IAM temporaires du rôle applicatif via le endpoint de sécurité — **documenté sans exploitation active des credentials**, sévérité Critical (accès infrastructure cloud).

**Leçon méthodologique :** Les fonctionnalités "génération de document depuis une ressource externe" sont des candidats SSRF à très haut ROI car souvent implémentées avec des moteurs headless dont le comportement de fetch réseau est mal audité par les développeurs eux-mêmes.

---

## Comment contribuer un cas d'étude

Voir [`CONTRIBUTING.md`](../../CONTRIBUTING.md). Format attendu : Observation initiale → Hypothèse formulée → Test → Résultat → Impact final → Leçon méthodologique. Anonymiser/généraliser systématiquement toute référence à un programme spécifique non déjà en disclosure publique confirmée.
