"""Tests del endpoint de salud (Health Check) — GET /health."""
import pytest


def test_health_check_returns_200(client):
    """El endpoint /health debe responder con HTTP 200."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_check_status_ok(client):
    """El cuerpo de /health debe indicar status 'ok'."""
    response = client.get("/health")
    data = response.json()
    assert data["status"] == "ok"


def test_health_check_has_message(client):
    """El cuerpo de /health debe incluir un campo 'message'."""
    response = client.get("/health")
    data = response.json()
    assert "message" in data
    assert len(data["message"]) > 0
