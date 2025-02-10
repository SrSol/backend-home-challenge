# File: tests/unit/user/application/test_create_user.py
import pytest
from datetime import datetime
from src.user.application.create_user import CreateUserCommand
from src.user.application.dto.user_dto import CreateUserDTO
from src.shared.domain.value_objects import Email
from src.user.domain.model.user import User

class TestCreateUserCommand:
    @pytest.fixture
    def create_user_command(self, mock_user_service):
        return CreateUserCommand(mock_user_service)

    def test_execute_success(self, create_user_command, mock_user_service, mock_user):
        # Given
        user_dto = CreateUserDTO(
            email="test@example.com",
            name="Test User"
        )
        
        # When
        result = create_user_command.execute(user_dto)
        
        # Then
        mock_user_service.create_user.assert_called_once_with(
            email=user_dto.email,
            name=user_dto.name
        )
        assert result.id == mock_user.id
        assert result.email == str(mock_user.email)
        assert result.name == mock_user.name
