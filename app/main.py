from fastapi import FastAPI

# Inicializamos la aplicación PRUEBA 1.0.0
# En esta fase, solo tenemos un endpoint de salud y un endpoint de documentos que devuelve datos falsos.
app = FastAPI(
    title="AWS Secure Document Vault",
    description="API para gestión y cifrado de documentos en la nube.",
    version="1.0.0"
)

# 1. Endpoint de Salud (Health Check)
# Estrategia: Cuando despleguemos en AWS, el balanceador de carga usará 
# esta ruta para saber si nuestra API está viva o si se ha caída.
@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok", "message": "El servidor está funcionando correctamente"}

# 2. Endpoint base para documentos (En el futuro conectará con S3)
@app.get("/documents", tags=["Documents"])
def get_documents():
    # Por ahora devolvemos datos falsos (Mock data). 
    # En la Fase 2, esto leerá los archivos reales desde Amazon S3.
    return [
        {"id": 1, "name": "informe_secreto.pdf", "size": "2MB", "encrypted": True},
        {"id": 2, "name": "claves_aws.txt", "size": "15KB", "encrypted": True}
    ]