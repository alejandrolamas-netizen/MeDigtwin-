# MeDigtwin Security Baseline

**Status:** baseline controls proposed in a pull request; not a security certification or production-readiness attestation.

## 1. Repository governance

- Keep the default branch protected: require pull requests, require CI/security checks, require approval where staffing permits, dismiss stale approvals, and block force pushes/deletion.
- Require MFA for GitHub maintainers and review organization/repository access quarterly.
- Enable GitHub secret scanning and push protection where available; enable private vulnerability reporting.
- Keep GitHub Actions permissions read-only by default. Grant job-specific permissions only when needed.
- Pin third-party Actions to full commit SHAs before production use; review action updates through Dependabot.
- Do not use `pull_request_target` to check out or execute untrusted pull-request code with write permissions or secrets.

## 2. Secrets and credentials

- Never commit API keys, OAuth tokens, signing keys, certificates, cloud credentials, `.env` files, or production data.
- Store runtime secrets in AWS Secrets Manager (or the deployment platform's secret store); inject them server-side using narrowly scoped roles.
- Never expose provider keys in `index.html`, browser bundles, logs, test fixtures, pull requests, or chat.
- If a secret is exposed: revoke/rotate immediately, inspect provider logs, assess use, and remove the secret from history where appropriate. A new commit deleting a secret does not invalidate it.
- Use short-lived OIDC credentials for CI/cloud access instead of long-lived static cloud keys.

## 3. Application and API

- Production must fail closed when identity-provider configuration or bearer credentials are missing/invalid. Demo mode must use synthetic data only and must never be mistaken for production.
- Validate and bound every external input; enforce tenant isolation and role-based authorization on every protected operation.
- Apply request throttling, payload/time limits, and cost controls to public endpoints; do not treat a request quota as a guaranteed spend ceiling.
- Return generic client errors; do not return stack traces, provider responses, tokens, or secrets.
- Keep external model access disabled by default. Send only the minimum synthetic or explicitly approved data to providers.
- Do not use this prototype for diagnosis, treatment, triage, or real patient decisions. Do not place PHI/PII in the demo environment.

## 4. Containers and cloud

- Run containers as a non-root user; keep the base image small and rebuild it regularly.
- Scan dependencies and images, publish only reviewed artifacts, and avoid mutable `latest` tags for production releases.
- Use private subnets, TLS at the edge, least-privilege IAM, encryption at rest, and managed secret injection.
- Enable audit logs, alerting, backup/restore testing, and retention controls. Restrict access to logs because they may contain sensitive metadata.
- Do not deploy infrastructure or enable provider integrations solely because CI passes; use reviewed infrastructure diffs and explicit environment approval.

## 5. CI/CD controls

The proposed workflows run Gitleaks, pip-audit, Bandit, and CodeQL. Dependency review can be added once the repository administrator enables GitHub's dependency graph; it is currently not supported by the repository settings. Treat findings as release blockers until triaged and documented. Scheduled scans are not a substitute for reviewing each change.

For production, also configure:
- required status checks and at least one approval (or documented owner review for a single-maintainer project);
- environment protection rules for production and required reviewers;
- action SHA pinning and restricted allowed actions;
- container image scanning and artifact provenance/signing;
- incident alerting and a tested rollback procedure.

## 6. Incident response

1. Contain: revoke credentials, disable affected integrations, and isolate affected deployments.
2. Preserve: retain relevant audit and cloud logs without copying sensitive data into issues.
3. Assess: determine affected tenants, data types, time window, and potential exposure.
4. Recover: patch, rotate credentials, redeploy a known-good artifact, and validate controls.
5. Notify: follow applicable contractual and legal requirements; do not make unsupported claims.
6. Learn: document timeline, root cause, corrective actions, and owners.

## 7. Limitations and owner actions

These repository files cannot enable GitHub repository settings or AWS account controls by themselves. A repository administrator must enable branch protection/rulesets, secret scanning/push protection, private vulnerability reporting, MFA, environment approvals, cloud logging/alerts, and IAM policies in the relevant consoles. Review the repository's **Settings → Security** and **Settings → Rules** after merging.

Passing automated scans does not establish that the system is secure, compliant with HIPAA/ISO 27001/SOC 2, or suitable for clinical use. A qualified review and environment-specific verification are still required.
