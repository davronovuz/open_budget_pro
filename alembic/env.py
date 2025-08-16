# alembic/env.py
from __future__ import annotations
import os
import sys
import importlib
from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool

# --- logging config ---
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- PYTHONPATH (Docker ichida) ---
BOT_ROOT = os.getenv("BOT_ROOT", "/usr/src/app/bot")
if BOT_ROOT not in sys.path:
    sys.path.insert(0, BOT_ROOT)

# --- .env (ixtiyoriy) ---
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# --- DB URL'ni POSTGRES_* dan tuzamiz (psycopg2!) ---
pg_user = os.getenv("POSTGRES_USER", "postgres")
pg_pass = os.getenv("POSTGRES_PASSWORD", "postgres")
pg_db   = os.getenv("POSTGRES_DB", "postgres")
pg_host = os.getenv("DB_HOST", "localhost")
pg_port = os.getenv("DB_PORT", "5432")

sync_db_url = f"postgresql+psycopg2://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}"
alembic_db_url = os.getenv("ALEMBIC_DB_URL")  # bo'lsa, ustunlik beradi
config.set_main_option("sqlalchemy.url", alembic_db_url or sync_db_url)

# --- Modellarni import qilish: MODELS_MODULE dan Base ---
models_module_name = os.getenv("MODELS_MODULE", "openbudget_models_single_file")
models_module = importlib.import_module(models_module_name)
Base = getattr(models_module, "Base", None)
if Base is None:
    raise RuntimeError(f"Base not found in module: {models_module_name}")

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section)
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
