"""initial

Revision ID: d047e346e411
Revises: 53ca1186a8a1
Create Date: 2025-01-24 17:25:26.178188

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd047e346e411'
down_revision: Union[str, None] = '53ca1186a8a1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
