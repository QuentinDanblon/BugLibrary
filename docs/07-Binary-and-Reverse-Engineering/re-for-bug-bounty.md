# Reverse Engineering for Bug Bounty

## When it is worth it

| Target type | RE value |
|-------------|----------|
| Thick clients / desktop | High — custom protocols |
| Games / anti-cheat (if in scope) | High skill bar |
| Mobile native crypto | Medium-high |
| IoT companion apps | High |
| Pure web SaaS | Low — prefer API |

## Goals in BB context

1. Recover protocol / API not in web  
2. Find insecure update mechanisms  
3. Spot auth bypass in client-trusted logic  
4. Identify dangerous IPC  

Not a goal: shipping cracks or license circumvention for piracy.

## FR

RE utile pour clients lourds, mobile natif, IoT. Objectif : protocole et auth, pas piratage.
