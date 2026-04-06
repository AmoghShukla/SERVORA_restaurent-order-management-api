"""Major Migrations

Revision ID: b4ae48087b8e
Revises: f7b2d1c4a9e0
Create Date: 2026-04-05 23:31:47.690652
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = 'b4ae48087b8e'
down_revision: Union[str, Sequence[str], None] = 'f7b2d1c4a9e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    user_role_enum = postgresql.ENUM(
        'USER', 'ADMIN', 'RESTAURANT_OWNER',
        name='userrole'
    )

    user_role_enum.create(op.get_bind())

    op.add_column('User_Table', sa.Column('user_password', sa.String(), nullable=True))
    op.add_column('User_Table', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('User_Table', sa.Column('user_role', user_role_enum, nullable=True))

    op.create_unique_constraint(None, 'User_Table', ['user_email'])


def downgrade() -> None:
    user_role_enum = postgresql.ENUM(
        'USER', 'ADMIN', 'RESTAURANT_OWNER',
        name='userrole'
    )

    op.drop_constraint(None, 'User_Table', type_='unique')
    op.drop_column('User_Table', 'user_role')
    op.drop_column('User_Table', 'created_at')
    op.drop_column('User_Table', 'user_password')

    user_role_enum.drop(op.get_bind())