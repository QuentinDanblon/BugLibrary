# Business Logic & Workflows

## Why logic pays

Scanners miss multi-step trust assumptions. Humans (and well-prompted agents) shine here.

## Pattern catalog

| Pattern | Hypothesis seed |
|---------|-----------------|
| Race (TOCTOU) | Double spend, double redeem, parallel apply |
| Step skipping | Jump to confirm without pay |
| Price/quantity tampering | Client-side price trusted |
| Coupon stacking | Limit not enforced server-side |
| Invite/accept | Accept as other user; role confusion |
| Refund/cancel | State rollback incomplete |
| Trial abuse | Identity reset resets trial |
| Workflow reordering | Ship before fraud check |
| Limit bypass | Seats/API quota client-enforced |

## Race testing (authorized, gentle)

- Parallelize **your own** legitimate actions only  
- Low concurrency first (2–5) to prove class  
- Stop if production impact risk rises  
- Many programs restrict heavy racing — read policy  

## State machine method

1. Draw intended states  
2. List legal transitions  
3. Attempt illegal transitions with replayed tokens  
4. Replay old tokens after state change  

## Pro tip

Read the **pricing page and help center** — they document intended rules the API may fail to enforce.

## FR

La logique métier bat les scanners. Courses, sauts d’étapes, prix, invites, remboursements. Dessiner la machine à états. Lire l’aide produit = spec gratuite.
