from __future__ import annotations

import pytest
from fastapi import HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from api import app as api


def test_simulation_model_returns_synthetic_metrics() -> None:
    result = api.run_model(api.SimulationInput())

    assert result == {
        "projected_arrivals": 428,
        "bed_occupancy_pct": 82,
        "icu_occupancy_pct": 76,
        "avg_wait_min": 43,
    }


def test_twin_analysis_is_disabled_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CLAUDE_ENABLED", raising=False)
    request = api.TwinAnalysisRequest(question="Explain the synthetic capacity metrics")

    with pytest.raises(HTTPException) as exc:
        api.analyze_twin(request, {"tenant_id": "test-tenant", "role": "demo"})

    assert exc.value.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert exc.value.detail == "Twin Analyst is disabled"


def test_twin_analysis_rejects_short_questions() -> None:
    with pytest.raises(ValidationError):
        api.TwinAnalysisRequest(question="no")


def test_production_authentication_requires_bearer_token(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("OIDC_ISSUER", "https://issuer.example.invalid")
    monkeypatch.setenv("OIDC_AUDIENCE", "meddigtwin-test")
    monkeypatch.setenv("OIDC_JWKS_URL", "https://issuer.example.invalid/.well-known/jwks.json")

    with pytest.raises(HTTPException) as exc:
        api.authenticated_tenant(credentials=None, x_tenant_id="attacker-selected-tenant")

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == "Bearer token required"


def test_cors_is_explicit_origin_only() -> None:
    cors = [middleware for middleware in api.app.user_middleware if middleware.cls is CORSMiddleware]

    assert len(cors) == 1
    options = cors[0].kwargs
    assert options["allow_origins"] == []
    assert options["allow_credentials"] is False
    assert "Authorization" in options["allow_headers"]
    assert "OPTIONS" in options["allow_methods"]
