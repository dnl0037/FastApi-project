"""create users table

Revision ID: 76a4c6ea8acd
Revises: 8bc2b8b18e0d
Create Date: 2023-02-09 14:40:47.429374

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '76a4c6ea8acd'
down_revision = '8bc2b8b18e0d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column("id", sa.Integer(), nullable=False),
                    sa.Column("email", sa.String(), nullable=False),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"),
                              nullable=False),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email")
                    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
