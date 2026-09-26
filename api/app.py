from __future__ import annotations

from datetime import datetime, timezone
import os
from uuid import uuid4

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="MedDigtwin API",
    version="0.1.0",
    description="Synthetic healthcare operational simulation API.",
)

BASELINE = {
    "arrivals_per_day": 428,
    "bed_occupancy_pct": 82,
    "icu_occupancy_pct": 76,
    "avg_wait_min": 43,
}

class SimulationInput(BaseModel):
    patient_demand_pct: float = Field(100, ge=60, le=150)
    nursing_availability_pct: float = Field(100, ge=50, le=120)
    icu_capacity_pct: float = Field(100, ge=60, le=140)
    laboratory_throughput_pct: float = Field(100, ge=60, le=140)

class SimulationResult(BaseModel):
    simulation_id: str
    tenant_id: str
    created_at: str
    inputs: SimulationInput
    projected_arrivals: int
    bed_occupancy_pct: int
    icu_occupancy_pct: int
    avg_wait_min: int

def tenant_or_demo(x_tenant_id: str | None) -> str:
    # Demo-only fallback. Production must use an authenticated identity provider.
    if os.getenv("ENVIRONMENT", "demo") == "production":
        raise HTTPException(status_code=401, detail="Authenticated tenant identity required")
    return x_tenant_id or "demo-synthetic"

def run_model(x: SimulationInput) -> dict[str, int]:
    arrivals = BASELINE["arrivals_per_day"] * x.patient_demand_pct / 100
    beds = min(
        99,
        BASELINE["bed_occupancy_pct"]
        + (x.patient_demand_pct - 100) * 0.22
        + (100 - x.nursing_availability_pct) * 0.12,
    )
    icu = min(
        99,
        BASELINE["icu_occupancy_pct"]
        + (x.patient_demand_pct - 100) * 0.25
        - (x.icu_capacity_pct - 100) * 0.45,
    )
    wait = max(
        12,
        BASELINE["avg_wait_min"]
        * (x.patient_demand_pct / 100)
        * (100 / x.nursing_availability_pct)
        * (100 / x.laboratory_throughput_pct),
    )
    return {
        "projected_arrivals": round(arrivals),
        "bed_occupancy_pct": round(beds),
        "icu_occupancy_pct": round(icu),
        "avg_wait_min": round(wait),
    }

@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "service": "meddigtwin-api",
        "synthetic_environment": True,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

@app.get("/api/v1/twin/state")
def twin_state(x_tenant_id: str | None = Header(default=None)) -> dict:
    return {
        "tenant_id": tenant_or_demo(x_tenant_id),
        "mode": "synthetic",
        "state": BASELINE,
        "domains": 8,
        "systems": 16,
        "relationships": 27,
        "horizon_hours": 24,
    }

@app.post("/api/v1/simulations", response_model=SimulationResult)
def create_simulation(
    payload: SimulationInput,
    x_tenant_id: str | None = Header(default=None),
) -> SimulationResult:
    tenant_id = tenant_or_demo(x_tenant_id)
    result = run_model(payload)
    return SimulationResult(
        simulation_id=str(uuid4()),
        tenant_id=tenant_id,
        created_at=datetime.now(timezone.utc).isoformat(),
        inputs=payload,
        **result,
    )

@app.post("/api/v1/scenarios/what-if", response_model=SimulationResult)
def what_if(
    payload: SimulationInput,
    x_tenant_id: str | None = Header(default=None),
) -> SimulationResult:
    return create_simulation(payload, x_tenant_id)

@app.get("/api/v1/bottlenecks")
def bottlenecks(x_tenant_id: str | None = Header(default=None)) -> dict:
    return {
        "tenant_id": tenant_or_demo(x_tenant_id),
        "mode": "synthetic",
        "items": [
            {"rank": 1, "resource": "Emergency capacity", "utilization_pct": 84, "signal": "HIGH"},
            {"rank": 2, "resource": "Nursing availability", "utilization_pct": 78, "signal": "WATCH"},
            {"rank": 3, "resource": "ICU capacity", "utilization_pct": 76, "signal": "WATCH"},
            {"rank": 4, "resource": "Operating rooms", "utilization_pct": 69, "signal": "NORMAL"},
            {"rank": 5, "resource": "Laboratory", "utilization_pct": 61, "signal": "NORMAL"},
        ],
    }
