"""seed_permissions_data

Revision ID: dafcee477031
Revises: ab2cce2286dc
Create Date: 2026-05-11 23:52:22.571378

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes

import app.models.seed.permission as seed


# revision identifiers, used by Alembic.
revision = 'dafcee477031'
down_revision = 'ab2cce2286dc'
branch_labels = None
depends_on = None


def upgrade():
    seed.upgrade()


def downgrade():
    seed.downgrade()
