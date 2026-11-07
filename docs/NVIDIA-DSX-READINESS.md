# NVIDIA DSX technical readiness — MedDigtwin

## Purpose

MedDigtwin is a synthetic-data operational digital-twin prototype for healthcare capacity planning. It models demand, nursing availability and ICU capacity, and supports scenario-based what-if analysis.

This document defines a credible engineering path toward demonstrating the workload on GPU infrastructure. It does not claim NVIDIA DSX, Dynamo, Run:ai, KAI Scheduler, GPU Operator, or NVIDIA AI Enterprise integration today.

## Demonstration objective

Show a reproducible workload lifecycle that an infrastructure team can inspect:

1. Generate a deterministic synthetic demand and capacity workload.
2. Execute scenario simulations through the existing API.
3. Record latency, throughput, CPU/memory utilization, queue depth and scenario completion.
4. Export a workload manifest and run metadata.
5. Compare a CPU baseline with a future GPU-enabled implementation only if a measured GPU implementation is added.
6. Preserve synthetic-only data boundaries.

## Candidate DSX / AI Factory mapping

| Area | Potential fit | Current evidence |
|---|---|---|
| Workload orchestration | Kubernetes / KAI Scheduler | Not integrated |
| GPU workload scheduling | Run:ai | Not integrated |
| Inference serving | NVIDIA Dynamo | Not integrated |
| Cluster operations | GPU Operator / AI Cluster Runtime | Not integrated |
| Workload observability | Workload Map / Fleet Intelligence | Not integrated |
| Model artifact delivery | Model Streamer | Not integrated |

These are candidate integration points, not existing capabilities.

## Required benchmark protocol

- Pin code revision, container image digest and dependency lockfiles.
- Publish hardware, driver, CUDA and runtime versions for every GPU experiment.
- Use fixed synthetic datasets, seeds, request mix and concurrency levels.
- Report p50/p95/p99 latency, throughput, error rate and resource utilization.
- Run at least three repetitions and publish raw measurements.
- Compare equivalent workloads; do not compare unlike CPU/GPU configurations.
- Record all failed runs and exclude no outliers without an explicit rationale.

## Security and data governance

- Synthetic data only. Never use real patient data in this demonstration.
- Keep credentials outside the repository and use short-lived OIDC credentials.
- Deploy only through the protected production GitHub Environment.
- Record the exact commit SHA and deployment artifact digest.

## Readiness status

- Existing: Python API, synthetic operational model, automated API tests, Docker build, CodeQL, Gitleaks, dependency audit and AWS deployment workflows.
- Added in this readiness branch: TypeScript CodeQL coverage, npm Dependabot, CDK CI and manual-only deployment triggers.
- Still required: configure required reviewers on GitHub Environment `production`, verify AWS OIDC trust conditions, run CI, capture benchmark evidence, and build a DSX/Kubernetes integration prototype.

## External representation

Describe this as an engineering prototype and an integration-ready exploration. Do not claim NVIDIA certification, partnership, endorsement, or production DSX integration unless separately confirmed.

## API load-probe harness

A dependency-free HTTP load probe is available at `tools/benchmark_api.py`. It posts a fixed synthetic scenario to `/api/v1/simulations` and records client-observed latency percentiles, throughput, status counts and errors as JSON.

Example (against an isolated synthetic environment only):

```bash
python tools/benchmark_api.py \\
  --base-url http://127.0.0.1:8000 \\
  --requests 200 \\
  --concurrency 10 \\
  --output benchmark-results/local-api.json
```

This is an API service load probe, not a GPU benchmark. The current `run_model` implementation is deterministic arithmetic; it does not contain a GPU inference workload. GPU-related claims require a separately implemented model-backed workload and measurements on identified GPU hardware. Keep raw result files with the commit SHA, container digest and environment manifest.
