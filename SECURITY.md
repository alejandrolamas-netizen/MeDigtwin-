# Security Policy — MedDigtwin

## Scope

MedDigtwin is an EmergentSoft Corporation product for healthcare operational simulation. The current product environment uses synthetic data.

## Security posture

The AWS-ready architecture uses:

- IAM least privilege
- ECS/Fargate task isolation
- ECR image scanning
- Cognito-based identity
- Tenant-scoped authorization
- DynamoDB encryption and point-in-time recovery
- CloudWatch logging
- AWS WAF
- Optional ACM TLS
- GitHub Actions OIDC instead of long-lived AWS access keys

## Data boundary

Do not submit patient-identifiable information, protected health information, production clinical datasets, credentials, API keys or access tokens to the current demo/prototype.

A deployment that processes real healthcare information requires a separate security, privacy, compliance and data-governance assessment.

## Reporting

Potential security issues should be reported privately to EmergentSoft Corporation through the official company contact channel. Do not publish credentials, exploit instructions or sensitive healthcare data in public issues.

## Product limitation

AWS-ready does not mean clinically validated, regulatory certified or authorized to process regulated health information.

MedDigtwin is an operational simulation product and is not a clinical diagnosis or treatment system.

© 2026 EmergentSoft Corporation.
