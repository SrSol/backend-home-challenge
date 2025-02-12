import pytest
from datetime import datetime, timedelta
from jose import jwt
from src.auth.infrastructure.jwt_service import JWTService

class TestJWTService:
    def test_create_access_token_success(self):
        # Given
        data = {"sub": "test@example.com", "user_id": 1}

        # When
        token = JWTService.create_access_token(data)

        # Then
        payload = jwt.decode(token, JWTService.SECRET_KEY, algorithms=[JWTService.ALGORITHM])
        assert payload["sub"] == data["sub"]
        assert payload["user_id"] == data["user_id"]
        assert "exp" in payload
        assert payload["type"] == "access_token"

    def test_verify_token_success(self):
        # Given
        data = {"sub": "test@example.com", "user_id": 1}
        token = JWTService.create_access_token(data)

        # When
        payload = JWTService.verify_token(token)

        # Then
        assert payload["sub"] == data["sub"]
        assert payload["user_id"] == data["user_id"]

    def test_verify_token_expired_fails(self):
        # Given
        expired_token = jwt.encode(
            {"exp": datetime.utcnow() - timedelta(days=1)},
            JWTService.SECRET_KEY,
            algorithm=JWTService.ALGORITHM
        )

        # When/Then
        with pytest.raises(ValueError, match="Could not validate credentials"):
            JWTService.verify_token(expired_token)

    def test_verify_token_invalid_signature_fails(self):
        # Given
        token = jwt.encode(
            {"sub": "test@example.com"},
            "wrong_secret",
            algorithm=JWTService.ALGORITHM
        )

        # When/Then
        with pytest.raises(ValueError, match="Could not validate credentials"):
            JWTService.verify_token(token)

    def test_verify_token_without_email_fails(self):
        # Given
        token = jwt.encode(
            {"foo": "bar"},
            JWTService.SECRET_KEY,
            algorithm=JWTService.ALGORITHM
        )

        # When/Then
        with pytest.raises(ValueError, match="Could not validate credentials"):
            JWTService.verify_token(token)

    def test_create_token_without_required_fields_fails(self):
        # When/Then
        with pytest.raises(ValueError, match="Token must include 'sub' and 'user_id'"):
            JWTService.create_access_token({"foo": "bar"}) 