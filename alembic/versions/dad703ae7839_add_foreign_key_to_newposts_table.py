"""add foreign-key to newposts table

Revision ID: dad703ae7839
Revises: 764ae162e526
Create Date: 2024-03-05 11:35:11.639270

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dad703ae7839'
down_revision: Union[str, None] = '764ae162e526'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('newposts',sa.Column('owner_id',sa.Integer(),nullable=False))#it adds new column named 'owner_id' to the 'newposts table'
    op.create_foreign_key('newposts_newusers',source_table="newposts",referent_table="newusers",
    local_cols=['owner_id'],remote_cols=['id'],ondelete="CASCADE")#it creates a foregin key constraint between the owner_id column in the newposts table and the id column in the newusers table usign the op.create_foreign_key() function 


def downgrade():
    op.drop_constraint('newposts_newusers_fk',table_name='newposts')
    op.drop_column('newposts','owner_id')
