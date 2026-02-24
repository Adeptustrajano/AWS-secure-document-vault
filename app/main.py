from fastapi import FastAPI, Depends
from app.api.routers import auth
from app.api.deps import get_current_user

# En esta fase inicial, nos centramos en establecer la estructura básica de la API
# y en implementar un sistema de autenticación simple.
app = FastAPI(
    title="AWS Secure Document Vault",
    description="API para gestión y cifrado de documentos en la nube.",
    version="1.0.0"
)

# Incluimos las rutas de autenticación
# Esto añade los endpoints /api/v1/auth/login y /api/v1/auth/me a tu API
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Autenticación"])

# 1. Endpoint de Salud (Health Check)
# Estrategia: Cuando despleguemos en AWS, el balanceador de carga usará 
# esta ruta para saber si nuestra API está viva o si se ha caída.
@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok", "message": "El servidor está funcionando correctamente"}

# 2. Endpoint base para documentos (En el futuro conectará con S3)
# -> NUEVO: Ahora requerimos que el usuario esté autenticado para ver los documentos
# Esto se logra usando Depends(get_current_user), que verifica el token JWT y devuelve la información del usuario.
@app.get("/documents", tags=["Documents"])
def get_documents(current_user: dict = Depends(get_current_user)):
    # Por ahora devolvemos datos falsos (Mock data). 
    # En la Fase 2, esto leerá los archivos reales desde Amazon S3.
    
    # Podemos incluso ver qué usuario nos está pidiendo los documentos
    # Esto es útil para personalizar la respuesta o para fines de auditoría.
    usuario_peticion = current_user.get("username")
    
    return {
        "user_requesting": usuario_peticion,
        "documents": [
            {"id": 1, "name": "informe_secreto.pdf", "size": "2MB", "encrypted": True},
            {"id": 2, "name": "claves_aws.txt", "size": "15KB", "encrypted": True}
        ]
    }