# MedDigtwin — AWS Marketplace Production Readiness

## Product

**MedDigtwin by EmergentSoft Corporation**  
Healthcare Operational Digital Twin.

Current product mode: synthetic operational healthcare data.

## Marketplace delivery model

Target: **AWS Marketplace SaaS Contract**.

Customer flow:

1. Customer subscribes in AWS Marketplace.
2. AWS Marketplace sends `x-amzn-marketplace-token` to `POST /marketplace/landing`.
3. MedDigtwin resolves the registration token server-side with `ResolveCustomer`.
4. Customer AWS account and LicenseArn are recorded.
5. MedDigtwin calls `GetEntitlements`.
6. An `awsmp-{customer_identifier}` tenant is provisioned idempotently.
7. The application uses the resulting tenant identity for isolation.
8. Entitlements are checked before paid access.
9. Entitlements should be revalidated when subscription state changes.

## AWS production baseline

The CDK stack now includes:

- VPC across two AZs
- ECS/Fargate
- ECR image scanning
- Cognito
- DynamoDB simulations
- DynamoDB audit
- DynamoDB Marketplace tenant registry
- CloudWatch Container Insights
- CloudWatch logs
- ALB
- HTTPS with ACM in production
- HTTP → HTTPS redirect
- AWS WAF managed common rule set
- IAM least-privilege application role
- AWS Marketplace ResolveCustomer/GetEntitlements permissions
- GitHub Actions OIDC
- point-in-time recovery on DynamoDB
- retained production data resources
- immutable container images in deployment workflow

## Required production inputs

The deployment workflow accepts:

- AWS Marketplace Product Code
- ACM certificate ARN
- public MedDigtwin domain
- production environment

The GitHub secret `AWS_GITHUB_ACTIONS_ROLE_ARN` must point to an IAM role trusted through GitHub OIDC.

## Security / healthcare boundary

MedDigtwin currently uses synthetic data.

Before processing real healthcare information, EmergentSoft and the customer must establish the applicable privacy, security, regulatory, contractual and data-governance requirements.

Marketplace entitlement is not clinical authorization.

MedDigtwin is an operational simulation product and does not by itself diagnose patients, prescribe treatment or replace qualified clinical judgment.

## NVIDIA integration targets

The product architecture already references:

- CUDA
- TensorRT
- Triton Inference Server
- NVIDIA NIM
- NGC
- NVIDIA AI Enterprise
- Omniverse / OpenUSD
- Modulus
- RAPIDS / cuDF
- NeMo

Recommended implementation boundary:

**MedDigtwin simulation/orchestration → NVIDIA acceleration adapter → GPU compute/inference**

This should remain optional until the corresponding NVIDIA workload is actually deployed and validated.

## Microsoft integration targets

Recommended enterprise adapters:

- Microsoft Foundry / Azure AI
- Azure OpenAI
- Microsoft Entra ID
- Microsoft Fabric
- Microsoft Defender for Cloud
- Microsoft Purview
- Power Platform
- Microsoft Teams
- Dynamics 365
- GitHub

Recommended boundary:

**MedDigtwin tenant/identity layer → Microsoft enterprise adapter → identity/data/security/workflow service**

These references do not by themselves represent Microsoft partnership, endorsement, certification or reseller authorization.

## Marketplace listing gates

- [ ] Seller account and Marketplace provider configuration validated
- [ ] SaaS Contract product configured
- [ ] Product Code confirmed
- [ ] Production HTTPS endpoint deployed
- [ ] DNS and ACM certificate validated
- [ ] ResolveCustomer E2E tested
- [ ] GetEntitlements E2E tested
- [ ] Tenant provisioning tested
- [ ] Cancellation/entitlement removal tested
- [ ] Customer onboarding tested
- [ ] Security documentation published
- [ ] Privacy/data handling documentation published
- [ ] Support contact and SLA documented
- [ ] Terms of Use published
- [ ] Privacy Policy published
- [ ] Product screenshots prepared
- [ ] Product description finalized
- [ ] Pricing dimensions finalized
- [ ] AWS Marketplace test transaction completed
- [ ] Production monitoring and incident response validated

## Current implementation status

The repository is technically structured for AWS deployment and now contains the Marketplace fulfillment integration. **This does not mean that the product is already published or buyable in AWS Marketplace.**

The remaining critical step is deployment and E2E validation against the actual AWS Marketplace product configuration.
