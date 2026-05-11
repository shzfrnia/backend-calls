from typing import Generator, TypedDict

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


TABLE_NAME = 'permission'

permission_table = table(
    TABLE_NAME,
    column('subject', sa.String),
    column('name', sa.String)
)


class PermissionDict(TypedDict):
    subject: str
    name: str


def generate_permissions(
        subject: str, permissions: tuple[tuple[int, str]]
) -> Generator[PermissionDict, None, None]:
    return (
        {'subject': subject, 'name': name}
        for name in permissions
    )


def upgrade():
    downgrade()

    op.bulk_insert(permission_table, [
        *generate_permissions(
            'server',
            (
                'write',
                'invite',
                'kick',
                'ban',
                'muteMic',
                'muteHead',
                'moveUser',
                'isAdmin'
            )
        ),

        *generate_permissions(
            'channel',
            (
                'write'
                'readHidden'
            )
        ),

        *generate_permissions(
            'role',
            (
                'write'
            )
        ),
    ])


def downgrade():
    op.execute(f"TRUNCATE TABLE {TABLE_NAME} CASCADE")
