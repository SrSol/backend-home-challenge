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

    # Índice para búsquedas por email (login y validaciones)
    op.create_index('ix_users_email', 'users', ['email'])
    # Índice para ordenar por fecha de creación
    op.create_index('ix_users_created_at', 'users', ['created_at'])

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

    # Índice para búsquedas por mesero
    op.create_index('ix_orders_waiter_id', 'orders', ['waiter_id'])
    # Índice para filtrar por rango de fechas (reportes)
    op.create_index('ix_orders_created_at', 'orders', ['created_at'])
    # Índice para búsquedas por cliente
    op.create_index('ix_orders_customer_name', 'orders', ['customer_name'])

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
    # Índice para búsquedas por orden
    op.create_index('ix_order_items_order_id', 'order_items', ['order_id'])
    # Índice para búsquedas y agrupaciones por producto
    op.create_index('ix_order_items_product_name', 'order_items', ['product_name'])

def downgrade() -> None:
    # Eliminar índices de order_items
    op.drop_index('ix_order_items_product_stats', table_name='order_items')
    op.drop_index('ix_order_items_order_id', table_name='order_items')
    op.drop_index('ix_order_items_product_name', table_name='order_items')

    # Eliminar índices de orders
    op.drop_index('ix_orders_waiter_id', table_name='orders')
    op.drop_index('ix_orders_created_at', table_name='orders')
    op.drop_index('ix_orders_customer_name', table_name='orders')

    # Eliminar índices de users
    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_created_at', table_name='users')

    # Eliminar tablas
    op.drop_table('order_items')
    op.drop_table('orders')
    op.drop_table('users')
