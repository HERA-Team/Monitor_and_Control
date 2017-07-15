"""Bring up to master.

Revision ID: b1063869f198
Revises: a68c0e31204e
Create Date: 2017-07-14 02:46:54.173568

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b1063869f198'
down_revision = 'a68c0e31204e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lib_raid_errors',
    sa.Column('time', sa.BigInteger(), nullable=False),
    sa.Column('hostname', sa.String(length=32), nullable=False),
    sa.Column('disk', sa.String(), nullable=False),
    sa.Column('log', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('time', 'hostname', 'disk')
    )
    op.create_table('lib_raid_status',
    sa.Column('time', sa.BigInteger(), nullable=False),
    sa.Column('hostname', sa.String(length=32), nullable=False),
    sa.Column('num_disks', sa.Integer(), nullable=False),
    sa.Column('info', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('time', 'hostname')
    )
    op.create_table('lib_remote_status',
    sa.Column('time', sa.BigInteger(), nullable=False),
    sa.Column('remote_name', sa.String(length=32), nullable=False),
    sa.Column('ping_time', sa.Float(), nullable=False),
    sa.Column('num_file_uploads', sa.Integer(), nullable=False),
    sa.Column('bandwidth_mbs', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('time', 'remote_name', 'ping_time')
    )
    op.create_table('lib_server_status',
    sa.Column('hostname', sa.String(length=32), nullable=False),
    sa.Column('mc_time', sa.BigInteger(), nullable=False),
    sa.Column('ip_address', sa.String(length=32), nullable=False),
    sa.Column('mc_system_timediff', sa.Float(), nullable=False),
    sa.Column('num_cores', sa.Integer(), nullable=False),
    sa.Column('cpu_load_pct', sa.Float(), nullable=False),
    sa.Column('uptime_days', sa.Float(), nullable=False),
    sa.Column('memory_used_pct', sa.Float(), nullable=False),
    sa.Column('memory_size_gb', sa.Float(), nullable=False),
    sa.Column('disk_space_pct', sa.Float(), nullable=False),
    sa.Column('disk_size_gb', sa.Float(), nullable=False),
    sa.Column('network_bandwidth_mbs', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('hostname', 'mc_time')
    )
    op.create_table('lib_status',
    sa.Column('time', sa.BigInteger(), nullable=False),
    sa.Column('num_files', sa.BigInteger(), nullable=False),
    sa.Column('data_volume_gb', sa.Float(), nullable=False),
    sa.Column('free_space_gb', sa.Float(), nullable=False),
    sa.Column('upload_min_elapsed', sa.Float(), nullable=False),
    sa.Column('num_processes', sa.Integer(), nullable=False),
    sa.Column('git_version', sa.String(length=32), nullable=False),
    sa.Column('git_hash', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('time')
    )
    op.create_table('rtp_server_status',
    sa.Column('hostname', sa.String(length=32), nullable=False),
    sa.Column('mc_time', sa.BigInteger(), nullable=False),
    sa.Column('ip_address', sa.String(length=32), nullable=False),
    sa.Column('mc_system_timediff', sa.Float(), nullable=False),
    sa.Column('num_cores', sa.Integer(), nullable=False),
    sa.Column('cpu_load_pct', sa.Float(), nullable=False),
    sa.Column('uptime_days', sa.Float(), nullable=False),
    sa.Column('memory_used_pct', sa.Float(), nullable=False),
    sa.Column('memory_size_gb', sa.Float(), nullable=False),
    sa.Column('disk_space_pct', sa.Float(), nullable=False),
    sa.Column('disk_size_gb', sa.Float(), nullable=False),
    sa.Column('network_bandwidth_mbs', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('hostname', 'mc_time')
    )
    op.create_table('rtp_status',
    sa.Column('time', sa.BigInteger(), nullable=False),
    sa.Column('status', sa.String(length=64), nullable=False),
    sa.Column('event_min_elapsed', sa.Float(), nullable=False),
    sa.Column('num_processes', sa.Integer(), nullable=False),
    sa.Column('restart_hours_elapsed', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('time')
    )
    op.create_table('lib_files',
    sa.Column('filename', sa.String(length=32), nullable=False),
    sa.Column('obsid', sa.BigInteger(), nullable=False),
    sa.Column('time', sa.BigInteger(), nullable=False),
    sa.Column('size_gb', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['obsid'], ['hera_obs.obsid'], ),
    sa.PrimaryKeyConstraint('filename')
    )
    op.create_table('rtp_process_event',
    sa.Column('time', sa.BigInteger(), nullable=False),
    sa.Column('obsid', sa.BigInteger(), nullable=False),
    sa.Column('event', sa.Enum('queued', 'started', 'finished', 'error', name='rtp_process_enum'), nullable=False),
    sa.ForeignKeyConstraint(['obsid'], ['hera_obs.obsid'], ),
    sa.PrimaryKeyConstraint('time', 'obsid')
    )
    op.create_table('rtp_process_record',
    sa.Column('time', sa.BigInteger(), nullable=False),
    sa.Column('obsid', sa.BigInteger(), nullable=False),
    sa.Column('pipeline_list', sa.Text(), nullable=False),
    sa.Column('git_version', sa.String(length=32), nullable=False),
    sa.Column('git_hash', sa.String(length=64), nullable=False),
    sa.ForeignKeyConstraint(['obsid'], ['hera_obs.obsid'], ),
    sa.PrimaryKeyConstraint('time', 'obsid')
    )
    op.add_column(u'connections', sa.Column('start_gpstime', sa.BigInteger(), nullable=False))
    op.add_column(u'connections', sa.Column('stop_gpstime', sa.BigInteger(), nullable=True))
    op.drop_column(u'connections', 'stop_date')
    op.drop_column(u'connections', 'start_date')
    op.add_column(u'geo_location', sa.Column('created_gpstime', sa.BigInteger(), nullable=False))
    op.drop_column(u'geo_location', 'created_date')
    op.add_column(u'hera_obs', sa.Column('jd_start', sa.Float(), nullable=False))
    op.add_column(u'hera_obs', sa.Column('starttime', sa.Float(), nullable=False))
    op.add_column(u'hera_obs', sa.Column('stoptime', sa.Float(), nullable=False))
    op.drop_column(u'hera_obs', 'stop_time_jd')
    op.drop_column(u'hera_obs', 'start_time_jd')
    op.add_column(u'paper_temperatures', sa.Column('time', sa.BigInteger(), nullable=False))
    op.drop_column(u'paper_temperatures', 'gps_time')
    op.drop_column(u'paper_temperatures', 'jd_time')
    op.add_column(u'part_info', sa.Column('posting_gpstime', sa.BigInteger(), nullable=False))
    op.drop_column(u'part_info', 'posting_date')
    op.add_column(u'parts_paper', sa.Column('start_gpstime', sa.BigInteger(), nullable=False))
    op.add_column(u'parts_paper', sa.Column('stop_gpstime', sa.BigInteger(), nullable=True))
    op.drop_column(u'parts_paper', 'stop_date')
    op.drop_column(u'parts_paper', 'start_date')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(u'parts_paper', sa.Column('start_date', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False))
    op.add_column(u'parts_paper', sa.Column('stop_date', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True))
    op.drop_column(u'parts_paper', 'stop_gpstime')
    op.drop_column(u'parts_paper', 'start_gpstime')
    op.add_column(u'part_info', sa.Column('posting_date', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False))
    op.drop_column(u'part_info', 'posting_gpstime')
    op.add_column(u'paper_temperatures', sa.Column('jd_time', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.add_column(u'paper_temperatures', sa.Column('gps_time', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.drop_column(u'paper_temperatures', 'time')
    op.add_column(u'hera_obs', sa.Column('start_time_jd', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.add_column(u'hera_obs', sa.Column('stop_time_jd', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.drop_column(u'hera_obs', 'stoptime')
    op.drop_column(u'hera_obs', 'starttime')
    op.drop_column(u'hera_obs', 'jd_start')
    op.add_column(u'geo_location', sa.Column('created_date', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False))
    op.drop_column(u'geo_location', 'created_gpstime')
    op.add_column(u'connections', sa.Column('start_date', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False))
    op.add_column(u'connections', sa.Column('stop_date', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True))
    op.drop_column(u'connections', 'stop_gpstime')
    op.drop_column(u'connections', 'start_gpstime')
    op.drop_table('rtp_process_record')
    op.drop_table('rtp_process_event')
    op.drop_table('lib_files')
    op.drop_table('rtp_status')
    op.drop_table('rtp_server_status')
    op.drop_table('lib_status')
    op.drop_table('lib_server_status')
    op.drop_table('lib_remote_status')
    op.drop_table('lib_raid_status')
    op.drop_table('lib_raid_errors')
    # ### end Alembic commands ###