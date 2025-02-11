from typing import Optional, List
from sqlalchemy.orm import Session

from src.user.domain.model.user import User
from src.user.domain.repository.user_repository import UserRepository
from src.user.infrastructure.persistence.models import UserModel
from src.shared.domain.value_objects import Email

class PostgresqlUserRepository(UserRepository):
    """PostgreSQL implementation of UserRepository"""

    def __init__(self, session: Session):
        self._session = session

    def save(self, user: User) -> User:
        user_model = UserModel(
            email=str(user.email),
            name=user.name,
            created_at=user.created_at
        )
        self._session.add(user_model)
        self._session.commit()
        self._session.refresh(user_model)
        return self._user_model_to_entity(user_model)

    def find_by_email(self, email: str) -> Optional[User]:
        user_model = self._session.query(UserModel).filter(
            UserModel.email == email
        ).first()
        return self._user_model_to_entity(user_model) if user_model else None

    def find_by_id(self, id: int) -> Optional[User]:
        user_model = self._session.query(UserModel).filter(
            UserModel.id == id
        ).first()
        return self._user_model_to_entity(user_model) if user_model else None

    def find_all(self) -> List[User]:
        user_models = self._session.query(UserModel).all()
        return [self._user_model_to_entity(um) for um in user_models]

    def _user_model_to_entity(self, user_model: UserModel) -> User:
        """Converts UserModel to User domain entity"""
        return User(
            id=user_model.id,
            email=Email(value=user_model.email),
            name=user_model.name,
            created_at=user_model.created_at
        )
