"""Add OrderItems table and orders created_at column

Revision ID: f7b2d1c4a9e0
Revises: 39c57e100095
Create Date: 2026-04-05 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f7b2d1c4a9e0'
down_revision: Union[str, Sequence[str], None] = '39c57e100095'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'OrderItems_Table',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('item_id', sa.Integer(), nullable=False),
        sa.Column('item_quantity', sa.Integer(), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['item_id'], ['Items_Table.item_id']),
        sa.ForeignKeyConstraint(['order_id'], ['Orders_Table.order_id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_OrderItems_Table_id'), 'OrderItems_Table', ['id'], unique=False)

    op.add_column('Orders_Table', sa.Column('created_at', sa.DateTime(), nullable=True))


def downgrade() -> None:
    op.drop_column('Orders_Table', 'created_at')

    op.drop_index(op.f('ix_OrderItems_Table_id'), table_name='OrderItems_Table')
    op.drop_table('OrderItems_Table')
