# Target & Hypothesis Prioritization

## Portfolio view (if multiple programs)

| Signal | Prefer | Deprioritize |
|--------|--------|--------------|
| Scope clarity | Clear assets + safe harbor | Vague “all properties” chaos |
| Asset freshness | Recent launches, beta | Static brochure sites |
| Complexity | AuthZ, multi-tenant, workflows | Marketing WordPress only |
| Competition | Sparse valid reports on niche | Overfarmed XSS-only surface |
| Payout fit | Your skill × reward table | Critical-only with no skill match |
| Response quality | Fast, fair triage | Chronic N/A without reason |

## Within one program

**Priority stack (typical SaaS):**

1. Authentication / session / SSO edge cases  
2. Object-level authZ (BOLA/IDOR) on money & PII objects  
3. Function-level authZ (admin/export/impersonation)  
4. Multi-tenant isolation  
5. Business logic (race, refund, invite, pricing)  
6. Injection only where input reaches dangerous sinks  
7. Classic reflected XSS last on hardened SPAs (unless high impact chain)  

## Time-boxing rules

- Recon block: **≤25%** of session after week 1 on a program  
- If 3 sessions yield zero signal: change **asset** or **hypothesis class**, not just tools  
- Duplicate-heavy classes: require stronger novelty before deep dive  

## Kill switches

Stop a target when:

- Scope shrinks and removes your niche  
- You are emotionally tilting (error rate up)  
- Legal ambiguity appears  

## FR

Prioriser clarté de scope, fraîcheur, complexité authZ, et adéquation payout/skills. Stack SaaS typique : auth → BOLA → BFLA → isolation tenant → logique métier → injections ciblées.
