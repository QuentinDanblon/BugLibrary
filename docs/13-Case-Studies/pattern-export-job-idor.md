# Pattern: Async Export Job IDOR

## Story (composite)

`POST /exports` returns `jobId`. `GET /exports/{jobId}/download` lacked owner check. Export contained PII.

## Why common

Async workers use internal IDs; download path added later without same middleware.

## Hunt method

Create export as A; access job as B; also try sequential job IDs carefully/low rate.

## Lessons

- Every sibling of a CRUD object needs authZ  
- Async multiplies forgotten checks  
- Impact = bulk data, raise severity  

## FR

Jobs async = IDOR fréquent. AuthZ sur create **et** download.
