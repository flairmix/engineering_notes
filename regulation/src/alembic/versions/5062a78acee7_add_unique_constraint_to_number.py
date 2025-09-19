"""add_unique_constraint_to_number

Revision ID: 5062a78acee7
Revises: a39f52f84b96
Create Date: 2025-09-19 17:08:04.231284

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5062a78acee7'
down_revision: Union[str, Sequence[str], None] = 'a39f52f84b96'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('documents') as batch_op:
        batch_op.create_unique_constraint(
            'uix_number_version',  
            ['number', 'version']
        )

def downgrade() -> None:
    with op.batch_alter_table('documents') as batch_op:
        batch_op.drop_constraint(
            'uix_number_version',  
            type_='unique'
        )
