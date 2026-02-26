"""Tests del módulo de autenticación — /api/v1/auth/*."""
import pytest


# ---------------------------------------------------------------------------
# POST /api/v1/auth/register
# ---------------------------------------------------------------------------

class TestRegister:
    def test_register_new_user_returns_200(self, client):
        """Registrar un usuario nuevo debe devolver HTTP 200."""
        response = client.post(
            "/api/v1/auth/register",
            params={"username": "alice", "email": "alice@example.com", "password": "Secret1!"},
        )
        assert response.status_code == 200

    def test_register_new_user_returns_success_message(self, client):
        """La respuesta de registro debe contener el nombre de usuario creado."""
        response = client.post(
            "/api/v1/auth/register",
            params={"username": "bob", "email": "bob@example.com", "password": "Secret2!"},
        )
        data = response.json()
        assert "user" in data
        assert data["user"] == "bob"

    def test_register_duplicate_user_returns_400(self, client):
        """Intentar registrar un usuario ya existente debe devolver HTTP 400."""
        params = {"username": "carol", "email": "carol@example.com", "password": "Secret3!"}
        client.post("/api/v1/auth/register", params=params)
        response = client.post("/api/v1/auth/register", params=params)
        assert response.status_code == 400

    def test_register_duplicate_user_error_detail(self, client):
        """El error de usuario duplicado debe incluir detalle explicativo."""
        params = {"username": "dave", "email": "dave@example.com", "password": "Secret4!"}
        client.post("/api/v1/auth/register", params=params)
        response = client.post("/api/v1/auth/register", params=params)
        assert "detail" in response.json()


# ---------------------------------------------------------------------------
# POST /api/v1/auth/login
# ---------------------------------------------------------------------------

class TestLogin:
    def test_login_valid_credentials_returns_200(self, client, registered_user):
        """Login con credenciales correctas debe devolver HTTP 200."""
        response = client.post(
            "/api/v1/auth/login",
            data={"username": registered_user["username"], "password": registered_user["password"]},
        )
        assert response.status_code == 200

    def test_login_returns_access_token(self, client, registered_user):
        """Login exitoso debe devolver un access_token JWT."""
        response = client.post(
            "/api/v1/auth/login",
            data={"username": registered_user["username"], "password": registered_user["password"]},
        )
        data = response.json()
        assert "access_token" in data
        assert len(data["access_token"]) > 0

    def test_login_returns_bearer_token_type(self, client, registered_user):
        """El tipo de token devuelto debe ser 'bearer'."""
        response = client.post(
            "/api/v1/auth/login",
            data={"username": registered_user["username"], "password": registered_user["password"]},
        )
        assert response.json()["token_type"] == "bearer"

    def test_login_wrong_password_returns_400(self, client, registered_user):
        """Login con contraseña incorrecta debe devolver HTTP 400."""
        response = client.post(
            "/api/v1/auth/login",
            data={"username": registered_user["username"], "password": "wrongpassword"},
        )
        assert response.status_code == 400

    def test_login_nonexistent_user_returns_400(self, client):
        """Login con usuario inexistente debe devolver HTTP 400."""
        response = client.post(
            "/api/v1/auth/login",
            data={"username": "nobody", "password": "pass"},
        )
        assert response.status_code == 400


# ---------------------------------------------------------------------------
# GET /api/v1/auth/me
# ---------------------------------------------------------------------------

class TestMe:
    def test_me_with_valid_token_returns_200(self, client, auth_headers):
        """El endpoint /me con token válido debe devolver HTTP 200."""
        response = client.get("/api/v1/auth/me", headers=auth_headers)
        assert response.status_code == 200

    def test_me_returns_username(self, client, auth_headers, registered_user):
        """El endpoint /me debe devolver el nombre del usuario autenticado."""
        response = client.get("/api/v1/auth/me", headers=auth_headers)
        data = response.json()
        assert "user" in data
        assert data["user"]["username"] == registered_user["username"]

    def test_me_without_token_returns_401(self, client):
        """El endpoint /me sin token debe devolver HTTP 401."""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401

    def test_me_with_invalid_token_returns_401(self, client):
        """El endpoint /me con un token inválido debe devolver HTTP 401."""
        headers = {"Authorization": "Bearer token.invalido.aqui"}
        response = client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == 401
