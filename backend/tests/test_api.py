"""
Integration & API unit tests for FastAPI backend endpoints.
"""

import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# Add backend directory to sys.path
backend_dir = str(Path(__file__).resolve().parent.parent)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.main import app
from app.database.session import init_db

# Initialize tables before running tests
init_db()

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "health_check" in data


def test_health_check_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "ai_model_loaded" in data


def test_predict_endpoint():
    payload = {
        "location": {"latitude": 30.3165, "longitude": 78.0322},
        "timestamp": "2025-08-20T12:00:00Z",
        "terrain": {"elevation": 1820.4, "slope": 34.7, "twi": 7.4},
        "rainfall": {"rain_1h": 18.2, "rain_24h": 84.5, "rain_3d": 162.2, "rain_7d": 280.1, "rain_14d": 421.3}
    }
    response = client.post("/api/v1/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "landslide_probability" in data
    assert "risk_score" in data
    assert "risk_level" in data
    assert 0 <= data["risk_score"] <= 100
    assert data["risk_level"] in ["LOW", "MODERATE", "HIGH", "CRITICAL"]


def test_citizen_report_endpoints():
    report_payload = {
        "latitude": 30.3165,
        "longitude": 78.0322,
        "reporter_name": "Test Reporter",
        "severity": 2,
        "description": "Roadside soil slippage observed."
    }

    # Test submission
    post_res = client.post("/api/v1/reports", json=report_payload)
    assert post_res.status_code == 201
    created_data = post_res.json()
    assert created_data["reporter_name"] == "Test Reporter"
    assert created_data["severity"] == 2
    assert "report_id" in created_data

    # Test retrieval
    get_res = client.get("/api/v1/reports")
    assert get_res.status_code == 200
    reports = get_res.json()
    assert isinstance(reports, list)
    assert len(reports) > 0
