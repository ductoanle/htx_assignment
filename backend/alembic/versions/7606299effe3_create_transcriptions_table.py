"""create transcriptions table

Revision ID: 7606299effe3
Revises:
Create Date: 2025-04-11 12:38:49.352447

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7606299effe3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'transcriptions',
        sa.Column('id', sa.Integer, primary_key=True),
        # enforce uniqueness, support for exact matches search
        sa.Column(
            'audio_file_name',
            sa.String(100),
            nullable=False,
            unique=True
        ),
        # Unlimited length text, supports all languages
        sa.Column('transcribed_text', sa.UnicodeText),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('transcriptions')
