"""Tests del endpoint de documentos — GET /documents."""
import pytest


class TestDocuments:
    def test_get_documents_without_auth_returns_401(self, client):
        """Acceder a /documents sin token debe devolver HTTP 401."""
        response = client.get("/documents")
        assert response.status_code == 401

    def test_get_documents_with_valid_token_returns_200(self, client, auth_headers):
        """Acceder a /documents con token válido debe devolver HTTP 200."""
        response = client.get("/documents", headers=auth_headers)
        assert response.status_code == 200

    def test_get_documents_returns_list(self, client, auth_headers):
        """La respuesta de /documents debe incluir una lista 'documents'."""
        response = client.get("/documents", headers=auth_headers)
        data = response.json()
        assert "documents" in data
        assert isinstance(data["documents"], list)

    def test_get_documents_includes_requesting_user(self, client, auth_headers, registered_user):
        """La respuesta debe indicar qué usuario realizó la petición."""
        response = client.get("/documents", headers=auth_headers)
        data = response.json()
        assert "user_requesting" in data
        assert data["user_requesting"] == registered_user["username"]

    def test_get_documents_with_invalid_token_returns_401(self, client):
        """Acceder a /documents con token inválido debe devolver HTTP 401."""
        headers = {"Authorization": "Bearer token.invalido.aqui"}
        response = client.get("/documents", headers=headers)
        assert response.status_code == 401

    def test_get_documents_items_have_required_fields(self, client, auth_headers):
        """Cada documento de la lista debe tener los campos: id, name, size, encrypted."""
        response = client.get("/documents", headers=auth_headers)
        documents = response.json()["documents"]
        # La fase 1 devuelve datos mock; si en fases futuras la lista pudiera estar
        # vacía, este test se debe actualizar para crear documentos de prueba primero.
        assert len(documents) > 0, "Se esperan documentos mock en la respuesta de la Fase 1"
        for doc in documents:
            assert "id" in doc
            assert "name" in doc
            assert "size" in doc
            assert "encrypted" in doc
