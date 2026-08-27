"""create contacts table

Revision ID: 65b843c76b3d
Revises: 430ee4511375
Create Date: 2026-05-27 16:01:25.706582

"""
from alembic import op
import sqlalchemy as sa

revision = '65b843c76b3d'
down_revision = '430ee4511375'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'contacts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ownerid', sa.Integer(), nullable=True),
        sa.Column('fullname', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('company', sa.String(length=255), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('contacts')
