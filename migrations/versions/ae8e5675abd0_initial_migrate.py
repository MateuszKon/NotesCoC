"""Initial migrate

Revision ID: ae8e5675abd0
Revises: 
Create Date: 2022-08-03 13:18:17.502609

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae8e5675abd0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=80), nullable=True),
    sa.Column('content', sa.String(length=1000), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_notes'))
    )
    op.create_table('persons',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_persons')),
    sa.UniqueConstraint('name', name=op.f('uq_persons_name'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('persons')
    op.drop_table('notes')
    # ### end Alembic commands ###
