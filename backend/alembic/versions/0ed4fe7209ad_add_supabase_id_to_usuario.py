"""add_supabase_id_to_usuario

Revision ID: 0ed4fe7209ad
Revises: f311a927f7da
Create Date: 2025-12-25 01:15:52.397854

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.engine.reflection import Inspector


# revision identifiers, used by Alembic.
revision: str = '0ed4fe7209ad'
down_revision: Union[str, Sequence[str], None] = 'f311a927f7da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)
    columns = [c['name'] for c in inspector.get_columns('Usuario')]
    # Adiciona a coluna como UUID
    if 'supabase_id' not in columns:
        op.add_column('Usuario', sa.Column('supabase_id', postgresql.UUID(as_uuid=True), nullable=True))

    # Cria a restrição de unicidade
    constraints = inspector.get_unique_constraints('Usuario')
    if not any(c['name'] == 'uq_usuario_supabase_id' for c in constraints):
        op.create_unique_constraint('uq_usuario_supabase_id', 'Usuario', ['supabase_id'])


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    inspector = Inspector.from_engine(bind)

    constraints = inspector.get_unique_constraints('Usuario')
    if any(c['name'] == 'uq_usuario_supabase_id' for c in constraints):
        op.drop_constraint('uq_usuario_supabase_id', 'Usuario', type_='unique')

    columns = [c['name'] for c in inspector.get_columns('Usuario')]
    if 'supabase_id' in columns:
        op.drop_column('Usuario', 'supabase_id')
