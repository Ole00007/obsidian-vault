"""create cases table and add soft delete to contacts

Revision ID: 8b1c2d3e4f5a
Revises: 7a8b9c0d1e2f
Create Date: 2026-06-19 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '8b1c2d3e4f5a'
down_revision = '7a8b9c0d1e2f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('contacts', sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column('contacts', sa.Column('deleted_at', sa.DateTime(), nullable=True))

    op.create_table(
        'cases',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('contactid', sa.Integer(), nullable=False),
        sa.Column('ownerid', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('casetype', sa.String(length=100), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='Intake'),
        sa.Column('priority', sa.String(length=20), nullable=False, server_default='Medium'),
        sa.Column('openedat', sa.Date(), nullable=False),
        sa.Column('duedate', sa.Date(), nullable=True),
        sa.Column('assignedto', sa.Integer(), nullable=True),
        sa.Column('createdat', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updatedat', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['contactid'], ['contacts.id'], name=op.f('cases_contactid_fkey'), ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['assignedto'], ['users.id'], name=op.f('cases_assignedto_fkey'), ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('cases')
    op.drop_column('contacts', 'deleted_at')
    op.drop_column('contacts', 'is_deleted')
