"""Add correlator config table

Revision ID: 9e208dfd0778
Revises: 7463268309ab
Create Date: 2020-10-07 05:01:49.357142+00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9e208dfd0778'
down_revision = '7463268309ab'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('correlator_configuration',
    sa.Column('config_file_hash', sa.String(), nullable=False),
    sa.Column('parameter', sa.String(), nullable=False),
    sa.Column('value', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('config_file_hash', 'parameter')
    )


def downgrade():
    op.drop_table('correlator_configuration')
