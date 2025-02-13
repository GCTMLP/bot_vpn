"""initial

Revision ID: 53ca1186a8a1
Revises: e4974b56c5ad
Create Date: 2025-01-24 17:24:37.606951

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '53ca1186a8a1'
down_revision: Union[str, None] = 'e4974b56c5ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
