"""initial tables

Revision ID: 001
Revises: 
Create Date: 2023-11-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # Índice único para email - validación y búsqueda
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    # Orders table
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('customer_name', sa.String(), nullable=False),
        sa.Column('waiter_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['waiter_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Order items table
    op.create_table(
        'order_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('product_name', sa.String(), nullable=False),
        sa.Column('unit_price', sa.Numeric(10, 2), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Índice compuesto para reportes de ventas por producto y fecha
    op.create_index(
        'ix_order_items_product_stats',
        'order_items',
        ['product_name', 'quantity', 'unit_price']
    )

def downgrade() -> None:
    # Eliminar índices de order_items
    op.drop_index('ix_order_items_product_stats', table_name='order_items')

    # Eliminar índices de users
    op.drop_index('ix_users_email', table_name='users')

    # Eliminar tablas
    op.drop_table('order_items')
    op.drop_table('orders')
    op.drop_table('users')
