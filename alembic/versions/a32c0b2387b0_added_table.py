"""Added  table

Revision ID: a32c0b2387b0
Revises: 
Create Date: 2021-01-06 14:26:32.794788

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a32c0b2387b0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('group_client_key',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('client_id', sa.String(length=36), nullable=True),
    sa.Column('client_domain', sa.String(length=36), nullable=True),
    sa.Column('device_id', sa.Integer(), nullable=True),
    sa.Column('client_key', sa.Binary(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('peer_client_key',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('client_id', sa.String(length=36), nullable=False),
    sa.Column('device_id', sa.Integer(), nullable=False),
    sa.Column('registration_id', sa.Integer(), nullable=False),
    sa.Column('identity_key_public', sa.Binary(), nullable=True),
    sa.Column('prekey_id', sa.Integer(), nullable=False),
    sa.Column('prekey', sa.Binary(), nullable=True),
    sa.Column('signed_prekey_id', sa.Integer(), nullable=False),
    sa.Column('signed_prekey', sa.Binary(), nullable=True),
    sa.Column('signed_prekey_signature', sa.Binary(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('status', sa.String(length=256), nullable=True),
    sa.Column('avatar', sa.String(length=256), nullable=True),
    sa.Column('auth_source', sa.String(length=50), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('last_active_at', sa.DateTime(), nullable=True),
    sa.Column('last_login_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('message',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('from_client_id', sa.String(length=36), nullable=True),
    sa.Column('client_id', sa.String(length=36), nullable=True),
    sa.Column('message', sa.Binary(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notify',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('client_id', sa.String(length=36), nullable=True),
    sa.Column('ref_client_id', sa.String(length=36), nullable=True),
    sa.Column('ref_group_id', sa.Integer(), nullable=True),
    sa.Column('notify_type', sa.String(length=36), nullable=True),
    sa.Column('notify_image', sa.String(length=255), nullable=True),
    sa.Column('notify_title', sa.String(length=255), nullable=True),
    sa.Column('notify_content', sa.String(length=255), nullable=True),
    sa.Column('notify_platform', sa.String(length=36), nullable=True),
    sa.Column('read_flg', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notify_token',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('client_id', sa.String(length=36), nullable=True),
    sa.Column('device_id', sa.String(length=255), nullable=False),
    sa.Column('device_type', sa.String(length=16), nullable=False),
    sa.Column('push_token', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('notify_token')
    op.drop_table('notify')
    op.drop_table('message')
    op.drop_table('user')
    op.drop_table('peer_client_key')
    op.drop_table('group_client_key')
    # ### end Alembic commands ###
