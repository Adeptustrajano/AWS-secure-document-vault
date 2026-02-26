"""
Configuración compartida para todos los tests de la Fase 1.

Estrategia:
- Sustituye PostgreSQL por SQLite en memoria para tests locales (sin dependencias externas).
- Sobreescribe la dependencia `get_db` de FastAPI para que cada test use la BD de test.
- Limpia los datos entre tests para garantizar el aislamiento.
"""
import os

# IMPORTANTE: Establecer antes de importar cualquier módulo de la app.
# Esto hace que SQLAlchemy use SQLite en lugar de PostgreSQL durante los tests.
os.environ.setdefault("DATABASE_URL", "sqlite:///./tests/test_vault.db")
os.environ.setdefault("SECRET_KEY", "clave-secreta-solo-para-tests-automatizados-no-usar-en-prod")
os.environ.setdefault("ENCRYPTION_KEY", "L2xz2fJnTsQqGJZIOwtZ4g1t_EyTGxQzd-5CQANC_3k=")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base, get_db
from app.main import app

SQLALCHEMY_TEST_URL = "sqlite:///./tests/test_vault.db"

# Motor SQLite para tests (check_same_thread=False requerido por SQLite)
engine = create_engine(
    SQLALCHEMY_TEST_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def create_test_tables():
    """Crea todas las tablas una vez por sesión de tests."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    # Eliminar fichero de BD de test al terminar
    import pathlib
    pathlib.Path("tests/test_vault.db").unlink(missing_ok=True)


@pytest.fixture
def client(create_test_tables):
    """
    TestClient con la BD de test inyectada.
    Limpia las tablas después de cada test para garantizar aislamiento.
    """
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

    # Limpiar datos entre tests
    with engine.connect() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(table.delete())
        conn.commit()


@pytest.fixture
def registered_user(client):
    """Crea un usuario de prueba y devuelve sus credenciales."""
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
    """Devuelve un token JWT válido para el usuario de prueba."""
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": registered_user["username"],
            "password": registered_user["password"],
        },
    )
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token):
    """Cabeceras de autorización listas para usar en peticiones autenticadas."""
    return {"Authorization": f"Bearer {auth_token}"}
