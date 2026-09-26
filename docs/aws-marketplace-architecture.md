# MedDigtwin — AWS Marketplace Deployment Architecture

## Objective

Evolve the current MedDigtwin browser prototype into a deployable AWS architecture suitable for a future AWS Marketplace SaaS listing.

## Recommended initial model

**SaaS contract / centralized application architecture**

The first production architecture should keep the application operated by EmergentSoft while customers access an isolated tenant experience.

### Logical architecture

Customer Browser
→ CloudFront
→ Application/API layer
→ Authentication and tenant authorization
→ MedDigtwin simulation services
→ Event/data services
→ Operational data store
→ Observability and audit

### AWS building blocks to evaluate

- Amazon CloudFront — global delivery
- Amazon S3 — static frontend assets where appropriate
- Amazon ECS on AWS Fargate — API and simulation services
- Amazon API Gateway — API boundary where appropriate
- Amazon Cognito or an enterprise identity integration — authentication
- Amazon Aurora PostgreSQL or Amazon DynamoDB — application state, depending on data model
- Amazon S3 — simulation datasets and artifacts
- Amazon EventBridge — domain events
- Amazon CloudWatch — logs, metrics and alarms
- AWS IAM — least-privilege service authorization
- AWS KMS — encryption key management
- AWS Secrets Manager — application secrets
- AWS WAF — web application protection

These services are architectural candidates, not claims that they are currently deployed.

## Tenant isolation

The application should use a tenant-aware authorization model.

Minimum logical controls:

- tenant identifier on authenticated sessions
- authorization checks at API boundaries
- tenant-scoped database access
- tenant-scoped object storage paths
- audit events containing tenant context
- administrative access separated from customer access

A stronger isolation model can be introduced for customers requiring dedicated infrastructure.

## MedDigtwin application layers

### 1. Presentation

Current HTML/JavaScript prototype becomes the frontend application.

Responsibilities:

- operational dashboard
- digital twin visualization
- simulation controls
- what-if scenarios
- bottleneck analysis
- architecture/status views

### 2. API

The backend exposes controlled operations such as:

- retrieve operational state
- create simulation
- execute simulation
- retrieve simulation result
- compare scenarios
- retrieve bottlenecks
- retrieve audit events

### 3. Simulation engine

The current browser simulation logic should be moved behind a server-side service before production use.

Responsibilities:

- demand modeling
- workforce constraints
- ICU capacity
- laboratory throughput
- bed occupancy
- wait-time estimation
- scenario execution

### 4. Data layer

Separate:

- configuration
- synthetic/demo datasets
- customer operational datasets
- simulation results
- audit records

Production healthcare data must never be mixed with the repository's demo data.

### 5. Event layer

EventBridge can provide a future event-driven integration boundary for operational events.

Potential events:

- patient-flow state update
- bed-capacity update
- workforce update
- laboratory throughput update
- simulation completed
- scenario created

## NVIDIA integration boundary

NVIDIA acceleration should be introduced as an optional compute layer rather than making the initial Marketplace architecture dependent on it.

Potential future workloads:

- GPU-accelerated simulation
- AI inference
- large-scale scenario evaluation
- digital-world visualization
- accelerated analytics

The Marketplace product should remain architecturally coherent without claiming NVIDIA deployment until it is actually implemented.

## Security baseline

Before production:

- IAM least privilege
- encrypted data at rest
- TLS in transit
- Secrets Manager for secrets
- KMS for key management
- CloudWatch logging and monitoring
- audit trail
- WAF for public endpoints
- dependency/security scanning
- protected CI/CD branches
- environment separation
- backup and recovery procedures
- incident-response procedure

## Healthcare boundary

The current product uses synthetic data.

Any deployment handling real healthcare information requires a separate security, privacy, legal and compliance assessment appropriate to the jurisdictions and customer requirements.

MedDigtwin should not be marketed as a clinical decision-making system unless a separate validated and regulated product scope is established.

## CI/CD

Recommended evolution:

GitHub
→ CI checks
→ container build
→ vulnerability scanning
→ Amazon ECR
→ deployment to ECS
→ CloudWatch monitoring

Infrastructure should be defined as code.

Candidate approaches:

- AWS CDK
- AWS CloudFormation
- Terraform, if selected by the engineering organization

## Marketplace readiness gates

Before AWS Marketplace submission:

1. Deploy a functional customer-accessible environment.
2. Validate authentication and tenant isolation.
3. Validate billing/entitlement integration required by the selected Marketplace model.
4. Validate monitoring and support procedures.
5. Produce architecture documentation.
6. Produce security documentation.
7. Produce product screenshots.
8. Validate onboarding.
9. Validate customer cancellation/deprovisioning.
10. Complete AWS Marketplace provider/product requirements applicable to the selected model.

## Current status

The GitHub repository currently contains the browser prototype and Marketplace listing draft.

The AWS infrastructure described here is a target architecture and must not be represented as deployed until implementation and validation are complete.

**Product:** MedDigtwin  
**Publisher:** EmergentSoft Corporation  
**Website:** https://emergentsoft.io
