# File: tests/integration/api/test_user_endpoints.py
import pytest
from fastapi import status

class TestUserEndpoints:
    def test_create_user_success(self, client, sample_user_dict):
        # When
        response = client.post("/api/v1/users/", json=sample_user_dict)

        # Then
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == sample_user_dict["email"]
        assert data["name"] == sample_user_dict["name"]
        assert "id" in data
        assert "created_at" in data

    @pytest.mark.parametrize("invalid_data,expected_detail", [
        (
            {"email": "invalid-email", "name": "Test User"},
            "value is not a valid email address"
        ),
        (
            {"email": "test@example.com", "name": ""},
            "string should have at least 2 characters"
        ),
        (
            {"name": "Test User"},
            "field required"
        ),
        (
            {"email": "test@example.com"},
            "field required"
        )
    ])
    def test_create_user_validation_error(self, client, invalid_data, expected_detail):
        # When
        response = client.post("/api/v1/users/", json=invalid_data)

        # Then
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_detail.lower() in response.json()["detail"].lower()

    def test_get_user_success(self, client, sample_user_dict):
        # Given
        created = client.post("/api/v1/users/", json=sample_user_dict)

        # When
        response = client.get(f"/api/v1/users/{sample_user_dict['email']}")

        # Then
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == sample_user_dict["email"]
        assert data["name"] == sample_user_dict["name"]

    def test_get_user_not_found(self, client):
        # When
        response = client.get("/api/v1/users/nonexistent@example.com")

        # Then
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"].lower()
