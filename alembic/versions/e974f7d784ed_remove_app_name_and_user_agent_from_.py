"""Remove app_name and user_agent from scan_events

Revision ID: e974f7d784ed
Revises: 17d14bb1f6bf
Create Date: 2025-08-08 11:25:32.773685

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e974f7d784ed'
down_revision: Union[str, Sequence[str], None] = '17d14bb1f6bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Remove the columns
    op.drop_column('scan_events', 'app_name')
    op.drop_column('scan_events', 'user_agent')


def downgrade() -> None:
    """Downgrade schema."""
    # Add the columns back
    op.add_column('scan_events', sa.Column('app_name', sa.String(), nullable=True))
    op.add_column('scan_events', sa.Column('user_agent', sa.String(), nullable=True))