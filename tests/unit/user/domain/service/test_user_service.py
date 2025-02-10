# File: tests/unit/user/domain/service/test_user_service.py
import pytest
from unittest.mock import Mock
from src.user.domain.service.user_service import UserService
from src.user.domain.model.user import User
from src.shared.domain.exceptions import ValidationException

class TestUserService:
    @pytest.fixture
    def user_repository(self):
        return Mock()

    @pytest.fixture
    def user_service(self, user_repository):
        return UserService(user_repository)

    def test_create_user_success(self, user_service, user_repository, sample_user, sample_user_dict):
        # Given
        user_repository.find_by_email.return_value = None
        user_repository.save.return_value = sample_user

        # When
        created_user = user_service.create_user(**sample_user_dict)

        # Then
        assert created_user == sample_user
        user_repository.find_by_email.assert_called_once_with(sample_user_dict["email"])
        user_repository.save.assert_called_once()

    def test_create_user_with_existing_email_fails(self, user_service, user_repository, sample_user, sample_user_dict):
        # Given
        user_repository.find_by_email.return_value = sample_user

        # When/Then
        with pytest.raises(ValidationException, match=f"Email {sample_user_dict['email']} is already registered"):
            user_service.create_user(**sample_user_dict)

        user_repository.save.assert_not_called()

    def test_get_user_by_email_success(self, user_service, user_repository, sample_user, sample_user_dict):
        # Given
        user_repository.find_by_email.return_value = sample_user

        # When
        found_user = user_service.get_user_by_email(sample_user_dict["email"])

        # Then
        assert found_user == sample_user
        user_repository.find_by_email.assert_called_once_with(sample_user_dict["email"])

    def test_get_user_by_email_not_found(self, user_service, user_repository, sample_user_dict):
        # Given
        user_repository.find_by_email.return_value = None

        # When
        found_user = user_service.get_user_by_email(sample_user_dict["email"])

        # Then
        assert found_user is None
        user_repository.find_by_email.assert_called_once_with(sample_user_dict["email"])
