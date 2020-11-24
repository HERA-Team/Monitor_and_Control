"""add more corr config tables

Revision ID: c9e558e762ff
Revises: 9e208dfd0778
Create Date: 2020-11-18 01:45:02.613979+00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c9e558e762ff'
down_revision = '9e208dfd0778'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('correlator_active_snap',
    sa.Column('config_file_hash', sa.String(), nullable=False),
    sa.Column('hostname', sa.String(), nullable=False),
    sa.Column('node', sa.Integer(), nullable=False),
    sa.Column('snap_loc_num', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('config_file_hash', 'hostname')
    )
    op.create_table('correlator_input_index',
    sa.Column('config_file_hash', sa.String(), nullable=False),
    sa.Column('hostname', sa.String(), nullable=False),
    sa.Column('node', sa.Integer(), nullable=False),
    sa.Column('snap_loc_num', sa.Integer(), nullable=False),
    sa.Column('antenna_index_position', sa.Integer(), nullable=False),
    sa.Column('correlator_index', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('config_file_hash', 'correlator_index')
    )
    op.create_table('correlator_phase_switch_index',
    sa.Column('config_file_hash', sa.String(), nullable=False),
    sa.Column('hostname', sa.String(), nullable=False),
    sa.Column('node', sa.Integer(), nullable=False),
    sa.Column('snap_loc_num', sa.Integer(), nullable=False),
    sa.Column('antpol_index_position', sa.Integer(), nullable=False),
    sa.Column('phase_switch_index', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('config_file_hash', 'hostname', 'phase_switch_index')
    )


def downgrade():
    op.drop_table('correlator_phase_switch_index')
    op.drop_table('correlator_input_index')
    op.drop_table('correlator_active_snap')
