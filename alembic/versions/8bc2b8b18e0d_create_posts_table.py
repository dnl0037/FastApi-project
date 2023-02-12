"""create posts table

Revision ID: 8bc2b8b18e0d
Revises: 
Create Date: 2023-02-09 14:35:18.269755

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '8bc2b8b18e0d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts", sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
                    sa.Column("title", sa.String(), nullable=False))

    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
