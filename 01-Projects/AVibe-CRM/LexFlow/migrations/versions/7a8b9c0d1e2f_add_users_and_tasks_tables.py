"""add users and tasks tables

Revision ID: 7a8b9c0d1e2f
Revises: 65b843c76b3d
Create Date: 2026-06-18 23:58:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = '7a8b9c0d1e2f'
down_revision = '65b843c76b3d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('caseid', sa.Integer(), nullable=False),
        sa.Column('userid', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('priority', sa.String(length=20), nullable=False),
        sa.Column('duedate', sa.Date(), nullable=True),
        sa.Column('createdat', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updatedat', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['caseid'], ['cases.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['userid'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('tasks')
    op.drop_table('users')
