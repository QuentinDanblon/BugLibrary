# API & GraphQL Checklist

## REST

- [ ] Resource inventory complete for feature
- [ ] BOLA on all IDs
- [ ] BFLA on privileged verbs
- [ ] Mass assignment create/update
- [ ] Excessive data exposure on read
- [ ] Version skew v1 vs v2
- [ ] Batch endpoints
- [ ] Webhook SSRF/signature

## GraphQL

- [ ] Mutations mapped
- [ ] Field-level sensitive data
- [ ] Nested resolver authZ
- [ ] Subscriptions authZ
- [ ] Batch/mixed operations
- [ ] File upload mutations
- [ ] Introspection used as map only

## FR

REST + GraphQL : BOLA/BFLA/mass assignment d’abord, DoS en dernier et souvent hors scope.
