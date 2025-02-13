"""initial

Revision ID: f4b196b15fd1
Revises: 5f90ff7e56b2
Create Date: 2025-01-24 17:18:58.023208

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4b196b15fd1'
down_revision: Union[str, None] = '5f90ff7e56b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
