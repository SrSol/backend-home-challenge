import pytest
from datetime import datetime
from src.user.application.get_user import GetUserQuery
from src.user.domain.model.user import User
from src.shared.domain.value_objects import Email
from src.user.application.dto.user_dto import UserResponseDTO

class TestGetUserQuery:
    @pytest.fixture
    def mock_user(self):
        return User(
            id=None,
            email=Email(value="test@example.com"),
            name="Test User",
            created_at=datetime.utcnow()
        )

    def test_execute_user_found(self, mocker, mock_user):
        # Given
        mock_service = mocker.Mock()
        mock_service.get_user_by_email.return_value = UserResponseDTO.from_entity(mock_user)

        query = GetUserQuery(mock_service)

        # When
        result = query.execute("test@example.com")

        # Then
        assert isinstance(result, UserResponseDTO)
        assert result.email == str(mock_user.email)
        assert result.name == mock_user.name
        mock_service.get_user_by_email.assert_called_once_with("test@example.com")

    def test_execute_user_not_found(self, mocker):
        # Given
        mock_service = mocker.Mock()
        mock_service.get_user_by_email.return_value = None

        query = GetUserQuery(mock_service)

        # When
        result = query.execute("nonexistent@example.com")

        # Then
        assert result is None
        mock_service.get_user_by_email.assert_called_once_with("nonexistent@example.com")
