# File: tests/unit/user/application/test_get_user.py
import pytest
from datetime import datetime
from src.user.application.get_user import GetUserQuery
from src.shared.domain.value_objects import Email
from src.user.domain.model.user import User

class TestGetUserQuery:
    @pytest.fixture
    def get_user_query(self, mock_user_service):
        return GetUserQuery(mock_user_service)

    def test_execute_user_found(self, get_user_query, mock_user_service, mock_user):
        # When
        result = get_user_query.execute("test@example.com")
        
        # Then
        mock_user_service.get_user_by_email.assert_called_once_with("test@example.com")
        assert result.id == mock_user.id
        assert result.email == str(mock_user.email)
        assert result.name == mock_user.name

    def test_execute_user_not_found(self, get_user_query, mock_user_service):
        # Given
        mock_user_service.get_user_by_email.return_value = None
        
        # When
        result = get_user_query.execute("nonexistent@example.com")
        
        # Then
        assert result is None
        mock_user_service.get_user_by_email.assert_called_once_with("nonexistent@example.com")
