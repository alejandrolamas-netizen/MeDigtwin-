from __future__ import annotations

from datetime import datetime, timezone
import os
from uuid import uuid4
from pathlib import Path
import boto3

from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWKClient, decode as jwt_decode
from pydantic import BaseModel, Field
import json


bearer_scheme = HTTPBearer(auto_error=False)
DATA_DIR = Path(os.getenv('DATA_DIR', '/tmp/meddigtwin-data'))
AUDIT_FILE = DATA_DIR / 'audit.jsonl'
SIMULATIONS_TABLE = os.getenv('DDB_SIMULATIONS_TABLE')
AUDIT_TABLE = os.getenv('DDB_AUDIT_TABLE')
_dynamodb = boto3.resource('dynamodb') if SIMULATIONS_TABLE or AUDIT_TABLE else None


def audit(event: str, identity: dict[str, str], details: dict) -> None:
    record = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'event': event,
        'tenant_id': identity.get('tenant_id'),
        'role': identity.get('role'),
        'details': details,
    }
    if AUDIT_TABLE and _dynamodb:
        _dynamodb.Table(AUDIT_TABLE).put_item(Item={
            'tenant_id': 'TENANT#' + str(identity.get('tenant_id')),
            'event_key': 'AUDIT#' + record['timestamp'] + '#' + str(uuid4()),
            **record,
        })
        return
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with AUDIT_FILE.open('a', encoding='utf-8') as fh:
        fh.write(json.dumps(record, separators=(',', ':')) + '\n')

def persist_simulation(result: SimulationResult) -> None:
    if SIMULATIONS_TABLE and _dynamodb:
        _dynamodb.Table(SIMULATIONS_TABLE).put_item(Item={
            'tenant_id': 'TENANT#' + result.tenant_id,
            'simulation_key': 'SIM#' + result.created_at + '#' + result.simulation_id,
            'simulation_id': result.simulation_id,
            'created_at': result.created_at,
            'inputs': result.inputs.model_dump(),
            'projected_arrivals': result.projected_arrivals,
            'bed_occupancy_pct': result.bed_occupancy_pct,
            'icu_occupancy_pct': result.icu_occupancy_pct,
            'avg_wait_min': result.avg_wait_min,
        })

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

def authenticated_tenant(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    x_tenant_id: str | None = Header(default=None),
) -> dict[str, str]:
    if os.getenv("ENVIRONMENT", "demo") != "production":
        return {"tenant_id": x_tenant_id or "demo-synthetic", "role": "demo"}

    issuer = os.getenv("OIDC_ISSUER")
    audience = os.getenv("OIDC_AUDIENCE")
    jwks_url = os.getenv("OIDC_JWKS_URL")
    if not issuer or not audience or not jwks_url:
        raise HTTPException(status_code=503, detail="OIDC configuration incomplete")
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Bearer token required")
    try:
        token = credentials.credentials
        key = PyJWKClient(jwks_url).get_signing_key_from_jwt(token).key
        claims = jwt_decode(token, key, algorithms=["RS256"], audience=audience, issuer=issuer)
        tenant_id = claims.get("tenant_id") or claims.get("custom:tenant_id")
        role = claims.get("role") or claims.get("custom:role") or "viewer"
        if not tenant_id:
            raise HTTPException(status_code=403, detail="tenant_id claim required")
        if role not in {"admin", "operator", "viewer"}:
            raise HTTPException(status_code=403, detail="Unsupported role")
        return {"tenant_id": str(tenant_id), "role": str(role)}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid OIDC token")

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
def twin_state(x_tenant_id: str | None = Header(default=None), identity: dict[str, str] = Depends(authenticated_tenant)) -> dict:
    return {
        "tenant_id": identity["tenant_id"],
        "role": identity["role"],
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
    identity: dict[str, str] = Depends(authenticated_tenant),
) -> SimulationResult:
    if identity["role"] not in {"admin", "operator", "demo"}:
        raise HTTPException(status_code=403, detail="operator role required")
    tenant_id = identity["tenant_id"]
    result = run_model(payload)
    simulation_id = str(uuid4())
    audit('simulation.created', identity, {'simulation_id': simulation_id, 'inputs': payload.model_dump()})
    output = SimulationResult(
        simulation_id=simulation_id,
        tenant_id=tenant_id,
        created_at=datetime.now(timezone.utc).isoformat(),
        inputs=payload,
        **result,
    )
    persist_simulation(output)
    return output

