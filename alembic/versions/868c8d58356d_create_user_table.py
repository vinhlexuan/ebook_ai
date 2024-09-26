"""create user table

Revision ID: 868c8d58356d
Revises: b88159d93365
Create Date: 2024-09-24 14:51:45.386549

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '868c8d58356d'
down_revision: Union[str, None] = 'b88159d93365'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(120), unique=True, nullable=False),
        sa.Column('password', sa.String(60), nullable=False),
        sa.Column('role_id', sa.Integer, sa.ForeignKey('roles.id'), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now())
    )

def downgrade() -> None:
    op.drop_table('users')
