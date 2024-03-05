"""create posts table

Revision ID: 204f5020b163
Revises: 
Create Date: 2024-03-04 15:21:18.678757

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '204f5020b163'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():  #we create table to run it to command prompt: alembic upgrade 204f5020b163
    op.create_table('newposts',sa.Column('id',sa.Integer(),nullable = False,primary_key = True),sa.Column('title',sa.String(),nullable = False))
    


def downgrade(): #revert the changes made to the database schema back to a previous state
    op.drop_table('newposts')
    
