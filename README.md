# AWS Secure Document Vault

API segura para gestión de documentos con enfoque en **seguridad**, **trazabilidad** y **buenas prácticas DevSecOps**.  
El proyecto está diseñado como laboratorio práctico para arquitectura cloud en AWS y desarrollo backend seguro.

---

## 🚀 Objetivo del proyecto

Construir una API robusta para:

- Registro y autenticación de usuarios (JWT + hash seguro de contraseñas).
- Gestión de documentos con controles de acceso.
- Cifrado de información sensible.
- Base sólida para evolucionar a una arquitectura cloud en AWS (S3, RDS, KMS, IAM, Cognito, Terraform).

---

## 🧱 Stack técnico (fase actual)

- **Backend:** Python, FastAPI
- **Base de datos:** PostgreSQL (entorno local con Docker)
- **Testing:** Pytest + TestClient
- **Contenedores:** Docker / Docker Compose
- **CI:** GitHub Actions (tests automatizados)

---

## 📌 Estado

> Proyecto en desarrollo activo (Phase 1).  
> La PR inicial incorpora suite de tests automatizados y stack local con Docker.

---

## 📂 Estructura del repositorio

- `app/` → código fuente de la API
- `tests/` → suite de pruebas automatizadas
- `.github/workflows/` → pipelines CI/CD
- `infrastructure/` → IaC y componentes de despliegue (evolutivo)
- `docs/` → documentación y diagramas

---

## ⚙️ Configuración local

### 1) Clonar repositorio

```bash
git clone https://github.com/Dmillan-dev/AWS-secure-document-vault.git
cd AWS-secure-document-vault
```

### 2) Configurar variables de entorno

```bash
cp .env.example .env
```

Edita `.env` y reemplaza todos los valores `CHANGE_ME_*`.

### 3) Levantar entorno con Docker

```bash
docker compose up --build
```

API disponible en:

- `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`

---

## 🧪 Testing

Instalación de dependencias de test:

```bash
pip install -r requirements.txt -r requirements-test.txt
```

Ejecución:

```bash
pytest tests/ -v
```

La suite está preparada para correr sin dependencias externas pesadas en local (DB de test aislada para ejecución rápida).

---

## 🔐 Principios de seguridad aplicados

- Hash de contraseñas con algoritmo robusto (bcrypt o equivalente).
- Autenticación basada en JWT.
- Separación de secretos vía variables de entorno.
- Base para cifrado y gestión de claves orientada a AWS KMS (roadmap).

---

## 🛣️ Roadmap (alto nivel)

- [x] Base API + autenticación inicial
- [x] Suite de tests Phase 1
- [x] Stack local Dockerizado
- [ ] Integración cloud storage (S3)
- [ ] Metadatos en RDS administrado
- [ ] Cifrado con KMS
- [ ] Terraform para despliegue reproducible
- [ ] Endurecimiento DevSecOps (SAST/DAST, políticas IAM, observabilidad)

---

## 🤝 Contribución

1. Crea una rama desde `main`
2. Implementa cambios con tests
3. Abre Pull Request con contexto funcional/técnico
4. Espera validación CI y review

---
