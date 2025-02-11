from fastapi import status
from jose import jwt
from src.auth.infrastructure.jwt_service import JWTService
from src.user.infrastructure.persistence.postgresql_user_repository import PostgresqlUserRepository

class TestAuthEndpoints:
    def test_login_success(self, client, mock_user, test_session):
        # Given
        repository = PostgresqlUserRepository(test_session)
        repository.save(mock_user)

        # When
        response = client.post(
            "/api/v1/login",
            json={"email": str(mock_user.email)}
        )

        # Then
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

        payload = jwt.decode(
            data["access_token"],
            JWTService.SECRET_KEY,
            algorithms=[JWTService.ALGORITHM]
        )
        assert payload["sub"] == str(mock_user.email)
        assert payload["user_id"] == mock_user.id
        assert "type" in payload
        assert payload["type"] == "access_token"

    def test_login_user_not_found(self, client):
        # When
        response = client.post(
            "/api/v1/login",
            json={"email": "nonexistent@example.com"}
        )

        # Then
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Incorrect email" in response.json()["detail"]

    def test_protected_endpoint_without_token(self, client):
        # When
        response = client.post("/api/v1/orders")

        # Then
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Not authenticated" in response.json()["detail"]

    def test_protected_endpoint_with_invalid_token(self, client):
        # When
        response = client.post(
            "/api/v1/orders",
            headers={"Authorization": "Bearer invalid-token"}
        )

        # Then
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Could not validate credentials" in response.json()["detail"]
