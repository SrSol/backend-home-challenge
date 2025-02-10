# File: tests/integration/infrastructure/persistence/test_postgresql_user_repository.py
import pytest
from datetime import datetime
from src.user.domain.model.user import User
from src.user.infrastructure.persistence.postgresql_user_repository import PostgresqlUserRepository
from src.shared.domain.exceptions import EntityNotFoundException

class TestPostgresqlUserRepository:
    @pytest.fixture
    def user_repository(self, test_session):
        return PostgresqlUserRepository(test_session)

    def test_save_new_user_success(self, user_repository, sample_user):
        # When
        saved_user = user_repository.save(sample_user)

        # Then
        assert saved_user.id is not None
        assert str(saved_user.email) == str(sample_user.email)
        assert saved_user.name == sample_user.name
        assert isinstance(saved_user.created_at, datetime)

    def test_find_by_email_success(self, user_repository, sample_user):
        # Given
        saved_user = user_repository.save(sample_user)

        # When
        found_user = user_repository.find_by_email(str(sample_user.email))

        # Then
        assert found_user is not None
        assert found_user.id == saved_user.id
        assert str(found_user.email) == str(saved_user.email)
        assert found_user.name == saved_user.name

    def test_find_by_email_not_found(self, user_repository):
        # When
        found_user = user_repository.find_by_email("nonexistent@example.com")

        # Then
        assert found_user is None

    def test_find_by_id_success(self, user_repository, sample_user):
        # Given
        saved_user = user_repository.save(sample_user)

        # When
        found_user = user_repository.find_by_id(saved_user.id)

        # Then
        assert found_user is not None
        assert found_user.id == saved_user.id
        assert str(found_user.email) == str(saved_user.email)
        assert found_user.name == saved_user.name

    def test_find_by_id_not_found(self, user_repository):
        # When
        found_user = user_repository.find_by_id(999)

        # Then
        assert found_user is None

    def test_find_all_empty(self, user_repository):
        # When
        users = user_repository.find_all()

        # Then
        assert len(users) == 0

    def test_find_all_with_users(self, user_repository, sample_user):
        # Given
        saved_user = user_repository.save(sample_user)

        # When
        users = user_repository.find_all()

        # Then
        assert len(users) == 1
        assert users[0].id == saved_user.id
        assert str(users[0].email) == str(saved_user.email)
        assert users[0].name == saved_user.name
