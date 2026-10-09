from types import SimpleNamespace
import sys

import pytest
from fastapi import HTTPException

from api import app as api_module


def test_twin_analyst_is_disabled_by_default(monkeypatch):
    monkeypatch.delenv("CLAUDE_ENABLED", raising=False)
    with pytest.raises(HTTPException) as exc:
        api_module.analyze_twin(
            api_module.TwinAnalysisRequest(question="Explain the simulated wait time"),
            identity={"tenant_id": "tenant-a", "role": "viewer"},
        )
    assert exc.value.status_code == 503
    assert "disabled" in exc.value.detail.lower()


def test_twin_analyst_fails_closed_without_quota_store(monkeypatch):
    monkeypatch.setenv("CLAUDE_ENABLED", "true")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-only-not-a-real-key")
    monkeypatch.setenv("CLAUDE_MODEL", "test-model")
    monkeypatch.setenv("CLAUDE_QUOTA_TABLE", "test-quota")
    monkeypatch.setattr(api_module, "_dynamodb", None)
    with pytest.raises(HTTPException) as exc:
        api_module.analyze_twin(
            api_module.TwinAnalysisRequest(question="Explain the simulated wait time"),
            identity={"tenant_id": "tenant-a", "role": "viewer"},
        )
    assert exc.value.status_code == 503
    assert "quota" in exc.value.detail.lower()


def test_twin_analyst_uses_server_context_and_returns_mocked_answer(monkeypatch):
    monkeypatch.setenv("CLAUDE_ENABLED", "true")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-only-not-a-real-key")
    monkeypatch.setenv("CLAUDE_MODEL", "test-model")
    monkeypatch.setenv("CLAUDE_MAX_OUTPUT_TOKENS", "300")
    monkeypatch.setattr(api_module, "_reserve_claude_quota", lambda tenant_id: None)
    monkeypatch.setattr(api_module, "audit", lambda *args, **kwargs: None)

    calls = {}

    class FakeMessages:
        def create(self, **kwargs):
            calls.update(kwargs)
            return SimpleNamespace(
                content=[SimpleNamespace(type="text", text="These are synthetic results.")],
                usage=SimpleNamespace(input_tokens=25, output_tokens=8),
            )

    class FakeAnthropic:
        def __init__(self, **kwargs):
            assert kwargs["api_key"] == "test-only-not-a-real-key"
            assert kwargs["timeout"] == 12.0
            assert kwargs["max_retries"] == 0
            self.messages = FakeMessages()

    monkeypatch.setitem(sys.modules, "anthropic", SimpleNamespace(Anthropic=FakeAnthropic))

    result = api_module.analyze_twin(
        api_module.TwinAnalysisRequest(
            question="Explain this scenario",
            scenario=api_module.SimulationInput(patient_demand_pct=120),
        ),
        identity={"tenant_id": "tenant-a", "role": "viewer"},
    )

    assert result.tenant_id == "tenant-a"
    assert result.mode == "synthetic"
    assert result.answer == "These are synthetic results."
    assert result.input_tokens == 25
    assert result.output_tokens == 8
    assert calls["max_tokens"] == 300
    assert "synthetic" in calls["system"].lower()
    assert "120" in calls["messages"][0]["content"]
    assert "Explain this scenario" in calls["messages"][0]["content"]


def test_api_responses_include_security_headers(monkeypatch):
    import asyncio
    from starlette.requests import Request
    from starlette.responses import Response

    monkeypatch.setenv("ENVIRONMENT", "production")
    scope = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": "GET",
        "scheme": "https",
        "path": "/health",
        "raw_path": b"/health",
        "query_string": b"",
        "headers": [],
        "client": ("127.0.0.1", 12345),
        "server": ("testserver", 443),
    }
    request = Request(scope)

    async def call_next(_request):
        return Response("ok")

    response = asyncio.run(api_module.add_security_headers(request, call_next))
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["referrer-policy"] == "no-referrer"
    assert response.headers["cache-control"] == "no-store"
    assert response.headers["strict-transport-security"].startswith("max-age=")
