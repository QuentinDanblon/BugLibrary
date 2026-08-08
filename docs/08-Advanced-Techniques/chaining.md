# Vulnerability Chaining

## Principle

Programs pay for **reachable impact**. A self-XSS + weak CSRF + cookie lacking HttpOnly can become ATO — if you demonstrate the chain cleanly.

## Chain documentation template

```markdown
## Chain
1. Finding A (precondition)
2. Finding B (bridge)
3. Finding C (impact)

## Minimal path
- Accounts required
- User interaction required? (click, visit)
- Network position assumptions

## Why not atomic-only
Explain residual risk if only one link is fixed.
```

## High-value chain patterns

| Start | Bridge | Impact |
|-------|--------|--------|
| Open redirect | Token in URL | ATO |
| XSS | Sensitive action endpoint | Account / data |
| SSRF | Internal admin no auth | RCE-class / data |
| IDOR read | Export job | Bulk PII |
| Info disc. (reset token format) | Weak entropy | ATO |

## Reporting ethics

Do not overclaim impossible interaction models. State UX assumptions honestly (e.g., victim must click).

## FR

Chaîner pour l’impact atteignable. Documenter chaque maillon et l’interaction utilisateur. Pas de sur-promesse.
