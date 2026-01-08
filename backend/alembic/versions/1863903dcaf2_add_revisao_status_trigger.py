"""add_revisao_status_trigger

Revision ID: 1863903dcaf2
Revises: ac9315d05b3d
Create Date: 2026-01-07 01:00:21.160392

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1863903dcaf2'
down_revision: Union[str, Sequence[str], None] = 'ac9315d05b3d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Criar a Função
    op.execute("""
        CREATE OR REPLACE FUNCTION update_revisao_status()
        RETURNS TRIGGER AS $$
        BEGIN
            IF NEW.data_realizada IS NOT NULL THEN
                NEW.status := 'REALIZADA';
            ELSIF NEW.data_prevista < CURRENT_DATE THEN
                NEW.status := 'ATRASADA';
            ELSE
                NEW.status := 'PENDENTE';
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    # 2. Criar a Trigger
    op.execute("""
        DROP TRIGGER IF EXISTS trg_update_revisao_status ON "Revisao";
        CREATE TRIGGER trg_update_revisao_status
        BEFORE INSERT OR UPDATE ON "Revisao"
        FOR EACH ROW
        EXECUTE FUNCTION update_revisao_status();
    """)


def downgrade() -> None:
    op.execute('DROP TRIGGER IF EXISTS trg_update_revisao_status ON "Revisao";')
    op.execute('DROP FUNCTION IF EXISTS update_revisao_status();')
