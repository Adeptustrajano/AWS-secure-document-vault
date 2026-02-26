"""Tests unitarios del servicio de cifrado (Fernet) — encryption_service."""
import pytest
from cryptography.fernet import Fernet

# Reutilizamos la clave de test ya definida en el entorno
from app.services.encryption_service import encrypt_file, decrypt_file


class TestEncryptFile:
    def test_encrypt_returns_bytes(self):
        """encrypt_file debe devolver bytes."""
        result = encrypt_file(b"contenido de prueba")
        assert isinstance(result, bytes)

    def test_encrypt_output_differs_from_input(self):
        """El contenido cifrado no debe ser igual al original."""
        original = b"documento confidencial"
        encrypted = encrypt_file(original)
        assert encrypted != original

    def test_encrypt_empty_content(self):
        """encrypt_file debe manejar contenido vacío sin errores."""
        result = encrypt_file(b"")
        assert isinstance(result, bytes)
        assert len(result) > 0  # Fernet siempre añade overhead (IV + HMAC)

    def test_encrypt_large_content(self):
        """encrypt_file debe manejar archivos grandes correctamente."""
        large_content = b"A" * 1_000_000  # 1 MB
        result = encrypt_file(large_content)
        assert isinstance(result, bytes)
        assert len(result) > len(large_content)


class TestDecryptFile:
    def test_decrypt_returns_original_content(self):
        """decrypt_file debe recuperar exactamente el contenido original."""
        original = b"hola mundo desde el vault"
        encrypted = encrypt_file(original)
        decrypted = decrypt_file(encrypted)
        assert decrypted == original

    def test_encrypt_decrypt_roundtrip_binary(self):
        """El ciclo cifrar/descifrar debe funcionar con contenido binario."""
        binary_content = bytes(range(256))
        assert decrypt_file(encrypt_file(binary_content)) == binary_content

    def test_decrypt_invalid_data_raises_http_exception(self):
        """Descifrar datos inválidos debe lanzar una HTTPException."""
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc_info:
            decrypt_file(b"datos_no_cifrados_invalidos")
        assert exc_info.value.status_code == 500

    def test_decrypt_tampered_data_raises_http_exception(self):
        """Descifrar datos manipulados (token corrupto) debe lanzar HTTPException."""
        from fastapi import HTTPException
        encrypted = encrypt_file(b"datos originales")
        # Corromper el token modificando bytes en el centro
        tampered = bytearray(encrypted)
        tampered[20] ^= 0xFF
        with pytest.raises(HTTPException):
            decrypt_file(bytes(tampered))
