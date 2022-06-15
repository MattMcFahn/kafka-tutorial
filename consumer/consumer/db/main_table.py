"""Errors table definition and functions."""
from logging import getLogger
from typing import Dict, Optional

from consumer.db.utils import get_db_metadata
from consumer.model import MainTable
from sqlalchemy import Column, Integer, Text
from sqlalchemy.engine.base import Engine
from sqlalchemy.exc import SQLAlchemyError

logger = getLogger(__name__)

main_table = MainTable(
    "<table_name>", get_db_metadata(), Column("id", Integer, primary_key=True), Column("other col", Text)
)


def get(engine: Engine, id: Optional[str] = None) -> Optional[Dict]:
    """Get last streamer state row."""
    connection = engine.connect()
    try:
        state = connection.execute(main_table.select().order_by(-main_table.c.id.desc())).all()

        return dict(state) if state else None
    except SQLAlchemyError as err:
        logger.error(err, extra={"id": id})

    return None
