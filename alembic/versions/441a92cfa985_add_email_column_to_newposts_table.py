"""add email column to newposts table

Revision ID: 441a92cfa985
Revises: 204f5020b163
Create Date: 2024-03-04 23:59:00.978692

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '441a92cfa985'  #this will update
down_revision: Union[str, None] = '204f5020b163'   # if we go down step it will go to the prevision of the previous one
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('newposts',sa.Column('email',sa.String(),nullable=False))


def downgrade():
    op.drop_column('newposts','email')
    
