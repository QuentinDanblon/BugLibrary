# Mobile → API Pivot

## Playbook

1. Exercise every premium feature in the app  
2. Export HAR-equivalent from proxy  
3. Deduplicate endpoints  
4. Diff against web-only API set — **mobile-only endpoints are gold**  
5. Run full BOLA/BFLA matrix on mobile-only routes  
6. Check weaker serialization (protobuf/json alternatives)  

## Pro tip

Older app versions often call `/v1` with missing checks that `/v2` fixed. If policy allows historical clients, keep an archive of APKs **you obtained legitimately**.

## FR

Features premium → endpoints mobile-only → matrice authZ. Les vieilles versions d’app gardent des API faibles.
