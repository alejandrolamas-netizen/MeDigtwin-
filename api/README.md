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
- Authentication/authorization is mandatory before production exposure.
- Simulation inputs are validated server-side.
- No clinical diagnosis or treatment recommendation is exposed by this API.
- Secrets must come from a managed secret store, never from source control.

## Target deployment

The API is intended to run as a container on Amazon ECS/Fargate behind a controlled HTTPS/API boundary. Infrastructure-as-code and production authentication are still required before deployment.
