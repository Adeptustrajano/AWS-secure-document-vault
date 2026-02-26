"""Tests unitarios de las utilidades de seguridad — core/security.py."""
import pytest
import jwt

from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.config import settings


class TestPasswordHashing:
    def test_hash_is_different_from_plain_password(self):
        """El hash no debe ser igual a la contraseña original."""
        password = "MiContraseña123!"
        hashed = get_password_hash(password)
        assert hashed != password

    def test_verify_correct_password_returns_true(self):
        """verify_password debe devolver True con la contraseña correcta."""
        password = "ContraseñaSegura99"
        hashed = get_password_hash(password)
        assert verify_password(password, hashed) is True

    def test_verify_wrong_password_returns_false(self):
        """verify_password debe devolver False con una contraseña incorrecta."""
        hashed = get_password_hash("contraseña_correcta")
        assert verify_password("contraseña_incorrecta", hashed) is False

    def test_same_password_produces_different_hashes(self):
        """bcrypt debe generar hashes diferentes para la misma contraseña (salt aleatorio)."""
        password = "mismaContraseña"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        assert hash1 != hash2

    def test_hash_prefix_is_bcrypt(self):
        """El hash generado debe comenzar con el prefijo de bcrypt."""
        hashed = get_password_hash("cualquierContraseña")
        assert hashed.startswith("$2b$")


class TestCreateAccessToken:
    def test_token_is_string(self):
        """create_access_token debe devolver una cadena de texto."""
        token = create_access_token({"sub": "usuario_test"})
        assert isinstance(token, str)

    def test_token_has_three_parts(self):
        """Un JWT debe tener tres partes separadas por puntos."""
        token = create_access_token({"sub": "usuario_test"})
        parts = token.split(".")
        assert len(parts) == 3

    def test_token_contains_correct_subject(self):
        """El payload del token debe contener el 'sub' correcto."""
        token = create_access_token({"sub": "alice"})
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert payload["sub"] == "alice"

    def test_token_has_expiration_field(self):
        """El payload del token debe incluir el campo de expiración 'exp'."""
        token = create_access_token({"sub": "usuario_test"})
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert "exp" in payload

    def test_token_with_custom_expiration(self):
        """create_access_token debe respetar el delta de expiración personalizado."""
        from datetime import timedelta, timezone, datetime
        delta = timedelta(hours=2)
        before = datetime.now(timezone.utc)
        token = create_access_token({"sub": "usuario_test"}, expires_delta=delta)
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        # La expiración debe estar aproximadamente 2 horas en el futuro (±5 segundos)
        expected = before + delta
        assert abs((exp - expected).total_seconds()) < 5

    def test_invalid_token_raises_decode_error(self):
        """Un token manipulado no debe poder decodificarse correctamente."""
        with pytest.raises(jwt.InvalidTokenError):
            jwt.decode("token.invalido.aqui", settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
