from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import verify_password, create_access_token, get_password_hash
from app.core.config import settings
from app.api.deps import get_current_user
# En este archivo se definen los endpoints relacionados con la autenticación de usuarios.
router = APIRouter()

# --- MOCK DB (Base de datos temporal de prueba) ---
# En un proyecto real, esto se reemplazaría por consultas a una base de datos
# La contraseña se almacena como un hash para mayor seguridad
fake_users_db = {
    "admin": {
        "username": "admin",
        "full_name": "Administrador del Vault",
        "email": "admin@vault.com",
        # Contraseña es "secret123"
        "hashed_password": get_password_hash("secret123"),
        "disabled": False,
    }
}
# --------------------------------------------------------

# Endpoint para iniciar sesión y obtener un token de acceso
@router.post("/login", response_model=dict)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # 1. Buscar usuario
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")
        
    # 2. Verificar contraseña
    if not verify_password(form_data.password, user_dict["hashed_password"]):
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")
        
    # 3. Generar Token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_dict["username"]}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

# Endpoint de prueba protegido
@router.get("/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    return {"message": "Si ves esto, estás autenticado", "user": current_user}