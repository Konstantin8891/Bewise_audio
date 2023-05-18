"""create users and audio db and fk constraint

Revision ID: 16a58cbf947e
Revises: 
Create Date: 2023-05-17 12:49:13.507297

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16a58cbf947e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column(
            'id',
            sa.Integer(),
            primary_key=True,
            index=True,
            nullable=False
        ),
        sa.Column(
            'uuid',
            sa.dialects.postgresql.UUID(as_uuid=True),
            nullable=False
        ),
        sa.Column(
            'name',
            sa.String(),
            nullable=False
        )
    )
    op.create_table(
        'audio',
        sa.Column(
            'id',
            sa.dialects.postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
            index=True
        ),
        sa.Column(
            'name',
            sa.String(),
            nullable=False
        ),
        sa.Column(
            'user_id',
            sa.Integer(),
            nullable=False
        )
    )
    op.create_foreign_key(
        'user_audio_fk',
        source_table='audio',
        referent_table='users',
        local_cols=['user_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    op.drop_constraint('user_audio_fk', table_name='audio')
    op.drop_table('audio')
    op.drop_table('users')
