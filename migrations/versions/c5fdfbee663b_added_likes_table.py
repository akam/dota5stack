"""added likes table

Revision ID: c5fdfbee663b
Revises: 0c1501053360
Create Date: 2017-05-31 13:54:15.165741

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5fdfbee663b'
down_revision = '0c1501053360'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('likes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('likee_id', sa.Integer(), nullable=True),
    sa.Column('liker_id', sa.Integer(), nullable=True),
    sa.CheckConstraint('liker_id != likee_id', name='no_self_like'),
    sa.ForeignKeyConstraint(['likee_id'], ['users.id'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['liker_id'], ['users.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('likes')
    # ### end Alembic commands ###