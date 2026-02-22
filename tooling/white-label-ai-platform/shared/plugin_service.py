"""Minimal AI plugin service scaffold.

Run:
  pip install fastapi uvicorn
  uvicorn plugin_service:app --host 0.0.0.0 --port 8100
"""

from datetime import datetime, UTC
from os import getenv
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field


class TrainRequest(BaseModel):
    dataset_uri: str
    hyperparameters: dict[str, Any] = Field(default_factory=dict)


class InferRequest(BaseModel):
    payload: dict[str, Any]


class UsageEvent(BaseModel):
    tenant_id: str
    workflow_id: str
    operation: str
    units: int = 1


PLUGIN_NAME = getenv("PLUGIN_NAME", "unknown-plugin")
PLUGIN_INDUSTRY = getenv("PLUGIN_INDUSTRY", "general")
PLUGIN_VERSION = getenv("PLUGIN_VERSION", "0.1.0")
PLUGIN_DESCRIPTION = getenv("PLUGIN_DESCRIPTION", "AI plugin service")

app = FastAPI(title=f"{PLUGIN_NAME} Service", version=PLUGIN_VERSION)


@app.get("/metadata")
def metadata() -> dict[str, str]:
    return {
        "name": PLUGIN_NAME,
        "industry": PLUGIN_INDUSTRY,
        "version": PLUGIN_VERSION,
        "description": PLUGIN_DESCRIPTION,
    }


@app.post("/train")
def train(req: TrainRequest) -> dict[str, Any]:
    return {
        "status": "accepted",
        "model_version": f"{PLUGIN_VERSION}-{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}",
        "dataset_uri": req.dataset_uri,
        "hyperparameters": req.hyperparameters,
    }


@app.post("/infer")
def infer(req: InferRequest) -> dict[str, Any]:
    # Placeholder inference response for integration wiring.
    return {
        "plugin": PLUGIN_NAME,
        "timestamp": datetime.now(UTC).isoformat(),
        "input": req.payload,
        "prediction": {
            "label": "ok",
            "score": 0.91,
            "reasoning": "baseline heuristic response"
        },
    }


@app.post("/events/usage")
def usage(req: UsageEvent) -> dict[str, Any]:
    return {
        "status": "recorded",
        "tenant_id": req.tenant_id,
        "workflow_id": req.workflow_id,
        "operation": req.operation,
        "units": req.units,
    }
