# Scope Middleware Spec (Safe Design)

Any automated HTTP client used for bug bounty should implement:

## Inputs

- `allowlist`: domains/hosts/wildcards from scope pack  
- `denylist`: explicit OOS  
- `budgets`: RPS, daily caps  

## Behavior

```text
on_request(url, method):
  host = parse(url).host
  if host in denylist or not match(allowlist):
    reject("out_of_scope")
  if budget_exceeded():
    reject("budget")
  if method in STATE_CHANGING and not human_approved:
    reject("gate")
  apply_rate_limit()
  send()
```

## Logging

- Log host, method, path, hypothesis ID  
- Never log Authorization headers in plaintext  

## FR

Tout client auto : allowlist, denylist, budgets, gate write, logs sans secrets.
