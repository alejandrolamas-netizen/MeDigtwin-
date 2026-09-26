# MedDigtwin CDK

AWS CDK infrastructure for the MedDigtwin API.

## Resources

- VPC across two Availability Zones
- ECR repository with image scanning
- ECS Fargate cluster/service
- CloudWatch Logs
- IAM task and execution roles
- Application Load Balancer
- /health target health check

## Deployment prerequisites

Install Node.js, AWS CDK and configure an AWS account locally or through CI.

Then:

    npm install
    npx cdk bootstrap
    npm run build
    npx cdk synth
    npx cdk deploy

The first deployment requires an ECR image tagged latest.

## Security boundary

This stack is a deployment foundation, not a claim of production healthcare compliance. It uses synthetic data only. HTTPS, authentication, tenant authorization, WAF, Secrets Manager and production healthcare-data controls must be added before handling real regulated data.

Do not commit AWS credentials or secrets.
