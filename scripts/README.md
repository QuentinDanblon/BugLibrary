# scripts/

Scripts d'automatisation référencés depuis [`docs/09-Automation-and-Tooling/README.md`](../docs/09-Automation-and-Tooling/README.md). Chaque script est un point de départ à adapter — jamais à exécuter en aveugle contre une cible réelle sans avoir vérifié le scope et les règles du programme.

## Scripts disponibles

| Script | Rôle |
|---|---|
| `recon_pipeline.sh` | Pipeline de reconnaissance incrémental (subdomain enum + probing + diff quotidien) |
| `jwt_alg_confusion_check.py` | Vérification rapide de confusion d'algorithme JWT (RS256→HS256, alg=none) |
| `race_condition_test.py` | Squelette de test de race condition via requêtes parallèles (HTTP/1.1 fallback si HTTP/2 non disponible) |

> ⚠️ **Rappel OPSEC :** Adapter systématiquement le rate limiting de chaque script aux règles explicites du programme ciblé avant exécution. Voir [`docs/11-Legal-Ethics-and-OPSEC`](../docs/11-Legal-Ethics-and-OPSEC/README.md).
