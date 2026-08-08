# AI Agent Scope Pack Template

```yaml
program_id: 
policy_url: 
policy_retrieved_at: 
safe_harbor: true|false|unknown

assets:
  allow:
    - type: domain
      value: app.example.com
    - type: wildcard
      value: "*.example.com"
      notes: "exclude marketing CDN per policy"
  deny:
    - type: domain
      value: vendor-status.example
      reason: third-party

actions:
  allow:
    - passive_recon
    - authenticated_read
    - limited_write_on_own_objects
  deny:
    - dos
    - spam_third_parties
    - social_engineering_employees
    - access_other_customers_data_beyond_minimal_poc

budgets:
  max_rps: 2
  max_requests_per_hour: 1000
  max_parallel_validations: 1

gates:
  state_changing_requests: human_approve
  report_submission: human_only
  oob_callbacks: allowlist_only

accounts:
  - label: Attacker-A
    role: user
  - label: Victim-B
    role: user

redaction:
  never_send_to_llm:
    - session_tokens
    - passwords
    - api_keys
    - raw_pii_dumps
```

## Human attestation

I confirm this pack matches the written program policy.

**Name:**  
**Date:**  
