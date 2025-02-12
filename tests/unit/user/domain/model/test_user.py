import pytest

from src.user.domain.model.user import User
from src.shared.domain.exceptions import ValidationException

class TestUserModel:
    def test_create_user_success(self):
        # When
        user = User.create(
            email="test@example.com",
            name="Test User"
        )
        
        # Then
        assert str(user.email) == "test@example.com"
        assert user.name == "Test User"
        assert user.id is None

    @pytest.mark.parametrize("invalid_email", [
        "invalid-email",
        "test@",
        "@domain.com",
        "test@domain",
        ""
    ])
    def test_create_user_with_invalid_email_fails(self, invalid_email):
        # When/Then
        with pytest.raises(ValidationException, match="Invalid email format"):
            User.create(
                email=invalid_email,
                name="Test User"
            )

    @pytest.mark.parametrize("invalid_name", [
        "",
        "a",
        " ",
        "  "
    ])
    def test_create_user_with_invalid_name_fails(self, invalid_name):
        # When/Then
        with pytest.raises(ValidationException, match="Name must be at least 2 characters long"):
            User.create(
                email="test@example.com",
                name=invalid_name
            )
