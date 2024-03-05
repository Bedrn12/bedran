"""auto-vote

Revision ID: f293ba4e78b5
Revises: 577ea43faec5
Create Date: 2024-03-05 14:05:11.267515

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f293ba4e78b5'
down_revision: Union[str, None] = '577ea43faec5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('newvotes',sa.Column('user_id',sa.Integer(),nullable=False),
                    sa.Column('post_id',sa.Integer(),nullable=False),
                    sa.ForeignKeyConstraint(['post_id'],['posts.id'],ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['user_id'],['users.id'],ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('user_id','post_id'))


def downgrade():
    op.drop_table('newvotes')
   