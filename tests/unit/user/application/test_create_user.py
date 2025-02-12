import pytest
from datetime import datetime
from src.user.application.create_user import CreateUserCommand
from src.user.domain.model.user import User
from src.shared.domain.value_objects import Email
from src.user.application.dto.user_dto import UserResponseDTO, CreateUserDTO

class TestCreateUserCommand:
    @pytest.fixture
    def mock_user(self):
        return User(
            id=None,
            email=Email(value="test@example.com"),
            name="Test User",
            created_at=datetime.utcnow()
        )

    def test_execute_success(self, mocker, mock_user):
        # Given
        mock_service = mocker.Mock()
        mock_service.create_user.return_value = UserResponseDTO.from_entity(mock_user)

        command = CreateUserCommand(mock_service)
        user_data = CreateUserDTO(
            email="test@example.com",
            name="Test User"
        )

        # When
        result = command.execute(user_data.model_dump())

        # Then
        assert isinstance(result, UserResponseDTO)
        assert result.email == str(mock_user.email)
        assert result.name == mock_user.name
        mock_service.create_user.assert_called_once_with(
            email="test@example.com",
            name="Test User"
        )
