import os
from cryptography.fernet import Fernet
from fastapi import HTTPException

# En un entorno real, esta clave NUNCA debe estar en el código.
# Debe venir de las variables de entorno o de un servicio como AWS KMS.
# Para generarla por primera vez puedes usar en consola: 
# python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", Fernet.generate_key().decode())

try:
    cipher_suite = Fernet(ENCRYPTION_KEY.encode())
except ValueError:
    raise RuntimeError("La ENCRYPTION_KEY no es válida. Debe ser una clave base64 de 32 bytes.")

def encrypt_file(file_content: bytes) -> bytes:
    """
    Toma el contenido de un archivo en bytes y devuelve el contenido cifrado.
    """
    try:
        encrypted_data = cipher_suite.encrypt(file_content)
        return encrypted_data
    except Exception as e:
        # Registramos el error pero no exponemos detalles internos
        print(f"Error durante el cifrado: {e}")
        raise HTTPException(status_code=500, detail="Error al cifrar el documento.")

def decrypt_file(encrypted_content: bytes) -> bytes:
    """
    Toma el contenido de un archivo cifrado en bytes y lo descifra.
    """
    try:
        decrypted_data = cipher_suite.decrypt(encrypted_content)
        return decrypted_data
    except Exception as e:
        print(f"Error durante el descifrado: {e}")
        raise HTTPException(status_code=500, detail="Error al descifrar el documento o clave inválida.")