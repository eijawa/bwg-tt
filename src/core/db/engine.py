from sqlalchemy import create_engine

from src.core import settings

engine = create_engine("postgresql" + settings.db_connection_string)
