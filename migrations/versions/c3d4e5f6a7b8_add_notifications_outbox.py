from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "c3d4e5f6a7b8"
down_revision: Union[str, None] = "b2c3d4e5f6a7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "notifications_outbox",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("medication_id", sa.Integer(), nullable=False),
        sa.Column("checklist_id", sa.Integer(), nullable=False),
        sa.Column("kind", sa.String(length=16), nullable=False),
        sa.Column("due_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False, server_default="pending"),
        sa.Column("attempts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.CheckConstraint(
            "kind IN ('reminder', 'followup')",
            name="ck_notifications_outbox_kind",
        ),
        sa.CheckConstraint(
            "status IN ('pending', 'sent', 'failed', 'dead')",
            name="ck_notifications_outbox_status",
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["medication_id"], ["medications.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["checklist_id"], ["checklist.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_notifications_outbox_status_due_at",
        "notifications_outbox",
        ["status", "due_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_notifications_outbox_status_due_at",
        table_name="notifications_outbox",
    )
    op.drop_table("notifications_outbox")
