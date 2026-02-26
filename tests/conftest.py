"""
Configuración compartida para todos los tests de la Fase 1.

Estrategia robusta para CI:
- Fuerza variables de entorno de test ANTES de importar la app.
- Usa SQLite en memoria con StaticPool para compartir la misma conexión.
- Crea tablas al inicio de la sesión y limpia datos tras cada test.
"""
import os

# Debe ir antes de importar módulos de app
os.environ["DATABASE_URL"] = "sqlite://"
os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("ENCRYPTION_KEY", "L2xz2fJnTsQqGJZIOwtZ4g1t_EyTGxQzd-5CQANC_3k=")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.database import Base, get_db
from app.main import app

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # clave para estabilidad con TestClient/threads
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def create_test_tables():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(create_test_tables):
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

    # Limpieza completa tras cada test
    with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(table.delete())


@pytest.fixture
def registered_user(client):
    credentials = {
        "username": "testuser",
        "password": "TestPass123!",
        "email": "testuser@example.com",
    }
    client.post(
        "/api/v1/auth/register",
        params={
            "username": credentials["username"],
            "email": credentials["email"],
            "password": credentials["password"],
        },
    )
    return credentials


@pytest.fixture
def auth_token(client, registered_user):
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": registered_user["username"],
            "password": registered_user["password"],
        },
    )
    body = response.json()
    return body["access_token"]


@pytest.fixture
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}
