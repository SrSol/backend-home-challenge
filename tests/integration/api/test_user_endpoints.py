import pytest
from fastapi import status

class TestUserEndpoints:
    @pytest.fixture
    def sample_user_data(self):
        return {
            "email": "test@example.com",
            "name": "Test User"
        }

    def test_create_user_success(self, client, sample_user_data):
        # When
        response = client.post("/api/v1/users/", json=sample_user_data)

        # Then
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == sample_user_data["email"]
        assert data["name"] == sample_user_data["name"]
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
