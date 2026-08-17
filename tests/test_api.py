import pytest

from app import app


@pytest.fixture()
def client():
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_analyze_endpoint(client):
    response = client.post("/api/analyze", json={
        "mismatches": 2,
        "pam_correct": True,
        "in_exon": True,
        "conservation_score": 0.72,
        "gc_content": 0.48,
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 0 <= data["risk_score"] <= 100


def test_analyze_validates_required_fields(client):
    response = client.post("/api/analyze", json={"mismatches": 1})
    assert response.status_code == 400
    assert "Missing fields" in response.get_json()["error"]


def test_patterns_endpoint(client):
    response = client.get("/api/patterns")
    assert response.status_code == 200


def test_ecological_endpoint(client):
    response = client.post("/api/ecological-risk", json={
        "gene_drive": True,
        "off_target_sites": 2,
        "population_impact": 0.5,
        "uncertainty": 0.2,
    })
    assert response.status_code == 200
    assert "score" in response.get_json()


def test_regulatory_endpoint(client):
    response = client.post("/api/regulatory-assessment", json={
        "genetic_score": 90,
        "ecological_score": 80,
        "ethical_flags": 4,
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["level"] == "HIGH"
    assert "human review" in data["recommendation"].lower()


def test_ecological_validation(client):
    response = client.post("/api/ecological-risk", json={
        "gene_drive": True,
        "off_target_sites": -1,
        "population_impact": 0.5,
        "uncertainty": 0.2,
    })
    assert response.status_code == 400
