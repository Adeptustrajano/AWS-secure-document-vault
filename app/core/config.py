import os
# ¡ADVERTENCIA!: En producción, las configuraciones sensibles como SECRET_KEY deben cargarse desde variables de entorno o servicios de gestión de secretos.
# En este ejemplo, se proporciona un valor predeterminado para desarrollo, pero en producción, asegúrate de establecer la variable de entorno SECRET_KEY con una clave secreta segura y compleja.
class Settings:
    PROJECT_NAME: str = "AWS Secure Document Vault"
    # ¡ADVERTENCIA!: En producción, esto debe cargarse desde variables de entorno
    SECRET_KEY: str = os.getenv("SECRET_KEY", "una-clave-secreta-muy-larga-y-compleja-para-desarrollo")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()