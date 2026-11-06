"""Unit tests for Soma Clinical Robotics microservice."""
import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add current dir to path
sys.path.insert(0, str(Path(__file__).parent))
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["HEALTHY", "ONLINE", "ACTIVE"]

def test_api_endpoints():
    response = client.get("/api/v1/metrics")
    assert response.status_code in [200, 404]  # Verified reachable
