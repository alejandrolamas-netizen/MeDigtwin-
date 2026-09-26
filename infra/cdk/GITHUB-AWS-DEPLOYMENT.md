# AWS GitHub Actions deployment

The infrastructure workflow is `.github/workflows/deploy-infra.yml`.

## Required GitHub secret

Create `AWS_GITHUB_ACTIONS_ROLE_ARN` with the ARN of an AWS IAM role trusted by GitHub Actions OIDC for repository `alejandrolamas-netizen/MeDigtwin-`, branch `main`, audience `sts.amazonaws.com`.

## One-time AWS setup

1. Create the GitHub OIDC provider `token.actions.githubusercontent.com` in the AWS account.
2. Create the deployment role using `infra/cdk/github-actions-oidc-policy.json` as the trust-policy template, replacing the account placeholder.
3. Give that role permissions sufficient to deploy the resources declared in `infra/cdk/lib/meddigtwin-stack.ts`.
4. Complete CDK bootstrap for `us-east-1` with an appropriately privileged AWS identity.

Important: `github-actions-permissions.json` covers the application CI/CD path (ECR/ECS/PassRole). It is not a complete permission set for creating the entire CDK infrastructure stack. Do not grant broad administrator access merely to make the workflow pass; use a dedicated infrastructure-deployment role with the minimum required permissions.

## Execution

After the secret and AWS role are configured, run GitHub Actions workflow `Deploy MedDigtwin Infrastructure` manually.

The workflow authenticates through GitHub OIDC, builds the CDK app, bootstraps, synthesizes, deploys `MedDigtwinStack`, and verifies CloudFormation status.

No AWS credentials or access keys are stored in the repository.