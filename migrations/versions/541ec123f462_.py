"""empty message

Revision ID: 541ec123f462
Revises: f2d00acca3b1
Create Date: 2024-07-31 14:22:36.538772

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '541ec123f462'
down_revision = 'f2d00acca3b1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('trip', schema=None) as batch_op:
        batch_op.add_column(sa.Column('latitude', sa.Float(), nullable=False))
        batch_op.add_column(sa.Column('longitude', sa.Float(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('trip', schema=None) as batch_op:
        batch_op.drop_column('longitude')
        batch_op.drop_column('latitude')

    # ### end Alembic commands ###