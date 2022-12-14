"""Larger content: max 5000 bytes

Revision ID: 525ba4ea2b19
Revises: 024db9a4ac35
Create Date: 2022-10-01 15:19:17.135453

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '525ba4ea2b19'
down_revision = '024db9a4ac35'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('notes', 'content',
               existing_type=sa.VARCHAR(length=1000),
               type_=sa.String(length=5000),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('notes', 'content',
               existing_type=sa.String(length=5000),
               type_=sa.VARCHAR(length=1000),
               existing_nullable=True)
    # ### end Alembic commands ###
