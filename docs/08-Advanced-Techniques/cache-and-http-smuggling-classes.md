# Cache & HTTP Edge Classes

## Cache deception / poisoning (conceptual)

Modern CDNs and app caches can confuse:

- What is keyed (host, path, cookies, headers)  
- What is stored (personalized content)  

### Hunter discipline

- Prefer non-destructive proofs (canary headers/body on your account)  
- Avoid poisoning shared caches with offensive content  
- Severity needs practical theft of another user’s data or security tokens  

## Request smuggling classes

Desync between front-end and back-end parsers. Advanced, environment-specific.

- Lab first when possible  
- On production BB: extreme caution; easy to cause availability issues  
- Many programs treat pure DoS as N/A  

## FR

Cache et smuggling : preuves non destructives, impact utilisateur réel. Attention disponibilité — souvent hors récompense si DoS pur.
