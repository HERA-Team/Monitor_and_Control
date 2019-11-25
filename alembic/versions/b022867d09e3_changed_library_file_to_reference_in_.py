"""changed library_file to reference in part_info

Revision ID: b022867d09e3
Revises: e83aa47e530b
Create Date: 2019-11-25 20:34:47.384076+00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b022867d09e3'
down_revision = 'e83aa47e530b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('part_info', sa.Column('reference', sa.String(length=256), nullable=True))
    op.drop_column('part_info', 'library_file')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('part_info', sa.Column('library_file', sa.VARCHAR(length=256), autoincrement=False, nullable=True))
    op.drop_column('part_info', 'reference')
    # ### end Alembic commands ###
