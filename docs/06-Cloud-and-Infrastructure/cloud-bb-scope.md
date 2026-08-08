# Cloud in Bug Bounty Scope

## Critical rule

**Cloud provider infrastructure is not your target** unless the program explicitly includes specific accounts/resources. You test **the customer’s assets** listed in scope.

## Typical in-scope

- Public storage buckets **owned by the program** and referenced by their apps  
- Subdomain → cloud service mappings for **their** brands  
- App SSRF that reaches **their** internal/cloud resources  
- Misconfigured product features exposing cloud URLs  

## Typical out-of-scope

- Scanning all of AWS/GCP/Azure for random buckets  
- Attacking cloud control plane of the vendor  
- Other customers’ tenants  

## FR

Tester les assets **du programme**, pas le cloud provider entier. Toujours relire le scope.
