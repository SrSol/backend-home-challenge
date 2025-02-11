import pytest
from datetime import datetime, timedelta
from jose import jwt
from src.auth.infrastructure.jwt_service import JWTService

class TestJWTService:
    def test_create_access_token_success(self):
        # Given
        data = {"sub": "test@example.com"}
        
        # When
        token = JWTService.create_access_token(data)
        
        # Then
        payload = jwt.decode(token, JWTService.SECRET_KEY, algorithms=[JWTService.ALGORITHM])
        assert payload["sub"] == "test@example.com"
        assert "exp" in payload

    def test_verify_token_success(self):
        # Given
        data = {"sub": "test@example.com"}
        token = JWTService.create_access_token(data)
        
        # When
        payload = JWTService.verify_token(token)
        
        # Then
        assert payload["sub"] == "test@example.com"

    def test_verify_token_expired_fails(self):
        # Given
        data = {"sub": "test@example.com", "exp": datetime.utcnow() - timedelta(minutes=1)}
        token = jwt.encode(data, JWTService.SECRET_KEY, algorithm=JWTService.ALGORITHM)
        
        # When/Then
        with pytest.raises(ValueError, match="Invalid token"):
            JWTService.verify_token(token)

    def test_verify_token_invalid_signature_fails(self):
        # Given
        data = {"sub": "test@example.com"}
        token = jwt.encode(data, "wrong-secret", algorithm=JWTService.ALGORITHM)
        
        # When/Then
        with pytest.raises(ValueError, match="Invalid token"):
            JWTService.verify_token(token)

    def test_verify_token_without_email_fails(self):
        # Given
        data = {"foo": "bar"}
        token = jwt.encode(data, JWTService.SECRET_KEY, algorithm=JWTService.ALGORITHM)
        
        # When/Then
        with pytest.raises(ValueError, match="Token has no email"):
            JWTService.verify_token(token) 