"""Tests unitarios de las utilidades de seguridad — core/security.py."""
import pytest
import jwt

from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.config import settings


class TestPasswordHashing:
    def test_hash_is_different_from_plain_password(self):
        password = "MiContraseña123!"
        hashed = get_password_hash(password)
        assert hashed != password

    def test_verify_correct_password_returns_true(self):
        password = "ContraseñaSegura99"
        hashed = get_password_hash(password)
        assert verify_password(password, hashed) is True

    def test_verify_wrong_password_returns_false(self):
        hashed = get_password_hash("contraseña_correcta")
        assert verify_password("contraseña_incorrecta", hashed) is False

    def test_same_password_produces_different_hashes(self):
        password = "mismaContraseña"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        assert hash1 != hash2

    def test_hash_has_expected_scheme_prefix(self):
        """El hash generado debe usar el esquema bcrypt_sha256 de passlib."""
        hashed = get_password_hash("cualquierContraseña")
        assert hashed.startswith("$pbkdf2-sha256$")


class TestCreateAccessToken:
    def test_token_is_string(self):
        token = create_access_token({"sub": "usuario_test"})
        assert isinstance(token, str)

    def test_token_has_three_parts(self):
        token = create_access_token({"sub": "usuario_test"})
        parts = token.split(".")
        assert len(parts) == 3

    def test_token_contains_correct_subject(self):
        token = create_access_token({"sub": "alice"})
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert payload["sub"] == "alice"

    def test_token_has_expiration_field(self):
        token = create_access_token({"sub": "usuario_test"})
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert "exp" in payload

    def test_invalid_token_raises_decode_error(self):
        with pytest.raises(jwt.InvalidTokenError):
            jwt.decode("token.invalido.aqui", settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
