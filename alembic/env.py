from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from dotenv import load_dotenv
import os

from alembic import context

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

# Import your Base metadata
from app.config.database import Base
# from app.models import * #Import all of your models
# Replace the model imports with explicit imports
from app.models.visa_request import VisaRequest
from app.models.applications import Applications
from app.models.application_details import ApplicationDetails
from app.models.application_remarks import ApplicationRemarks
from app.models.application_assignment import ApplicationAssignmentHistory
from app.models.enums import (
    GENDER_ENUM,
    VISA_STATUS_ENUM,
    APPLICATION_STATUS_ENUM,
    COUPON_TYPE_ENUM,
    PAYMENT_STATUS_ENUM,
    FIELD_TYPE_ENUM,
    DOCUMENT_TYPE_ENUM,
    VERIFICATION_STATUS_ENUM,
    REMARK_TYPE_ENUM,
    IS_INTERNAL_ENUM,
    ASSIGNMENT_STATUS_ENUM
)
target_metadata = Base.metadata

print("Loaded tables:", list(Base.metadata.tables.keys()))
print("Loaded models:", [
    VisaRequest.__tablename__,
    Applications.__tablename__,
    ApplicationDetails.__tablename__,
    ApplicationRemarks.__tablename__,
    ApplicationAssignmentHistory.__tablename__,
])
print("database_url:", os.getenv('DATABASE_URL'))

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option('sqlalchemy.url', os.getenv('DATABASE_URL'))

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
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
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
