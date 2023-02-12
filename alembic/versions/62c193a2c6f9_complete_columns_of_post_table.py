"""complete columns of post table

Revision ID: 62c193a2c6f9
Revises: f08200f64023
Create Date: 2023-02-09 15:08:46.273471

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '62c193a2c6f9'
down_revision = 'f08200f64023'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    op.add_column("posts", sa.Column("published", sa.Boolean(), server_default="TRUE", nullable=False))
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"),
                                     nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
