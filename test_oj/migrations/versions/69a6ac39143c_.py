"""empty message

Revision ID: 69a6ac39143c
Revises: 
Create Date: 2019-04-30 17:34:39.795911

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69a6ac39143c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('account',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=False),
    sa.Column('nickname', sa.String(length=30), nullable=False),
    sa.Column('password', sa.String(length=200), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('permLevel', sa.Integer(), nullable=False),
    sa.Column('signUpTime', sa.DateTime(), nullable=False),
    sa.Column('lastLoginTime', sa.DateTime(), nullable=False),
    sa.Column('icon', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('uid'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('uid'),
    sa.UniqueConstraint('username'),
    mysql_collate='utf8_general_ci'
    )
    op.create_table('account_valid',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('uid'),
    sa.UniqueConstraint('uid')
    )
    op.create_table('problem',
    sa.Column('problemName', sa.String(length=100), nullable=False),
    sa.Column('problemId', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('problemName'),
    sa.UniqueConstraint('problemId'),
    sa.UniqueConstraint('uid'),
    mysql_collate='utf8_general_ci'
    )
    op.create_table('submission',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('result', sa.String(length=10), nullable=False),
    sa.Column('resTime', sa.Float(), nullable=False),
    sa.Column('resMem', sa.Float(), nullable=False),
    sa.Column('code', sa.Text(), nullable=False),
    sa.Column('lang', sa.String(length=10), nullable=False),
    sa.Column('rank', sa.Integer(), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('uid'),
    mysql_collate='utf8_general_ci'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('submission')
    op.drop_table('problem')
    op.drop_table('account_valid')
    op.drop_table('account')
    # ### end Alembic commands ###