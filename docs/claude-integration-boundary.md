# Claude Twin Analyst — MedDigtwin

**Status:** implementation added on the feature branch; not merged, deployed, or verified against the live Anthropic API. The feature is disabled by default.

## Pilot capability

The API exposes `POST /api/v1/twin/analysis`. It accepts a bounded question (5–800 characters) and an optional validated simulation scenario. The server runs the existing deterministic simulator and supplies only server-generated synthetic baseline, scenario outputs, and operational signals to Claude.

Example request:

```json
{
  "question": "Explain the simulated wait time and suggest scenarios to compare.",
  "scenario": {
    "patient_demand_pct": 120,
    "nursing_availability_pct": 100,
    "icu_capacity_pct": 100,
    "laboratory_throughput_pct": 100
  }
}
```

The endpoint returns a request ID, tenant ID, configured model, explanation, and token usage when the provider supplies it. It does not persist or mutate simulation state.

The `index.html` interface includes a Twin Analyst page. Configure the static page's host application before use:
- Set `window.MEDDIGTWIN_API_BASE` to the API origin (without a trailing slash).
- For authenticated use, have the host application's login layer supply a short-lived access token through `window.MEDDIGTWIN_AUTH_TOKEN`; this must be an OIDC access token accepted by the API, never the Anthropic key.
- Only in an isolated synthetic demo, explicitly set `window.MEDDIGTWIN_DEMO_MODE = true` to send the demo tenant header. Do not enable this for production.
- The browser must never receive `ANTHROPIC_API_KEY`.

## Safety and spend controls in this branch

- `CLAUDE_ENABLED` defaults to false; the CDK task environment explicitly sets it to false.
- The Anthropic SDK is called server-side only. The API key is read from `ANTHROPIC_API_KEY`; it is never returned to the browser.
- The optional CDK secret integration imports a Secrets Manager secret by ARN and injects its value into the ECS container. Store the raw API key as the secret value, not a JSON object.
- A new DynamoDB quota table uses partition key `tenant_id` and sort key `period_key`. A conditional atomic update reserves one request per tenant per UTC month before the provider call. The default limit is 50 requests per tenant per month; configuration is bounded to 1–1000.
- Maximum output defaults to 600 tokens and is bounded to 128–800. The provider call has a 12-second timeout and zero automatic retries.
- If the quota table is missing or unavailable, the endpoint fails closed. Quota reservation happens before the provider call, so a failed provider call still consumes one request.
- Request text and full provider responses are not included in audit metadata. Provider errors are returned as a generic error.
- The model ID must be explicitly configured with CDK context `claudeModel`; validate that model ID and API access in the Anthropic account before enabling.
- Application request quotas are not a hard monetary spend cap. Configure account-level billing alerts or limits separately where available.

## Explicit boundaries

- Synthetic operational data only; no real patient data, PHI, identifiers, secrets, or unapproved external data.
- No diagnosis, treatment recommendations, patient-level decisions, or claims of clinical validation.
- No arbitrary tools, external URLs, workflow triggers, state writes, or physical-system control.
- The simulator remains the source of numeric results. Claude is an explanation layer, not an authority for operational instructions.
- Existing tenant authentication is used. Production requests must be authenticated through the configured OIDC identity provider.

## Test coverage added

`api/tests/test_twin_analyst.py` includes mocked tests for disabled-by-default behavior, fail-closed quota configuration, and a mocked provider response. These tests do not make paid network calls. **They have not been executed in this environment**, so passing status is not claimed.

Run from the repository root after installing API requirements and pytest:

```bash
python -m pytest api/tests/test_twin_analyst.py -q
```

## Setup checklist — do not enable before review

1. Review this branch and run the mocked tests plus existing repository checks.
2. Create a Secrets Manager secret containing the raw Anthropic API key. Never commit the key or send it in chat.
3. Configure CDK context with the secret ARN and a model ID verified for the Anthropic account, for example `anthropicSecretArn=...` and `claudeModel=...`. Do not set the API key itself as CDK context.
4. Review the CDK diff, IAM grants, DynamoDB quota table, network egress, logging, and tenant isolation.
5. Verify Anthropic billing and set account-level spend alerts/limits where available.
6. Only after approval and tests, make a separate reviewed change to enable `CLAUDE_ENABLED`. This branch deliberately keeps it off.
7. Deploy only through the normal reviewed release path, then run a synthetic-data smoke test and monitor token usage and errors.

## Repository facts

- API: `api/app.py`
- Dependency: `api/requirements.txt`
- Mocked tests: `api/tests/test_twin_analyst.py`
- Browser interface: `index.html` (Twin Analyst page)
- AWS CDK: `infra/cdk/lib/meddigtwin-stack.ts`
- No claim is made that AWS resources are deployed or that a live Anthropic request has succeeded.
