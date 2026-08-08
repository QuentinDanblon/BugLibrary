# Authentication & Session

## Hypothesis classes (authorized testing)

| Class | What to verify carefully |
|-------|---------------------------|
| Registration | Privilege self-assignment, disposable domain edge cases |
| Login | Enumeration only if in scope & non-abusive; MFA flows |
| Session | Fixation, concurrent session, logout completeness |
| Cookie flags | Secure/HttpOnly/SameSite mismatches with CSRF design |
| Password reset | Token entropy, reuse, host header influence on links (classic) |
| OAuth | `redirect_uri` partial match, `state`, token in URL, mix-up |
| SSO/SAML | If in scope: assertion handling classes (advanced) |
| Remember-me | Long-lived tokens binding |

## OAuth/OIDC high-signal checklist

- [ ] Exact `redirect_uri` match enforced  
- [ ] `state` validated  
- [ ] Authorization code not reusable  
- [ ] Tokens not leaked to third-party analytics via Referer  
- [ ] Account linking without proof of email ownership  
- [ ] PKCE used for public clients; verify completeness  

## Session testing discipline

- Use separate browsers/profiles per role  
- After privilege change, confirm session claims refresh  
- Test CSRF defense consistency on state-changing routes  

## Safe harbor reminder

Do not lock real user accounts. Do not spam password resets to third parties. Use your own inboxes.

## Pro tip

**Account linking** and **secondary email add** are still among the highest EV auth features on mature programs.

## FR

Classes : inscription, session, reset, OAuth, linking. Discipline multi-profils. Pas d’abus sur de vrais utilisateurs. Linking email = jackpot fréquent.
