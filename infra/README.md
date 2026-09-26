# MedDigtwin AWS Infrastructure

Target deployment for the MedDigtwin API.

## Target path

GitHub
→ CI
→ Amazon ECR
→ Amazon ECS/Fargate
→ HTTPS/API boundary
→ MedDigtwin API

## Infrastructure principles

- Infrastructure as Code.
- No secrets in Git.
- Least-privilege IAM.
- Separate environments.
- Synthetic data by default.
- CloudWatch observability.
- KMS encryption where applicable.
- Production healthcare data requires a separate security/privacy assessment.

## Current state

This directory documents the infrastructure target. AWS resources are not claimed as deployed until they are provisioned and validated in an AWS account.

## Next implementation units

1. VPC/networking
2. ECR repository
3. ECS cluster/service/task definition
4. IAM execution/task roles
5. HTTPS ingress
6. CloudWatch logs
7. Secrets Manager integration
8. CI/CD deployment
9. Health checks and rollback
10. Marketplace fulfillment/entitlement integration
