# Template de Triage Mental / Mental Triage Template

> À utiliser en < 60 secondes face à un signal suspect, pour décider s'il mérite un approfondissement immédiat. Voir méthodologie : [`docs/01-Mindset-and-Methodology`](../docs/01-Mindset-and-Methodology/README.md).

---

## Signal observé

*Description brève et factuelle de ce qui a attiré l'attention.*

## Filtre rapide

- [ ] Le comportement observé est-il **contrôlable par l'attaquant** (pas juste une observation passive) ?
- [ ] Traverse-t-il une **frontière de confiance** (utilisateur↔utilisateur, tenant↔tenant, rôle↔rôle, client↔serveur) ?
- [ ] A-t-il un **impact direct mesurable** (fuite de données, exécution de code, gain financier, contournement de contrôle) ?

**Décision :** [ Creuser immédiatement / Noter pour plus tard / Ignorer ]

## Si "Creuser immédiatement"

- **Hypothèse formulée :** *Étant donné [observation], il est probable que [mécanisme] soit vulnérable à [classe], ce qui permettrait [impact]. Test précis : [action].*
- **Time-box :** [ex: 30-45 min max avant réévaluation]
- **Compte(s) de test nécessaire(s) :** [...]

## Résultat du test

- **Confirmé ?** [Oui / Non / Partiellement — nécessite plus de contexte]
- **Sévérité estimée si confirmé :** [Critical / High / Medium / Low]
- **Prochaine action :** [Rédiger un rapport / Chercher un chaînage / Abandonner cette piste]

## Notes de chaînage potentiel

*Ce signal peut-il se combiner avec un autre signal déjà noté dans les notes de recon ? Référencer.*
