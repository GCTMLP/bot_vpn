"""initial

Revision ID: e4974b56c5ad
Revises: c55bebe6d621
Create Date: 2025-01-24 17:21:58.613751

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e4974b56c5ad'
down_revision: Union[str, None] = 'c55bebe6d621'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
