"""change datetime

Revision ID: 92597850bea6
Revises: 909a40bc033c
Create Date: 2025-02-03 17:05:05.915827

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '92597850bea6'
down_revision: Union[str, None] = '909a40bc033c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
