"""fix column tag

Revision ID: 7214d33d9feb
Revises: 3008deefa98c
Create Date: 2024-03-19 21:32:29.037650

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7214d33d9feb'
down_revision: Union[str, None] = '3008deefa98c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('air_quality', sa.Column('type_gas', sa.String(), nullable=True))
    op.add_column('air_quality', sa.Column('tag', sa.String(), nullable=True))
    op.drop_index('ix_air_quality_tags', table_name='air_quality')
    op.drop_index('ix_air_quality_type', table_name='air_quality')
    op.create_index(op.f('ix_air_quality_tag'), 'air_quality', ['tag'], unique=False)
    op.create_index(op.f('ix_air_quality_type_gas'), 'air_quality', ['type_gas'], unique=False)
    op.drop_column('air_quality', 'type')
    op.drop_column('air_quality', 'tags')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('air_quality', sa.Column('tags', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('air_quality', sa.Column('type', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_air_quality_type_gas'), table_name='air_quality')
    op.drop_index(op.f('ix_air_quality_tag'), table_name='air_quality')
    op.create_index('ix_air_quality_type', 'air_quality', ['type'], unique=False)
    op.create_index('ix_air_quality_tags', 'air_quality', ['tags'], unique=False)
    op.drop_column('air_quality', 'tag')
    op.drop_column('air_quality', 'type_gas')
    # ### end Alembic commands ###
