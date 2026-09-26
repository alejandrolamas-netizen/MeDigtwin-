# GitHub Actions → AWS OIDC setup

This procedure connects the repository to AWS without storing long-lived AWS access keys in GitHub.

## 1. Create the GitHub OIDC provider

In the AWS account, create the IAM OIDC provider:
- URL: https://token.actions.githubusercontent.com
- Audience: sts.amazonaws.com

## 2. Create the deployment role

Create an IAM role whose trust policy is based on infra/cdk/github-actions-oidc-policy.json.
Replace <AWS_ACCOUNT_ID> with the real AWS account ID.
The trust condition restricts role assumption to repo:alejandrolamas-netizen/MeDigtwin-:ref:refs/heads/main.

## 3. Attach deployment permissions

Use infra/cdk/github-actions-permissions.json.
Replace <AWS_ACCOUNT_ID> with the real account ID.
Review permissions before applying them to a production account.

## 4. Add the GitHub secret

Repository: alejandrolamas-netizen/MeDigtwin-
Secret: AWS_GITHUB_ACTIONS_ROLE_ARN
Value: arn:aws:iam::<AWS_ACCOUNT_ID>:role/<ROLE_NAME>

## 5. First AWS deployment

The CDK stack must be deployed before the application workflow can update ECS:

    cd infra/cdk
    npm install
    npx cdk bootstrap
    npm run build
    npx cdk synth
    npx cdk deploy

The first ECS deployment also requires an image in ECR tagged latest.

## 6. Security requirements

- Never commit AWS access keys.
- Keep GitHub OIDC restricted to the repository and main branch.
- Review IAM permissions before production use.
- Enable CloudTrail and appropriate audit logging.
- Add HTTPS, authentication, tenant authorization and WAF before production healthcare workloads.
- MedDigtwin currently uses synthetic data only.

## Current limitation

The repository can prepare this configuration, but actual IAM creation, CDK deployment and endpoint validation require access to the target AWS account. No AWS resource is considered deployed until AWS confirms successful creation.