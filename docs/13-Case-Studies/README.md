# 13 — Case Studies

## Objectif de cette section

Deux catégories de cas dans ce document :

1. **Cas réels documentés** — rapports effectivement divulgués publiquement sur HackerOne, cités avec leur lien et leurs faits exacts (pas de détail inventé au-delà de ce que le rapport public confirme).
2. **Cas pédagogiques généralisés** — compositions inspirées de patterns récurrents observés dans la communauté, non attribuées à un programme nommé, utiles pour illustrer une méthodologie de chaînage même sans rapport source unique.

## Cas réels documentés (disclosures publiques HackerOne)

### Cas réel 1 — IDOR sur l'édition d'email menant à une prise de compte (Atavist / Automattic)

**Source :** [HackerOne Report #950881](https://hackerone.com/reports/950881) — divulgué publiquement, programme Automattic.

**Observation initiale :** Le chercheur (`bugra`) modifie son adresse email depuis la page de compte `https://magazine.atavist.com/cms/reader/account` et intercepte la requête via un proxy. La requête contient un paramètre `id` correspondant à l'ID utilisateur.

**Hypothèse formulée :** Si l'`id` est accepté côté client sans revérification serveur de la correspondance avec le compte authentifié, et que les IDs utilisateurs sont séquentiels, l'attaque est généralisable à l'ensemble de la base utilisateurs.

**Test :** Remplacement de l'`id` par celui d'un second compte de test, envoi de la requête modifiée.

**Résultat confirmé :** L'email du second compte est modifié avec succès — aucune vérification serveur de propriété de la ressource. Les IDs étant séquentiels, l'attaque est triviale à automatiser sur l'ensemble des comptes.

**Impact final :** Chaînage direct avec le flux "mot de passe oublié" — changer l'email d'un compte cible puis déclencher `/forgot` sur la nouvelle adresse email contrôlée par l'attaquant permet une **prise de compte sans aucune interaction de la victime**. Rapport classé critique, bounty accordé (montant non communiqué publiquement par le programme).

**Leçon méthodologique :** Une IDOR sur un champ en apparence anodin (email de compte) devient critique dès qu'elle se chaîne avec un flux d'authentification existant (reset password) — toujours se demander "qu'est-ce que cette donnée modifiable permet de déclencher ensuite ?", pas seulement "cette donnée est-elle sensible en elle-même ?".

---

### Cas réel 2 — SSRF critique via génération de rapports d'analytics (programme HackerOne lui-même)

**Source :** [HackerOne Report #2262382](https://hackerone.com/reports/2262382) — divulgué publiquement par HackerOne sur son propre programme, chercheur `mega7`.

**Observation initiale :** Une fonctionnalité de génération de rapports convertit du contenu HTML en PDF côté serveur (`ApplicationController.render_to_string` alimentant un moteur de rendu PDF). Un message d'erreur "Missing template for element: `#{element[:template]}`" reflétait la valeur du paramètre `template` sans sanitization.

**Hypothèse formulée (déduite du diff de correctif publié par HackerOne) :** La valeur non sanitizée du champ `template`, réinjectée dans le pipeline de rendu HTML→PDF, était probablement exploitable pour forcer le moteur de rendu à effectuer des requêtes serveur vers des ressources arbitraires — signature classique de SSRF via un moteur de templating/rendu.

**Test :** Le chercheur a démontré la capacité à faire émettre des requêtes serveur vers des services AWS internes depuis l'application, jusqu'à confirmer l'accès aux endpoints de credentials temporaires — puis s'est arrêté à ce stade sans extraire ou utiliser les credentials.

**Résultat confirmé :** Accès démontré aux services AWS internes de l'infrastructure applicative, avec possibilité d'obtenir des credentials IAM temporaires.

**Impact final :** HackerOne a noté le rapport **CVSS 3.0 = 10.0 (Critical)** — vecteur `AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N/CR:H/IR:H/AR:H` — et a explicitement remercié le chercheur pour s'être arrêté au bon moment ("stopping at the right point in testing, demonstrating a responsible and ethical approach").

**Leçon méthodologique :** Deux points structurants — (1) tout message d'erreur qui reflète un paramètre d'entrée dans un contexte de rendu serveur (templating, PDF, image) est un candidat direct à l'hypothèse SSRF/injection, même sans réponse HTTP visible immédiate ; (2) démontrer l'accès aux credentials sans les extraire/utiliser est la pratique attendue pour un rapport noté "responsable et éthique" — la preuve d'accès suffit, l'exploitation active dégrade la relation avec le programme sans augmenter la sévérité du rapport.

---

## Cas pédagogiques généralisés

> 💡 Pour trouver d'autres cas réels à ajouter ici, consulte la Hacktivity publique de HackerOne (filtrable par sévérité/bounty) et les write-ups référencés dans [`14-Resources-and-Continuous-Learning`](../14-Resources-and-Continuous-Learning/README.md).

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
