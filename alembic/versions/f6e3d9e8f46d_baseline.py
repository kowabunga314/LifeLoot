"""baseline

Revision ID: f6e3d9e8f46d
Revises: 
Create Date: 2020-07-17 23:24:00.169152

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6e3d9e8f46d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=True),
    sa.Column('active', sa.Boolean(), server_default='True', nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('games',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('home_id', sa.Integer(), nullable=True),
    sa.Column('home_life', sa.Integer(), nullable=True),
    sa.Column('away_id', sa.Integer(), nullable=True),
    sa.Column('away_life', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['away_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['home_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_games_away_id'), 'games', ['away_id'], unique=False)
    op.create_index(op.f('ix_games_home_id'), 'games', ['home_id'], unique=False)
    op.create_index(op.f('ix_games_id'), 'games', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_games_id'), table_name='games')
    op.drop_index(op.f('ix_games_home_id'), table_name='games')
    op.drop_index(op.f('ix_games_away_id'), table_name='games')
    op.drop_table('games')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
