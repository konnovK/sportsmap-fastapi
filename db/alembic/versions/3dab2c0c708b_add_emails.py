"""add emails

Revision ID: 3dab2c0c708b
Revises: 06efe96365d4
Create Date: 2023-05-14 14:36:19.310499

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3dab2c0c708b'
down_revision = '06efe96365d4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('email_subscriber',
    sa.Column('secret', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('secret', name=op.f('pk__email_subscriber')),
    sa.UniqueConstraint('email', name=op.f('uq__email_subscriber__email'))
    )
    op.create_table('email_password_refresh',
    sa.Column('secret', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('secret', name=op.f('pk__email_password_refresh')),
    sa.UniqueConstraint('email', name=op.f('uq__email_password_refresh__email'))
    )
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('email_subscriber')
    op.drop_table('email_password_refresh')
    pass
    # ### end Alembic commands ###