from environs import Env

from config import DbConfig
from .setup import create_engine, create_session_pool

env = Env()
env.read_env()

_db_config = DbConfig.from_env(env)
engine = create_engine(_db_config)
session_pool = create_session_pool(engine)
