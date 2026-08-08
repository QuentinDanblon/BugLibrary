# Pattern: GraphQL Nested Resolver AuthZ Gap

## Story (composite)

`organization(id:)` authorized, but nested `secretIntegrations { apiKey }` resolver skipped authZ field checks for members vs admins.

## Hunt method

Request sensitive fields as low-priv member; compare with admin.

## Lessons

- Field-level authZ is mandatory in GraphQL  
- Introspection helps map sensitive fields  
- Excessive data exposure often lives in nested types  

## FR

AuthZ par champ. Les types imbriqués fuient souvent des secrets.
