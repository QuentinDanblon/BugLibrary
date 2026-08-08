# SSRF → Cloud Edge Cases

## Modern context (2024–2026)

Cloud providers hardened Instance Metadata Services (IMDSv2, GCP headers, etc.). Blind claims of “full cloud takeover via SSRF” need **evidence**.

## Still valuable

- Reachability of internal admin panels  
- Access to internal HTTP APIs with weak auth  
- Reading cloud-only endpoints that return short-lived creds **if still possible**  
- File processors fetching `file://` or internal URLs  

## Safe demonstration

1. Out-of-band proof to hunter-controlled endpoint  
2. If internal: single non-destructive request  
3. No lateral movement theater  
4. Stop at impact sufficient for severity  

## FR

IMDS est plus dur ; prouver l’impact réel. Une requête non destructive suffit souvent.
