# Security Policy — MedDigtwin

## Scope and data boundary

MedDigtwin is an EmergentSoft Corporation healthcare **operational simulation** prototype. The demo is intended for synthetic data only. It is not a medical device or clinical decision-support system.

Do not submit patient-identifiable information, protected health information, production clinical datasets, credentials, API keys, access tokens, private keys, or exploit payloads that could harm a live service in public issues or pull requests.

## Reporting a vulnerability

Please do not disclose exploitable vulnerabilities in a public issue. Use GitHub's repository **Security → Advisories → Report a vulnerability** feature if private vulnerability reporting is enabled. If it is unavailable, contact EmergentSoft through its official company contact channel and request a private security-reporting route. Do not include secrets or personal/health information in the report.

Include:
- affected component and commit/version;
- impact and preconditions;
- minimal reproduction steps using synthetic data and without disrupting a service;
- suggested mitigation, if known.

Target response times are acknowledgment within 5 business days and initial triage within 10 business days. These are goals, not guarantees.

## Exposed credentials

If a credential may have been exposed, revoke it immediately, issue a replacement through the provider, inspect provider access logs, and assess potential misuse. Removing the value from the latest commit is not enough; history may still contain it.

## Safe-harbor expectations

Testing must be authorized, limited in scope, and avoid accessing real data, degrading services, persistence, or lateral movement. Stop if you encounter real personal or health information and report it privately.

## Product limitations

An AWS-ready architecture or passing automated scan is not a security certification, clinical validation, or proof of HIPAA, ISO 27001, or SOC 2 compliance. Any deployment handling real healthcare information requires separate security, privacy, legal, and data-governance review.

© 2026 EmergentSoft Corporation.