@app.get("/api/v1/simulations/{simulation_id}", response_model=SimulationResult)
def get_simulation(
    simulation_id: str,
    identity: dict[str, str] = Depends(authenticated_tenant),
) -> SimulationResult:
    if SIMULATIONS_TABLE and _dynamodb:
        from boto3.dynamodb.conditions import Key
        response = _dynamodb.Table(SIMULATIONS_TABLE).query(
            KeyConditionExpression=Key('tenant_id').eq('TENANT#' + identity['tenant_id']),
            ScanIndexForward=False,
            Limit=100,
        )
        for item in response.get('Items', []):
            if item.get('simulation_id') == simulation_id:
                return SimulationResult(
                    simulation_id=item['simulation_id'],
                    tenant_id=identity['tenant_id'],
                    created_at=item['created_at'],
                    inputs=SimulationInput(**item['inputs']),
                    projected_arrivals=int(item['projected_arrivals']),
                    bed_occupancy_pct=int(item['bed_occupancy_pct']),
                    icu_occupancy_pct=int(item['icu_occupancy_pct']),
                    avg_wait_min=int(item['avg_wait_min']),
                )
    raise HTTPException(status_code=404, detail="Simulation not found")


@app.post("/api/v1/scenarios/what-if", response_model=SimulationResult)
def what_if(
    payload: SimulationInput,
    x_tenant_id: str | None = Header(default=None),
    identity: dict[str, str] = Depends(authenticated_tenant),
) -> SimulationResult:
    return create_simulation(payload, x_tenant_id, identity)

@app.get("/api/v1/audit")
def audit_status(
    x_tenant_id: str | None = Header(default=None),
    identity: dict[str, str] = Depends(authenticated_tenant),
) -> dict:
    if identity["role"] not in {"admin", "demo"}:
        raise HTTPException(status_code=403, detail="admin role required")
    if AUDIT_TABLE and _dynamodb:
        from boto3.dynamodb.conditions import Key
        response = _dynamodb.Table(AUDIT_TABLE).query(
            KeyConditionExpression=Key('tenant_id').eq('TENANT#' + identity['tenant_id']),
            ScanIndexForward=False,
            Limit=100,
        )
        return {"tenant_id": identity["tenant_id"], "events": response.get("Items", [])}
    events = []
    if AUDIT_FILE.exists():
        for line in AUDIT_FILE.read_text(encoding="utf-8").splitlines()[-100:]:
            try:
                item = json.loads(line)
                if item.get("tenant_id") == identity["tenant_id"]:
                    events.append(item)
            except json.JSONDecodeError:
                continue
    return {"tenant_id": identity["tenant_id"], "events": events}

@app.get("/api/v1/bottlenecks")
def bottlenecks(
    x_tenant_id: str | None = Header(default=None),
    identity: dict[str, str] = Depends(authenticated_tenant),
) -> dict:
    return {
        "tenant_id": identity["tenant_id"],
        "mode": "synthetic",
        "items": [
            {"rank": 1, "resource": "Emergency capacity", "utilization_pct": 84, "signal": "HIGH"},
            {"rank": 2, "resource": "Nursing availability", "utilization_pct": 78, "signal": "WATCH"},
            {"rank": 3, "resource": "ICU capacity", "utilization_pct": 76, "signal": "WATCH"},
            {"rank": 4, "resource": "Operating rooms", "utilization_pct": 69, "signal": "NORMAL"},
            {"rank": 5, "resource": "Laboratory", "utilization_pct": 61, "signal": "NORMAL"},
        ],
    }
