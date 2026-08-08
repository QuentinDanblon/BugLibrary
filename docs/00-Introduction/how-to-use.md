# How to Use This Library / Comment utiliser cette bibliothèque

## English

### Path A — First serious bounty week

1. `11-Legal-Ethics-and-OPSEC` (full)
2. `01-Mindset-and-Methodology` → hypothesis-driven + prioritization
3. `02-Reconnaissance` → ASM only for your in-scope assets
4. Pick **one** domain deep: usually `03-Web` or `04-API`
5. `10-Reporting` + `templates/bug-report-template.md`
6. `12-Checklists` day-of sheet

### Path B — API-heavy modern SaaS

1. Scope parsing checklist (`11` + `12`)
2. `04-API-GraphQL-Hunting` end-to-end
3. Auth/session section in `03`
4. Cloud pivot classes in `06` (only if in scope)
5. Report impact patterns in `10`

### Path C — AI multi-agent hunting team

1. `08/ai-agents-bug-hunting.md` (orchestration contracts)
2. `09-Automation-and-Tooling` (rate limits, signal filters)
3. Feed agents **only** in-scope asset lists from recon templates
4. Human gate before any state-changing request
5. Unified report assembly via templates

### Path D — Mentoring / team standard

1. Adopt methodology from `01` as team SOP
2. Enforce report template from `templates/`
3. Weekly Living Document PR (`14`)
4. Case studies (`13`) for postmortems — never shaming, always patterns

### How *not* to use it

- Skimming only tool names without methodology  
- Running mass scanners against entire programs without rate discipline  
- Copy-pasting AI-generated “PoCs” without understanding or safe validation  
- Treating checklists as brain-off scripts  

### Navigation tips

- Each section folder has a `README.md` index  
- Cross-links beat duplication — prefer linking Legal/Reporting from technique pages  
- Prefer the **newest** dated note when techniques conflict  

---

## Français

### Parcours A — Première semaine bounty sérieuse

Légal → Mindset → Recon → un domaine profond (Web/API) → Reporting → Checklist du jour.

### Parcours C — Équipe multi-agents IA

Contrats d’orchestration (`08`) → Automation (`09`) → listes d’assets scopées → **gate humain** avant toute action à effet de bord → rapport unifié.

### Mauvais usages

Scanner massif sans discipline, PoC IA non compris, checklists en mode pilote automatique, ignorer le scope.
