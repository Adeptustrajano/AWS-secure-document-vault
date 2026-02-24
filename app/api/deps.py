from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from app.core.config import settings

# Configuración de OAuth2 con JWT
# Esto le dice a FastAPI dónde está el endpoint de login que devuelve el token JWT.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

# Esta función se usa como dependencia en los endpoints que requieran autenticación.
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        # Aquí buscaremos el usuario en la Base de Datos.
        # Validamos que el token tiene formato y firma correctos.
        token_data = {"username": username}
    except jwt.InvalidTokenError:
        raise credentials_exception
        
    return token_data