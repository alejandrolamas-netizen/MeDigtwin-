# Claude integration boundary — MedDigtwin

**Status:** design decision only. This document does not claim that Claude is integrated, deployed, or tested.

## Why this belongs in the API

The current prototype has a browser UI in `index.html` and a FastAPI service in `api/app.py`. The UI already calls `/api/v1/simulations` when `window.MEDDIGTWIN_API_BASE` is configured. Claude must be called by the server, never directly by the browser.

## First use case

A read-only **Twin Analyst** may explain synthetic twin state, describe bottlenecks, and summarize or compare existing simulation outputs. The model is an explanation layer; `run_model` and the simulator remain the source of numeric results.

### Allowed
- Read allowlisted, synthetic state and simulation summaries from the current tenant.
- Return a bounded explanation with explicit uncertainty and a reminder that results are simulated.
- Record minimal audit metadata (tenant, request ID, model identifier, token counts when available, outcome and timestamp).

### Not allowed in the first release
- Clinical diagnosis, treatment advice, or claims of clinical validation.
- Real patient data, PHI, identifiers, secrets, or unapproved external data.
- Writing simulation state, changing configuration, calling arbitrary URLs, executing tools, triggering workflows, or controlling physical systems.
- Treating model output as an authoritative operational instruction.

## Proposed API boundary

Only after implementation and tests are added, expose a dedicated authenticated endpoint such as `POST /api/v1/twin/analysis`. It must use `authenticated_tenant`, enforce tenant isolation, accept a narrow request schema with length limits, and assemble context from server-side allowlisted data. Do not accept arbitrary client-supplied system prompts or raw tenant identity as authorization.

The endpoint must not be enabled by default. Use explicit configuration such as `CLAUDE_ENABLED=false`; if disabled, unconfigured, or unable to enforce quotas, fail closed without calling the provider. The browser must never receive the Anthropic API key.

## Security and spend gates

1. Store `ANTHROPIC_API_KEY` in an approved secret store (for AWS deployments, evaluate Secrets Manager and task-role access); never put it in source, logs, HTML, or client configuration.
2. Make the model ID configurable and verify it against the Anthropic account/API before use.
3. Set a low output-token ceiling, request timeout, bounded retries (default zero retries for the first pilot), and maximum input size.
4. Enforce a durable, atomic per-tenant request/token quota. An in-process counter alone is insufficient for multiple ECS tasks. If the quota store is unavailable, reject the request.
5. Set a provider/account spend limit or alert separately where available. Application quotas are defense in depth, not a guarantee of a hard dollar cap.
6. Do not log API keys, full prompts, or full model responses by default. Redact errors and avoid sending patient information.
7. Keep the feature read-only and disabled in production until security and operational review is complete.

## Required tests before enabling

- Unit tests with a mocked Anthropic client; tests must not make paid network calls.
- Disabled/unconfigured mode returns safely without provider invocation.
- Viewer/operator authorization and tenant isolation are enforced.
- Request size, output-token ceiling, timeout, provider error and quota-exhaustion paths are covered.
- Quota-store failure fails closed; no state-changing tools or simulation writes occur.
- Logs and error responses do not disclose credentials or sensitive input.
- Existing simulation and health routes remain unchanged.

## Repository audit notes

- `api/app.py` contains FastAPI routes and `authenticated_tenant`; the simulation model is deterministic and synthetic.
- `api/requirements.txt` does not currently declare the Anthropic SDK.
- No automated test files were found in the test paths inspected during this audit. Test discovery and the actual test command must be confirmed before implementation.
- `infra/README.md` describes the infrastructure target, and `infra/cdk/lib/meddigtwin-stack.ts` defines the ECS task environment. Any secret/quota infrastructure change requires a separate reviewed implementation; it is not included in this documentation-only change.

## Implementation acceptance checklist

- [ ] Confirm supported Anthropic model ID and current account spend controls.
- [ ] Implement server-side provider adapter and narrow response schema.
- [ ] Implement durable per-tenant quotas and secret injection.
- [ ] Add mocked unit/API tests and run the repository's available checks.
- [ ] Review privacy, tenant isolation, logs, timeout, and failure behavior.
- [ ] Keep feature off until all gates pass; deploy only through a reviewed release process.
