"""empty message

Revision ID: 2b0de5859ca6
Revises: bbee1eec0895
Create Date: 2024-07-23 01:16:16.777554

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b0de5859ca6'
down_revision = 'bbee1eec0895'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('trip', schema=None) as batch_op:
        batch_op.add_column(sa.Column('budget', sa.Integer(), nullable=True))
        batch_op.drop_column('bugdet')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('trip', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bugdet', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_column('budget')

    # ### end Alembic commands ###
