"""add last few columns to newposts table

Revision ID: 577ea43faec5
Revises: dad703ae7839
Create Date: 2024-03-05 11:58:34.490122

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '577ea43faec5'
down_revision: Union[str, None] = 'dad703ae7839'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('newposts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('newposts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))



def downgrade() -> None:
    pass
