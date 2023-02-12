"""add foreign-key to post table

Revision ID: f08200f64023
Revises: 76a4c6ea8acd
Create Date: 2023-02-09 14:58:38.055854

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'f08200f64023'
down_revision = '76a4c6ea8acd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key("posts_user_fk", "posts", "users", ["owner_id"], ["id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("post_user_fk", "posts")
    op.drop_column("posts", "owner_id")
    pass
