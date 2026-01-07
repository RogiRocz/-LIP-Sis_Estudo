"""Muda intervalo_revisoes para array

Revision ID: ac9315d05b3d
Revises: 0ed4fe7209ad
Create Date: 2026-01-04 17:05:15.922925

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ac9315d05b3d'
down_revision: Union[str, Sequence[str], None] = '0ed4fe7209ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('Usuario', 'intervalo_revisoes',
               existing_type=sa.VARCHAR(length=50),
               type_=postgresql.ARRAY(sa.Integer()),
               postgresql_using="string_to_array(intervalo_revisoes, ',')::integer[]",
               existing_nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('Usuario', 'intervalo_revisoes',
               existing_type=postgresql.ARRAY(sa.Integer()),
               type_=sa.VARCHAR(length=50),
               postgresql_using="array_to_string(intervalo_revisoes, ',')",
               existing_nullable=True)
