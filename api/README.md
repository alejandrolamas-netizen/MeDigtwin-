# MedDigtwin API

Backend contract for the MedDigtwin SaaS evolution.

## Initial endpoints

- GET /health
- GET /api/v1/twin/state
- POST /api/v1/simulations
- GET /api/v1/simulations/{simulationId}
- POST /api/v1/scenarios/what-if
- GET /api/v1/bottlenecks

## Design rules

- Synthetic data only in the initial implementation.
- Every request is tenant-scoped.
- Authentication/authorization is enforced for the production environment through OIDC/Cognito-compatible JWT validation.
- Simulation inputs are validated server-side.
- No clinical diagnosis or treatment recommendation is exposed by this API.
- Secrets must come from a managed secret store, never from source control.

## AWS-ready deployment

The API is packaged as a container for Amazon ECS/Fargate behind an Application Load Balancer. The repository includes AWS CDK infrastructure, ECR image scanning, Cognito identity, DynamoDB persistence, audit logging, WAF support and GitHub Actions OIDC CI/CD.

A verified live AWS deployment is a separate operational milestone and must not be claimed until the corresponding AWS resources and health checks have been confirmed.
