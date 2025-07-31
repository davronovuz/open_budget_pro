import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy.engine import Connection

from alembic import context
from infrastructure.database.models import Base
from config import load_config

# Alembic konfiguratsiyasini yuklash
config = context.config

# Log konfiguratsiyasini sozlash
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# SQLAlchemy metadata (model bazasi)
target_metadata = Base.metadata

# .env fayldan konfiguratsiyani yuklash
try:
    db_config = load_config(".env")

    # SQLAlchemy URL ni yaratish
    if not hasattr(db_config, 'db') or db_config.db is None:
        raise ValueError("Database konfiguratsiyasi topilmadi!")

    sqlalchemy_url = db_config.db.construct_sqlalchemy_url()
    config.set_main_option("sqlalchemy.url", sqlalchemy_url)

except Exception as e:
    print(f"Konfiguratsiya yuklashda xato: {e}")
    raise


def run_migrations_offline() -> None:
    """Offline rejimda migratsiyalarni bajarish (faqat SQL generatsiya qilish)"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations(connectable):
    """Asinxron migratsiyalarni bajarish"""
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


def do_run_migrations(connection: Connection) -> None:
    """Migratsiyalarni bajarish"""
    context.configure(
        connection=connection,
        target_metadata=target_metadata
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Online rejimda migratsiyalarni bajarish"""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    asyncio.run(run_async_migrations(connectable))


# Migratsiya rejimini tanlash
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()