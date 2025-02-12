import pytest
from unittest.mock import Mock
from datetime import datetime
from src.user.domain.service.user_service import UserService
from src.user.domain.model.user import User
from src.shared.domain.exceptions import ValidationException
from src.shared.domain.value_objects import Email
from src.user.application.dto.user_dto import UserResponseDTO

class TestUserService:
    @pytest.fixture
    def user_repository(self):
        return Mock()

    @pytest.fixture
    def user_service(self, user_repository):
        return UserService(user_repository)

    @pytest.fixture
    def sample_user(self):
        return User(
            id=None,
            email=Email(value="test@example.com"),
            name="Test User",
            created_at=datetime.utcnow()
        )

    def test_create_user_success(self, user_service, user_repository, sample_user):
        # Given
        user_repository.find_by_email.return_value = None
        user_repository.save.return_value = sample_user

        # When
        result = user_service.create_user(
            email="test@example.com",
            name="Test User"
        )

        # Then
        assert isinstance(result, UserResponseDTO)
        assert result.email == str(sample_user.email)
        assert result.name == sample_user.name
        user_repository.save.assert_called_once()

    def test_create_user_with_existing_email_fails(self, user_service, user_repository, sample_user):
        # Given
        user_repository.find_by_email.return_value = sample_user

        # When/Then
        with pytest.raises(ValidationException, match="Email test@example.com is already registered"):
            user_service.create_user(
                email="test@example.com",
                name="Test User"
            )

    def test_get_user_by_email_success(self, user_service, user_repository, sample_user):
        # Given
        user_repository.find_by_email.return_value = sample_user

        # When
        result = user_service.get_user_by_email("test@example.com")

        # Then
        assert isinstance(result, UserResponseDTO)
        assert result.email == str(sample_user.email)
        assert result.name == sample_user.name
        user_repository.find_by_email.assert_called_once_with("test@example.com")

    def test_get_user_by_email_not_found(self, user_service, user_repository, sample_user_dict):
        # Given
        user_repository.find_by_email.return_value = None

        # When
        found_user = user_service.get_user_by_email(sample_user_dict["email"])

        # Then
        assert found_user is None
        user_repository.find_by_email.assert_called_once_with(sample_user_dict["email"])
