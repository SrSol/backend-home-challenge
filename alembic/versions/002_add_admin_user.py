"""add admin user

Revision ID: 002
Revises: 001
Create Date: 2023-11-15 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Insertar usuario admin
    connection = op.get_bind()
    connection.execute(
        sa.text("""
            INSERT INTO users (email, name, created_at)
            VALUES (:email, :name, :created_at)
            ON CONFLICT (email) DO NOTHING
        """),
        {
            "email": "admin@email.com",
            "name": "Admin",
            "created_at": datetime.utcnow()
        }
    )

def downgrade() -> None:
    # Eliminar usuario admin
    connection = op.get_bind()
    connection.execute(
        sa.text("""
            DELETE FROM users 
            WHERE email = :email
        """),
        {"email": "admin@email.com"}
    )
