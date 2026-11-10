"""Replace is_superuser with role

Revision ID: 7b3f2c9d1a54
Revises: fe56fa70289e
Create Date: 2026-11-10 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b3f2c9d1a54'
down_revision = 'fe56fa70289e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'user',
        sa.Column('role', sa.String(length=20), nullable=False, server_default='member'),
    )
    # Existing superusers keep full access as admins; everyone else is a member.
    op.execute("UPDATE \"user\" SET role = 'admin' WHERE is_superuser")
    op.drop_column('user', 'is_superuser')


def downgrade():
    op.add_column(
        'user',
        sa.Column('is_superuser', sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    # The manager role has no equivalent in the old model and becomes a normal user.
    op.execute("UPDATE \"user\" SET is_superuser = (role = 'admin')")
    op.alter_column('user', 'is_superuser', server_default=None)
    op.drop_column('user', 'role')
