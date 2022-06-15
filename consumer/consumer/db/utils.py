"""Utility functions for interacting with the database"""
from functools import lru_cache
from os import getenv

from sqlalchemy import MetaData, create_engine


def build_db_url(host: str, name: str, user: str, password: str, port: str) -> str:
    """Build a postgres url from the db config"""

    return f"postgresql://{user}:{password}@{host}:{port}/{name}"


@lru_cache
def get_db_engine():
    """Get a SQLAlchemy core database engine."""
    db_url = build_db_url(
        host=getenv("HOST", "localhost"),
        user=getenv("SINK_USER", ""),
        port=getenv("PORT", ""),
        name=getenv("SINK_NAME", ""),
        password=getenv("SINK_PASSWORD", ""),
    )
    return create_engine(db_url)


def get_db_metadata():
    """Configure metadata for Psql schema."""
    return MetaData(bind=get_db_engine(), schema="main")
