"""added relationship between Team and User

Revision ID: 0684cbddd656
Revises: a0b077fc3849
Create Date: 2017-06-01 12:40:19.950555

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0684cbddd656'
down_revision = 'a0b077fc3849'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('teams_users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('team_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('teams_users')
    # ### end Alembic commands ###
