from __future__ import with_statement

import logging
from logging.config import fileConfig

from flask import current_app

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
config.set_main_option(
    'sqlalchemy.url',
    str(current_app.extensions['migrate'].db.get_engine().url).replace(
        '%', '%%'))
target_metadata = current_app.extensions['migrate'].db.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    # this callback is used to prevent an auto-migration from being generated
    # when there are no changes to the schema
    # reference: http://alembic.zzzcomputing.com/en/latest/cookbook.html
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No changes in schema detected.')

    connectable = current_app.extensions['migrate'].db.get_engine()

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            process_revision_directives=process_revision_directives,
            **current_app.extensions['migrate'].configure_args,
            include_object=include_object
        )

        with context.begin_transaction():
            context.run_migrations()


def include_object(object, name, type_, reflected, compare_to):
    if type_ == 'table' and name in {
        'default_client_scope',
        'fed_user_role_mapping',
        'credential',
        'user_session',
        'redirect_uris',
        'resource_attribute',
        'policy_config',
        'realm_required_credential',
        'group_role_mapping',
        'required_action_config',
        'resource_server_perm_ticket',
        'resource_scope',
        'fed_user_required_action',
        'default_client_scope',
        'fed_user_role_mapping',
        'client_scope_attributes',
        'user_session_note',
        'user_consent',
        'realm_default_groups',
        'fed_user_attribute',
        'group_attribute',
        'user_role_mapping',
        'user_session',
        'idp_mapper_config',
        'required_action_config',
        'admin_event_entity',
        'resource_server_scope',
        'resource_scope',
        'keycloak_group',
        'authenticator_config',
        'event_entity',
        'federated_identity',
        'client_scope_role_mapping',
        'offline_user_session',
        'databasechangeloglock',
        'identity_provider_config',
        'client_initial_access',
        'realm_smtp_config',
        'fed_user_credential',
        'policy_config',
        'resource_uris',
        'resource_server',
        'scope_policy',
        'realm_attribute',
        'client',
        'client_attributes',
        'resource_server_resource',
        'associated_policy',
        'role_attribute',
        'scope_mapping',
        'realm_enabled_event_types',
        'component',
        'client_session_role',
        'client_node_registrations',
        'identity_provider_mapper',
        'identity_provider',
        'client_session',
        'user_attribute',
        'fed_user_group_membership',
        'client_auth_flow_bindings',
        'keycloak_role',
        'client_session_note',
        'user_required_action',
        'migration_model',
        'required_action_provider',
        'user_federation_config',
        'federated_user',
        'fed_user_required_action',
        'resource_server_policy',
        'component_config',
        'resource_policy',
        'authenticator_config_entry',
        'user_federation_provider',
        'client_session_auth_status',
        'redirect_uris',
        'user_federation_mapper',
        'credential',
        'client_user_session_note',
        'user_federation_mapper_config',
        'username_login_failure',
        'realm_localizations',
        'user_consent_client_scope',
        'resource_server_perm_ticket',
        'protocol_mapper',
        'user_group_membership',
        'fed_user_consent',
        'realm_required_credential',
        'web_origins',
        'protocol_mapper_config',
        'databasechangelog',
        'client_session_prot_mapper',
        'authentication_execution',
        'realm_supported_locales',
        'authentication_flow',
        'resource_attribute',
        'realm',
        'broker_link',
        'realm_events_listeners',
        'client_scope',
        'fed_user_consent_cl_scope',
        'client_scope_client',
        'offline_client_session',
        'user_entity',
        'composite_role',
        'group_role_mapping',
    }:
        return False
    return True


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
