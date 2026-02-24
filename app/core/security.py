from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from passlib.context import CryptContext
from app.core.config import settings

# Contexto para encriptar contraseñas usando bcrypt
# bcrypt es un algoritmo de hashing de contraseñas que es resistente a ataques de fuerza bruta y es ampliamente utilizado en aplicaciones web para almacenar contraseñas de manera segura.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# La función verify_password se encarga de verificar si una contraseña en texto plano coincide con su hash almacenado.
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# La función get_password_hash se encarga de generar un hash seguro para una contraseña dada utilizando el contexto de encriptación definido anteriormente.
# Esto es importante para almacenar contraseñas de manera segura en la base de datos, ya que el hash resultante no puede ser revertido a la contraseña original.
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# La función create_access_token se encarga de generar un token de acceso JWT (JSON Web Token) que se utiliza para autenticar a los usuarios en la aplicación.
# El token contiene información codificada, como el ID del usuario, y tiene una fecha de expiración para garantizar la seguridad.
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt