"""Errors table definition and functions."""
from logging import getLogger
from typing import Dict

from sqlalchemy import Column, Float, Table, Text, insert
from sqlalchemy.engine.base import Engine
from sqlalchemy.exc import SQLAlchemyError

from consumer.db.utils import get_db_metadata

logger = getLogger(__name__)

metadata = get_db_metadata()

main_table = Table(
    "main_table",
    metadata,
    Column("id", Text, primary_key=True, comment="processed as the offset on the broker"),
    Column("random", Float),
    Column("uniform", Float),
    Column("triangular", Float),
    Column("betavariate", Float),
    Column("expovariate", Float),
    Column("gammavariate", Float),
    Column("gauss", Float),
)


def write_event(engine: Engine, event: Dict) -> None:
    """Write an event to the database"""
    connection = engine.connect()
    try:
        stmt = insert(main_table).values(**event)
        state = connection.execute(stmt)
        return state
    except SQLAlchemyError as err:
        logger.error(err)
