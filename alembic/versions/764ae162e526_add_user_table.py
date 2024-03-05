"""add user table

Revision ID: 764ae162e526
Revises: 441a92cfa985
Create Date: 2024-03-05 00:19:51.180521

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '764ae162e526'
down_revision: Union[str, None] = '441a92cfa985'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('newusers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),  # instead of specifying the primary constraint in above row we specified here
        sa.UniqueConstraint('email')  # and this ensures that we don't have duplicate emails
    )


def downgrade():
    op.drop_table('newusers')
    
