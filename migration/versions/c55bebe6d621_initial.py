"""initial

Revision ID: c55bebe6d621
Revises: f4b196b15fd1
Create Date: 2025-01-24 17:20:47.904982

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c55bebe6d621'
down_revision: Union[str, None] = 'f4b196b15fd1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
